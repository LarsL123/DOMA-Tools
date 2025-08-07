import config
import os
import time
import sys

from modules.utils import addExtension, removeAlreadyUploadedMaps
from modules.SOAP import uploadPartialFile, PublishMap, TestConnectionUpload, getAllMapsUpload


TestConnectionUpload()
existingMaps = getAllMapsUpload()

folders = os.listdir(config.MAPS_PATH)
folders = folders[237:]

localFolderCount = len(folders)
print(f"Found {localFolderCount} folders in {config.MAPS_PATH}")

# folders = removeAlreadyUploadedMaps(folders, existingMaps)


print(f"Removed {localFolderCount - len(folders)} folders from upload because there are matching elements allready uploaded. A folder is considered matching if the name and comment is the same as an already uploaded map.")
print(f"Uploading {len(folders)} elements. They are: {folders}"  )

for fileName in folders:
    try:
        time.sleep(config.RATE_LIMIT) 
        print(f"Uploading map {fileName}")
        folderPath = os.path.join(config.MAPS_PATH, fileName)

        imagePath = addExtension(folderPath, fileName)
        newImageName = uploadPartialFile(imagePath)

        blankImagePath = addExtension(folderPath,fileName + ".blank")
        newBlankImageName =  uploadPartialFile(blankImagePath)

        thumbnailImagePath = addExtension(folderPath, fileName + ".thumbnail")
        newthumbnailImageName = uploadPartialFile(thumbnailImagePath)

        reponse = PublishMap(folderPath, newImageName , newBlankImageName, newthumbnailImageName)

        if reponse.Success:
            print(f"Map {fileName} was uploaded successfully!")
        else:
            print(f"An error occurred when publishing map {fileName} to the server.")
            # print(f"Error message: {reponse.ErrorMessage}")
            print("Continuing...")
    
    except Exception as e:
        print(f"A program error occurred when uploading map {fileName}.")
        print(e)
        sys.exit(1)
        print("Skipping the map...")



