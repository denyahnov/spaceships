from classes import *

class BoosterEngine(Attachment):
	"""Booster Engine Attachment"""
	def __init__(self):
		super().__init__(
			title = "Booster Engine",
			base_price = {
				"Titanium": 3,
				"Gear": 1,
				"Plasma": 2,
			},
			price_scale = 1,
			description = "This extra engine allows you to have a burst of speed for a short duration"
		)