import pygame as pg
from scripts.parametros import *

class Camara:
	def __init__(self, ancho=ANCHO, alto=ALTO):
		self.camara = pg.Rect(0, 0, ancho, alto)
		self.ancho = ancho
		self.alto = alto

	def offset(self, objeto):
		return objeto.rect.move(self.camara.topleft)

	def update(self, objetivo):
		x = -objetivo.rect.centerx + int(ANCHO / 2)
		y = -objetivo.rect.centery + int(ALTO / 2)
		#x = -objetivo.rect.x + int(ANCHO / 2)
		#y = -objetivo.rect.y + int(ALTO / 2)

		# limites de camara
		x = min(0, x) # limite izquierdo
		y = min(0, y) # limite arriba
		x = max(-(self.ancho - ANCHO), x) # limite derecha
		y = max(-(self.alto - ALTO), y) # limite abajo
		self.camara = pg.Rect(x, y, self.ancho, self.alto)