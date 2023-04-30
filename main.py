import GameMaker as gm

from player import *
from currency import *

MAP_SIZE = 5000

window = gm.Window([1920,1080],"Spaceships",background_color=(10,10,10),fullscreen=True,fps=120)

import ui

player = Player(window.H_WIDTH,window.H_HEIGHT)
exit = Button([window.WIDTH-25,0,25,25],"x",foreground_color=(230,0,0),hovered_color=(170,0,0),pressed_color=(120,0,0),outline=0)
arrow = Arrow()

stars = GenerateStars(int(MAP_SIZE * 1.5),MAP_SIZE)
asteroids = GenerateAsteroids(int(MAP_SIZE * 0.25),MAP_SIZE)

while window.RUNNING:
	if exit.status == gm.PRESSED: window.RUNNING = False

	ui.OPEN = not window.get_key(Globals.K_UNFOCUS)

	if Globals.K_GUI in window.keys_up: ui.FOCUSED = not ui.FOCUSED

	ui.DrawUI(window)

	stars.draw(window.screen,player)
	asteroids.draw(window.screen,player)

	player.MoveTick(window,asteroids,ui.FOCUSED)

	window.draw(player,gm.FOREGROUND)

	window.draw(exit,gm.GUI)

	if player.focused: 
		arrow.draw(window,player)

	window.update()