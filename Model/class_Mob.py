from Model.class_Charac import Charac


# Mob est la classe générique des mobs
# Carastéristiques des mobs:
#   Ils ont des spells (définis dans la classe fille)
class Mob(Charac):
	def __init__(
		self, x, y, width, height, images, weight, baseAcc_x, baseJumpForce, maxSpeed_x, windowWidth, hp, atkList
	):
		Charac.__init__(
			self, x, y, width, height, images, weight, baseAcc_x, baseJumpForce, maxSpeed_x, windowWidth, hp, atkList
		)
		self.states['RmoveLeft'] = 100
		self.states['RmoveRight'] = 100
		self.states['FjumpLeft'] = 100
		self.states['FjumpRight'] = 100
		self.states['Oaa1Right'] = 75
		self.states['Oaa1Left'] = 75
		self.states['OdmgRight'] = 400
		self.states['OdmgLeft'] = 400
		self.up = False
		self.left = False
		self.right = False
		self.spell1 = False

	def update(self, hero, fps):
		Charac.update(self, hero, fps)
