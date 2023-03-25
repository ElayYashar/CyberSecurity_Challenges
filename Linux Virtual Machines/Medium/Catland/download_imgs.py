import requests
from bs4 import BeautifulSoup
import os

url = "http://10.0.0.5/images"

def get_all_images(url: str):
    request = requests.get(url).text
    soup = BeautifulSoup(request, 'html.parser')
    
    imageNames = []
    
    for x in soup.find_all('a'):
        fileName = x.get("href")
        if fileName.endswith("jpeg"):
            imageNames.append(fileName)
            
    return imageNames

def download_images(images: list):
    try:
        os.makedirs("Images")
    except FileExistsError:
        # directory already exists
        pass
    
    for image in images:
        result = requests.get(url + "/" + image)
        open('Images/' + image, 'wb').write(result.content)

def main():
    download_images(get_all_images(url))

if __name__ == '__main__': main()