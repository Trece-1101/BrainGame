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
		self.vel = vec2(0, 0)
		self.pos = vec2(x * TAMAÑO_TILE, y * TAMAÑO_TILE)
		self.saltando = False
		self.sentido = "D"
		self.stamina = PLAYER_STAMINA

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

		

	def colision_plataforma(self, dir):
		# metodo para detectar colision con cualquier plataforma. spritexollide any chequea
		# colision entre un sprite (self = player) vs una coleccion/grupo (game.plataformas)
		# False para que no desaparezca al colisionar
		# Devuelve una lista que contiene los sprites de un grupo que colisionan con el sprite
		if dir == "x":
			colision = pg.sprite.spritecollide(self, self.game.plataformas, False)
			if colision:
				if self.vel.x > 0:
					# colision en el sentido x moviendose de izq a derecha
					# mi posicion de x tiene que ser la izq de la plataforma menos el ancho
					# de mi rectangulo de colision
					self.pos.x = colision[0].rect.left - self.rect.width
				if self.vel.x < 0:
					# colision en el sentido x moviendose de derecha a izquierda
					# mi posicion de x tiene que ser la derecha de la plataforma
					self.pos.x = colision[0].rect.right
				self.vel.x = 0
				self.rect.x = self.pos.x				
		if dir == "y":
			colision = pg.sprite.spritecollide(self, self.game.plataformas, False)
			if colision:
				if self.vel.y > 0:
					# colision en el sentido y moviendose de arriba para abajo (cayendo y+)
					# mi posicion y (mi cabeza) tiene que ser el techa de la plataforma menos mi
					# altura (= mis pies)
					self.pos.y = colision[0].rect.top - self.rect.height
				if self.vel.y < 0:					
					# colision en el sentido y moviendose de abajo para arriba (saltando y-)
					# mi posicion de y (mi cabeza) tiene que ser el fondo de la plataforma
					self.pos.y = colision[0].rect.bottom
				self.saltando = False
				self.vel.y = 0
				self.rect.y = self.pos.y
				


	def saltar(self):
		self.rect.y += 2
		colision = pg.sprite.spritecollide(self, self.game.plataformas, False)
		self.rect.y -= 2
		if colision and not self.saltando:
			#print("salto", " ", colision)
			#print(self.saltando)
			#self.game.sfx_salto.play()
			self.saltando = True
			self.vel.y = PLAYER_SALTO


	def control_salto(self):
		if self.saltando:
			if self.vel.y < CORTE_SALTO:
				self.vel.y = CORTE_SALTO

	def pad_salto(self):
		self.vel.y = PLAYER_SALTO * BOOST_PAD_SALTO


	def fisica_aceleracion(self):
		self.acel.x += self.vel.x * PLAYER_FRICCION
		self.vel += self.acel

		# descomentar para tener una idea de como esta funcionando la fisica
		# y modificar los valores en parametros para cambiar comportamiento
		#print("acelX {0}".format(self.acel.x))
		#print("velX {0}".format(self.vel.x))
		#print("velY {0}".format(self.vel.y))

		self.pos += self.vel * self.game.dt
		self.rect.x = self.pos.x
		self.colision_plataforma("x")
		self.rect.y = self.pos.y
		self.colision_plataforma("y")


	def acelerar(self):
		if self.sentido == "D":
			self.acel.x = PLAYER_ACEL * BOOST_ACELERADOR
		elif self.sentido == "I":
			self.acel.x = -(PLAYER_ACEL * BOOST_ACELERADOR)

		self.fisica_aceleracion()

	

	def update(self):
		self.acel = vec2(0, GRAVEDAD)		

		tecla = pg.key.get_pressed()			
		if tecla[pg.K_LEFT] and not tecla[pg.K_RIGHT]:
			self.acel.x = -PLAYER_ACEL
			self.sentido = "I"

		elif tecla[pg.K_RIGHT] and not tecla[pg.K_LEFT]:
			self.acel.x = PLAYER_ACEL
			self.sentido = "D"


		if tecla[pg.K_SPACE]:
			pass					
	
		if tecla[pg.K_LSHIFT]:
			if self.sentido == "D" and self.stamina > 0:
				self.acel.x = PLAYER_ACEL * PLAYER_DASH
				self.stamina -= 1
			elif self.sentido == "I" and self.stamina > 0:
				self.acel.x = -(PLAYER_ACEL * PLAYER_DASH)
				self.stamina -= 1
			print(self.stamina)


		self.fisica_aceleracion()
		



class Enemigo(pg.sprite.Sprite):
	"""docstring for Enemigo"""
	def __init__(self, arg):
		super(Enemigo, self).__init__()
		self.arg = arg
		
		