import pygame


def load_imgs(img_lists, path):
	res = {}
	for key, imgs in img_lists.items():
		imgs_r = [pygame.transform.scale2x(pygame.image.load(f"{path}/{img}.png").convert_alpha()) for img in imgs]
		imgs_l = [pygame.transform.flip(img, True, False) for img in imgs_r]
		res[f"{key}Right"] = imgs_r
		res[f"{key}Left"] = imgs_l
	return res
