import pygame
from Model.class_Animated import Animated
from Model.class_Charac import Charac
from Model.class_Mob import Mob
from Model.class_Atk import Atk
from utils import load_imgs


# Hero est la classe générique des héros
# Carastéristiques des héros:
#   Ils sont controlés au clavier
#   Ils peuvent double-sauter
#   Ils ont des spells (définis dans la classe fille)
class Demon(Mob):
	def __init__(self, x, y, windowWidth, strength):
		img_lists = {
			"Ridle": ["boss_idle_1", "boss_idle_2"],
			"Odmg": ["boss_dmg"],
			"Oaa1": ["boss_atkranged1_1", "boss_atkranged1_2"],
			"Oaa2": ["boss_atkranged2_1", "boss_atkranged2_2"],
			"Oaa3": ["boss_atkranged3_1", "boss_atkranged3_2"],
			"D": ["boss_dead", "boss_dead"],
		}
		imgpath = "Images/Boss"
		imagesDemon = load_imgs(img_lists, imgpath, scale=4)
		atkList = [
			Atk(
				"feu", 1.5, 32, 16, load_imgs({"idle": ["fire_1", "fire_2"]}, imgpath),
				10, 3, -1, 0, 6, 0, 3000
			),
			Atk(
				"vent", 2, 32, 16, load_imgs({"idle": ["wind_1", "wind_1"]}, imgpath),
				5, 6, -8, 0, 10, 0, 3000
			),
			Atk(
				"glace", 2, 32, 16, load_imgs({"idle": ["wind_1", "wind_1"]}, imgpath),
				18, 2, 5, 0.8, 0, 0, 2000
			)
		]
		Mob.__init__(self, x, y, 256, 96, imagesDemon, 0.01, 0.008, 2, 3, windowWidth, 250*strength, atkList)
		self.states["Oaa1Right"] = 200
		self.states["Oaa1Left"] = 200
		self.states["Oaa2Right"] = 200
		self.states["Oaa2Left"] = 200
		self.states["Oaa3Right"] = 200
		self.states["Oaa3Left"] = 200
		self.states["DRight"] = 200
		self.states["DLeft"] = 200
		self.strength = strength
		self.spellMax = int(7*strength)
		self.spellCount = 0
		self.flee_x = 0
		self.flee_y = 0
		self.min_x = 5.0*windowWidth/10.0
		self.max_x = windowWidth-self.rect.width
		self.max_y = y + 50
		self.min_y = y
		self.flee_x = (pygame.time.get_ticks()%(self.max_x-self.min_x))+self.min_x
		self.flee_y = (pygame.time.get_ticks()%(self.max_y-self.min_y))+self.min_y
		self.flee_set = True

	def update(self, hero, fps):
		# TODO : L'IA DU BOSS ICI
		if self.y > self.flee_y:
			self.jump()
		if self.flee_set:
			if self.x > hero.get_x1():
				Animated.changeState(self, "RidleLeft")
			else:
				Animated.changeState(self, "RidleRight")
			if self.x-10 > self.flee_x:
				self.moveLeft()
			elif self.x+10 < self.flee_x:
				self.moveRight()
			else:
				self.flee_set = False
				self.spellCount = 0
		else:
			if abs(self.speed_x) > 0:
				self.stop()
			else:
				if self.state[0] != 'O':
					if self.spellCount < self.spellMax:
						if hero.isOnGround() and abs(self.x - hero.get_x1()) > 300:  # Lancer boule de feu
							if self.x > hero.get_x2():
								Animated.changeState(self, "RidleLeft")
								atkEffect = self.atkList[0].launch(self.x+self.rect.width/2, self.y+self.rect.height*2, -1, self.strength)
							else:
								Animated.changeState(self, "RidleRight")
								atkEffect = self.atkList[0].launch(self.x+self.rect.width/2, self.y+self.rect.height*2, 1, self.strength)
							if atkEffect is not None:
								self.atkEffectList.append(atkEffect)
								self.spellCount += 1
								if self.x > hero.get_x2():
									Animated.changeState(self, "Oaa1Left")
								else:
									Animated.changeState(self, "Oaa1Right")
						elif abs(self.x - hero.get_x1()) > 300:  # Lancer lame de vent
							if self.x > hero.get_x2():
								Animated.changeState(self, "RidleLeft")
								atkEffect = self.atkList[1].launch(self.x+self.rect.width/2, self.y+self.rect.height*2, -1, self.strength)
							else:
								Animated.changeState(self, "RidleRight")
								atkEffect = self.atkList[1].launch(self.x+self.rect.width/2, self.y+self.rect.height*2, 1, self.strength)
							if atkEffect is not None:
								self.atkEffectList.append(atkEffect)
								self.spellCount += 1
								if self.x > hero.get_x2():
									Animated.changeState(self, "Oaa2Left")
								else:
									Animated.changeState(self, "Oaa2Right")
						else:  # Lancer pic de glace
							if self.x > hero.get_x2():
								Animated.changeState(self, "RidleLeft")
								atkEffect = self.atkList[2].launch(hero.get_x1(), -100, -1, self.strength)
							else:
								Animated.changeState(self, "RidleRight")
								atkEffect = self.atkList[2].launch(hero.get_x1(), -100, 1, self.strength)
							if atkEffect is not None:
								self.atkEffectList.append(atkEffect)
								self.spellCount += 1
								if self.x > hero.get_x2():
									Animated.changeState(self, "Oaa3Left")
								else:
									Animated.changeState(self, "Oaa3Right")

					else:
						self.flee_set = True
						self.flee_x = (pygame.time.get_ticks()%(self.max_x-self.min_x))+self.min_x
						self.flee_y = (pygame.time.get_ticks()%(self.max_y-self.min_y))+self.min_y

		Mob.update(self, hero, fps)

	def set_hp(self, dmg):
		Charac.set_hp(self, dmg)
		if self.hp <= 0:
			if self.facing == 1:
				Animated.changeState(self, "DRight")
			else:
				Animated.changeState(self, "DLeft")
			self.baseJumpForce = 0
			self.speed_x = 0
			self.baseAcc_x = 0
			self.currAcc_x = 0

	def testAtkEffect(self, atkEffect):
		temp_speed_x = self.speed_x
		temp_speed_y = self.speed_y
		Charac.testAtkEffect(self, atkEffect)
		self.speed_x = temp_speed_x
		self.speed_y = temp_speed_y
