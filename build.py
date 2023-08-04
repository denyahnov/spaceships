import os
from git import Repo

directory = "\\".join(__file__.split("\\")[:-1])
build_cmd =  'pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/denya/OneDrive/Desktop/GitHub/spaceships/app_icon.ico" --name "Spaceships"  "C:/Users/denya/OneDrive/Desktop/GitHub/spaceships/main.py"'

os.system(build_cmd)

repo = Repo(directory)

origin = repo.remote("origin")  

assert origin.exists()
origin.fetch()

repo.index.add([directory + '\\output\\Spaceships.exe'])
repo.index.commit('Build Game')
origin.push()