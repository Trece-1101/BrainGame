import pygame as pg
from scripts.parametros import *


class Acelerador(pg.sprite.Sprite):
	"""docstring for Acelerador"""
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.items
		self._layer = ITEM_LAYER
		super(Acelerador, self).__init__(self.groups)
		self.game = game
		self.type = items["A"]
		self.image = pg.Surface((TAMAÑO_TILE, TAMAÑO_TILE))
		self.image = pg.transform.scale(self.image, (16, 16))
		self.image.fill(AMARILLO)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE

class PadSalto(pg.sprite.Sprite):
	"""docstring for Acelerador"""
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.items
		self._layer = ITEM_LAYER
		super(PadSalto, self).__init__(self.groups)
		self.game = game
		self.type = items["S"]
		self.image = pg.Surface((TAMAÑO_TILE, TAMAÑO_TILE))
		self.image = pg.transform.scale(self.image, (16, 16))
		self.image.fill(BLANCO)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE

class Combotron(pg.sprite.Sprite):
	"""docstring for Acelerador"""
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.items
		self._layer = ITEM_LAYER
		super(Combotron, self).__init__(self.groups)
		self.game = game
		self.type = items["C"]
		self.image = pg.Surface((TAMAÑO_TILE, TAMAÑO_TILE))
		self.image = pg.transform.scale(self.image, (16, 16))
		self.image.fill(NEGRO)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
