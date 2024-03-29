import Globals

from classes import *

import timeit

from GameMaker.Physics import Movement2D

class Player():
	def __init__(self,username,spawnpoint=[0,0],camera = Vector3(0,0,0)):
		self.size = 55
		self.health = 100

		self.angle = 0
		self.velocity = 0

		self.focused = True
		self.username = username
		self.spawnpoint = spawnpoint

		self.spaceship = Spaceship(self.size)
		self.mothership = Mothership(self.username,Vector2(self.spawnpoint[0],self.spawnpoint[1]),90)

		self.position = Vector2(self.spawnpoint[0],self.spawnpoint[1])

		self.camera_target = self.position

		self.camera = camera

		self.Movement = Movement2D(min_speed=0.01,max_speed=3.2,speed=0.07,scaling=0.98)
		self.Rotation = Movement2D(max_speed=2.5,speed=0.2)

		self.projectiles = {
			"Laser": [],
		}

		self.trail = []

		self.ticks = 0
		self.shoot_cooldown = 18
		self.last_shoot = -self.shoot_cooldown
		self.left_right_shot = False

		self.collision = None

	def setUsername(self,text):
		self.username = text
		self.mothership.title = text
		self.mothership.text.update(text)

	def setSpawnpoint(self,position,change_pos=False):
		self.spawnpoint = position

		if change_pos:
			self.position.x, self.position.y = self.spawnpoint
			self.mothership.position.x, self.mothership.position.y = self.spawnpoint
			self.camera.x, self.camera.z = self.spawnpoint

			self.mothership.updateCenter()

	def Shoot(self,true=True):
		if true and self.ticks > self.last_shoot + self.shoot_cooldown:
			offset = AngleToPosition(90 - self.angle + (90 if self.left_right_shot else -90), 8)

			self.projectiles["Laser"].append(Laser(self.ticks,self.position + offset,self.angle))
			self.last_shoot = self.ticks
			self.left_right_shot = not self.left_right_shot

			self.velocity *= 0.5

	def MoveCamera(self,target,smoothing=20):
		self.camera += AngleToPosition(Angle2(self.camera, target), Distance2(self.camera, target) / smoothing)

	def MoveTick(self,window,ui_focused):
		size = self.screen_position(window.screen)

		if self.collision != None:
			self.angle = self.collision - 90
		elif not ui_focused:
			self.Movement.move_left(window.get_key(Globals.K_BACKWARD) and self.velocity > 0)
			self.Movement.move_right(window.get_key(Globals.K_FORWARD))

			self.Rotation.move_left(window.get_key(Globals.K_LEFT))
			self.Rotation.move_right(window.get_key(Globals.K_RIGHT))

		self.velocity = self.Movement.tick()

		if not ui_focused:
			self.Shoot(window.get_key(Globals.K_SHOOT))

		self.angle += self.Rotation.tick()

		self.position += AngleToPosition(90 - self.angle,self.velocity)

		if not ui_focused:
			if window.get_key(Globals.K_UNFOCUS): 
				self.camera_target = self.mothership.center
				self.focused = False
			else:
				self.camera_target = self.position
				self.focused = True

		self.MoveCamera(self.camera_target)

		self.collision = None

	def screen_position(self,window,position=[]):
		if len(position) == 0: position = [self.position.x, self.position.y]

		return RectStruct(
			window.get_width()/2 + (position[0] - self.camera.x), 
			window.get_height()/2 - (position[1] - self.camera.z), 
			self.size * self.camera.y/10,
			self.size * self.camera.y/10,
		)

	def draw_projectiles(self,window):
		for _type,projectiles in self.projectiles.items():
			for projectile in projectiles:
				projectile.Move(self.ticks)

				if not projectile.Alive(self.ticks):
					self.projectiles[_type].remove(projectile)
				else:
					projectile.draw(window,self)

	def draw_trail(self,window):
		for t in self.trail:
			if t.Alive():
				t.draw(window,self)
			else:
				self.trail.remove(t)

	def draw(self,window):
		self.trail.append(Trail([self.position.x, self.position.y, 4, 4], self.angle))

		self.draw_projectiles(window)
		self.draw_trail(window)

		self.spaceship.draw(window,self.screen_position(window),360 - self.angle,self.velocity)

		self.mothership.draw(window,self)

	def dump(self):
		return {
			"Username": self.username,
			"Position":[
				round(self.position.x,2),
				round(self.position.y,2),
				round(self.angle,2),
				round(self.velocity,2),
			],
			"Projectiles": {_type: [entity.dump() for entity in entities] for _type,entities in self.projectiles.items()}
		}
