import pygame as pg
from scripts.parametros import *


class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.sprites, game.items
        self._layer = ITEM_LAYER
        super(PowerUp, self).__init__(self.groups)
        self.game = game
        self.type = ""
        self.image = self.game.spritesheet.get_imagen(0, 0, 0, 0)
        self.image = pg.transform.scale(
            self.image, (TAMAÑO_TILE_ITEM, TAMAÑO_TILE_ITEM))
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TAMAÑO_TILE
        self.rect.y = y * TAMAÑO_TILE


class Acelerador(PowerUp):
    def __init__(self, game, x, y):
        PowerUp.__init__(self, game, x, y)
        self.type = items["A"]
        self.image = self.game.spritesheet.get_imagen(198, 132, 64, 64)


class PadSalto(PowerUp):
    def __init__(self, game, x, y):
        PowerUp.__init__(self, game, x, y)
        self.type = items["S"]
        self.image = self.game.spritesheet.get_imagen(198, 66, 64, 64)


class Combotron(PowerUp):
    def __init__(self, game, x, y):
        PowerUp.__init__(self, game, x, y)
        self.type = items["C"]
        self.image = self.game.spritesheet.get_imagen(198, 198, 64, 64)


class Tiempotron(PowerUp):
    def __init__(self, game, x, y):
        PowerUp.__init__(self, game, x, y)
        self.type = items["T"]
        self.image = self.game.spritesheet.get_imagen(198, 0, 64, 64)
