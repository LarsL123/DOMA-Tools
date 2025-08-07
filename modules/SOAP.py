from suds.client import Client
from os import path
import sys
import base64
import json

import config


# Create a SOAP client
try:
    uploadClient = Client(config.UPLOAD_WSDL_WEBSERVICE_URL)
    downloadClient = Client(config.DOWNLOAD_WSDL_WEBSERVICE_URL)
except Exception as e:
    print(e)
    print("Was not able to connect to the server. Check internett connection and url in config.py. ")
    sys.exit(0)



def suds_to_dict(suds_obj):
    from suds.sudsobject import asdict
    def recurse(data):
        out = {}
        for k, v in asdict(data).items():
            if hasattr(v, '__keylist__'):
                out[k] = recurse(v)
            elif isinstance(v, list):
                out[k] = [recurse(i) if hasattr(i, '__keylist__') else i for i in v]
            else:
                out[k] = v
        return out
    return recurse(suds_obj)

def date_to_iso_dict(dict_obj):
    dict_obj["Date"] = dict_obj["Date"].isoformat()


#Returns a list of all maps in the database as a suds reponse object.
def getAllMapsDownload():
    request = downloadClient.factory.create("GetAllMapsRequest")

    request.Username = config.DOWNLOAD["USERNAME"]
    request.Password = config.DOWNLOAD["PASSWORD"]

    return downloadClient.service.GetAllMaps(request).Maps

#Returns a list of all maps in the database as a suds reponse object.
def getAllMapsUpload():
    request = uploadClient.factory.create("GetAllMapsRequest")

    request.Username = config.UPLOAD["USERNAME"]
    request.Password = config.UPLOAD["PASSWORD"]

    return uploadClient.service.GetAllMaps(request).Maps

import random

def uploadPartialFile(path):
    print(f"Uploading {path}")

    try:
        with open(path, "rb") as image_file:
            image_data = image_file.read()
    except FileNotFoundError:
        print(f"Error: Tries to load image with path: {path}. Image cound not be read. Continuing...")
        return None

    # Generate random filename. Not shure if this i needed but Mats did it in his Quickroute program.
    random_filename = f"{random.randint(0, 100000000)}.{path.split('.')[-1]}"

    position = 0
    while position < len(image_data):
        length = min(config.CHUNK_SIZE, len(image_data) - position)
        chunk = image_data[position:position + length]
        position += length

        # Base64 encode the chunk. Decode ascii is important
        encoded_chunk = base64.b64encode(chunk).decode('ascii')

        request = uploadClient.factory.create("UploadPartialFileRequest")
        request.Username = config.UPLOAD["USERNAME"]
        request.Password = config.UPLOAD["PASSWORD"]
        request.FileName = random_filename
        request.Data = encoded_chunk

        response = uploadClient.service.UploadPartialFile(request)

        if not response.Success:
            print(f"Was not able to upload file {path}!, Error message: {response.ErrorMessage}")
            print("Continuing...")
            return None

    return random_filename


def PublishMap(mapsFolderPath, imageName, blankImageName, thumbnailImageName):
    request = uploadClient.factory.create("PublishPreUploadedMapRequest")

    request.Username = config.UPLOAD["USERNAME"]
    request.Password = config.UPLOAD["PASSWORD"]

    try:
        mapInfo = json.load(open(path.join(mapsFolderPath, "properties.json")))
        setMapInfo(request, mapInfo)
    except Exception as e:
        print(f"Error: Tries to upload map at: {mapsFolderPath}. Was not able to load or parse properties.json file!")
        print(e)
        print("Continuing...")
        return

    request.PreUploadedMapImageFileName = imageName
    request.PreUploadedBlankMapImageFileName = blankImageName
    request.PreUploadedThumbnailImageFileName = thumbnailImageName

    return uploadClient.service.PublishPreUploadedMap(request)

def TestConnectionUpload():
    request = uploadClient.factory.create("ConnectRequest")

    request.Username = config.UPLOAD["USERNAME"]
    request.Password = config.UPLOAD["PASSWORD"]

    # Test connection to the server
    response = uploadClient.service.Connect(request)
    if not response["Success"]:
        print(response)
        sys.exit(0)

    return response

def getMapCategoriesUpload():
    request = uploadClient.factory.create("GetAllCategoriesRequest")

    request.Username = config.UPLOAD["USERNAME"]
    request.Password = config.UPLOAD["PASSWORD"]

    return uploadClient.service.GetAllCategories(request)

def getMapCategoriesDownload():
    request = downloadClient.factory.create("GetAllCategoriesRequest")

    request.Username = config.DOWNLOAD["USERNAME"]
    request.Password = config.DOWNLOAD["PASSWORD"]

    return downloadClient.service.GetAllCategories(request)

#The easiest way. Probably a better way to do this.
def setMapInfo(request, mapInfo):
    # request.MapInfo.ID = mapInfo["ID"] #Imortant: Setting this will override other maps with the same ID.
    request.MapInfo.UserID = mapInfo["UserID"]
    request.MapInfo.CategoryID = mapInfo["CategoryID"]
    request.MapInfo.Date = mapInfo["Date"]
    request.MapInfo.Name = mapInfo["Name"]
    request.MapInfo.Organiser = mapInfo["Organiser"]
    request.MapInfo.Country = mapInfo["Country"]
    request.MapInfo.Discipline = mapInfo["Discipline"]
    request.MapInfo.RelayLeg = mapInfo["RelayLeg"]
    request.MapInfo.MapName = mapInfo["MapName"]
    request.MapInfo.ResultListUrl = mapInfo["ResultListUrl"]
    request.MapInfo.Comment = mapInfo["Comment"]
