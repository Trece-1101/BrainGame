import pygame as pg
from random import randrange, uniform, choice
from scripts.parametros import *

def colision_plataforma(sprite, grupo, dir):
		# metodo para detectar colision con cualquier plataforma. spritexollide chequea
		# colision entre un sprite (self = player) vs una coleccion/grupo (game.plataformas)
		# False para que no desaparezca al colisionar
		# Devuelve una lista que contiene los sprites de un grupo que colisionan con el sprite
		#print(sprite)
		#print(grupo)
		if dir == "x":
			colision = pg.sprite.spritecollide(sprite, grupo, False)
			if colision:
				if sprite.vel.x > 0:
					# colision en el sentido x moviendose de izq a derecha
					# mi posicion de x tiene que ser la izq de la plataforma menos el ancho
					# de mi rectangulo de colision
					sprite.pos.x = colision[0].rect.left - sprite.rect.width
				if sprite.vel.x < 0:
					# colision en el sentido x moviendose de derecha a izquierda
					# mi posicion de x tiene que ser la derecha de la plataforma
					sprite.pos.x = colision[0].rect.right
				sprite.vel.x = 0
				sprite.rect.x = sprite.pos.x				
		if dir == "y":
			colision = pg.sprite.spritecollide(sprite, grupo, False)
			if colision:
				if sprite.vel.y > 0:
					# colision en el sentido y moviendose de arriba para abajo (cayendo y+)
					# mi posicion y (mi cabeza) tiene que ser el techa de la plataforma menos mi
					# altura (= mis pies)
					sprite.pos.y = colision[0].rect.top - sprite.rect.height
					for plataforma in colision:
						if plataforma.type == "trampa" and sprite.type == "player":
							plataforma.pisada = True
				if sprite.vel.y < 0:					
					# colision en el sentido y moviendose de abajo para arriba (saltando y-)
					# mi posicion de y (mi cabeza) tiene que ser el fondo de la plataforma
					sprite.pos.y = colision[0].rect.bottom
				if isinstance(sprite, PlayerOne):
					sprite.saltando = False
				sprite.vel.y = 0
				sprite.rect.y = sprite.pos.y


