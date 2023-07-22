import GameMaker as gm
from GameMaker.Assets import *

import random
from functions import *

def CircleCollision(player,position,a):
	item = a.draw_image

	distance = Distance(position, Vector2(item.x + item.w/2,item.y + item.h/2))

	if distance < item.w/2:
		player.collision = Angle(position, Vector2(item.x + item.w/2,item.y + item.h/2))

def GenerateAsteroids(amount,pos_range):
	return AssetList([Asteroid(
		Vector2(random.randint(-pos_range,pos_range), random.randint(-pos_range,pos_range)), 
		size=random.uniform(0.5,1.5), 
		angle=random.randint(0,360),
		velocity=random.uniform(0.03,0.1),
		rotation_speed=random.uniform(0.05,0.165),
	) for i in range(amount)])

def GenerateStars(amount,pos_range):
	return AssetList([Star( Vector2(random.randint(-pos_range,pos_range), random.randint(-pos_range,pos_range)), size=random.uniform(0.5,1.5), angle=random.randint(0,360)) for i in range(amount)])

def BrokenAsteroid():
	return AssetList([
		Asteroid(
			position=self.parent.position,
			size=self.parent.size,
			angle=self.parent.angle,
			velocity=self.parent.velocity,
			rotation_speed=self.parent.rotation_speed,
			path=f"assets\\draw_asteroid_{i+2}.png"
		) for i in range(4)
	])

class AssetList():
	def __init__(self,items):
		self.items = items

		try:
			items[0].Move
			self.should_move = True
		except:
			self.should_move = False

		try:
			items[0].collision
			self.collision_check = True
		except:
			self.collision_check = False

	def draw(self,window,player,tick):
		for item in self.items:

			if self.should_move: item.Move(tick)

			if self.collision_check: item.Collide(player,window)
	
			item.draw_image.x = window.get_width()/2 + item.position.x - player.camera.x
			item.draw_image.y = window.get_height()/2 - item.position.y + player.camera.z

			if 0 - item.draw_image.w < item.draw_image.x < window.get_width():
				if 0 - item.draw_image.h < item.draw_image.y < window.get_height():
					item.draw_image.draw(window)

	def dump(self):
		return self.items[0].title,[item.dump() for item in self.items]

class Spaceship():
	"""docstring for Spaceship"""
	def __init__(self,size):
		self.attachments = []

		self.body = RotatedImage("assets\\draw_spaceship_body.png",[0,0,size,size])
		self.fire = RotatedImage("assets\\draw_spaceship_fire.png",[0,0,size,size])

	def draw(self,window,rect,angle,speed):
		self.body.x,self.body.y,self.body.w,self.body.h = rect.format()
		self.fire.x,self.fire.y,self.fire.w,self.fire.h = rect.format()

		self.body.rotation = angle
		self.fire.rotation = angle

		offset = AngleToPosition(90 - angle, speed * 3)

		self.fire.x += offset.x
		self.fire.y += offset.y

		self.fire.draw(window)
		self.body.draw(window)

class Attachment():
	"""docstring for Attachment"""
	def __init__(self,title,base_price,price_scale,description):
		self.title = title
		self.base_price = base_price
		self.price_scale = price_scale
		self.description = description

class Currency():
	"""Base Class for Currency"""
	def __init__(self,title,icon,draw_image,description,value=0,position=[0,0],hide=[0,0]):
		self.title = title
		self.icon = icon
		self.draw_image = draw_image
		self.description = description

		self.position = position
		self.hide = hide

		self.value = value
		self.text = Text(self.value,self.position,color=(255,255,255),center=[gm.CENTER,gm.CENTER])

	def Animate(self,visible=True,smoothing=5):
		if visible:
			self.icon.x += (self.position[0] - self.icon.x) / smoothing
		else:
			self.icon.x += ((self.position[0] - (self.icon.w + self.text.w + 5)) - self.icon.x + self.hide[0]) / smoothing

	def draw(self,window):
		# self.text.update(self.value)

		self.text.x = self.icon.x + self.icon.w + self.text.w/2 + 3
		self.text.y = self.icon.y + self.text.h/2 + 7

		self.icon.draw(window)
		self.text.draw(window)

class Asteroid():
	"""Base Asteroid Class"""
	def __init__(self,position,angle=0,size=1,velocity=0.05,rotation_speed=0.1,path="assets\\draw_asteroid_1.png"):
		self.start_position = position
		self.position = self.start_position
		self.size = size
		self.angle = angle
		self.draw_image = RotatedImage(path,[position.x,position.y,60*size,60*size],rotation=self.angle)

		self.velocity = velocity
		self.rotation_speed = rotation_speed

		self.title = "Asteroid"

		self.collision = None

	def draw(self,window,tick):
		self.position = self.start_position + AngleToPosition(90 - self.angle,self.velocity * tick)

		self.draw_image.x = self.position.x
		self.draw_image.y = self.position.y

		self.draw_image.w = 60 * self.size
		self.draw_image.h = 60 * self.size

		self.draw_image.rotation = self.angle + self.rotation_speed * tick

		self.draw_image.draw(window)

	def Move(self,tick):
		self.position = self.start_position + AngleToPosition(90 - self.angle,self.velocity * tick)
		self.draw_image.rotation = self.angle + self.rotation_speed * tick

	def Collide(self,player,window):
		size = player.screen_position(window)

		CircleCollision(player,Vector2(size.x + size.w/2, size.y + size.h/2),self)

