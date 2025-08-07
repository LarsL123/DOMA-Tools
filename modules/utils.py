import os
import config
import json

# Needed because of varying file extensions when uploading maps.
def addExtension(folderPath,fileName):
    jpgName = os.path.join(folderPath, fileName+ ".jpg")
    if os.path.isfile(jpgName):
        return jpgName
    
    pngName = os.path.join(folderPath, fileName+ ".png")
    if os.path.isfile(pngName):
        return pngName
    
    return None

# Used for upload.py to remove already uploaded maps.
# def removeAlreadyUploadedMaps(folders, existingMaps):
#     # Create a set of (Name, Comment) tuples for fast lookup
#     existing_name_comment_pairs = {
#         (map["Name"], map["Comment"]) for map in existingMaps
#     }

#     filtered_folders = []

#     for folder in folders:
#         properties_path = os.path.join(config.MAPS_PATH, folder, "properties.json")
#         if not os.path.isfile(properties_path):
#             continue

#         try:
#             with open(properties_path, "r", encoding="utf-8") as f:
#                 props = json.load(f)
#                 name = props.get("Name")
#                 comment = props.get("Comment")

#                 if (name, comment) not in existing_name_comment_pairs:
#                     filtered_folders.append(folder)
#                 else:
#                     print(f"Skipping {folder} because it already exists with the same name and comment.")

#         except Exception as e:
#             print(f"Error reading properties.json in {folder}: {e}")

#     return filtered_folders


def removeAlreadyUploadedMaps(folders, existingMaps):
    existing_names = set()
    existing_comments = set()
    for map in existingMaps:
        existing_names.add(map["Name"])
        existing_comments.add(map["Comment"])
    filtered_folders = []
    for folder in folders:
        properties_path = os.path.join(config.MAPS_PATH, folder, "properties.json")
        if not os.path.isfile(properties_path):
            continue
        with open(properties_path, "r", encoding="utf-8") as f:
            try:
                props = json.load(f)
                name = props.get("Name")
                comment = props.get("Comment")
                if (name not in existing_names) and (comment not in existing_comments):
                    filtered_folders.append(folder)
                else:
                    print("Do you want to skip this map? (y/n)")
                    user_input = input().strip().lower()
                    if user_input == "n":
                        filtered_folders.append(folder)
                        print(f"Map {folder} will be uploaded.")
                    else:
                        print(f"Skipping {folder} because it already exists with the same name or comment.")
            except Exception as e:
                print(f"Error reading properties.json in {folder}: {e}")

    return filtered_folders

