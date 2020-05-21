import pygame as pg
from scripts.parametros import *


class Gui(pg.sprite.Sprite):
    def __init__(self, game, pantalla, x, y, pct, color_lleno, color_medio, color_vacio, texto):
        self.groups = game.sprites, game.gui
        self._layer = GUI_LAYER
        super(Gui, self).__init__(self.groups)
        self.pantalla = pantalla
        self.x = x
        self.y = y
        self.pct = pct
        self.color_lleno = color_lleno
        self.color_medio = color_medio
        self.color_vacio = color_vacio
        self.texto = texto

    def dibujar_gui(self):
        if self.pct < 0:
            self.pct = 0
        elif self.pct > 100:
            self.pct = 100
        self.ancho = 100
        self.alto = 40
        relleno = self.pct * self.ancho
        borde = pg.Rect(self.x, self.y, self.ancho, self.alto)
        relleno_rect = pg.Rect(self.x, self.y, relleno, self.alto)
        if self.pct >= 0.8:
            color = self.color_lleno
        elif pct > 0.3 and pct < 0.8:
            color = self.color_medio
        else:
            color = self.color_vacio
        pg.draw.rect(self.pantalla, color, relleno_rect)
        pg.draw.rect(self.pantalla, BLANCO, borde, 2)
        dibujar_texto(self.pantalla, self.texto, 20, BLANCO, x + 55, y + 45)

    def update(self):
        self.dibujar_gui()
