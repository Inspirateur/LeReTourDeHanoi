import pygame
from Model.class_Animated import Animated
from Model.class_Mob import Mob
from Model.class_Atk import Atk
from utils import load_imgs


# Hero est la classe générique des héros
# Carastéristiques des héros:
#   Ils sont controlés au clavier
#   Ils peuvent double-sauter
#   Ils ont des spells (définis dans la classe fille)
class Corbeau(Mob):
	def __init__(self, x, y, windowWidth, strength):
		img_lists = {
			"Ridle": ["c_fly_1", "c_fly_2"],
			"Rmove": ["c_fly_1", "c_fly_2"],
			"Odmg": ["c_dmg"]
		}
		imgpath = "Images/Corbeau"
		imagesCorbeau = load_imgs(img_lists, imgpath)
		atkList = [
			Atk(
				"shuriken", 2, 16, 16, load_imgs({"idle": ["shuriken"]}, imgpath),
				2, 3, 1, 0.3, 0, 2, 2000
			)
		]
		Mob.__init__(self, x, y, 32, 32, imagesCorbeau, 0.01, 1, 1, 8, windowWidth, 10*strength, atkList)
		self.strength = strength
		self.min_y = (pygame.time.get_ticks()%100) + 300
		self.left = True
		self.right = False

	def update(self, hero, fps):
		# TODO : L'IA DU CORBEAU ICI
		if self.y > self.min_y:
			self.jump()
		if self.left:
			self.moveLeft()
			Animated.changeState(self, "RmoveLeft")
		else:
			self.moveRight()
			Animated.changeState(self, "RmoveRight")

		if self.x < 50 and self.left:
			self.left = False
			self.right = True
		elif self.x+self.rect.width > self.windowWidth - 100 and self.right:
			self.left = True
			self.right = False

		atkEffect = self.atkList[0].launch(self.x+self.rect.width/2, self.y+self.rect.height, 1, self.strength, self.speed_x)
		if atkEffect is not None:
			self.atkEffectList.append(atkEffect)

		Mob.update(self, hero, fps)
