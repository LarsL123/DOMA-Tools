import json
from os import path, makedirs
#Self defines modules
import config
import modules.SOAP as SOAP
from modules.fetch import fetchMapImages, fetchTunbnailImage

import time 

maps = SOAP.getAllMapsDownload()
# maps = maps[0:2] for testing

# print(maps[0])

for map in maps:
    print("Trying to download: ", map["ID"])
    dirName = path.join(config.MAPS_PATH, str(map["ID"]))
    if path.exists(dirName):
        print("SKipped")
        continue

    time.sleep(2) #Rate limit to avoid server issues
    map = SOAP.suds_to_dict(map)
    SOAP.date_to_iso_dict(map)

    dirName = path.join(config.MAPS_PATH, str(map["ID"]))
    makedirs(dirName, exist_ok=True)
    
    fetchMapImages(str(map["ID"]), dirName)
    fetchTunbnailImage(str(map["ID"]), dirName)

    # Save properties to a file
    with open(path.join(dirName,"properties.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(map))

        










