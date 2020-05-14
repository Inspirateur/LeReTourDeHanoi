import pygame
from Model.class_Animated import Animated
from Model.class_Mob import Mob
from Model.class_Atk import Atk
from utils import load_imgs
from random import randint


# Hero est la classe générique des héros
# Carastéristiques des héros:
#   Ils sont controlés au clavier
#   Ils peuvent double-sauter
#   Ils ont des spells (définis dans la classe fille)
class Archer(Mob):
	def __init__(self, x, y, windowWidth, strength):
		img_lists = {
			"Ridle": ["a_idle"],
			"Odmg": ["a_dmg_2"],
			"Oaa1": ["a_atk_1", "a_atk_2", "a_atk_3", "a_atk_4"],
			"Rmove": ["a_move_1", "a_move_2", "a_move_3"],
		}
		imgpath = "Images/Archer"
		imagesArcher = load_imgs(img_lists, imgpath)
		atkList = [
			Atk(
				"fleche", 3, 32, 16, load_imgs({"idle": ["Fleche"]}, imgpath),
				2, 3, -1, 0.05, 15, -1, 3000
			)
		]
		Mob.__init__(self, x, y, 64, 64, imagesArcher, 0.2, 1, 5, 7, windowWidth, 20*strength, atkList)
		self.strength = strength
		self.arrowMax = 3 + int(strength)
		self.arrowCount = 0
		self.flee_x = 0
		self.flee_set = False

	def update(self, hero, fps):
		# TODO : L'IA DE L'ARCHER ICI
		if self.flee_set:
			if self.x-30 > self.flee_x:
				Animated.changeState(self, "RmoveLeft")
				self.moveLeft()
			elif self.x+30 < self.flee_x:
				Animated.changeState(self, "RmoveRight")
				self.moveRight()
			else:
				self.flee_set = False
				self.arrowCount = 0
		else:
			if abs(self.speed_x) > 0:
				self.stop()
			else:
				if self.state[0] != 'O':
					if self.arrowCount < self.arrowMax:
						if self.x > hero.get_x2():
							Animated.changeState(self, "RidleLeft")
							atkEffect = self.atkList[0].launch(self.x+self.rect.width, self.y+20, -1, self.strength)
						else:
							Animated.changeState(self, "RidleRight")
							atkEffect = self.atkList[0].launch(self.x-self.atkList[0].get_width(), self.y+20, 1, self.strength)
						if atkEffect is not None:
							self.atkEffectList.append(atkEffect)
							self.arrowCount += 1
							if self.x > hero.get_x2():
								Animated.changeState(self, "Oaa1Left")
							else:
								Animated.changeState(self, "Oaa1Right")
					else:
						self.flee_set = True
						self.flee_x = randint(self.rect.width, self.windowWidth-100)

		Mob.update(self, hero, fps)
