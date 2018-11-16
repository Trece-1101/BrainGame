import pygame as pg
import os
from scripts.parametros import *
from scripts.game import *
from scripts.tutorial import *




def stop_creditos(pantalla, clock):
	esperar = True
	while esperar:
		clock.tick(FPS)
		for evento in pg.event.get():
			if evento.type == pg.QUIT:
				esperar = False
			if evento.type == pg.KEYUP:
				if evento.key == pg.K_ESCAPE:
					esperar = False
				elif evento.key == pg.K_m:
					esperar = False





def creditos(pantalla, clock):
	fuente = pg.font.Font('freesansbold.ttf', 26)
	fuente.set_bold(True)
	
	titulo = pg.image.load(IMAGEN_MENU_PRINCIPAL)
	img_titulo = titulo.get_rect()
	titulo_top = 10
	img_titulo.top = titulo_top
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height

	fondo = pg.image.load(FONDO_MENU_PRINCIPAL)
	img_fondo= fondo.get_rect()
	img_fondo.top = 0
	img_fondo.centerx = MITAD_ANCHO

	instrucciones = INSTRUCCIONES_CREDITOS

	pantalla.blit(fondo, img_fondo)
	pantalla.blit(titulo, img_titulo)
	
	pg.display.flip()

	timer_off = False
	for i in range(len(instrucciones)):
		inicio_timer = pg.time.get_ticks()
		print("inicio_timer", inicio_timer)
		inst = fuente.render(instrucciones[i], 1, BLANCO)
		instRect = inst.get_rect()
		titulo_top += 5 # 10 pixeles entre linea y linea
		instRect.top = titulo_top + 280
		instRect.centerx = MITAD_ANCHO
		titulo_top += instRect.height
		while  not timer_off:						
			fin_timer = pg.time.get_ticks()
			res = (fin_timer - inicio_timer)
			if res > TIMER_OFF_INSTRUCCIONES:
				timer_off = True
		pantalla.blit(inst, instRect)
		pg.display.flip()
		timer_off = False


	stop_creditos(pantalla, clock)


def controles(pantalla, clock):
	fuente = pg.font.Font('freesansbold.ttf', 18)
	fuente.set_bold(True)
	
	titulo = pg.image.load(IMAGEN_MENU_PRINCIPAL)
	img_titulo = titulo.get_rect()
	titulo_top = 10
	img_titulo.top = titulo_top
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height

	fondo = pg.image.load(FONDO_MENU_PRINCIPAL)
	img_fondo= fondo.get_rect()
	img_fondo.top = 0
	img_fondo.centerx = MITAD_ANCHO

	instrucciones = INSTRUCCIONES_CONTROLES

	pantalla.blit(fondo, img_fondo)
	pantalla.blit(titulo, img_titulo)
	
	for i in range(len(instrucciones)):
		inst = fuente.render(instrucciones[i], 1, BLANCO)
		instRect = inst.get_rect()
		titulo_top += 3 # 10 pixeles entre linea y linea
		instRect.top = titulo_top + 280
		instRect.centerx = MITAD_ANCHO
		titulo_top += instRect.height
		pantalla.blit(inst, instRect)
		

	pg.display.flip()

	stop_creditos(pantalla, clock)


def stop_dificultad(pantalla, clock):
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
				elif evento.key == pg.K_d:
					run = True
					return DIFICULTAD_HARD
				elif evento.key == pg.K_m:
					run = True
					return DIFICULTAD_NORMAL
				elif evento.key == pg.K_f:
					run = True
					return DIFICULTAD_FACIL


def menu_dificultad(pantalla, clock):
	pg.mixer.music.load(MUSICA_MENU_PRINCIPAL)
	pg.mixer.music.play(loops=-1)
	fuente = pg.font.Font('freesansbold.ttf', 28)
	fuente.set_bold(True)
	
	titulo = pg.image.load(IMAGEN_MENU_PRINCIPAL)
	img_titulo = titulo.get_rect()
	titulo_top = 10
	img_titulo.top = titulo_top
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height

	fondo = pg.image.load(FONDO_MENU_PRINCIPAL)
	img_fondo= fondo.get_rect()
	img_fondo.top = 0
	img_fondo.centerx = MITAD_ANCHO

	instrucciones = INSTRUCCIONES_DIFICULTAD

	pantalla.blit(fondo, img_fondo)
	pantalla.blit(titulo, img_titulo)

	for i in range(len(instrucciones)):
		inst = fuente.render(instrucciones[i], 1, BLANCO)
		instRect = inst.get_rect()
		titulo_top += 5 # 10 pixeles entre linea y linea
		instRect.top = titulo_top + 220
		instRect.centerx = MITAD_ANCHO
		titulo_top += instRect.height
		pantalla.blit(inst, instRect)


	pg.display.flip()
	dificultad = stop_dificultad(pantalla, clock)
	return dificultad

