from Model.class_Animated import Animated
from Model.class_Mob import Mob
from Model.class_Atk import Atk
from utils import load_imgs


# Hero est la classe générique des héros
# Carastéristiques des héros:
#   Ils sont controlés au clavier
#   Ils peuvent double-sauter
#   Ils ont des spells (définis dans la classe fille)
class Ninja(Mob):
	def __init__(self, x, y, windowWidth, strength):
		img_lists = {
			"Ridle": ["n_idle_1", "n_idle_2"],
			"Rmove": ["n_aa_1", "n_mv", "n_aa_1", "n_mv"],
			"Fjump": ["n_jp"],
			"Oaa1": ["n_aa_1", "n_aa_2", "n_aa_3", "n_aa_4"],
			"Odmg": ["n_hurt"],
		}
		imgpath = "Images/Ninja"
		imagesNinja = load_imgs(img_lists, imgpath)
		atkList = [
			Atk(
				"sabre", 2.5, 64, 32, load_imgs({"idle": ["particlehit"]}, "Images/Blanchon"),
				10, 10, -1, 0, 0, 0, 400
			)
		]
		Mob.__init__(self, x, y, 64, 64, imagesNinja, 0.3, 2, 8, 8, windowWidth, 30*strength, atkList)
		self.strength = strength
		self.areaWidth = 250
		self.left = False
		self.right = False

	def update(self, hero, fps):
		# TODO : L'IA DU NINJA ICI
		if self.onGround:
			if self.left:
				self.moveLeft()
			else:
				self.moveRight()
		elif self.x-self.areaWidth > hero.get_x2():
			self.jump()
			self.left = True
			self.right = False
			Animated.changeState(self, "FjumpLeft")
		elif self.x+self.rect.width+self.areaWidth < hero.get_x1():
			self.jump()
			self.left = False
			self.right = True
			Animated.changeState(self, "FjumpRight")
		else:
			if abs(self.speed_x) > 0:
				self.stop()
			else:
				if self.state[0] != 'O':
					if self.x > hero.get_x1():
						Animated.changeState(self, "RidleLeft")
						atkEffect = self.atkList[0].launch(self.x-self.rect.width/2, self.y+20, -1, self.strength)
					else:
						Animated.changeState(self, "RidleRight")
						atkEffect = self.atkList[0].launch(self.x+self.rect.width, self.y+20, 1, self.strength)
					if atkEffect is not None:
						self.atkEffectList.append(atkEffect)
						if self.x > hero.get_x1():
							Animated.changeState(self, "Oaa1Left")
						else:
							Animated.changeState(self, "Oaa1Right")

		Mob.update(self, hero, fps)
