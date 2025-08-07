from modules.SOAP import getAllMapsUpload
import config

import os
import json

def get_title_from_properties(properties_path):
    try:
        with open(properties_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('Name')
    except Exception:
        return None

def get_local_titles(maps_folder):
    titles = set()
    for folder_name in os.listdir(maps_folder):
        folder_path = os.path.join(maps_folder, folder_name)
        properties_path = os.path.join(folder_path, 'properties.json')

        if os.path.isdir(folder_path) and os.path.isfile(properties_path):
            title = get_title_from_properties(properties_path)
            if title:
                titles.add(title)
    return titles

# Checks if any local 

def main_find_by_name():
        maps_folder = config.MAPS_PATH
        search_name = input("Enter the 'Name' field to search for: ").strip()
        matching_folders = []
        for folder_name in os.listdir(maps_folder):
            folder_path = os.path.join(maps_folder, folder_name)
            properties_path = os.path.join(folder_path, 'properties.json')
            if os.path.isdir(folder_path) and os.path.isfile(properties_path):
                title = get_title_from_properties(properties_path)
                if title == search_name:
                    matching_folders.append(folder_name)
        if matching_folders:
            print(f"Folders with Name '{search_name}':")
            for folder in matching_folders:
                print(folder)
        else:
            print(f"No folders found with Name '{search_name}'.")

def main():
    maps_folder = config.MAPS_PATH  # Adjust path if needed
    local_titles = get_local_titles(maps_folder)
    remote_maps = getAllMapsUpload()
    print(remote_maps[0])
    remote_titles = set()
    for item in remote_maps:
        title = item["Name"]
        if title:
            remote_titles.add(title)
    duplicates = local_titles.intersection(remote_titles)
    if duplicates:
        print("Duplicate titles found:")
        for title in duplicates:
            print(title)
    else:
        print("No duplicate titles found.")

if __name__ == "__main__":
    # main_find_by_name()
    main()

    
