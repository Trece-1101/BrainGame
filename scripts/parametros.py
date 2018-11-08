# modulo para almacenar parametros constantes re-utilizables

import pygame as pg

# Pantalla
TITULO = "Mi juego"
ANCHO = 1024
ALTO = 640
MITAD_ANCHO = ANCHO / 2
MITAD_ALTO = ALTO / 2
FPS = 60
ACTUALIZACION_CUADROS = 250
FUENTE = "arial"

# Constantes Personaje y enemigos
vec2 = pg.math.Vector2 # vector2 para movimiento y posicion
PLAYER_ACEL = 100 # 120 px por segundo
PLAYER_FRICCION = -0.1
PLAYER_DASH = 2
PLAYER_STAMINA = 100
PLAYER_SALTO = -3000
CORTE_SALTO = -500
GRAVEDAD = 180
BOOST_POW = -50
PLAYER_VIDA_INICIAL = 10
PLAYER_IMG = ""

# Capas
PLAYER_LAYER = 2
PLATAFORMA_LAYER = 1
ITEM_LAYER = 1
ENEMIGO_LAYER = 2

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CELESTE = (0, 155, 155)

# Tiles
TAMAÑO_TILE = 32
ANCHO_GRILLA = ANCHO / TAMAÑO_TILE #  32 ancho
ALTO_GRILLA = ALTO / TAMAÑO_TILE # 20 alto
OFFSETX_CAMARA = 200

# Items
items = {"A": "acelerar", 
		"S": "saltar", 
		"C": "combotron", 
		"B": "BotAraña",
		"AV": "Antivirus" }

PROB_ACELERADOR = 100
BOOST_ACELERADOR = 40
PROB_PAD_SALTO = 100
BOOST_PAD_SALTO = 1.2

# Enemigos
DANIO_BOT = 5
DANIO_AV = 10
MOV_AV = [150, 175, 200, 225, 250]
#VEL_AV = [2, 3, 4, 5, 6, 8, 10]
VEL_AV = [0.5]
VEL_BOT = [10, 15, 20, 25, 30, 35]
RADIO_DETECCION = [200, 250, 300, 350, 400]
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