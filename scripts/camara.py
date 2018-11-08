# clase para la camara
# La camara va a ser un Rect, un rectangulo del tipo Rect(x, y, w, h) donde x e y son
# los valores donde se ubica la esquina superior izquierda del rect, w es el ancho y h el alto
# del area total del mapa. Si no se pasa valor de ancho y alto para instanciar la camara le damos 
# por defecto el ancho y alto de la pantalla del juego. Pero no se deberia instanciar nunca sin
# estos valores

import pygame as pg
from scripts.parametros import *
from scripts.personajes import *

class Camara:
	def __init__(self, game, ancho=ANCHO, alto=ALTO):
		self.game = game
		self.camara = pg.Rect(0, 0, ancho, alto)
		self.ancho = ancho
		self.alto = alto

	def aplicar_camara(self, sprite):
		# el rectangulo del objeto sobre el que se aplique la camara 
		return sprite.rect.move(self.camara.topleft)

	def update(self, sprite):
		# sprite es originalmente el player, la camara va a seguir al player y dejarlo siempre
		# en el centro de la camara (que es un rectangulo). Para eso hay que mover el vertice xy de
		# la camara. En x lo obtenemos con el valor de la mitad de la pantalla menos
		#print(self.game.player.sentido) 
		if self.game.player.sentido == "D":
			x = int(MITAD_ANCHO) - sprite.rect.centerx - OFFSETX_CAMARA
		elif self.game.player.sentido == "I":
			x = int(MITAD_ANCHO) - sprite.rect.centerx - OFFSETX_CAMARA
		y = int(MITAD_ALTO) - sprite.rect.centery

		# limites de camara
		x = min(0, x) # limite izquierdo
		y = min(0, y) # limite arriba
		x = max(-(self.ancho - ANCHO), x) # limite derecha
		y = max(-(self.alto - ALTO), y) # limite abajo


		# movemos la camara tirandola de su xy
		self.camara = pg.Rect(x, y, self.ancho, self.alto)	