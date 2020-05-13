from Model.class_Animated import Animated
from Model.class_Mob import Mob
from Model.class_Archer import Archer


# Hero est la classe générique des héros
# Carastéristiques des héros:
#   Ils sont controlés au clavier
#   Ils peuvent double-sauter
#   Ils ont des spells (définis dans la classe fille)
class SacDeSable(Archer):
	def __init__(self, x, y, windowWidth, strength):
		Archer.__init__(self, x, y, windowWidth, strength)

	def update(self, hero, fps):
		if self.x < self.windowWidth/2 - 30:
			Animated.changeState(self, "RmoveRight")
			self.moveRight()
		elif self.x > self.windowWidth/2 + 30:
			Animated.changeState(self, "RmoveLeft")
			self.moveLeft()
		else:
			if self.x > hero.get_x2():
				Animated.changeState(self, "RidleLeft")
			else:
				Animated.changeState(self, "RidleRight")
			self.stop()
		Mob.update(self, hero, fps)
