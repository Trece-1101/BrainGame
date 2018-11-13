import pygame as pg
import os
from scripts.parametros import *
from scripts.game import *

def stop(pantalla, clock):
	# metodo para esperar el input de usuario en pantalla principal y de game_over
	esperar = True
	while esperar:
		clock.tick(FPS)
		for evento in pg.event.get():
			if evento.type == pg.QUIT:
				esperar = False
				run = False
				dificultad = 0
			if evento.type == pg.KEYUP:
				if evento.key == pg.K_ESCAPE:
					esperar = False
					run = False
					dificultad = 0
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
				elif evento.key == pg.K_c:
					menu(pantalla, clock, MUSICA_GAME_OVER, IMAGEN_MENU_PRINCIPAL, FONDO_MENU_PRINCIPAL, INSTRUCCIONES_CREDITOS)

	return [run, dificultad]

def fade(pantalla): 
	fade = pg.Surface((ANCHO, ALTO))
	fade.fill((0,0,0))
	for alpha in range(0, 300):
		fade.set_alpha(alpha)
		#self.dibujar()
		pantalla.blit(fade, (0,0))
		pg.display.update()
		pg.time.wait(1)
		#pg.time.delay(1)

def menu(pantalla, clock, musica, img_titulo, img_fondo, instrucciones):
		# pantalla de menu principal
		pg.mixer.music.load(musica)
		pg.mixer.music.play(loops=-1)
		fuente = pg.font.Font('freesansbold.ttf', 20)
		
		# Imagen principal que sirve de titulo
		titulo = pg.image.load(img_titulo)
		img_titulo = titulo.get_rect()
		titulo_top = 50
		img_titulo.top = titulo_top
		img_titulo.centerx = MITAD_ANCHO
		titulo_top += img_titulo.height

		fondo = pg.image.load(img_fondo)
		img_fondo= fondo.get_rect()
		img_fondo.top = 0
		img_fondo.centerx = MITAD_ANCHO

		# Pasar las instrucciones como una lista para controlar las lineas
		instrucciones = instrucciones

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
		res = stop(pantalla, clock)
		#fade(pantalla)
		return [res[0], res[1]]


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