'''def stop_menu_principal(pantalla, clock):
	esperar = True
	while esperar:
		clock.tick(FPS)
		for evento in pg.event.get():
			if evento.type == pg.QUIT:
				esperar = False
				run = False
				dificultad = "0"
			if evento.type == pg.KEYUP:
				if evento.key == pg.K_ESCAPE:
					esperar = False
					run = False
					dificultad = "0"
				elif evento.key == pg.K_j:
					esperar = False
					run = True
					dificultad = menu_dificultad(pantalla, clock)				
				elif evento.key == pg.K_c:
					creditos(pantalla, clock)

	return [run, dificultad]'''

def stop_game_over(pantalla, clock):
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
	return run


def fade(pantalla): 
	fade = pg.Surface((ANCHO, ALTO))
	fade.fill((0,0,0))
	for alpha in range(0, 300):
		fade.set_alpha(alpha)
		pantalla.blit(fade, (0,0))
		pg.display.update()
		pg.time.delay(1)		

def intro(pantalla, clock, instrucciones):
	fuente = pg.font.Font('freesansbold.ttf', 22)
	fuente.set_bold(True)
	
	titulo = pg.image.load(IMAGEN_INTRO)
	img_titulo = titulo.get_rect()
	titulo_top = 0
	img_titulo.top = titulo_top
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height

	fondo = pg.image.load(FONDO_INTRO)
	img_fondo= fondo.get_rect()
	img_fondo.top = 0
	img_fondo.centerx = MITAD_ANCHO

	instrucciones = instrucciones

	pantalla.blit(fondo, img_fondo)
	pantalla.blit(titulo, img_titulo)
	
	pg.display.flip()

	timer_off = False
	for i in range(len(instrucciones)):
		inicio_timer = pg.time.get_ticks()
		print("inicio_timer", inicio_timer)
		inst = fuente.render(instrucciones[i], 1, BLANCO)
		instRect = inst.get_rect()
		titulo_top += 2 # 10 pixeles entre linea y linea
		instRect.top = titulo_top + 10
		instRect.centerx = MITAD_ANCHO
		titulo_top += instRect.height
		while  not timer_off:						
			fin_timer = pg.time.get_ticks()
			res = (fin_timer - inicio_timer)
			if res > TIMER_OFF_INSTRUCCIONES:
				timer_off = True
		pantalla.blit(inst, instRect)
		pg.display.flip()
		timer_off = False



def menu_principal(pantalla, clock):
	menu = True
	pg.mixer.music.load(MUSICA_MENU_PRINCIPAL)
	pg.mixer.music.play(loops=-1)
	while menu:		
		fuente = pg.font.Font('freesansbold.ttf', 22)
		fuente.set_bold(True)
		
		# Imagen principal que sirve de titulo
		titulo = pg.image.load(IMAGEN_MENU_PRINCIPAL)
		img_titulo = titulo.get_rect()
		titulo_top = 20
		img_titulo.top = titulo_top
		img_titulo.centerx = MITAD_ANCHO
		titulo_top += img_titulo.height

		fondo = pg.image.load(FONDO_MENU_PRINCIPAL)
		img_fondo= fondo.get_rect()
		img_fondo.top = 0
		img_fondo.centerx = MITAD_ANCHO
		instrucciones = INSTRUCCIONES_MENU_PRINCIPAL
		pantalla.blit(fondo, img_fondo)
		pantalla.blit(titulo, img_titulo)
		for i in range(len(instrucciones)):
			inst = fuente.render(instrucciones[i], 1, BLANCO)
			instRect = inst.get_rect()
			titulo_top += 5 # 10 pixeles entre linea y linea
			if i == 0:
				instRect.top = titulo_top + 220
			else:
				instRect.top = titulo_top + 230
			instRect.centerx = MITAD_ANCHO
			titulo_top += instRect.height
			pantalla.blit(inst, instRect)

		res = []
		run = ""
		dificultad = ""
		esperar = True
		pg.display.flip()
		while esperar:
			for evento in pg.event.get():
				if evento.type == pg.QUIT:			
					run = False
					menu = False
					esperar = False
					dificultad = "0"
				if evento.type == pg.KEYUP:
					if evento.key == pg.K_ESCAPE:					
						run = False
						menu = False
						esperar = False
						dificultad = "0"
					elif evento.key == pg.K_j:					
						run = True
						dificultad = menu_dificultad(pantalla, clock)
						menu = False
						esperar = False			
					elif evento.key == pg.K_c:
						creditos(pantalla, clock)
						esperar = False
					elif evento.key == pg.K_r:
						controles(pantalla,clock)
						esperar = False
					elif evento.key == pg.K_t:
						t = Tutorial()
						while t.run:
							t.nuevo_juego()
						pg.mixer.music.load(MUSICA_MENU_PRINCIPAL)
						pg.mixer.music.play(loops=-1)
						esperar = False
					elif evento.key == pg.K_i:
						intro(pantalla, clock, INSTRUCCIONES_INTRO_1)
						intro(pantalla, clock, INSTRUCCIONES_INTRO_2)
						intro(pantalla, clock, INSTRUCCIONES_INTRO_3)
						esperar = false

	
	

	fade(pantalla)
	return [run, dificultad]



