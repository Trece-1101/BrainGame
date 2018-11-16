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
		self.game = game
		self.image = self.game.spritesheet.get_imagen(132, 330, 64, 64)	
		self.image.set_colorkey(NEGRO)
		self.rect = self.image.get_rect()
		self.image = pg.transform.scale(self.image, (TAMAÑO_TILE_CARPETA, TAMAÑO_TILE_CARPETA))
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		self.pos = vec2(x, y) * TAMAÑO_TILE

	def abierto(self):
		self.image = self.game.spritesheet.get_imagen(132, 396, 64, 64)	
		self.image.set_colorkey(NEGRO)
		self.image = pg.transform.scale(self.image, (TAMAÑO_TILE_CARPETA, TAMAÑO_TILE_CARPETA))
		# mascara de colision
		self.mascara_col = pg.mask.from_surface(self.image)

	def cerrado(self):
		self.image = self.game.spritesheet.get_imagen(132, 330, 64, 64)	
		self.image.set_colorkey(NEGRO)
		self.image = pg.transform.scale(self.image, (TAMAÑO_TILE_CARPETA, TAMAÑO_TILE_CARPETA))
		# mascara de colision
		self.mascara_col = pg.mask.from_surface(self.image)

	def update(self):
		dist_obj = self.pos - self.game.player.pos
		if (abs(dist_obj[0]) < RADIO_DETECCION_PORTAL) and (abs(dist_obj[1]) < 70):
			self.abierto()
		else:
			self.cerrado()


class PlataformaCentro(pg.sprite.Sprite):
	"""docstring for Plataforma"""
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.plataformas
		super(PlataformaCentro, self).__init__(self.groups)
		self.game = game
		self.image = self.game.spritesheet.get_imagen(0, 330, 64, 64)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		self.type = "normal"

class PlataformaExtremoI(pg.sprite.Sprite):
	"""docstring for Plataforma"""
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.plataformas
		super(PlataformaExtremoI, self).__init__(self.groups)
		self.game = game
		self.image = self.game.spritesheet.get_imagen(0, 264, 64, 64)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		self.type = "normal"

class PlataformaExtremoD(pg.sprite.Sprite):
	"""docstring for Plataforma"""
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.plataformas
		super(PlataformaExtremoD, self).__init__(self.groups)
		self.game = game
		self.image = self.game.spritesheet.get_imagen(0, 198, 64, 64)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		self.type = "normal"

class PlataformaTrampaCentro(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.plataformas
		super(PlataformaTrampaCentro, self).__init__(self.groups)
		self.game = game
		self.image = self.game.spritesheet.get_imagen(0, 66, 64, 64)
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
			#self.kill()
			self.rect.y += 5
			if self.rect.y - pos_original > 100:
				#print(str(self.rect.y - pos_original))
				self.kill()

class PlataformaTrampaI(PlataformaTrampaCentro):
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.plataformas
		super(PlataformaTrampaI, self).__init__(game, x, y)
		self.game = game
		self.image = self.game.spritesheet.get_imagen(0, 132, 64, 64)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		self.type = "trampa"
		self.pisada = False

class PlataformaTrampaD(PlataformaTrampaCentro):
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.plataformas
		super(PlataformaTrampaD, self).__init__(game, x, y)
		self.game = game
		self.image = self.game.spritesheet.get_imagen(0, 0, 64, 64)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		self.type = "trampa"
		self.pisada = False 