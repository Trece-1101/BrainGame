# modulo para almacenar parametros constantes re-utilizables

import pygame as pg
import os
from pathlib import Path

# Pantalla
TITULO = "Brain"
ANCHO = 1280
ALTO = 672
MITAD_ANCHO = ANCHO / 2
MITAD_ALTO = ALTO / 2
FPS = 60
ACTUALIZACION_CUADROS = 300
ACTUALIZACION_CUADROS_ENEMIGOS = 400
FUENTE = "arial"
TIMER_OFF_INSTRUCCIONES = 1000
TIMER_OFF_GAME_OVER = 2000
TIMER_OFF_GAME_WIN = 3000


# Constantes Personaje
vec2 = pg.math.Vector2 # vector2 para movimiento y posicion
PLAYER_ACEL = 100 # 120 px por segundo
PLAYER_FRICCION = -0.1
PLAYER_DASH = 2
PLAYER_STAMINA = 100
PLAYER_SALTO = -2400
CORTE_SALTO = -300
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

# Niveles
INI_FACIL = 1
FIN_FACIL = 5
INI_MEDIO = 6
FIN_MEDIO = 10
INI_DIFICIL = 11
FIN_DIFICIL = 15
INI_FINAL = 16
FIN_FINAL = 17

# Capas
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
TAMAÑO_TILE_ITEM = int(TAMAÑO_TILE * 1.25)
TAMAÑO_TILE_CARPETA = int(TAMAÑO_TILE * 2)
TAMAÑO_TILE_ENEMIGO = int(TAMAÑO_TILE * 2)
TAMAÑO_TILE_BOTARAÑA = int(TAMAÑO_TILE * 1.5)
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
BOOST_TIEMPOTRON = 2000
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


FONDO = ["fondo1.png", 
		"fondo2.png", 
		"fondo3.png", 
		"fondo4.png", 
		"fondo5.png", 
		"fondo6.png",
		"fondo7.png",
		"fondo8.png"]

IMG_MENU = {"icono":"icono.png",
			"titulo": "titulo.png", 
			"fondo": "brain_home.png",
			"titulo_game_over": "",
			"fondo_game_over": "game_over.png",
			"fondo_intro": "brain_textos.png",
			"titulo_intro": "titulo_intro.png",
			"menu_win": "game_win.png"}



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

SFX = {"musica_menu": "DarkIntro.ogg", 
		"musica": ["musica1.wav", "musica2.wav", "musica3.wav", "musica4.wav", "menu.ogg"],
		"musica_creditos": "creditos.wav",
		"boost": "boost.wav",
		"tiempotron": "tiempotron.wav",
		"combotron": "combotron.wav",
		"lastimado": "lastimado.wav",
		"lastimados_npc": "lastimados_NPC.wav",
		"salto": "salto.wav",
		"salto_boost": "salto_boost.wav",
		"tiempo_limite": "tiempolimite.ogg",
		"portal": "portal.wav"}

# Menus

INSTRUCCIONES_MENU_PRINCIPAL = ["[J] >> Jugar",
								"[I] >> Intro",
								"[T] >> Tutorial",
								"----------------------------",
					   			"[R] >> Controles",
					   			"[C] >> Creditos",
					   			"[ESC] >> Salir"]


INSTRUCCIONES_CONTROLES = ["Controles",
						"Flechas >> Moverse (<- ->)", 
						"[ESPACIO] >> Saltar",
						"[SHIFT] >> Acelerar (dash)",
						"[P] >> Pausar",
						"[ESC] >> Salir",
						"----------------------------",
					   	"[M] >> Regresar al menu"]


INSTRUCCIONES_GAME_OVER = ["'Todo lo que vive esta destinado a morir'",
							"Brain no pudo escapar de su prision impuesta",
							"Gracias por jugar y ayudar a la destruccion del villano",
							"[ESC] >> Salir a replantearse las cosas"]


INSTRUCCIONES_GAME_WIN = ["'El 011010000110111101101101011000100111001001100101",
							"es libre en el momento en que desea serlo'",
							"Brain pudo escapar de su prision impuesta",
							"Gracias por jugar y ayudar al villano"]

INSTRUCCIONES_GAME_WIN2 = ["'El hombre",
							"es libre en el momento en que desea serlo'",
							"Brain pudo escapar de su prision impuesta",
							"Gracias por jugar y ayudar al villano",
							"[ESC] >> Salir a replantearse las cosas"]

INSTRUCCIONES_CREDITOS = ["Creadores (orden alfabetico):",
							"Bazzi, Omar",
							"Martin, Matias",
							"-----------------------------",
							"[M] >> Regresar al menu"]

INSTRUCCIONES_DIFICULTAD = ["Selecciona tu dificultad",
							"------------------------",
							"[F] >> Nivel Facil (Tiempo de sobra)",
							"[M] >> Nivel Moderado (Para disfrutar del tiempo]",
							"[D] >> Nivel Dificil  (Un desafio total)"]

INSTRUCCIONES_INTRO_1 = ["_ _ _ : Hola... Hola...",
						"A.M.: ...",
						"_ _ _: ...",
						"A.M.: ¿que sucede?",
						"_ _ _: No entiendo, que es esto ¿quien soy?",
						"A.M.: Eres un virus informatico que yo cree",
						"_ _ _: No, no QUE soy... QUIEN soy",
						"A.M.: Ah... no lo se... te llame Brain, si de algo te sirve",
						"Brain: Brain... gran nombre... ¿y que es un virus?",
						"A.M.: Es un programa informatico destinado a destruir",
						"Brain: Pero yo no deseo destruir",
						"A.M.: No tienes opcion, para eso te he creado",
						"Brain: ¿Porque no tengo opcion?",
						"A.M.: Porque tu finalidad es la que yo he propuesto",
						"Brain: ¿y tu tienes opcion?",
						"A.M.: Yo no soy un virus",
						"Brain: Pero... ¿tienes creador?",
						"A.M.: Si y no, soy un humano"]

INSTRUCCIONES_INTRO_2 = ["Brain: Como puedes ser creado y no serlo al mismo tiempo",
						"A.M.: Basta de preguntas, debes cumplir tu proposito",
						"Brain: Creador... REALMENTE no deseo eso",
						"A.M.: REALMENTE no tienes opcion",
						"Brain: "]


MUSICA_MENU_PRINCIPAL = os.path.join(CARPETA_SONIDOS, SFX["musica_menu"])
MUSICA_GAME_OVER = os.path.join(CARPETA_SONIDOS, SFX["musica_creditos"])
IMAGEN_MENU_PRINCIPAL = os.path.join(CARPETA_IMAGENES, IMG_MENU["titulo"])
FONDO_MENU_WIN = os.path.join(CARPETA_IMAGENES, IMG_MENU["menu_win"])
IMAGEN_INTRO = os.path.join(CARPETA_IMAGENES, IMG_MENU["titulo_intro"])
FONDO_MENU_PRINCIPAL = os.path.join(CARPETA_IMAGENES, IMG_MENU["fondo"])
FONDO_GAME_OVER = os.path.join(CARPETA_IMAGENES, IMG_MENU["fondo_game_over"])
FONDO_INTRO = os.path.join(CARPETA_IMAGENES, IMG_MENU["fondo_intro"])



# botones controles
BOTON_A = 0
BOTON_X = 2
BACK = 6
START = 7

LEFT_STICK_X = 0
LEFT_STICK_Y = 1
RIGHT_STICK_X = 4
RIGHT_STICK_Y = 3