def menu_game_over(pantalla, clock):
	pg.mixer.music.load(MUSICA_GAME_OVER)
	pg.mixer.music.play(loops=-1)
	fuente = pg.font.Font('freesansbold.ttf', 22)
	fuente.set_bold(True)
	
	titulo = pg.image.load(IMAGEN_MENU_PRINCIPAL)
	img_titulo = titulo.get_rect()
	titulo_top = 5
	img_titulo.top = titulo_top
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height

	fondo = pg.image.load(FONDO_GAME_OVER)
	img_fondo= fondo.get_rect()
	img_fondo.top = 0
	img_fondo.centerx = MITAD_ANCHO

	instrucciones = INSTRUCCIONES_GAME_OVER

	pantalla.blit(fondo, img_fondo)
	pantalla.blit(titulo, img_titulo)




	pg.display.flip()

	timer_off = False
	for i in range(len(instrucciones)):
		inicio_timer = pg.time.get_ticks()
		inst = fuente.render(instrucciones[i], 1, BLANCO)
		instRect = inst.get_rect()
		titulo_top += 5 # 10 pixeles entre linea y linea
		instRect.top = titulo_top + 240
		instRect.centerx = MITAD_ANCHO
		titulo_top += instRect.height
		while  not timer_off:						
			fin_timer = pg.time.get_ticks()
			res = (fin_timer - inicio_timer)
			if res > TIMER_OFF_GAME_OVER:
				timer_off = True
		pantalla.blit(inst, instRect)
		pg.display.flip()
		timer_off = False


	pg.display.flip()
	res = stop_game_over(pantalla, clock)
	return res


def truco_game_win(pantalla, clock):
	fuente = pg.font.Font('freesansbold.ttf', 22)
	fuente.set_bold(True)
	
	titulo = pg.image.load(IMAGEN_MENU_PRINCIPAL)
	img_titulo = titulo.get_rect()
	titulo_top = 5
	img_titulo.top = titulo_top
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height

	fondo = pg.image.load(FONDO_MENU_WIN)
	img_fondo= fondo.get_rect()
	img_fondo.top = 0
	img_fondo.centerx = MITAD_ANCHO

	instrucciones = INSTRUCCIONES_GAME_WIN
	instrucciones2 = INSTRUCCIONES_GAME_WIN2

	pantalla.blit(fondo, img_fondo)
	pantalla.blit(titulo, img_titulo)

	titulo_top = 10
	img_titulo.top = titulo_top
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height
	for i in range(len(instrucciones2)):
		inst = fuente.render(instrucciones2[i], 1, BLANCO)
		instRect = inst.get_rect()
		titulo_top += 5 # 10 pixeles entre linea y linea
		instRect.top = titulo_top + 250
		instRect.centerx = MITAD_ANCHO
		titulo_top += instRect.height
		pantalla.blit(inst, instRect)

	pg.display.flip()

