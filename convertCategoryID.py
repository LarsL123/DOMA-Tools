import config
from modules.SOAP import getMapCategoriesUpload, getMapCategoriesDownload

import os
import json

maps_folder = config.MAPS_PATH

print("The dowload categoryids:")
print(getMapCategoriesDownload())

print("The upload categories: ")
print(getMapCategoriesUpload())

isReady = True

if isReady:
    category_id_map = {
    35: 332,  
    36: 333,
    42: 350,
    44: 351
    # Add more mappings as needed
    }

    for foldername in os.listdir(config.MAPS_PATH):
        folder_path = os.path.join(config.MAPS_PATH, foldername)
        properties_path = os.path.join(folder_path, "properties.json")
        if os.path.isdir(folder_path) and os.path.isfile(properties_path):
            with open(properties_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            old_id = data.get("CategoryID")

            if old_id in category_id_map:
                data["CategoryID"] = category_id_map[old_id]
                with open(properties_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=True, indent=4)
                print(f"Updated CategoryID {old_id} to {data['CategoryID']} in {foldername}")

            else:
                print(f"CategoryID {old_id} in {foldername} not found in mapping. Skipping...")


    