class Star():
	"""Visual Star"""
	def __init__(self,position,angle=0,size=1):
		self.position = position
		self.size = size
		self.angle = angle
		self.draw_image = RotatedImage("assets\\draw_star_1.png",[position.x,position.y,10*size,10*size],rotation=self.angle)

		self.title = "Star"

	def draw(self,window,tick):
		self.draw_image.x = self.position.x
		self.draw_image.y = self.position.y

		self.draw_image.w = 10 * self.size
		self.draw_image.h = 10 * self.size

		self.draw_image.rotation = self.angle

		self.draw_image.draw(window)

class Laser():
	"""Laser Weapon Class"""
	def __init__(self,position,rotation,size=1):
		self.position = position
		self.rotation = rotation
		self.size = size
		self.draw_image = RotatedImage("assets\\draw_laser_1.png",[0,0,self.size*5,self.size*5])

		self.velocity = 6
		self.lifetime = 200
		self.ticks = 0

		self.title = "Laser"

	def Alive(self):
		return self.ticks < self.lifetime

	def MoveTick(self):
		self.position += AngleToPosition(90 - self.rotation,self.velocity)
		self.ticks += 1

	def draw(self,window,player):
		self.draw_image.x = window.get_width()/2 + self.position.x - player.camera.x
		self.draw_image.y = window.get_height()/2 - self.position.y + player.camera.z

		self.draw_image.w = 5 * self.size
		self.draw_image.h = 5 * self.size

		self.draw_image.rotation = 180 - self.rotation

		self.draw_image.draw(window)
		
class Mothership():
	"""Main Player Base for Upgrades"""
	def __init__(self,title,position,rotation=0):
		self.position = position
		self.rotation = rotation

		self.draw_image = RotatedImage("assets\\draw_mothership_body.png",[0,0,400,450])

		self.center = Vector2(self.position.x + self.draw_image.w/2, self.position.y - self.draw_image.h/2)

		self.title = title
		self.text = Text(title,[0,0],center=[gm.CENTER,gm.CENTER],color=(255,255,255),font_size=50)

		self.health = 100
		self.healthbar = ProgressBar([0,0,200,12])

	def draw(self,window,player):
		self.draw_image.x = window.get_width()/2 + self.position.x - player.camera.x
		self.draw_image.y = window.get_height()/2 - self.position.y + player.camera.z

		self.draw_image.rotation = self.rotation

		self.draw_image.draw(window)

		self.text.x = self.draw_image.x + self.draw_image.w/2
		self.text.y = self.draw_image.y + self.draw_image.h/2 - 10

		self.healthbar.x = self.draw_image.x + self.draw_image.w/2 - self.healthbar.w/2
		self.healthbar.y = self.draw_image.y + self.draw_image.h/2 + 20

		self.healthbar.update(self.health / 100)

		self.text.draw(window)
		self.healthbar.draw(window)

class Arrow():
	def __init__(self):
		self.icon = RotatedImage("assets\\icon_arrow.png",[0,0,60,60])

	def draw(self,window,player):
		angle,distance = Angle(player.position,player.mothership.center),Distance(player.position,player.mothership.center)

		if distance < 200: return

		if distance > 630: distance = 630

		position = AngleToPosition(angle, distance/2)

		self.icon.x, self.icon.y =  window.H_WIDTH + position.x, window.H_HEIGHT - position.y

		self.icon.rotation = angle + 90

		window.draw(self.icon)

class Trail():
	def __init__(self,position,rotation = 0):
		self.position = RectStruct(*position)

		self.rotation = rotation

		self.increment = 4.5

		self.loffset = AngleToPosition(self.rotation + 35,13)
		self.roffset = AngleToPosition(self.rotation - 35,13)

		self.left = AlphaRectangle(self.position + self.loffset, [171,219,227,70], 90 - self.rotation)
		self.right = AlphaRectangle(self.position - self.roffset, [171,219,227,70], 90 - self.rotation)

	def Alive(self):
		return self.left.color[3] > self.increment

	def draw(self,window,player):
		self.left.color[3] -= self.increment
		self.right.color[3] -= self.increment

		self.left.x = window.get_width()/2 + self.position.x - player.camera.x + self.loffset.x - self.position.w/2
		self.left.y = window.get_height()/2 - self.position.y + player.camera.z + self.loffset.y - self.position.h/2

		self.right.x = window.get_width()/2 + self.position.x - player.camera.x - self.roffset.x - self.position.w/2
		self.right.y = window.get_height()/2 - self.position.y + player.camera.z - self.roffset.y - self.position.h/2

		self.left.draw(window)
		self.right.draw(window)