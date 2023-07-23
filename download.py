import os
import requests
from multiprocessing.pool import ThreadPool

ASSET_URL = "https://github.com/denyahnov/spaceships/blob/main/assets/"
DOWNLOAD_URL = "https://github.com/denyahnov/spaceships/blob/main/assets/%s?raw=true"

def CheckAsset(image):
	if image not in os.listdir("assets"):
		Download(DOWNLOAD_URL % image, "assets\\" + image)
	
		print(image,"-> Downloaded")
	else:
		print(image)

def Download(url,path=""):
	response = requests.get(url)

	with open(path,"wb") as file:
		file.write(response.content)

def GetAssets():
	if not os.path.exists("assets"):
		os.mkdir("assets")

	response = requests.get(ASSET_URL)

	images = [item["name"] for item in response.json()["payload"]["tree"]["items"]]

	with ThreadPool(processes = 20) as pool:
		return [result for result in pool.map(CheckAsset,images)]


if __name__ == '__main__':
	GetAssets()