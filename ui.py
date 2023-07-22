from currency import *

class LinkedButton():
	def __init__(self,text,image,parent,offset,size,hover_scaling=1.1,clicked_scaling=1.05):
		self.text = Text(text,[0,0],color=(96,134,156),center=[gm.CENTER, gm.CENTER])
		self.size = [0,0] + size
		self.image = RotatedImage(image,self.size)
		self.parent = parent
		self.offset = offset

		self.hover_scaling = hover_scaling
		self.clicked_scaling = clicked_scaling

		self.status = gm.NONE

	def draw(self):
		return [self.image, self.text]

	def update(self):
		self.image.x = self.parent.x + self.offset[0]
		self.image.y = self.parent.y + self.offset[1]

		x,y = pg.mouse.get_pos()
		click = pg.mouse.get_pressed(num_buttons=3)[0]

		w = (x >= self.image.x) and (x <= self.image.x + self.image.w)
		h = (y >= self.image.y) and (y <= self.image.y + self.image.h)

		self.status = gm.HELD if w and h and click and self.status in [gm.PRESSED,gm.HELD] else gm.PRESSED if w and h and click else gm.RELEASED if not click and self.status in [gm.PRESSED,gm.HELD] else gm.HOVERED if w and h else gm.NONE

		if self.status in [gm.HOVERED,gm.RELEASED]:
			
			self.image.w = self.size[2] * self.hover_scaling
			self.image.h = self.size[3] * self.hover_scaling

			self.image.x -= (self.image.w - self.size[2]) / 2
			self.image.y -= (self.image.h - self.size[3]) / 2

			self.image.image = pg.transform.scale(self.image.image, (self.image.w, self.image.h))
		elif self.status in [gm.PRESSED,gm.HELD,gm.RELEASED]:
			
			self.image.w = self.size[2] * self.clicked_scaling
			self.image.h = self.size[3] * self.clicked_scaling

			self.image.x -= (self.image.w - self.size[2]) / 2
			self.image.y -= (self.image.h - self.size[3]) / 2

			self.image.image = pg.transform.scale(self.image.image, (self.image.w, self.image.h))
		else:
			self.image.w = self.size[2]
			self.image.h = self.size[3]

			self.image.image = pg.transform.scale(self.image.image, (self.image.w, self.image.h))

		self.text.x = self.image.x + self.image.w / 2
		self.text.y = self.image.y + self.image.h / 2

class Checkbox():
	def __init__(self,position):
		self.position = position
		self.background = RotatedImage("assets\\icon_ui_square.png",self.position)
		self.check = RotatedImage("assets\\icon_ui_check.png",self.position)


titanium 	= Titanium(0,0)
gear 		= Gear(0,40)
plasma 		= Plasma(0,80)
magnesium 	= Magnesium(0,120)

inventory = Currency("",RotatedImage("assets\\icon_ui_background.png",[-500,160,500,400]),None,"",position=[390,160],hide=[-500,160])

play_button = LinkedButton("Continue", "assets\\icon_ui_button.png",inventory.icon,[138,110],[220,60])
settings_button = LinkedButton("Settings", "assets\\icon_ui_button.png",inventory.icon,[138,190],[220,60])
exit_button = LinkedButton("Exit", "assets\\icon_ui_button.png",inventory.icon,[138,270],[220,60])

account_button_1 = LinkedButton("", "assets\\icon_ui_square.png",inventory.icon,[55,95],[64,64])
account_button_2 = LinkedButton("", "assets\\icon_ui_account.png",inventory.icon,[55,95],[64,64])

world_info = Text("Map Size: \nMap Seed: ",[0,0],font_size=10,color=(220,220,220))

global OPEN
global FOCUSED

OPEN = True
FOCUSED = False

ALPHA = 160,20

def Animate():
	global OPEN
	global FOCUSED

	titanium.Animate(OPEN and not FOCUSED)
	gear.Animate(OPEN and not FOCUSED)
	plasma.Animate(OPEN and not FOCUSED)
	magnesium.Animate(OPEN and not FOCUSED)

	inventory.Animate(FOCUSED)

	play_button.update()
	settings_button.update()
	exit_button.update()
	account_button_1.update()
	account_button_2.update()

	world_info.x = inventory.icon.x + 90
	world_info.y = inventory.icon.y + 330

def DrawUI(window):
	global FOCUSED

	Animate()

	if play_button.status in [gm.PRESSED, gm.HELD]:
		FOCUSED = False

	if exit_button.status in [gm.PRESSED, gm.HELD]:
		window.RUNNING = False

	window.draw(
		[inventory.icon,world_info] + 
		play_button.draw() + 
		settings_button.draw() + 
		exit_button.draw() + 
		account_button_1.draw() +
		account_button_2.draw(),
	gm.GUI)

	window.draw([titanium,gear,plasma,magnesium],gm.GUI)