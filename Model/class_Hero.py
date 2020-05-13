import pygame
from Model.class_Animated import Animated
from Model.class_Charac import Charac


# Hero est la classe générique des héros
# Carastéristiques des héros:
#   Ils sont controlés au clavier
#   Ils peuvent double-sauter
#   Ils ont des spells (définis dans la classe fille)
class Hero(Charac):
	def __init__(
		self, x, y, width, height, images, weight, baseAcc_x, baseJumpForce,
		maxSpeed_x, windowWidth, hp, atkList, difHard=False
	):
		Charac.__init__(
			self, x, y, width, height, images, weight, baseAcc_x, baseJumpForce, maxSpeed_x, windowWidth, hp, atkList
		)
		self.states['RmoveLeft'] = 100
		self.states['RmoveRight'] = 100
		self.states['FjumpLeft'] = 100
		self.states['FjumpRight'] = 100
		self.states['FfallLeft'] = 50
		self.states['FfallRight'] = 50
		self.states['RslideLeft'] = 50
		self.states['RslideRight'] = 50
		self.states['FcrouchLeft'] = 50
		self.states['FcrouchRight'] = 50
		self.states['Oaa1Right'] = 75
		self.states['Oaa1Left'] = 75
		self.states['Oaa2Right'] = 60
		self.states['Oaa2Left'] = 60
		self.states['Oaa3Right'] = 60
		self.states['Oaa3Left'] = 60
		self.states['OaaaRight'] = 75
		self.states['OaaaLeft'] = 75
		self.states['OdmgRight'] = 100
		self.states['OdmgLeft'] = 100
		self.states['DRight'] = 500
		self.states['DLeft'] = 500
		self.autoHitTimer2 = 0  # Sert à transformer l'auto hit 1 apres un coup reussi
		self.autoHitTimer3 = 0  # Sert à transformer l'auto hit 2 apres un coup reussi
		self.combo = 1
		self.doubleJump = True
		self.jumpKeyReset = False
		self.up = False
		self.down = False
		self.left = False
		self.right = False
		self.autoHit = False
		self.spell1 = False
		self.guard = False
		self.ult = False
		self.difHard = difHard
		self.punch = pygame.mixer.Sound("Music/punch.wav")
		self.sword = pygame.mixer.Sound("Music/sword.wav")
		self.eof = pygame.mixer.Sound("Music/error.wav")
		self.bloc = pygame.mixer.Sound("Music/bloc.wav")
		self.applause = pygame.mixer.Sound("Music/applause.wav")

	def key_down(self, event):
		if event.key == pygame.K_RIGHT:
			self.right = True
		elif event.key == pygame.K_LEFT:
			self.left = True
		elif event.key == pygame.K_UP:
			self.up = True
		elif event.key == pygame.K_DOWN:
			self.down = True
		elif event.key == pygame.K_a:
			self.autoHit = True
		elif event.key == pygame.K_z:
			self.spell1 = True
		elif event.key == pygame.K_e:
			self.guard = True
		elif event.key == pygame.K_r:
			self.ult = True

	def key_up(self, event):
		if event.key == pygame.K_RIGHT:
			self.right = False
		elif event.key == pygame.K_LEFT:
			self.left = False
		elif event.key == pygame.K_UP:
			self.up = False
		elif event.key == pygame.K_DOWN:
			self.down = False
		elif event.key == pygame.K_a:
			self.autoHit = False
		elif event.key == pygame.K_z:
			self.spell1 = False
		elif event.key == pygame.K_e:
			self.guard = False
		elif event.key == pygame.K_r:
			self.ult = False

	def get_x1(self):
		return self.x+10

	def get_x2(self):
		return self.x+self.rect.width-10

	def get_y1(self):
		return self.y

	def get_y2(self):
		return self.y+self.rect.height

	def isOnGround(self):
		return self.onGround

	def get_combo(self):
		return self.combo

	def update(self, hero, fps):
		# BLOC GESTION MOUVEMENT -----------------------------------
		if self.state[0] != 'O':  # Pas de mouvement ni d'attaque si le personnage est en animation one time
			# Left = true && Right = false
			if self.left and not self.right:
				Charac.moveLeft(self)
				if self.onGround:
					if self.speed_x > 0:
						Animated.changeState(self, "RslideLeft")
					else:
						Animated.changeState(self, "RmoveLeft")
			elif self.right:  # Left = false && Right = true
				Charac.moveRight(self)
				if self.onGround:
					if self.speed_x < 0:
						Animated.changeState(self, "RslideRight")
					else:
						Animated.changeState(self, "RmoveRight")
			else:  # pas de déplacement horizontal
				Charac.stop(self)
				if self.onGround:
					if self.speed_x < 0:
						Animated.changeState(self, "RslideRight")
					elif self.speed_x > 0:
						Animated.changeState(self, "RslideLeft")
					else:
						if self.facing == 1:
							if self.down:
								Animated.changeState(self, "FcrouchRight")
							else:
								Animated.changeState(self, "RidleRight")
						else:
							if self.down:
								Animated.changeState(self, "FcrouchLeft")
							else:
								Animated.changeState(self, "RidleLeft")

			if self.up:
				if self.onGround:
					Charac.jump(self)
					self.jumpKeyReset = True
					if self.facing == 1:
						Animated.changeState(self, "FjumpRight")
					else:
						Animated.changeState(self, "FjumpLeft")
				elif self.doubleJump:
					Charac.jump(self)
					self.doubleJump = False
					if self.facing == 1:
						Animated.changeState(self, "FjumpRight")
					else:
						Animated.changeState(self, "FjumpLeft")
			else:  # Il faut relacher la touche de saut pour pouvoir doublesauter
				if self.jumpKeyReset and not self.onGround:
					self.doubleJump = True
					self.jumpKeyReset = False

			if self.speed_y > 0:
				if self.facing == 1:
					Animated.changeState(self, "FfallRight")
				else:
					Animated.changeState(self, "FfallLeft")
			# BLOC GESTION SPELL -------------------------------------
			if self.autoHit:
				if self.onGround:
					if self.autoHitTimer2 > 0:  # Le joueur peut declencher l'auto hit 2
						if self.facing == 1:
							atkEffect = self.atkList[1].launch(
								self.x+self.rect.width, self.y+20, self.facing, self.combo
							)
						else:
							atkEffect = self.atkList[1].launch(
								self.x-self.atkList[1].get_width(), self.y+20, self.facing, self.combo
							)
						if atkEffect is not None:
							self.speed_x = 0
							self.currAcc_x = 0
							self.autoHitTimer2 = 0
							self.atkEffectList.append(atkEffect)
							if self.facing == 1:
								Animated.changeState(self, "Oaa2Right")
							else:
								Animated.changeState(self, "Oaa2Left")
					elif self.autoHitTimer3 > 0:  # Le joueur peut declencher l'auto hit 3
						if self.facing == 1:
							BonusSpeed_x = 6
							BonusSpeed_y = -1.5
							atkEffect = self.atkList[2].launch(
								self.x+self.rect.width, self.y+20, self.facing, self.combo, BonusSpeed_x
							)
						else:
							BonusSpeed_x = -6
							BonusSpeed_y = -2
							atkEffect = self.atkList[2].launch(
								self.x-self.atkList[2].get_width(), self.y+20,
								self.facing, self.combo, BonusSpeed_x
							)
						if atkEffect is not None:
							self.onGround = False
							self.speed_x = BonusSpeed_x
							self.speed_y = BonusSpeed_y
							self.autoHitTimer3 = 0
							self.atkEffectList.append(atkEffect)
							if self.facing == 1:
								Animated.changeState(self, "Oaa3Right")
							else:
								Animated.changeState(self, "Oaa3Left")
							self.atkList[0].put_cd(1)  # Si le coup de pied est lance on met un cd sur le coup de poing
					else:  # Le joueur declenche l'auto hit 1
						if self.facing == 1:
							atkEffect = self.atkList[0].launch(self.x+self.rect.width, self.y+20, self.facing, self.combo)
						else:
							atkEffect = self.atkList[0].launch(self.x-self.atkList[0].get_width(), self.y+20, self.facing, self.combo)
						if atkEffect is not None:
							self.speed_x = 0
							self.currAcc_x = 0
							self.atkEffectList.append(atkEffect)
							if self.facing == 1:
								Animated.changeState(self, "Oaa1Right")
							else:
								Animated.changeState(self, "Oaa1Left")
				else:  # On lance une auto hit en l'air
					if self.facing == 1:
						atkEffect = self.atkList[4].launch(self.x+self.rect.width, self.y+20, self.facing, self.combo)
					else:
						atkEffect = self.atkList[4].launch(self.x-self.atkList[4].get_width(), self.y+20, self.facing, self.combo)
					if atkEffect is not None:
						self.speed_x = 0
						if self.speed_y >= 0:
							self.speed_y = 0
						self.currAcc_x = 0
						self.atkEffectList.append(atkEffect)
						if self.facing == 1:
							Animated.changeState(self, "OaaaRight")
						else:
							Animated.changeState(self, "OaaaLeft")

			if self.spell1:
				if self.facing == 1:
					if self.speed_x > 0:
						bnspd_x = self.speed_x
					else:
						bnspd_x = 0
					atkEffect = self.atkList[3].launch(
						self.x+self.rect.width/2+20*self.facing, self.y+20, self.facing, self.combo, bnspd_x
					)
				else:
					if self.speed_x < 0:
						bnspd_x = self.speed_x
					else:
						bnspd_x = 0
					atkEffect = self.atkList[3].launch(
						self.x+self.rect.width/2+20*self.facing-self.atkList[3].get_width(),
						self.y+20, self.facing, self.combo, bnspd_x
					)
				if atkEffect is not None:
					self.atkEffectList.append(atkEffect)
					if self.facing == 1:
						Animated.changeState(self, "Oaa1Right")
					else:
						Animated.changeState(self, "Oaa1Left")

		if self.autoHitTimer2 > 0:
			self.autoHitTimer2 = self.autoHitTimer2 - (1000.0/fps)

		if self.autoHitTimer3 > 0:
			self.autoHitTimer3 = self.autoHitTimer3 - (1000.0/fps)

		Charac.update(self, hero, fps)

	# Ici on peut vérifier si l'atk i à touché quelqu'un avant de la suppr
	def deleteAtkEffect(self, i):
		if self.atkEffectList[i].didHit():  # L'attaque a touché
			self.comboManager(self.atkEffectList[i].get_nom())
		Charac.deleteAtkEffect(self, i)

	def comboManager(self, attName):
		comboTemp = self.combo
		if attName == "autoHit1":
			self.combo += 0.1
			self.autoHitTimer2 = 3000
			self.atkList[1].put_on_cd()
			self.punch.play()
		elif attName == "autoHit2":
			self.combo += 0.2
			self.autoHitTimer2 = 0
			self.autoHitTimer3 = 3000
			self.atkList[2].put_on_cd()
			self.sword.play()
		elif attName == "autoHit3":
			self.combo += 0.3
			self.autoHitTimer2 = 0
			self.autoHitTimer3 = 0
			self.punch.play()
		elif attName == "EOF":
			self.combo += 0.1
			self.eof.play()
		elif attName == "airAutoHit":
			self.combo += 0.1
			self.sword.play()
		if (int(self.combo) - int(comboTemp)) == 1:
			self.applause.play()

	def set_hp(self, dmg):
		# en HARD on drop tout le combo en prenant des dmg
		if self.difHard:
			self.combo = 1
		else:  # en NORMAL on drop que la moitié du bonus > 1
			self.combo = float("{0:.2f}".format(1+(self.combo-1)/2))
		if self.state[:7] == "Fcrouch":
			dmg = dmg/2.0
			self.bloc.play()
		Charac.set_hp(self, dmg)
		if self.hp <= 0.0:
			if self.facing == 1:
				Animated.changeState(self, "DRight")
			else:
				Animated.changeState(self, "DLeft")
		else:
			if self.facing == 1:
				Animated.changeState(self, "OdmgRight")
			else:
				Animated.changeState(self, "OdmgLeft")

	def get_autoHitTimer2(self):
		return self.autoHitTimer2

	def get_autoHitTimer3(self):
		return self.autoHitTimer3

	def giveDoubleJump(self):
		self.doubleJump = True