class PlayerOne(pg.sprite.Sprite):
	"""docstring for PlayerOne"""
	def __init__(self, game, x, y):
		self.groups = game.sprites
		self._layer = PLAYER_LAYER
		super(PlayerOne, self).__init__(self.groups)
		self.game = game
		self.cuadro_actual = 0
		self.ultimo_update = 0
		self.cargar_imagenes()
		self.image = self.cuadros_idle[0]
		self.image.set_colorkey(NEGRO)
		self.rect = self.image.get_rect()
		self.vel = vec2(0, 0)
		self.acel = vec2(0, 0)
		self.pos = vec2(x * TAMAÑO_TILE, y * TAMAÑO_TILE)
		self.saltando = False
		self.sentido = "D"
		self.stamina = PLAYER_STAMINA
		self.vida = PLAYER_VIDA_INICIAL
		self.type = "player"
		self.col = 0
		self.fila = 0

	def cargar_imagenes(self):
		self.cuadros_idle = [self.game.spritesheet.get_imagen(132, 264, 64, 64),
							self.game.spritesheet.get_imagen(132, 198, 64, 64),
							self.game.spritesheet.get_imagen(132, 132, 64, 64),
							self.game.spritesheet.get_imagen(132, 66, 64, 64),
							self.game.spritesheet.get_imagen(132, 0, 64, 64)]

		self.cuadros_caminar_d = [self.game.spritesheet.get_imagen(66, 396, 64, 64),
								self.game.spritesheet.get_imagen(66, 330, 64, 64),
								self.game.spritesheet.get_imagen(66, 264, 64, 64),
								self.game.spritesheet.get_imagen(66, 198, 64, 64)]

		self.cuadros_caminar_i = []
		for cuadro in self.cuadros_caminar_d:
			self.cuadros_caminar_i.append(pg.transform.flip(cuadro, True, False)) 		

		self.cuadros_correr_d = [self.game.spritesheet.get_imagen(66, 132, 64, 64),
								self.game.spritesheet.get_imagen(66, 66, 64, 64)]

		self.cuadros_correr_i = []
		for cuadro in self.cuadros_correr_d:
			self.cuadros_correr_i.append(pg.transform.flip(cuadro, True, False))

		self.cuadro_saltar_d = self.game.spritesheet.get_imagen(0 , 396, 64, 64)
		self.cuadro_saltar_i = pg.transform.flip(self.cuadro_saltar_d, True, False)

		self.cuadro_morir = self.game.spritesheet.get_imagen(66 , 0, 64, 64)

		# quitar el fondo negro
		for cuadro in self.cuadros_idle:
			cuadro.set_colorkey(NEGRO)

		for cuadro in self.cuadros_caminar_d:
			cuadro.set_colorkey(NEGRO)

		for cuadro in self.cuadros_caminar_i:
			cuadro.set_colorkey(NEGRO)

		for cuadro in self.cuadros_correr_d:
			cuadro.set_colorkey(NEGRO)

		for cuadro in self.cuadros_correr_i:
			cuadro.set_colorkey(NEGRO)

		self.cuadro_saltar_d.set_colorkey(NEGRO)
		self.cuadro_saltar_i.set_colorkey(NEGRO)

		self.cuadro_morir.set_colorkey(NEGRO)

	

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

		if not self.saltando and not self.caminando:
			if (este_instante - self.ultimo_update) > ACTUALIZACION_CUADROS:
				self.ultimo_update = este_instante
				self.cuadro_actual = (self.cuadro_actual + 1) % len(self.cuadros_idle)
				self.image = self.cuadros_idle[self.cuadro_actual]

		if self.saltando:
			if self.sentido == "D":
				self.image = self.cuadro_saltar_d
			elif self.sentido == "I":
				self.image = self.cuadro_saltar_i

		# mascara de colision
		self.mascara_col = pg.mask.from_surface(self.image)	



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
		colision_plataforma(self, self.game.plataformas, "x")
		self.rect.y = self.pos.y
		colision_plataforma(self, self.game.plataformas, "y")


	def acelerar(self):
		if self.sentido == "D":
			self.acel.x = PLAYER_ACEL * BOOST_ACELERADOR
		elif self.sentido == "I":
			self.acel.x = -(PLAYER_ACEL * BOOST_ACELERADOR)

		self.fisica_aceleracion()

	def lastimar(self, danio):
		self.vida -= danio

	

	def update(self):
		self.animar()		
		self.acel = vec2(0, GRAVEDAD)
		if self.vel.y == 0:
			if self.sentido == "D":
				self.col = self.pos.x / 32 - 2
				self.fila = (self.pos.y / 32) - 2
			elif self.sentido == "I":
				self.col = self.pos.x / 32 + 2
				self.fila = (self.pos.y / 32) - 2
		tecla = pg.key.get_pressed()			
		if tecla[pg.K_LEFT] and not tecla[pg.K_RIGHT]:
			self.acel.x = -PLAYER_ACEL
			self.sentido = "I"

		elif tecla[pg.K_RIGHT] and not tecla[pg.K_LEFT]:
			self.acel.x = PLAYER_ACEL
			self.sentido = "D"	
	
		if tecla[pg.K_LSHIFT]:
			if self.sentido == "D" and self.stamina > 0:
				self.acel.x = PLAYER_ACEL * PLAYER_DASH
				self.stamina -= 1
			elif self.sentido == "I" and self.stamina > 0:
				self.acel.x = -(PLAYER_ACEL * PLAYER_DASH)
				self.stamina -= 1

		self.fisica_aceleracion()




class Botaraña(pg.sprite.Sprite):
	"""docstring for Enemigo"""	
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.bots
		self.layer = ENEMIGO_LAYER
		super(Botaraña, self).__init__(self.groups)
		self.game = game
		self.cuadro_actual = 0
		self.ultimo_update = 0
		self.type = items["B"]
		self.image = pg.Surface((TAMAÑO_TILE, TAMAÑO_TILE))
		self.image.fill(NEGRO)
		#self.cargar_imagenes()
		#self.image = self.cuadros_idle[0]
		self.rect = self.image.get_rect()
		self.vel = vec2(0, 0)
		self.acel = vec2(0, 0)
		self.pos = vec2(x, y) * TAMAÑO_TILE
		self.rect.center = self.pos
		self.acel = vec2(0, 0)
		self.vivo = True
		self.idle = True
		self.mascara_col = pg.mask.from_surface(self.image)

	def cargar_imagenes(self):
		pass
		'''self.cuadros_idle = [self.game.spritesheet.get_imagen(),
							self.game.spritesheet.get_imagen(),
							self.game.spritesheet.get_imagen(),
							self.game.spritesheet.get_imagen()]


		self.cuadros_caminar_d = [self.game.spritesheet.get_imagen(),
								self.game.spritesheet.get_imagen(),
								self.game.spritesheet.get_imagen(),
								self.game.spritesheet.get_imagen()]	

		self.cuadros_caminar_i = [self.game.spritesheet.get_imagen(),
								self.game.spritesheet.get_imagen(),
								self.game.spritesheet.get_imagen(),
								self.game.spritesheet.get_imagen()]

		self.cuadros_correr_d = [self.game.spritesheet.get_imagen(),]		

		

		#self.cuadro_saltar = self.game.spritesheet_player.get_imagen(438, 93, 67, 94)

		# quitar el fondo negro
		#for cuadro in self.cuadros_correr_d:
		#	cuadro.set_colorkey(NEGRO)

		#for cuadro in self.cuadros_correr_i:
		#	cuadro.set_colorkey(NEGRO)

		#for cuadro in self.cuadros_idle:
		#	cuadro.set_colorkey(NEGRO)'''

		


	def animar(self):
		este_instante = pg.time.get_ticks()

		if self.idle:
			if este_instante - self.ultimo_update > ACTUALIZACION_CUADROS:
				self.ultimo_update = este_instante
				self.cuadro_actual = (self.cuadro_actual + 1) % len(self.cuadros_idle)
				self.image = self.cuadros_idle[self.cuadro_actual]
		else:
			if este_instante - self.ultimo_update > ACTUALIZACION_CUADROS:
				self.ultimo_update = este_instante
				self.cuadro_actual = (self.cuadro_actual + 1) % len(self.cuadros_correr_d)				
				if self.vel.x > 0:
					self.image = self.cuadros_correr_d[self.cuadro_actual]
				else:
					self.image = self.cuadros_correr_i[self.cuadro_actual]

		# mascara de colision
		self.mascara_col = pg.mask.from_surface(self.image)

	def morir(self):
		self.vel.x = 0
		self.vivo = False
		self.animar()



	def update(self):
		#self.animar()
		self.acel = vec2(0, GRAVEDAD)
		dist_obj = self.pos - self.game.player.pos
		#print(self.pos)
		#print(dist_obj[1])
		if (abs(dist_obj[0]) < choice(RADIO_DETECCION)) and (abs(dist_obj[1]) < 70):
			#print("detectado")
			if dist_obj[0] > 0:             
				self.acel.x -= choice(VEL_BOT)
			else:
				self.acel.x += choice(VEL_BOT)
		else:
			self.acel.x = 0				
			#print("no detectado")

		self.vel += self.acel
		self.pos += self.vel * self.game.dt
		self.rect.x = self.pos.x
		colision_plataforma(self, self.game.plataformas, "x")
		self.rect.y = self.pos.y
		colision_plataforma(self, self.game.plataformas, "y")
		


