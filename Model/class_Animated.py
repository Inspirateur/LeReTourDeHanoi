import pygame
from Model.class_Entity import Entity


# images contient des sets dimages pour chaque animation
# states contient les etats animes (ex: idle, walkLeft, walkRight ...)
class Animated(Entity):
	facing: int

	def __init__(self, x, y, width, height, images):
		Entity.__init__(self, x, y)
		self.rect = pygame.Rect(x, y, width, height)
		self.images = images
		self.indexImg = 0
		self.states = {"RidleLeft": 500, "RidleRight": 500}
		self.state = next(iter(self.states.keys()))
		self.timerAnim = 0

	def changeState(self, newState):
		if self.state[0] != 'D' and newState != self.state and newState in self.images:
			self.state = newState
			self.indexImg = 0
			self.timerAnim = 0

	def nextImg(self, fps):
		self.timerAnim = self.timerAnim + (1000/fps)
		timeState = self.states[self.state]
		if self.timerAnim > timeState:
			self.timerAnim = self.timerAnim - timeState
			self.indexImg = self.indexImg + 1
			if self.indexImg == len(self.images[self.state]):
				if self.state[0] == 'R':  # Si l'animation est en mode repeat
					self.indexImg = 0
				elif self.state[0] == 'F' or self.state[0] == 'D':  # Si l'animation est en mode freeze ou dead
					self.indexImg -= 1
				elif self.state[0] == 'O':  # Si l'animation est en mode one-time
					if self.facing == 1:
						self.changeState("RidleRight")
					else:
						self.changeState("RidleLeft")
					self.timerAnim = 0

	# Permet d'empecher au hero de glisser
	def isFirstFrame(self):
		return self.indexImg == 0

	def isLastFrame(self):
		return self.indexImg == len(self.images[self.state]) - 1

	def get_img(self):
		return self.images[self.state][self.indexImg]

	# Permet de mettre a jour la position de l'image a afficher
	def update(self, hero, fps):
		self.rect.x = self.x
		self.rect.y = self.y

	def get_rect(self):
		return self.rect
