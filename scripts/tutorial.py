import pygame as pg
import os
import random
import sys
from pathlib import Path
from scripts.parametros import *
from scripts.personajes import *
from scripts.tiles import *
from scripts.camara import *
from scripts.item import *
from scripts.menus import *
from scripts.controles import *

class Tutorial():
	def __init__(self):
		# inicializar el juego
		pg.init() # inicializo el modulo pygame, obligatorio
		pg.mixer.init() # modulo de sonido
		os.environ['SDL_VIDEO_CENTERED'] = '1' # centro de la pantalla
		self.pantalla = pg.display.set_mode((ANCHO, ALTO)) # tamaño de la ventana del juego
		pg.display.set_caption(TITULO) # titulo que aparece en la ventana
		self.FPSclock = pg.time.Clock()
		iniciar = menu_principal(self.pantalla, self.FPSclock)
		self.run = True
		self.jugando = True # bool para determinar el game_over o no	
		self.fuente = pg.font.match_font(FUENTE)
		self.cargar_datos()
		pg.display.set_icon(self.icono)
		self.pausado = False
		self.c_niveles = 1
		#if verificar_controles():
		#	j = 
