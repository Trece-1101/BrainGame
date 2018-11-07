import pygame as pg
from scripts.parametros import *


class PlayerOne(pg.sprite.Sprite):
	"""docstring for PlayerOne"""
	def __init__(self, game, x, y):
		self.groups = game.sprites
		#self._layer = PLAYER_LAYER
		super(PlayerOne, self).__init__(self.groups)
		self.game = game
		self.image = pg.Surface((TAMAÑO_TILE, TAMAÑO_TILE))
		self.image.fill(AZUL)
		self.rect = self.image.get_rect()
		self.vx = 0
		self.vy = 0
		self.x = x * TAMAÑO_TILE
		self.y = y * TAMAÑO_TILE
		

	def cargar_imagenes(self):
		self.cuadros_idle = [self.game.spritesheet_player.get_imagen(67, 196, 66, 92),
							self.game.spritesheet_player.get_imagen(0, 196, 66, 92)]		

		self.cuadros_correr_d = [self.game.spritesheet_player.get_imagen(0, 0, 72, 97),
								self.game.spritesheet_player.get_imagen(73, 0, 72, 97),
								self.game.spritesheet_player.get_imagen(146, 0, 72, 97),
								self.game.spritesheet_player.get_imagen(0, 98, 72, 97),
								self.game.spritesheet_player.get_imagen(73, 98, 72, 97),
								self.game.spritesheet_player.get_imagen(146, 98, 72, 97),
								self.game.spritesheet_player.get_imagen(219, 0, 72, 97)]

		self.cuadros_caminar_i = []
		for cuadro in self.cuadros_correr_d:
			self.cuadros_caminar_i.append(pg.transform.flip(cuadro, True, False))

		self.cuadro_saltar = self.game.spritesheet_player.get_imagen(438, 93, 67, 94)

		# quitar el fondo negro
		for cuadro in self.cuadros_idle:
			cuadro.set_colorkey(NEGRO)

		for cuadro in self.cuadros_correr_d:
			cuadro.set_colorkey(NEGRO)

		for cuadro in self.cuadros_correr_i:
			cuadro.set_colorkey(NEGRO)

		self.cuadro_saltar.set_colorkey(NEGRO)

	def control_salto(self):
		if self.saltando:
			if self.vel.y < CORTE_SALTO:
				self.vel.y = CORTE_SALTO

	def saltar(self):
		self.rect.y += 2		
		colisiones = pg.sprite.spritecollide(self, self.game.plataformas, False)
		self.rect.y -= 2
		if colisiones and not self.salto:
			#self.game.sfx_salto.play()
			self.saltando = True
			self.vel.y = PLAYER_SALTO

	def animar(self):
		este_instante = pg.time.get_ticks()
		if self.vel.x > UMBRAL_CORRER or self.vel.x < -UMBRAL_CORRER:
			self.caminando = True
		else:
			self.caminando = False

		if self.caminando:
			if este_instante - self.ultimo_update > ACTUALIZACION_CUADROS:
				self.ultimo_update = este_instante
				self.cuadro_actual = (self.cuadro_actual + 1) % len(self.cuadros_correr_d)				
				if self.vel.x > 0:
					self.image = self.cuadros_correr_d[self.cuadro_actual]
				else:
					self.image = self.cuadros_correr_i[self.cuadro_actual]

		if not self.salto and not self.caminando:
			if (este_instante - self.ultimo_update) > ACTUALIZACION_CUADROS:
				self.ultimo_update = este_instante
				self.cuadro_actual = (self.cuadro_actual + 1) % len(self.cuadros_idle)
				self.image = self.cuadros_idle[self.cuadro_actual]

		# mascara de colision
		self.mascara_col = pg.mask.from_surface(self.image)


	def update(self):
		#self.animar()
		#self.acel = vec2(0, GRAVEDAD)
		tecla = pg.key.get_pressed()
		if tecla[pg.K_LEFT] and not tecla[pg.K_RIGHT]:
			self.acel.x = -PLAYER_ACEL

		if tecla[pg.K_RIGHT] and not tecla[pg.K_LEFT]:
			self.acel.x = PLAYER_ACEL

		if tecla[pg.K_SPACE]:
			self.saltar()

		self.acel.x += self.vel.x * PLAYER_FRICCION	
		self.vel += self.acel
		self.pos += self.vel + 0.5 * self.acel # v + a/2|		

		self.rect.midbottom = self.pos