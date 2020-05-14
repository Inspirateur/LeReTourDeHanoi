import pygame


def load_imgs(img_lists, path, scale=2):
	res = {}
	for key, imgs in img_lists.items():
		imgs_r = []
		imgs_l = []
		for img in imgs:
			img = pygame.image.load(f"{path}/{img}.png").convert_alpha()
			rect = img.get_rect()
			img = pygame.transform.scale(img, (rect.w*scale, rect.h*scale))
			imgs_r.append(img)
			imgs_l.append(pygame.transform.flip(img, True, False))
		res[f"{key}Right"] = imgs_r
		res[f"{key}Left"] = imgs_l
	return res
