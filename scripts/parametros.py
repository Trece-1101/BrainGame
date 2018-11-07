# modulo para almacenar parametros constantes re-utilizables

import pygame as pg

# Pantalla
TITULO = "Mi juego"
ANCHO = 1024
ALTO = 640
MITAD_ANCHO = ANCHO / 2
MITAD_ALTO = ALTO / 2
FPS = 60
ACT_CUADROS = 250
FUENTE = "arial"

# Constantes Personaje y enemigos
vec2 = pg.math.Vector2 # vector2 para movimiento y posicion
PLAYER_ACEL = 1
PLAYER_FRICCION = -0.1
PLAYER_SALTO = -30
CORTE_SALTO = -8
UMBRAL_CORRER = 0.5
GRAVEDAD = 1
BOOST_POW = -50

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