class Antivirus(pg.sprite.Sprite):
	"""docstring for Enemigo"""	
	def __init__(self, game, x, y):
		self.groups = game.sprites, game.antivirus
		self.layer = ENEMIGO_LAYER
		super(Antivirus, self).__init__(self.groups)
		self.game = game
		self.cuadro_actual = 0
		self.ultimo_update = 0
		self.type = items["AV"]
		self.cargar_imagenes()
		self.image = self.cuadros_idle[0]
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE		
		self.vx = choice(VEL_AV)
		if randrange(100) < 50:
			self.vx *= -1
		self.iniciox = self.rect.x
		self.movimimiento = choice(MOV_AV)
		self.vivo = True

	def cargar_imagenes(self):
		self.cuadros_idle = [self.game.spritesheet.get_imagen(198, 330, 64, 64),
							self.game.spritesheet.get_imagen(462, 66, 64, 64),
							self.game.spritesheet.get_imagen(462, 132, 64, 64),
							self.game.spritesheet.get_imagen(462, 198, 64, 64)]

		self.cuadro_muerto = self.game.spritesheet.get_imagen(396, 330, 64, 64)

		self.cuadros_correr_d = [self.game.spritesheet.get_imagen(462, 0, 64, 64),
								self.game.spritesheet.get_imagen(396, 396, 64, 64)]			

		self.cuadros_correr_i = []
		for cuadro in self.cuadros_correr_d:
			self.cuadros_correr_i.append(pg.transform.flip(cuadro, True, False))	

		# quitar el fondo negro
		for cuadro in self.cuadros_correr_d:
			cuadro.set_colorkey(NEGRO)

		for cuadro in self.cuadros_correr_i:
			cuadro.set_colorkey(NEGRO)

		for cuadro in self.cuadros_idle:
			cuadro.set_colorkey(NEGRO)

		self.cuadro_muerto.set_colorkey(NEGRO)


	def morir(self):
		self.vx = 0
		self.vivo = False
		self.animar()


	def animar(self):
		este_instante = pg.time.get_ticks()
		if not self.vivo:
			self.image = self.cuadro_muerto
		else:
			if este_instante - self.ultimo_update > ACTUALIZACION_CUADROS_ENEMIGOS:
					self.ultimo_update = este_instante
					self.cuadro_actual = (self.cuadro_actual + 1) % len(self.cuadros_correr_d)
					if self.vx != 0:				
						if self.vx > 0:
							self.image = self.cuadros_correr_d[self.cuadro_actual]
						else:
							self.image = self.cuadros_correr_i[self.cuadro_actual]
					elif self.vx == 0:
						self.image = self.cuadros_idle[self.cuadro_actual]

		# mascara de colision
		self.mascara_col = pg.mask.from_surface(self.image)
	

	def update(self):
		self.animar()
		self.rect.x += self.vx
		vel = self.vx
		if ((self.rect.x - self.iniciox) > self.movimimiento) or ((self.rect.x - self.iniciox) < - self.movimimiento):
			self.vx *= -1