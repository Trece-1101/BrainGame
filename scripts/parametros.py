# modulo para almacenar parametros constantes re-utilizables

import pygame as pg

# Pantalla
TITULO = "Mi juego"
ANCHO = 1440
ALTO = 896
MITAD_ANCHO = ANCHO / 2
MITAD_ALTO = ALTO / 2
FPS = 60
ACTUALIZACION_CUADROS = 150
FUENTE = "arial"
IMG_MENU = {"titulo": "star_title.png", "fondo": "Virus_Fondo.png"}

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
PLAYER_IMG = ""
SPRITESHEET_BRAIN = "sprites.png"
UMBRAL_CORRER = 50

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
TAMAÑO_TILE = 32
ANCHO_GRILLA = ANCHO / TAMAÑO_TILE # 1024 = 32 ancho;  1440 = 45 ancho
ALTO_GRILLA = ALTO / TAMAÑO_TILE # 640 = 20 alto; 896 = 28 alto
OFFSETX_CAMARA = 200

# Items
items = {"A": "acelerar", 
		"S": "saltar", 
		"C": "combotron", 
		"B": "BotAraña",
		"AV": "Antivirus" }

PROB_ACELERADOR = 50
BOOST_ACELERADOR = 40
PROB_PAD_SALTO = 60
BOOST_PAD_SALTO = 1.2
PROB_COMBOTRON = 50

# Enemigos
DANIO_BOT = 5
DANIO_AV = 10
MOV_AV = [150, 175, 200, 225, 250]
VEL_AV = [2, 3, 4, 5, 6]
VEL_BOT = [10, 15, 20, 25, 30, 35]
TIEMPO_ANIMACION_MUERTE = 500
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


SPRITESHEETS = {"bot": "Prueba_sprite.png"}
SPRITESHEET_ARAÑA = "araña.png"


# sonidos
SFX = {"musica_menu": "menu.ogg", 
		"musica": ["musica1.wav", "musica2.wav", "musica3.wav", "musica4.wav"],
		"musica_creditos": "creditos.wav",
		"boost": "boost.wav",
		"itembinario": "itembinario.wav",
		"lastimado": "lastimado.wav",
		"lastimados_npc": "lastimados_NPC.wav",
		"salto": "salto.wav",
		"salto_boost": "salto_boost.wav",
		"tiempo_limite": "tiempolimite.wav"}
