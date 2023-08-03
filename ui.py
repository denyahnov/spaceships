from currency import *

class LinkedButton():
	def __init__(self,text,image,parent,offset,size,hover_scaling=1.1,clicked_scaling=1.05):
		self.text = Text(text,[0,0],color=(96,134,156),center=[gm.CENTER, gm.CENTER],font_size=24)
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
	global settings

	def __init__(self,variable,text,parent,position):
		self.variable = variable
		self.parent = parent
		self.position = position + [32,32]
		self.text = Text(text,[0,0],color=(96,134,156),center=[gm.CENTER, gm.LEFT],font_size=20)
		
		self.check = RotatedImage("assets\\icon_ui_check.png",self.position)
		self.background = RotatedImage("assets\\icon_ui_square.png",self.position)

		self.status = gm.NONE

	def draw(self):
		return [self.background, self.text] + ([self.check] if settings.Get(self.variable) else [])

	def update(self):
		global SETTINGS

		self.check.x = self.parent.x + self.position[0]
		self.check.y = self.parent.y + self.position[1]

		self.background.x, self.background.y = self.check.x, self.check.y
		self.text.x, self.text.y = self.check.x + 38, self.check.y + self.check.h / 2

		x,y = pg.mouse.get_pos()
		click = pg.mouse.get_pressed(num_buttons=3)[0]

		w = (x >= self.background.x) and (x <= self.background.x + self.background.w)
		h = (y >= self.background.y) and (y <= self.background.y + self.background.h)

		self.status = gm.HELD if w and h and click and self.status in [gm.PRESSED,gm.HELD] else gm.PRESSED if w and h and click else gm.RELEASED if not click and self.status in [gm.PRESSED,gm.HELD] else gm.HOVERED if w and h else gm.NONE

		if self.status == gm.RELEASED and SETTINGS:
			settings.Set(self.variable, not settings.Get(self.variable))

global settings
settings = None

titanium 	= Titanium(0,0)
gear 		= Gear(0,40)
plasma 		= Plasma(0,80)
magnesium 	= Magnesium(0,120)

inventory = Currency("",RotatedImage("assets\\icon_ui_background.png",[-500,160,500,400]),None,"",position=[390,160],hide=[-500,160])

disconnect_button = LinkedButton("Disconnect", "assets\\icon_ui_button.png",inventory.icon,[138,110],[220,60])
settings_button = LinkedButton("Settings", "assets\\icon_ui_button.png",inventory.icon,[138,190],[220,60])
exit_button = LinkedButton("Exit", "assets\\icon_ui_button.png",inventory.icon,[138,270],[220,60])

account_button_1 = LinkedButton("", "assets\\icon_ui_square.png",inventory.icon,[55,95],[64,64])
account_button_2 = LinkedButton("", "assets\\icon_ui_account.png",inventory.icon,[55,95],[64,64])

world_info = Text("Map Size: \nMap Seed: ",[0,0],font_size=10,color=(220,220,220),center=[gm.TOP,gm.LEFT])

settings_exit1 = LinkedButton("", "assets\\icon_ui_square.png",inventory.icon,[390,95],[48,48])
settings_exit2 = LinkedButton("", "assets\\icon_ui_cross.png", inventory.icon,[390,95],[48,48])

checkboxes = [
	Checkbox("bShowFps","Show FPS Counter",	inventory.icon,	[100,110]),
	Checkbox("bShowCoords","Show Player Position",	inventory.icon,	[100,150]),
]

username_text = Text("Account Username:",[0,0],font_size=16,color=(96,134,156))
username_input = Textbox([0,0,280,36],max_length=20,background_color=(96,134,156),text_color=(96,134,156),foreground_color=(157,190,209))
username_save = LinkedButton("Save", "assets\\icon_ui_button.png",inventory.icon,[168,190],[160,40])

server_input = Textbox([0,0,250,80],max_length=6,background_color=(96,134,156),text_color=(96,134,156),foreground_color=(157,190,209),only_in="1234567890")

code_text = Text("Enter Code",[server_input.x + 10,server_input.y + 10],color=(96,134,156),center=[gm.CENTER,gm.CENTER])

server_ready1 = LinkedButton("", "assets\\icon_ui_square.png",server_input,[server_input.w + 10,0],[server_input.h,server_input.h])
server_ready2 = LinkedButton("", "assets\\icon_ui_check.png", server_input,[server_input.w + 10,0],[server_input.h,server_input.h])

