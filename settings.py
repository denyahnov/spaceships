import json

global SETTINGS

SETTINGS = {
	"szAccountName": "Player",
	"bShowFps": True,
}

def Load():
	global SETTINGS

	try:
		with open("setttings.json","r") as file:
			SETTINGS |= json.load(file)
	except FileNotFoundError:
		Save()

def Save():
	global SETTINGS

	with open("setttings.json","w") as file:
		json.dump(SETTINGS,file,indent=4)

def Get(key):
	global SETTINGS

	try:
		return SETTINGS[key]
	except KeyError:
		return None

def Set(key,value):
	global SETTINGS

	SETTINGS[key] = value
