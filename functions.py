import math
from vector import *

def AngleToPosition(angle,distance):
	return Vector2(distance * math.cos(math.radians(angle)), distance * math.sin(math.radians(angle)))

def Angle(point1,point2):
	return math.degrees(math.atan2( point2.y-point1.y, point2.x-point1.x ))

def Distance(point1,point2):
	return math.sqrt( pow(point2.x-point1.x,2) + pow(point2.y-point1.y,2) )

def Angle2(point1,point2):
	return math.degrees(math.atan2( point2.y-point1.z, point2.x-point1.x ))

def Distance2(point1,point2):
	return math.sqrt( pow(point2.x-point1.x,2) + pow(point2.y-point1.z,2) )

