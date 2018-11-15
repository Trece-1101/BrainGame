# modulo para almacenar parametros constantes re-utilizables

import pygame as pg
import os
from pathlib import Path

# Pantalla
TITULO = "Mi juego"
ANCHO = 1440
ALTO = 896
MITAD_ANCHO = ANCHO / 2
MITAD_ALTO = ALTO / 2
FPS = 60
ACTUALIZACION_CUADROS = 250
ACTUALIZACION_CUADROS_ENEMIGOS = 400
FUENTE = "arial"


# Constantes Personaje
vec2 = pg.math.Vector2 # vector2 para movimiento y posicion
PLAYER_ACEL = 100 # 120 px por segundo
PLAYER_FRICCION = -0.1
PLAYER_DASH = 2
PLAYER_STAMINA = 100
PLAYER_SALTO = -2500
CORTE_SALTO = -500
GRAVEDAD = 150
BOOST_POW = -50
PLAYER_VIDA_INICIAL = 50
UMBRAL_CORRER = 100

# Dificultades
TIEMPO_NIVEL = 30000
DIFICULTAD_IMPOSIBLE = 0.4
DIFICULTAD_HARD = 0.8
DIFICULTAD_NORMAL = 1
DIFICULTAD_FACIL = 1.2
DIFICULTAD_BATY = 1.5

# Capas
FONDO_LAYER = 0
PLAYER_LAYER = 2
PLATAFORMA_LAYER = 1
ITEM_LAYER = 1
ENEMIGO_LAYER = 2
PORTAL_LAYER = 1

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CELESTE = (0, 155, 155)

# Tiles
TAMAÑO_TILE = 40
ANCHO_GRILLA = ANCHO / TAMAÑO_TILE # 1024 = 32 ancho;  1440 = 45 ancho
ALTO_GRILLA = ALTO / TAMAÑO_TILE # 640 = 20 alto; 896 = 28 alto
OFFSETX_CAMARA = 200

# Items
items = {"A": "acelerar", 
		"S": "saltar", 
		"C": "combotron",
		"T": "tiempotron", 
		"B": "BotAraña",
		"AV": "Antivirus" }

PROB_ACELERADOR = 60
PROB_PAD_SALTO = 50
PROB_COMBOTRON = 70
PROB_TIEMPOTRON = 30
BOOST_PAD_SALTO = 1.2
BOOST_ACELERADOR = 50
BOOST_COMBOTRON = 15
BOOST_TIEMPOTRON = 1000
RADIO_DETECCION_PORTAL = 450

# Enemigos
DANIO_BOT = 2000
DANIO_AV = 3000
MOV_AV = [150, 175, 200, 225, 250]
VEL_AV = [2, 3, 4, 5, 6]
VEL_BOT = [20, 25, 30, 35, 50]
TIEMPO_ANIMACION_MUERTE = 500
RADIO_DETECCION = [200, 250, 300, 350, 400]



# imagenes
CARPETA_IMAGENES = Path("gfx")
SPRITESHEET = "spritesheet.png"
SPRITESHEET_ARAÑA = "spritesheet_araña.png"


FONDOS = {"fondo1": "fondo1.png",
		"fondo2": "fondo2.png",
		"fondo3": "fondo3.png",
		"fondo4": "fondo4.png",
		"fondo5": "fondo5.png",
		"fondo6": "fondo6.png"}

FONDO = ["fondo1.png", "fondo2.png", "fondo3.png", "fondo4.png", "fondo5.png", "fondo6.png"]

IMG_MENU = {"titulo": "star_title.png", "fondo": "Virus_Fondo.png"}



IMG_ENEMIGOS = {"av_idle": "avIdle.png",
				"av_run1": "avrun.png",
				"bot_idle": "botIdle.png",
				"bot_run": "botrun.png",
				"bot_walk1": "botwalk1.png",
				"bot_walk2": "botwalk2.png",
				"bot_walk11": "botwalkizq1.png",
				"bot_walk12": "botwalkizq2.png",
				"prueba": "p1_front.png",
				"prueba2": "p3_front.png"}


SPRITESHEETS = {"bot": "Prueba_sprite.png"}

# sonidos
CARPETA_SONIDOS = Path("sfx") 

SFX = {"musica_menu": "menu.ogg", 
		"musica": ["musica1.wav", "musica2.wav", "musica3.wav", "musica4.wav"],
		"musica_creditos": "creditos.wav",
		"boost": "boost.wav",
		"tiempotron": "tiempotron.wav",
		"combotron": "combotron.wav",
		"lastimado": "lastimado.wav",
		"lastimados_npc": "lastimados_NPC.wav",
		"salto": "salto.wav",
		"salto_boost": "salto_boost.wav",
		"tiempo_limite": "tiempolimite.wav",
		"portal": "portal.wav"}

# Menus

INSTRUCCIONES_MENU_PRINCIPAL = ["Flechas para moverse (<- ->) -- Tecla [ESPACIO] para saltar -- Tecla [SHIFT] para acelerar (dash)",
					   			"J para jugar",
					   			"P para pausar",
					   			"C creditos",
					   			"ESC para salir"]
INSTRUCCIONES_GAME_OVER = ["Gracias por jugar",
							"ESC para salir"]

INSTRUCCIONES_CREDITOS = ["Creadores (orden alfabetico):",
							"Bazzi Omar",
							"Martin Matias",
							"M para regresar al menu",
							"ESC para salir"]

INSTRUCCIONES_DIFICULTAD = ["F - Nivel Facil - Tiempo de sobra",
							"M - Nivel Moderado - Para disfrutar tu tiempo",
							"D - Nivel Dificil - Un desafio total"]


MUSICA_MENU_PRINCIPAL = os.path.join(CARPETA_SONIDOS, SFX["musica_menu"])
MUSICA_GAME_OVER = os.path.join(CARPETA_SONIDOS, SFX["musica_creditos"])
IMAGEN_MENU_PRINCIPAL = os.path.join(CARPETA_IMAGENES, IMG_MENU["titulo"])
FONDO_MENU_PRINCIPAL = os.path.join(CARPETA_IMAGENES, IMG_MENU["fondo"])