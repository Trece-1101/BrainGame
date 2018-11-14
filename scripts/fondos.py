import pygame as pg
from scripts.parametros import *

class FondoPantalla(pg.sprite.Sprite):
	"""docstring for Fondo"""
	def __init__(self, game, imagen, x=0, y=0):
		self.groups = game.sprites, game.fondos
		self._layer = FONDO_LAYER
		super(FondoPantalla, self).__init__(self.groups)
		self.image = pg.image.load(imagen)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		