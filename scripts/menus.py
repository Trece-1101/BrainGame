import pygame as pg
import os
from pathlib import Path
from scripts.parametros import *
from scripts.game import *


def MenuPrincipal2():
	# pantalla de menu principal

	#pg.mixer.music.play(loops = -1)

	gfx = Path("gfx")

	os.environ['SDL_VIDEO_CENTERED'] = '1'


	pantalla = pygame.display.set_mode((ANCHO, ALTO))

	pg.display.set_caption(TITULO)
	fuente = pg.font.Font(FUENTE , 20)

	# Imagen principal que sirve de titulo
	img_titulo = IMG_MENU['titulo'].get_rect()
	titulo_top = 50
	img_titulo.top = topCoord
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height

	img_fondo= IMG_MENU["fondo"].get_rect()
	fondoRect.top = 0
	img_fondo.centerx = MITAD_ANCHO

	# Pasar las instrucciones como una lista para controlar las lineas
	instrucciones = ["Flechas para moverse (<- ->)",
					   "Tecla [ESPACIO] para saltar",
					   "Tecla [SHIFT] para acelerar (dash)",
					   "J para Jugar",
					   "P para pausar",
					   "ESC para salir"]

	pantalla.fill(CELESTE)

	pantalla.blit(IMG_MENU['fondo_titulo'], fondoRect)
	pantalla.blit(IMG_MENU['titulo'], titleRect)

	# Position and draw the text.
	for i in range(len(instrucciones)):
		inst = BASICFONT.render(instrucciones[i], 1, NEGRO)
		instRect = inst.get_rect()
		top += 10 # 10 pixeles entre linea y linea
		instRect.top = topCoord
		instRect.centerx = MITAD_ANCHO
		top += instRect.height
		pantalla.blit(inst, instRect)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				salir()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					salir()
				elif even.key == K_j:
					return "jugar"


		pg.display.update()
		FPSCLOCK.tick()


def stop(clock):
	# metodo para esperar el input de usuario en pantalla principal y de game_over
	esperar = True
	while esperar:
		clock.tick(FPS)
		for evento in pg.event.get():
			if evento.type == pg.QUIT:
				esperar = False
				run = False
			if evento.type == pg.KEYUP:
				if evento.key == pg.K_ESCAPE:
					esperar = False
					run = False
				elif evento.key == pg.K_d:
					esperar = False
					run = True
					dificultad = DIFICULTAD_HARD
				elif evento.key == pg.K_f:
					esperar = False
					run = True
					dificultad = DIFICULTAD_FACIL
				elif evento.key == pg.K_m:
					esperar = False
					run = True
					dificultad = DIFICULTAD_NORMAL

	return [run, dificultad]

def menu_principal(pantalla, clock):
		# pantalla de menu principal
		carpeta_sonidos = Path("sfx")
		carpeta_imagenes = Path("gfx")
		pg.mixer.music.load(os.path.join(carpeta_sonidos, SFX["musica_menu"]))
		pg.mixer.music.play(loops=-1)
		fuente = pg.font.Font('freesansbold.ttf', 20)
		#pantalla.fill(CELESTE)
		#dibujar_texto(pantalla, TITULO, 48, BLANCO, MITAD_ANCHO, ALTO / 4)
		#dibujar_texto(pantalla, "Flechas para mover, espacio para saltar", 22, BLANCO, MITAD_ANCHO, MITAD_ALTO)
		#dibujar_texto(pantalla, "Presione una tecla para continuar", 22, BLANCO, MITAD_ANCHO, ALTO * 3/4)

		# Imagen principal que sirve de titulo
		titulo = pg.image.load(os.path.join(carpeta_imagenes, IMG_MENU["titulo"]))
		img_titulo = titulo.get_rect()
		titulo_top = 50
		img_titulo.top = titulo_top
		img_titulo.centerx = MITAD_ANCHO
		titulo_top += img_titulo.height

		fondo = pg.image.load(os.path.join(carpeta_imagenes, IMG_MENU["fondo"]))
		img_fondo= fondo.get_rect()
		img_fondo.top = 0
		img_fondo.centerx = MITAD_ANCHO

		# Pasar las instrucciones como una lista para controlar las lineas
		instrucciones = ["Flechas para moverse (<- ->) -- Tecla [ESPACIO] para saltar -- Tecla [SHIFT] para acelerar (dash)",
					   "Presiona: 'F' nivel facil -- 'M' nivel moderado -- 'D' nivel dificil",
					   "P para pausar",
					   "ESC para salir"]

		pantalla.blit(fondo, img_fondo)
		pantalla.blit(titulo, img_titulo)

		# Position and draw the text.
		for i in range(len(instrucciones)):
			inst = fuente.render(instrucciones[i], 1, NEGRO)
			instRect = inst.get_rect()
			titulo_top += 10 # 10 pixeles entre linea y linea
			instRect.top = titulo_top
			instRect.centerx = MITAD_ANCHO
			titulo_top += instRect.height
			pantalla.blit(inst, instRect)


		pg.display.flip()
		res = stop(clock)
		return [res[0], res[1]]

def game_over():
		# pantalla de menu para volver a jugar
		self.quit()


def pantalla_pausa(pantalla):
	pantalla_pausa = pg.Surface(pantalla.get_size()).convert_alpha()
	pantalla_pausa.fill((0, 0, 0, 180))
	dibujar_texto(pantalla_pausa, "Juego Pausado", 80, ROJO, MITAD_ANCHO, MITAD_ALTO)
	return pantalla_pausa

def dibujar_texto(pantalla, texto, tamaño, color, x, y, align="topleft"):
		# metodo para recibir un string y dibujarlo en pantalla
		match_fuente = pg.font.match_font(FUENTE)
		fuente = pg.font.Font(match_fuente, tamaño)
		texto_surface = fuente.render(texto, True, color)
		texto_rect = texto_surface.get_rect()
		texto_rect.midtop = (x, y)
		pantalla.blit(texto_surface, texto_rect)

def fade(): 
	fade = pg.Surface((ANCHO, ALTO))
	fade.fill((0,0,0))
	for alpha in range(0, 300):
		fade.set_alpha(alpha)
		#self.dibujar()
		self.pantalla.blit(fade, (0,0))
		pg.display.update()
		pg.time.delay(2)

