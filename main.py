import GameMaker as gm

from sys import exit

import update
import download

load_log = ["Loading Assets..."]

download.GetAssets()

from player import *
from currency import *

load_log.append("Checking for Updates...")

window = gm.Window([1920,1080],"Spaceships",background_color=(10,10,10),fullscreen=True,fps=70)

import ui
import network
import settings

if update.CheckUpdate():
	while window.RUNNING:
		ui.UpdateMenu(window)

	exit("Game -> Window Closed!")

ui.ShowLog(window,load_log)

settings.Load()

ui.Init(settings)

load_log.append("Loaded!")

def MainMenu():
	while window.RUNNING:
		output = ui.MainMenu(window)

		if output != 0: break
	else:
		exit("Game -> Window Closed!")

	if output == 1:
		load_log.append("Finding Server...")

		ui.ShowLog(window,load_log)

		servers = network.FindServers()

		if servers == None or len(servers) == 0:
			exit("Network -> No Available Servers")

		load_log.append("Server Found!")
		load_log.append("Connecting...")

		chosen_server = servers[0]

		ui.ShowLog(window,load_log)
	else:
		chosen_server = network.CheckServer(network.CodetoIP(output))

		if chosen_server["Response"] == 0:
			exit("Network -> Invalid Code '%s'" % output)

	return chosen_server

def Main(chosen_server):
	player = Player(settings.Get("szAccountName"))
	arrow = Arrow()

	ui.Reset()
	
	client = network.Client(player)
	client.Connect(chosen_server["Address"],65432)

	load_log.append("Connected!")
	load_log.append("Creating World...")

	ui.ShowLog(window,load_log)

	random.seed(chosen_server["WorldSeed"])

	ui.world_info.update(f"Map Size: {chosen_server['WorldSize']}\nMap Seed: {chosen_server['WorldSeed']}")

	stars = GenerateStars(int(chosen_server["WorldSize"] * 1.5),chosen_server["WorldSize"])
	asteroids = GenerateAsteroids(int(chosen_server["WorldSize"] * 0.2),chosen_server["WorldSize"])

	for asteroid in asteroids.items:
		asteroid.draw_image.rotation += asteroid.rotation_speed * chosen_server["WorldTicks"]

		asteroid.position += AngleToPosition(90 - asteroid.angle, asteroid.velocity * chosen_server["WorldTicks"])

	other_players = {}

	while client.data == {}:
		network.sleep(network.TPS)

	player.setSpawnpoint(client.data["Spawnpoint"],True)

	while window.RUNNING and client.CONNECTED:
		player.ticks = client.data["Tick"]

		for values in client.data["Players"]:
			enemy, (x, y, angle, velocity), projectiles = values["Port"],values["Position"],values["Projectiles"]

			if enemy not in other_players:
				other_players[enemy] = {
					"Spaceship": Spaceship(55,False),
					"Mothership": Mothership(values["Username"],Vector2(*values["Spawnpoint"]),90,False),
					"Projectiles":{"Laser": {}}
				} 

			for _type,entities in projectiles.items():
				if _type == "Laser":
					for start_tick,lx,ly,langle in projectiles["Laser"]:
						if str(start_tick) not in other_players[enemy]["Projectiles"]["Laser"]:
							other_players[enemy]["Projectiles"]["Laser"][str(start_tick)] = Laser(start_tick,Vector2(lx,ly),langle)

			other_players[enemy]["Spaceship"].draw(
				window.screen,
				player.screen_position(window.screen,[x,y]),
				360 - angle, velocity
			)

			other_players[enemy]["Mothership"].draw(
				window.screen,
				player,
			)

			for _type,projectiles in other_players[enemy]["Projectiles"].items():
				for projectile in projectiles:
					if projectiles[projectile] == None: continue

					projectiles[projectile].Move(player.ticks)

					if not projectiles[projectile].Alive(player.ticks):
						other_players[enemy]["Projectiles"][_type][projectile] = None
					else:
						projectiles[projectile].draw(window.screen,player)
			

		ui.OPEN = not window.get_key(Globals.K_UNFOCUS)

		if Globals.K_GUI in window.keys_up: ui.FOCUSED = not ui.FOCUSED

		disconnect = ui.DrawUI(window,player)

		if disconnect: return 1

		stars.draw(window.screen,player,client.data["Tick"])
		asteroids.draw(window.screen,player,client.data["Tick"])

		player.MoveTick(window,ui.FOCUSED)

		window.draw(player,gm.FOREGROUND)

		if player.focused: 
			arrow.draw(window,player)

		if settings.Get("bShowFps"):
			window.draw(Text("%s FPS" % int(window.clock.get_fps()),[10, window.HEIGHT - 30],font_size=20,color=(255,255,255)))

		if settings.Get("bShowCoords"):
			window.draw(Text(player.position.rounded(1),[window.WIDTH - 10, window.HEIGHT - 10],font_size=20,color=(255,255,255),center=[gm.BOTTOM,gm.RIGHT]))

		window.update()

	settings.Save()

	return 0

if __name__ == '__main__':
	output = 1

	while output == 1:
		chosen_server = MainMenu()

		output = Main(chosen_server)