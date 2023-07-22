import GameMaker as gm

from player import *
from currency import *

window = gm.Window([1920,1080],"Spaceships",background_color=(10,10,10),fullscreen=True,fps=70)

import ui
import network
import settings

settings.Load()
ui.settings = settings

player = Player(settings.Get("szAccountName"),window.H_WIDTH,window.H_HEIGHT)
arrow = Arrow()

servers = network.FindServers()

if len(servers) == 0: 
	exit("Network -> No Available Servers")

chosen_server = servers[0]

client = network.Client(player)
client.Connect(chosen_server["Address"],65432)

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

while window.RUNNING and client.CONNECTED:
	player.ticks = client.data["Tick"]

	for values in client.data["Players"]:
		enemy, (x, y, angle, velocity), projectiles = values["Port"],values["Position"],values["Projectiles"]

		if enemy not in other_players:
			other_players[enemy] = {"Spaceship": Spaceship(55),"Projectiles":{"Laser": {}}} 

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

	ui.DrawUI(window)

	stars.draw(window.screen,player,client.data["Tick"])
	asteroids.draw(window.screen,player,client.data["Tick"])

	player.MoveTick(window,ui.FOCUSED)

	window.draw(player,gm.FOREGROUND)

	if player.focused: 
		arrow.draw(window,player)

	if settings.Get("bShowFps"):
		window.draw(Text("%s FPS" % int(window.clock.get_fps()),[10, window.HEIGHT - 30],font_size=20,color=(255,255,255)))

	window.update()

settings.Save()