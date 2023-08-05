import os
import time
import requests
import calendar

download_url = "https://github.com/denyahnov/spaceships/tree-commit-info/main/dist"

def CheckUpdate():
	client_time = int(os.path.getctime(__file__))

	response = requests.get(download_url,headers={"x-requested-with": "XMLHttpRequest"})

	server_date = response.json()["Spaceships.exe"]["date"]

	server_time = calendar.timegm(time.strptime(server_date.split('T')[0] + " " + server_date.split('T')[-1].split(".")[0], '%Y-%m-%d %H:%M:%S'))

	requires_update = server_time > client_time

	return requires_update

if __name__ == '__main__':
	print(CheckUpdate())