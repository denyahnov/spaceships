import GameMaker as gm

from player import *
from currency import *

MAP_SIZE = 5000

window = gm.Window([1920,1080],"Spaceships",background_color=(10,10,10),fullscreen=True,fps=70)

import ui
import network
import settings

settings.Load()

player = Player(settings.Get("szAccountName"),window.H_WIDTH,window.H_HEIGHT)
arrow = Arrow()

servers = network.FindServers()

if len(servers) == 0: 
	exit("Network -> No Available Servers")

chosen_server = servers[0]

client = network.Client(player)
client.Connect(chosen_server["Address"],65432)

random.seed(chosen_server["Seed"])

stars = GenerateStars(int(MAP_SIZE * 1.5),MAP_SIZE)
asteroids = GenerateAsteroids(int(MAP_SIZE * 0.25),MAP_SIZE)

for asteroid in asteroids.items:
	asteroid.draw_image.rotation += asteroid.rotation_speed * chosen_server["Ticks"]

	asteroid.position += AngleToPosition(90 - asteroid.angle, asteroid.velocity * chosen_server["Ticks"])

other_players = {}

while window.RUNNING and client.CONNECTED:
	for enemy, x, y, angle, velocity in client.data["Players"]:
		if enemy not in other_players: 
			other_players[enemy] = Spaceship(55)

		other_players[enemy].draw(
			window.screen,
			player.screen_position(window.screen,[x,y]),
			360 - angle, velocity
		)

	ui.OPEN = not window.get_key(Globals.K_UNFOCUS)

	if Globals.K_GUI in window.keys_up: ui.FOCUSED = not ui.FOCUSED

	ui.DrawUI(window)

	stars.draw(window.screen,player,client.data["Tick"])
	asteroids.draw(window.screen,player,client.data["Tick"])

	player.MoveTick(window,ui.FOCUSED)

	window.draw(player,gm.FOREGROUND)

	if player.focused: 
		arrow.draw(window,player)

	window.draw(Text("%s FPS" % int(window.clock.get_fps()),[10, window.HEIGHT - 30],font_size=20,color=(255,255,255)))

	window.update()