def menu_game_win(pantalla, clock):
	pg.mixer.music.load(MUSICA_GAME_OVER)
	pg.mixer.music.play(loops=-1)
	fuente = pg.font.Font('freesansbold.ttf', 22)
	fuente.set_bold(True)
	
	titulo = pg.image.load(IMAGEN_MENU_PRINCIPAL)
	img_titulo = titulo.get_rect()
	titulo_top = 10
	img_titulo.top = titulo_top
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height

	fondo = pg.image.load(FONDO_MENU_WIN)
	img_fondo= fondo.get_rect()
	img_fondo.top = 0
	img_fondo.centerx = MITAD_ANCHO

	instrucciones = INSTRUCCIONES_GAME_WIN
	instrucciones2 = INSTRUCCIONES_GAME_WIN2

	pantalla.blit(fondo, img_fondo)
	pantalla.blit(titulo, img_titulo)


	pg.display.flip()

	timer_off = False
	for i in range(len(instrucciones)):
		inicio_timer = pg.time.get_ticks()
		inst = fuente.render(instrucciones[i], 1, BLANCO)
		instRect = inst.get_rect()
		titulo_top += 5 # 10 pixeles entre linea y linea
		instRect.top = titulo_top + 250
		instRect.centerx = MITAD_ANCHO
		titulo_top += instRect.height
		while  not timer_off:						
			fin_timer = pg.time.get_ticks()
			res = (fin_timer - inicio_timer)
			if res > TIMER_OFF_GAME_WIN:
				timer_off = True
		pantalla.blit(inst, instRect)
		pg.display.flip()
		timer_off = False

	inicio_timer = pg.time.get_ticks()
	while  not timer_off:						
		fin_timer = pg.time.get_ticks()
		res = (fin_timer - inicio_timer)
		if res > TIMER_OFF_INSTRUCCIONES:
			timer_off = True

	truco_game_win(pantalla, clock)

	pg.display.flip()
	res = stop_game_over(pantalla, clock)
	return res

'''def plantilla_menu(pantalla, clock, tipo):
	if tipo == "menu_principal":
		musica = MUSICA_MENU_PRINCIPAL
		tamaño = 24
		imagen = IMAGEN_MENU_PRINCIPAL
		fondo = FONDO_MENU_PRINCIPAL
		instrucciones = INSTRUCCIONES_MENU_PRINCIPAL
		altura_rect = 250
	elif tipo == "creditos":
		musica = MUSICA_GAME_OVER
		tamaño = 28
		imagen = IMAGEN_MENU_PRINCIPAL
		fondo = FONDO_MENU_PRINCIPAL
		instrucciones = INSTRUCCIONES_CREDITOS
		altura_rect = 280
	elif tipo == "game_over":
		musica = MUSICA_GAME_OVER
		tamaño = 22
		imagen = IMAGEN_MENU_PRINCIPAL
		fondo = FONDO_GAME_OVER
		instrucciones = INSTRUCCIONES_GAME_OVER
		altura_rect = 450



	pg.mixer.music.load(musica)
	pg.mixer.music.play(loops=-1)
	fuente = pg.font.Font('freesansbold.ttf', tamaño)
	fuente.set_bold(True)
	
	# Imagen principal que sirve de titulo
	titulo = pg.image.load(imagen)
	img_titulo = titulo.get_rect()
	titulo_top = 20
	img_titulo.top = titulo_top
	img_titulo.centerx = MITAD_ANCHO
	titulo_top += img_titulo.height

	fondo = pg.image.load(fondo)
	img_fondo= fondo.get_rect()
	img_fondo.top = 0
	img_fondo.centerx = MITAD_ANCHO

	# Pasar las instrucciones como una lista para controlar las lineas
	#instrucciones = instrucciones

	pantalla.blit(fondo, img_fondo)
	pantalla.blit(titulo, img_titulo)


	for i in range(len(instrucciones)):
		inst = fuente.render(instrucciones[i], 1, BLANCO)
		instRect = inst.get_rect()
		titulo_top += 10 # 10 pixeles entre linea y linea
		if i == 0:
			instRect.top = titulo_top + altura_rect
		else:
			instRect.top = titulo_top + altura_rect + 10
		instRect.centerx = MITAD_ANCHO
		titulo_top += instRect.height
		pantalla.blit(inst, instRect)


	pg.display.flip()

	if tipo == "menu_principal":
		res = stop_menu_principal(pantalla, clock)
		return [res[0], res[1]]
	elif tipo == "creditos":
		res = stop_creditos(pantalla, clock)
		return [res[0], res[1]]
	elif tipo == "game_over":
		res = stop_game_over(pantalla, clock)
		return res

	fade(pantalla)
	#return [res[0], res[1]]'''


def pantalla_pausa(pantalla):
	pantalla_pausa = pg.Surface(pantalla.get_size()).convert_alpha()
	pantalla_pausa.fill((0, 0, 0, 180))
	dibujar_texto(pantalla_pausa, "Juego Pausado", 100, BLANCO, MITAD_ANCHO, MITAD_ALTO)
	return pantalla_pausa


def dibujar_texto(pantalla, texto, tamaño, color, x, y, align="topleft"):
		# metodo para recibir un string y dibujarlo en pantalla
		match_fuente = pg.font.match_font(FUENTE)
		fuente = pg.font.Font(match_fuente, tamaño)
		fuente.set_bold(True)
		texto_surface = fuente.render(texto, True, color)
		texto_rect = texto_surface.get_rect()
		texto_rect.midtop = (x, y)
		pantalla.blit(texto_surface, texto_rect)