autojoin_button = LinkedButton("Autojoin", "assets\\icon_ui_button.png",server_input,[0,100],[320,80])
exit_menu = LinkedButton("Exit", "assets\\icon_ui_button.png",server_input,[60,330],[200,80])

title_screen = RotatedImage("assets\\icon_title.png",[0,0,800,120])

global OPEN
global FOCUSED
global ACCOUNT

OPEN = True
FOCUSED = False
SETTINGS = False
ACCOUNT = False

def ShowLog(window,log):
	window.draw(Text("\n".join(log),[window.H_WIDTH,window.H_HEIGHT],color=(255,255,255),center=[gm.CENTER,gm.CENTER],font_size=32))
	window.update()

def Reset():
	global OPEN
	global FOCUSED
	global ACCOUNT

	OPEN = True
	FOCUSED = False
	SETTINGS = False
	ACCOUNT = False

def Init(s):
	global settings

	settings = s

	username_input.text = settings.Get("szAccountName")
	username_input.draw_text.update(username_input.text)

def MainMenu(window):
	server_input.x = window.H_WIDTH - 160
	server_input.y = 250

	code_text.x = server_input.x + server_input.w/2
	code_text.y = server_input.y + server_input.h/2

	title_screen.x = window.H_WIDTH - title_screen.w/2
	title_screen.y = 50

	server_input.update(window)

	server_ready1.update()
	server_ready2.update()

	autojoin_button.update()
	exit_menu.update()

	window.draw([title_screen,server_input] + server_ready1.draw() + server_ready2.draw() + autojoin_button.draw() + exit_menu.draw(),gm.GUI)

	if len(server_input.text) == 0:
		window.draw(code_text,gm.GUI)

	window.update()

	if exit_menu.status == gm.PRESSED:
		window.RUNNING = False

	if autojoin_button.status == gm.RELEASED:
		return 1

	if server_ready1.status == gm.RELEASED:
		return server_input.text

	return 0

def Animate():
	global OPEN
	global FOCUSED

	titanium.Animate(OPEN and not FOCUSED)
	gear.Animate(OPEN and not FOCUSED)
	plasma.Animate(OPEN and not FOCUSED)
	magnesium.Animate(OPEN and not FOCUSED)

	inventory.Animate(FOCUSED)

	disconnect_button.update()
	settings_button.update()
	exit_button.update()
	account_button_1.update()
	account_button_2.update()

	settings_exit1.update()
	settings_exit2.update()

	username_save.update()

	[c.update() for c in checkboxes]

	world_info.x = inventory.icon.x + 60
	world_info.y = inventory.icon.y + 330

	username_text.x = inventory.icon.x + 100
	username_text.y = inventory.icon.y + 120

	username_input.x = inventory.icon.x + 100
	username_input.y = inventory.icon.y + 140

def DrawUI(window,player):
	global FOCUSED
	global SETTINGS
	global ACCOUNT

	global settings

	Animate()

	if not FOCUSED:
		SETTINGS = False
		ACCOUNT = False

	if not SETTINGS and not ACCOUNT and disconnect_button.status == gm.RELEASED:
		return True

	if not SETTINGS and not ACCOUNT and settings_button.status == gm.RELEASED:
		SETTINGS = True

	if not SETTINGS and not ACCOUNT and exit_button.status == gm.RELEASED:
		window.RUNNING = False

	if not SETTINGS and not ACCOUNT and account_button_1.status == gm.RELEASED:
		ACCOUNT = True

		username_input.text = settings.Get("szAccountName")
		username_input.draw_text.update(username_input.text)

	if settings_exit1.status == gm.RELEASED:
		if SETTINGS:
			SETTINGS = False
		elif ACCOUNT:
			ACCOUNT = False
		elif FOCUSED:
			FOCUSED = False

	if ACCOUNT:
		username_input.update(window)

		if username_save.status == gm.RELEASED:
			player.setUsername(username_input.text)
			settings.Set("szAccountName", username_input.text)

	window.draw([inventory.icon,world_info] + settings_exit1.draw() + settings_exit2.draw(), gm.GUI)

	if SETTINGS:
		for c in checkboxes:
			window.draw(c.draw(),gm.GUI)
	elif ACCOUNT:
		window.draw([username_text,username_input] + username_save.draw(),gm.GUI)
	else:
		window.draw(
			disconnect_button.draw() + 
			settings_button.draw() + 
			exit_button.draw() + 
			account_button_1.draw() + 
			account_button_2.draw(),
			gm.GUI
		)

	window.draw([titanium,gear,plasma,magnesium],gm.GUI)

	return False