# importation de pygame
import pygame
# importation de la bibliothèque system
import sys
# importation de nos classes
from Model.class_Hero import Hero
from Model.class_Platform import Platform
from Model.class_Atk import Atk
from Model.class_Archer import Archer
from Model.class_Samurai import Samurai
from Model.class_Ninja import Ninja
from Model.class_Corbeau import Corbeau
from Model.class_Demon import Demon
from Model.class_Moine import Moine
from utils import load_imgs
from random import randint


# initialisation de pygame
def main(self, name, difHard):
	from Model.class_Menu import DieMenu

	if name == "":
		name = "nom par defaut"

	pygame.init()

	WIDTH = 1280
	HEIGHT = 720
	fenetre = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

	fond_e = pygame.transform.scale(
		pygame.image.load("Images/Background/niveauRecurciforce.png").convert(),
		(WIDTH, HEIGHT)
	)

	blanchonAa1 = pygame.image.load("Images/Spell/aa1.png").convert()
	blanchonAa2 = pygame.image.load("Images/Spell/aa2.png").convert()
	blanchonAa3 = pygame.image.load("Images/Spell/aa3.png").convert()
	blanchonAaMidAir = pygame.image.load("Images/Spell/aaMidAir.png").convert()
	blanchonVector = pygame.image.load("Images/Spell/vector.png").convert()

	imagesBlanchonList = {
		"Ridle": ["b_idle_1", "b_idle_2"],
		"Rmove": ["b_move_0", "b_move_1", "b_move_2", "b_move_1"],
		"Ffall": ["b_jumpdown_1", "b_jumpdown_2"],
		"Fcrouch": ["b_crouch_1", "b_crouch_2"],
		"Rslide": ["b_slide"],
		"Fjump": ["b_jumpup_1", "b_jumpup_2", "b_jumpup_3"],
		"Oaa1": ["b_aa1_1", "b_aa1_2", "b_aa1_3", "b_aa1_3"],
		"Oaa2": ["b_aa2_1", "b_aa2_2", "b_aa2_3", "b_aa2_4", "b_aa2_5", "b_aa2_5"],
		"Oaa3": ["b_aa3_1", "b_aa3_2", "b_aa3_3", "b_aa3_4", "b_aa3_5", "b_aa3_6", "b_aa3_6", "b_aa3_6"],
		"Oaaa": ["b_aa2_2", "b_atkjumpdown", "b_atkjumpdown"],
		"Odmg": ["b_dmg_2", "b_dmg_2"],
		"D": ["b_gameover", "b_gameover"],
	}
	path = "Images/Blanchon"
	imagesBlanchon = load_imgs(imagesBlanchonList, path)
	blanchon_atkList = [
		Atk("autoHit1", 0.5, 32, 32, load_imgs({"idle": ["particlehit"]}, path, 1), 10, 5, -1, 0, 0, 0, 225),
		Atk("autoHit2", 0.7, 32, 32, load_imgs({"idle": ["particlehit"]}, path, 1), 15, 5, -2, 0, 0, 0, 300),
		Atk("autoHit3", 0.7, 32, 32, load_imgs({"idle": ["particlehit"]}, path, 1), 15, 6, -16, 0, 0, 0, 500),
		Atk("EOF", 4, 32, 17, load_imgs({"idle": ["vector"]}, path), 15, 4, -1, 0, 4, 0, 2000),
		Atk("airAutoHit", 1, 64, 32, load_imgs({"idle": ["particlehit"]}, path, 1), 10, 5, 5, 0, 0, 0, 300)
	]
	blanchon = Hero(200, 200, 64, 64, imagesBlanchon, 0.3, 0.7, 8, 6, WIDTH, 100.0, blanchon_atkList, difHard)
	sol = Platform(0, HEIGHT - 70, WIDTH, 10, pygame.image.load("Images/plateformtest.png").convert_alpha(), 0.4)

	# INIT ENNEMIS
	foes = []

	# INIT POLICE
	Mult = pygame.font.Font("Polices/Lady Radical.ttf", 25)
	Mult.set_bold(False)
	MultB = pygame.font.Font("Polices/Lady Radical.ttf", 40)
	MultB.set_bold(False)
	damageFont = pygame.font.Font("Polices/Lady Radical.ttf", 30)
	timerFont = pygame.font.Font("Polices/Lady Radical.ttf", 25)
	timerFont.set_bold(False)
	levelFont = pygame.font.Font("Polices/Lady Radical.ttf", 25)
	levelFont.set_bold(False)
	scoreFont = pygame.font.Font("Polices/Lady Radical.ttf", 25)
	levelFont.set_bold(False)
	clearFont = pygame.font.Font("Polices/Lady Radical.ttf", 30)
	clearFont.set_bold(False)
	clearLabel = clearFont.render("STAGE CLEAR", 1, (10, 200, 50))

	# INIT MUSIQUE
	pygame.mixer.init()
	musicMob = "Music/mob.wav"
	musicBoss = "Music/boss.wav"
	# INIT VAR DE JEU
	damageArray = []
	timerDamage = 300
	score = 0
	niveau = 1

	tempsParSalve = 10.0

	# INIT SYSTEM CLOCK
	clock = pygame.time.Clock()
	fps = 60

	while not blanchon.isDead():
		salve = 1
		# INIT PLATEFORMES
		platforms = [
			Platform(
				randint(100, 400), HEIGHT - 180, 100, 10,
				pygame.image.load("Images/plateform.png").convert_alpha(), 1
			),
			Platform(
				randint(100, 400), HEIGHT - 280, 100, 10,
				pygame.image.load("Images/plateform.png").convert_alpha(), 1
			)
		]
		while salve < 6 and not blanchon.isDead():
			i = 0
			if salve < 5:
				# AJOUTER DES MOBS A FOES
				while i < int(niveau + salve / 5):
					mobId = randint(0, 3)
					if mobId == 0:
						foes.append(Ninja(randint(50, WIDTH - 100), HEIGHT-300, WIDTH, 1 + niveau / 10))
					elif mobId == 1:
						foes.append(Samurai(randint(50, WIDTH - 100), HEIGHT-300, WIDTH, 1 + niveau / 10))
					elif mobId == 2:
						foes.append(Archer(randint(50, WIDTH - 100), HEIGHT-300, WIDTH, 1 + niveau / 10))
					elif mobId == 3:
						foes.append(Corbeau(randint(50, WIDTH - 100), HEIGHT-300, WIDTH, 1 + niveau / 10))
					i += 1
			else:
				# AJOUTER UN BOSS A FOES
				while i < 1 + int(niveau / 5):
					if (niveau + i) % 2 == 0:
						foes.append(Demon(500, 350, WIDTH, 1 + niveau / 10))
					elif (niveau + i) % 2 == 1:
						foes.append(Moine(500, 350, WIDTH, 1 + niveau / 10))
					i += 1
			niveauLabel = levelFont.render(f"{niveau} - {salve}", 1, (250, 250, 250))
			timer = tempsParSalve
			timeSave = pygame.time.get_ticks()
			if salve == 5:
				pygame.mixer.music.load(musicBoss)
				pygame.mixer.music.play(-1)
			elif salve == 1:
				pygame.mixer.music.load(musicMob)
				pygame.mixer.music.set_volume(0.4)
				pygame.mixer.music.play(-1)
			# BOUCLE DE JEU =========================================================================================
			while len(foes) > 0 and (timer > 0.0 or salve >= 4) and not blanchon.isDead():
				# GESTION TIMER-----------------------------------------------------------------
				if timer <= 0.0:
					timer = 0
				else:
					timer = timer - (pygame.time.get_ticks() - timeSave) / 1000.0
					timeSave = pygame.time.get_ticks()

				# render text
				if salve != 5:
					timerLabel = timerFont.render(f"{timer:.1f} sec", 1, (50, 100, 200))
				else:
					timerLabel = timerFont.render("BOSS", 1, (50, 100, 200))
				scoreLabel = scoreFont.render(f"Score : {int(score)}", 1, (200, 200, 100))

				clock.tick(fps)
				# GESTION EVENT------------------------------------------------------------------
				for event in pygame.event.get():
					if event.type == pygame.QUIT:  # si l'utilisateur clique sur la croix
						sys.exit()  # on ferme la fenêtre
					if event.type == pygame.KEYDOWN:
						blanchon.key_down(event)
					if event.type == pygame.KEYUP:
						blanchon.key_up(event)

				# GESTION DU DECORS--------------------------------------------------------------
				# Fond
				fenetre.blit(fond_e, (0, 0))
				# timer
				fenetre.blit(timerLabel, (490, 660))
				fenetre.blit(niveauLabel, (500, 690))

				# Plateformes
				nbPlatf = len(platforms)
				for i in range(0, nbPlatf):
					fenetre.blit(platforms[i].get_img(), platforms[i].get_rect())

				# GESTION DU HERO----------------------------------------------------------------
				# Affichage Multiplicateur de dégats
				Multipl = Mult.render("Mult : ", 1, (255, 255, 0))
				combo = blanchon.get_combo()
				if combo < 2:
					MultiplCombo = MultB.render(f"{combo:.2f}", 1, (255, 255, 0))
				elif combo < 3:
					MultiplCombo = MultB.render(f"{combo:.2f}", 1, (0, 0, 255))
				elif combo < 4:
					MultiplCombo = MultB.render(f"{combo:.2f}", 1, (255, 0, 255))
				else:
					MultiplCombo = MultB.render(f"{combo:.2f}", 1, (255, 0, 0))

				fenetre.blit(Multipl, (700, 660))
				fenetre.blit(MultiplCombo, (800, 650))
				# Affichage du score
				fenetre.blit(scoreLabel, (700, 690))

				# CoolDown Attaque de Blanchon
				colorRect = (125, 125, 125, 128)

				if not blanchon.get_onGround():
					cd = blanchon_atkList[4].get_cd()
					if cd > 0:
						pygame.draw.rect(fenetre, (0, 0, 0), (95, 655, 60, 60))
					else:
						pygame.draw.rect(fenetre, (200, 200, 50), (95, 655, 60, 60))
					tailleRect1 = 60*cd/blanchon_atkList[4].get_maxCd()
					posRect1 = 715 - tailleRect1
					fenetre.blit(blanchonAaMidAir, (100, 660))
					CdAH = damageFont.render(f"{cd:.1f}" if cd else "", 1, (255, 0, 0))
				elif blanchon.get_autoHitTimer3() > 0:
					pygame.draw.rect(fenetre, (200, 200, 50), (95, 655, 60, 60))
					fenetre.blit(blanchonAa3, (100, 660))
					tailleRect1 = 60*blanchon.get_autoHitTimer3()/3000
					posRect1 = 715 - tailleRect1
					CdAH = damageFont.render(
						f"{blanchon.get_autoHitTimer3()/1000:.1f}" if blanchon.get_autoHitTimer3() else "",
						1, (255, 0, 0)
					)
				elif blanchon.get_autoHitTimer2() > 0:
					pygame.draw.rect(fenetre, (200, 200, 50), (95, 655, 60, 60))
					fenetre.blit(blanchonAa2, (100, 660))
					tailleRect1 = 60*blanchon.get_autoHitTimer2()/3000
					posRect1 = 715 - tailleRect1
					CdAH = damageFont.render(
						f"{blanchon.get_autoHitTimer2()/1000:.1f}" if blanchon.get_autoHitTimer2() else "",
						1, (255, 0, 0)
					)
				else:
					cd = blanchon_atkList[0].get_cd()
					if cd > 0:
						pygame.draw.rect(fenetre, (0, 0, 0), (95, 655, 60, 60))
					else:
						pygame.draw.rect(fenetre, (200, 200, 50), (95, 655, 60, 60))

					fenetre.blit(blanchonAa1, (100, 660))
					tailleRect1 = 60*cd/blanchon_atkList[0].get_maxCd()
					posRect1 = 715 - tailleRect1
					CdAH = damageFont.render(f"{cd:.1f}" if cd else "", 1, (255, 0, 0))

				CaseAa = pygame.Surface((60, tailleRect1), pygame.SRCALPHA)
				CaseAa.fill(colorRect)
				fenetre.blit(CaseAa, (95, posRect1))
				fenetre.blit(CdAH, (110, 670))
				if blanchon_atkList[3].get_cd() > 0:
					pygame.draw.rect(fenetre, (0, 0, 0), (175, 655, 60, 60))
					pygame.draw.rect(fenetre, (255, 255, 255), (180, 660, 50, 50))
				else:
					pygame.draw.rect(fenetre, (200, 200, 50), (175, 655, 60, 60))
					pygame.draw.rect(fenetre, (255, 255, 255), (180, 660, 50, 50))

				fenetre.blit(blanchonVector, (189, 677))

				tailleRect2 = 60*blanchon_atkList[3].get_cd()/blanchon_atkList[3].get_maxCd()
				posRect2 = 715 - tailleRect2
				CaseAa = pygame.Surface((60, tailleRect2), pygame.SRCALPHA)
				CaseAa.fill((125, 125, 125, 128))
				fenetre.blit(CaseAa, (175, posRect2))

				CdProj = damageFont.render(f"{blanchon_atkList[3].get_cd():.1f}", 1, (255, 0, 0))
				if blanchon_atkList[3].get_cd() > 0:
					fenetre.blit(CdProj, (190, 670))
				# Teste Hero => Plateforme
				heroOnGround = blanchon.isOnGround()
				blanchon.setOnAir()
				blanchon.testPlatform(sol)
				for i in range(0, nbPlatf):
					blanchon.testPlatform(platforms[i])

				# Le hero est descendu d'une plateforme
				if heroOnGround and not blanchon.isOnGround():
					blanchon.giveDoubleJump()  # On lui donne un saut

				blanchon.update(blanchon, fps)

				# AFFICHAGE DES DEGATS----------------------------------------------------------
				i = 0
				while i < len(damageArray):
					if damageArray[i][2] > 0:
						fenetre.blit(damageArray[i][0], damageArray[i][1])
						damageArray[i][2] = damageArray[i][2] - (1000 / fps)
						i += 1
					else:
						damageArray.pop(i)

				# GESTION DES MOBS---------------------------------------------------------------
				# Teste Mob => Plateforme && Atk Hero => Mob
				nbAtkHero = len(blanchon.get_AtkEffectList())
				i = 0
				while i < len(foes):
					foes[i].nextImg(fps)
					fenetre.blit(foes[i].get_img(), foes[i].get_rect())
					pygame.draw.rect(
						fenetre, (0, 0, 0), (foes[i].get_rect().x, foes[i].get_rect().y - 10, 60, 6)
					)
					pygame.draw.rect(
						fenetre, (255, 0, 0), (
							foes[i].get_rect().x, foes[i].get_rect().y - 10,
							int(max(min(foes[i].get_hp()/foes[i].get_hpMax()*60, 60), 0)), 6
						)
					)
					foes[i].setOnAir()
					foes[i].testPlatform(sol)

					for j in range(0, nbPlatf):
						foes[i].testPlatform(platforms[j])

					# Check si le mob i se fait toucher par l'atk de hero k
					for k in range(0, nbAtkHero):
						hpBefore = foes[i].get_hp()
						foes[i].testAtkEffect(blanchon.get_AtkEffectList()[k])
						degats = foes[i].get_hp() - hpBefore
						if degats < 0.0:
							damageArray.append([
								damageFont.render(f"{degats:.1f}", 1, (50, 150, 255)),
								(foes[i].get_x(), foes[i].get_y() - 40), timerDamage
							])

					nbAtkFoe = len(foes[i].get_AtkEffectList())
					for l in range(0, nbAtkFoe):
						hpBefore = blanchon.get_hp()
						blanchon.testAtkEffect(foes[i].get_AtkEffectList()[l])
						degats = blanchon.get_hp() - hpBefore
						if degats < 0:
							damageArray.append([
								damageFont.render(f"{degats:.1f}", 1, (255, 0, 0)),
								(blanchon.get_x(), blanchon.get_y() - 40), timerDamage
							])

						fenetre.blit(
							foes[i].get_AtkEffectList()[l].get_img(),
							foes[i].get_AtkEffectList()[l].get_rect()
						)

					foes[i].update(blanchon, fps)
					if foes[i].get_hp() <= 0:
						# AJOUT DES POINTS AU SCORE
						score += foes[i].get_hpMax() * foes[i].get_hpMax()
						foes.pop(i)
					else:
						i += 1

				for i in range(0, nbAtkHero):
					fenetre.blit(blanchon.get_AtkEffectList()[k].get_img(), blanchon.get_AtkEffectList()[k].get_rect())

				# Affichage Hero
				blanchon.nextImg(fps)
				fenetre.blit(blanchon.get_img(), blanchon.get_rect())
				pygame.draw.rect(fenetre, (0, 0, 0), (blanchon.get_rect().x, blanchon.get_rect().y - 10, 60, 6))
				pygame.draw.rect(
					fenetre, (0, 255, 0), (
						blanchon.get_rect().x, blanchon.get_rect().y - 10,
						int(max(blanchon.get_hp()/float(blanchon.get_hpMax())*60, 0)), 6
					)
				)

				pygame.display.flip()
			# AJOUTE DES POINTS AU SCORE
			score += (tempsParSalve - timer) * 500
			salve += 1

		# ON FAIT UNE PAUSE ENTRE CHAQUE NIVEAU
		if not blanchon.isDead():
			timePause = 3000.0
			timeStart = pygame.time.get_ticks()
			while timePause > 0.0:
				clock.tick(fps)
				timePause = timePause - pygame.time.get_ticks() + timeStart
				timeStart = pygame.time.get_ticks()

				fenetre.blit(fond_e, (0, 0))

				for i in range(0, len(foes)):
					foes[i].update(blanchon, fps)
					fenetre.blit(foes[i].get_img(), foes[i].get_rect())

				blanchon.setOnAir()
				blanchon.testPlatform(sol)

				for i in range(0, len(blanchon.get_AtkEffectList())):
					blanchon.get_AtkEffectList()[i].update(blanchon, fps)
					fenetre.blit(blanchon.get_AtkEffectList()[i].get_img(), blanchon.get_AtkEffectList()[i].get_rect())
				blanchon.update(blanchon, fps)
				fenetre.blit(blanchon.get_img(), blanchon.get_rect())

				fenetre.blit(clearLabel, (400, 300))
				pygame.display.flip()
			niveau += 1

	dieMenu = DieMenu(fenetre, ("Rejouer", "Menu"), name, score)
	dieMenu.run(difHard)

	pygame.display.flip()

# RENVOYER AU MENU
