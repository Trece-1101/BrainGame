import pygame as pg
from scripts.parametros import *


class Spritesheet:
	def __init__(self, archivo):
		self.spritesheet = pg.image.load(archivo).convert()

	def get_imagen(self, x, y, ancho, alto):
		imagen = pg.Surface((ancho, alto))
		imagen.blit(self.spritesheet, (0, 0), (x, y, ancho, alto))
		imagen = pg.transform.scale(imagen, (TAMAÑO_TILE, TAMAÑO_TILE))
		return imagen	

class Mapa:
	def __init__(self, archivo):
		self.data_mapa = []
		with open(archivo, "rt") as arc:
			for line in arc:
				self.data_mapa.append(line.strip())
		#print(self.data_mapa)

		self.ancho_tile = len(self.data_mapa[0])
		self.alto_tile = len(self.data_mapa)
		self.ancho = self.ancho_tile * TAMAÑO_TILE
		self.alto = self.alto_tile * TAMAÑO_TILE

class Portal(pg.sprite.Sprite):
	"""docstring for Portal"""	
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.portales
		super(Portal, self).__init__(self.groups)
		#self.image = self.game.pared_img
		self.image = pg.Surface((TAMAÑO_TILE, TAMAÑO_TILE))
		self.image.fill(NEGRO)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		

class Plataforma(pg.sprite.Sprite):
	"""docstring for Plataforma"""
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.plataformas
		super(Plataforma, self).__init__(self.groups)
		self.game = game
		#self.image = self.game.pared_img
		self.image = pg.Surface((TAMAÑO_TILE, TAMAÑO_TILE))
		self.image.fill(VERDE)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		self.type = "normal"

class PlataformaTrampa(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.plataformas
		super(PlataformaTrampa, self).__init__(self.groups)
		self.game = game
		#self.image = self.game.pared_img
		self.image = pg.Surface((TAMAÑO_TILE, TAMAÑO_TILE))
		self.image.fill(AMARILLO)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		self.type = "trampa"
		self.pisada = False

	def update(self):
		pos_original = self.rect.y
		if self.pisada:
			self.kill()
			#self.rect.y += 5
			#if self.rect.y - pos_original > 100:
			#	print(str(self.rect.y - pos_original))
			#	self.kill()