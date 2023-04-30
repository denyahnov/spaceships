from classes import *

from GameMaker.Assets import RotatedImage

ICON_SIZE = 40,40

class Titanium(Currency):
	def __init__(self,*position):
		super().__init__(
			title = "Titanium",
			icon = RotatedImage("assets\\icon_currency_titanium.png",[*position,ICON_SIZE[0],ICON_SIZE[1]]),
			draw_image = RotatedImage("assets\\draw_currency_titanium.png",[0,0,0,0]),
			description = "Used in almost any craft, most commonly for structure",
			position = position,
		)

class Gear(Currency):
	def __init__(self,*position):
		super().__init__(
			title = "Gear",
			icon = RotatedImage("assets\\icon_currency_gear.png",[*position,ICON_SIZE[0],ICON_SIZE[1]]),
			draw_image = RotatedImage("assets\\draw_currency_gear.png",[0,0,0,0]),
			description = "Used for mechanical crafts, usually if moving parts are required",
			position = position,
		)

class Plasma(Currency):
	def __init__(self,*position):
		super().__init__(
			title = "Plasma",
			icon = RotatedImage("assets\\icon_currency_plasma.png",[*position,ICON_SIZE[0],ICON_SIZE[1]]),
			draw_image = RotatedImage("assets\\draw_currency_plasma.png",[0,0,0,0]),
			description = "High tier element used as an energy source in crafts",
			position = position,
		)

class Magnesium(Currency):
	def __init__(self,*position):
		super().__init__(
			title = "Magnesium",
			icon = RotatedImage("assets\\icon_currency_magnesium.png",[*position,ICON_SIZE[0],ICON_SIZE[1]]),
			draw_image = RotatedImage("assets\\draw_currency_magnesium.png",[0,0,0,0]),
			description = "Explosive material commonly used in combat craft",
			position = position,
		)