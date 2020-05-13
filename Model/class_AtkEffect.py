from Model.class_Animated import Animated


# Atk Effect est le spell en lui meme
# Carastéristiques des atk effect:
#   un set d'images (pas d'état)
#   des dégâts (dmg)
#   une force de répulsion px/fps(knockback)
#   une durée ms(duration) => l'attaque disparait au contact de toute façon
#   un poids acc_y(weight)
#   une vitesse initiale px/fps (speed_x et speed_y)
class AtkEffect(Animated):
	def __init__(
		self, nom, x, y, width, height, images, dmg, knockback_x, knockback_y, weight, speed_x, speed_y, facing, duration
	):
		Animated.__init__(self, x, y, width, height, images)
		self.states["idleRight"] = 75
		self.states["idleLeft"] = 75
		self.nom = nom
		self.dmg = dmg
		self.knockback_x = knockback_x
		self.knockback_y = knockback_y
		self.weight = weight
		self.speed_x = speed_x
		self.speed_y = speed_y
		self.duration = duration
		self.images = images
		self.hit = False
		if facing == 1:
			Animated.changeState(self, "idleRight")
		else:
			Animated.changeState(self, "idleLeft")

	def get_x1(self):
		return self.x

	def get_x2(self):
		return self.x+self.rect.width

	def get_y1(self):
		return self.y

	def get_y2(self):
		return self.y+self.rect.height

	def get_knockBack_x(self):
		return self.knockback_x

	def get_knockBack_y(self):
		return self.knockback_y

	def get_dmg(self):
		return self.dmg

	def get_duration(self):
		return self.duration

	def get_nom(self):
		return self.nom

	def isLive(self):
		return self.duration > 0

	def didHit(self):
		return self.hit

	def delete(self):
		self.hit = True
		self.duration = 0

	def update(self, hero, fps):
		if self.duration > 0:
			self.duration = self.duration - (1000/fps)
			self.speed_y += self.weight
			self.x += self.speed_x
			self.y += self.speed_y
			Animated.update(self, hero, fps)
