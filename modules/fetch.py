import config
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from os import path


def fetchMapImages(mapId, dirName):
    # Define the URL
    URL = config.DOWNLOAD_MAPS_URL + mapId

    # Headers to mimic a browser request
    HEADERS = {
        "User-Agent": "Mozilla/5.0"
    }

    # Fetch HTML content
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract and download images
    image_tags = soup.find_all("img", {"id": ["mapImage", "hiddenMapImage"]})
    for img in image_tags:
        img_url = urljoin(URL, img["src"])
        img_name = path.basename(img["src"])
        stored_img_path = path.join(dirName, img_name)

        #Fetch image data
        img_data = requests.get(img_url, headers=HEADERS).content

        with open(stored_img_path, "wb") as img_file:
            img_file.write(img_data)

        print(f"Downloaded: {img_name}")

def fetchTunbnailImage(mapId, dirName):
    URL = urljoin(urljoin(config.DOWNLOAD["URL"], "map_images/"), mapId + ".thumbnail.jpg")

     # Headers to mimic a browser request
    HEADERS = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(URL, headers=HEADERS)
    imageData = response.content

    if response.status_code != 200:
        URL = urljoin(urljoin(config.DOWNLOAD["URL"], "map_images/"), mapId + ".thumbnail.png")
        response = requests.get(URL, headers=HEADERS)
        imageData = response.content
        if response.status_code != 200:
            print(f"Error: Unable to fetch thumbnail image for map ID {mapId}. Status code: {response.status_code}. Skipping to next map.")
            return
    
    thumbnail_img_name = path.join(dirName,path.basename(URL))

    with open(thumbnail_img_name, "wb") as img_file:
            img_file.write(imageData)
     