from Model.class_Animated import Animated
from Model.class_Mob import Mob
from Model.class_Atk import Atk
from utils import load_imgs


# Hero est la classe générique des héros
# Carastéristiques des héros:
#   Ils sont controlés au clavier
#   Ils peuvent double-sauter
#   Ils ont des spells (définis dans la classe fille)
class Samurai(Mob):
	def __init__(self, x, y, windowWidth, strength):
		img_lists = {
			"Ridle": ["s_idle_1", "s_idle_2"],
			"Rmove": ["s_move_0", "s_move_1", "s_move_0", "s_move_1"],
			"Oaa1": ["s_atk_1", "s_atk_2", "s_atk_3", "s_atk_3"],
			"Odmg": ["s_dmg_2"],
		}
		imgpath = "Images/Samurai"
		imagesSamurai = load_imgs(img_lists, imgpath)
		atkList = [
			Atk(
				"sabre", 4, 96, 96, load_imgs({"idle": ["particle_sam"]}, imgpath),
				10, 10, -4, 0, 4, 0, 400
			)
		]
		Mob.__init__(self, x, y, 96, 96, imagesSamurai, 0.5, 1, 4, 3, windowWidth, 40*strength, atkList)
		self.states["Oaa1Right"] = 100
		self.states["Oaa1Left"] = 100
		self.strength = strength
		self.areaWidth = 200

	def update(self, hero, fps):
		# TODO : L'IA DU Samurai ICI
		if self.x-self.areaWidth > hero.get_x2():
			self.moveLeft()
			Animated.changeState(self, "RmoveLeft")
		elif self.x+self.rect.width+self.areaWidth < hero.get_x1():
			self.moveRight()
			Animated.changeState(self, "RmoveRight")
		else:
			if abs(self.speed_x) > 0:
				self.stop()
			else:
				if self.state[0] != 'O':
					if self.x > hero.get_x1():
						Animated.changeState(self, "RidleLeft")
						atkEffect = self.atkList[0].launch(self.x, self.y+20, -1, self.strength)
					else:
						Animated.changeState(self, "RidleRight")
						atkEffect = self.atkList[0].launch(self.x, self.y+20, 1, self.strength)
					if atkEffect is not None:
						self.atkEffectList.append(atkEffect)
						if self.x > hero.get_x1():
							Animated.changeState(self, "Oaa1Left")
						else:
							Animated.changeState(self, "Oaa1Right")

		Mob.update(self, hero, fps)
