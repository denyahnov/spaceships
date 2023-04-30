from currency import *

titanium 	= Titanium(0,0)
gear 		= Gear(0,40)
plasma 		= Plasma(0,80)
magnesium 	= Magnesium(0,120)

background = AlphaRectangle([0,0,2000,2000],color=[40,40,50,0])

inventory = Currency("",RotatedImage("assets\\icon_ui_background.png",[-500,160,500,400]),None,"",position=[390,160],hide=[-500,160])

OPEN = True
FOCUSED = False

ALPHA = 160,20

def Animate():
	titanium.Animate(OPEN and not FOCUSED)
	gear.Animate(OPEN and not FOCUSED)
	plasma.Animate(OPEN and not FOCUSED)
	magnesium.Animate(OPEN and not FOCUSED)

	inventory.Animate(FOCUSED)

	if FOCUSED and background.color[3] < ALPHA[0]:
		background.color[3] += ALPHA[1]
	if not FOCUSED and background.color[3] > 0:
		background.color[3] -= ALPHA[1]

def DrawUI(window,true=True):
	Animate()

	window.draw([background,inventory.icon],gm.GUI)

	window.draw([titanium,gear,plasma,magnesium],gm.GUI)