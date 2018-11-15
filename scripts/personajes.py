import pygame as pg
from random import randrange, uniform, choice
from scripts.parametros import *

def colision_plataforma(sprite, grupo, dir):
		# funcion para detectar colision con cualquier plataforma. spritexollide chequea
		# colision entre un sprite (sprite del player o enemigo) vs una coleccion/grupo (game.plataformas)
		# False para que no desaparezca al colisionar
		# Devuelve una lista que contiene los sprites de un grupo que colisionan con el sprite
		# Esta como una funcion y no como parte de una clase ya que se requiere que dos clases distintas la
		# utilicen (player y un tipo de enemigo). Considerar crear una super clase y hacer herencia.
		# descomentar al final para entender
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
				# si el sprite que colisiona es el del jugador volvemos su atributo saltando a False
				if isinstance(sprite, PlayerOne):
					sprite.saltando = False
				sprite.vel.y = 0
				sprite.rect.y = sprite.pos.y

		#print("direccion {0} -- colision {1} -- sprite {2} -- grupo {3}".format(dir, colision, sprite, grupo))


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
		self.rect = self.image.get_rect()
		self.vel = vec2(0, 0)
		self.acel = vec2(0, 0)
		self.pos = vec2(x * TAMAÑO_TILE, y * TAMAÑO_TILE)
		self.saltando = False
		self.sentido = "D"
		self.stamina = PLAYER_STAMINA
		self.type = "player"
		self.col = 0
		self.fila = 0

	def cargar_imagenes(self):
		# usamos de imagenes el spritesheet cargado al iniciar el juego junto con el metodo
		# de la clase spritesheet

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
		# en este metodo animamos todos los movimientos. Las animaciones dependen de si el player
		# esta idle, caminando, corriendo o saltando

		# creamos un timer para actualizar los cuadros dada una cantidad de milisengudos que
		# viene desde parametros por ACTUALIZACION CUADROS y dependiendo lo que el player esta
		# haciendo (caminar, correr, idle) buscamos en la lista de sprites el cuadro (la formula
		# toma al cuadro siguiente al actual y modula por la longitud de la lista de cuadros para
		# dicha accion, de manera tal que si hay 5 cuadros y mi sumatoria va por el 12er cuadro actual
		# da como resultado el cuadro n°3 ((12+1) % 5) y si lo pensamos logicamente si mi lista tiene 5
		# cuadros y yo estoy por utilizar el 13ro quiere decir que es el cuadro 3 (5+5 = dos iteraciones + 3)

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

		# mascara de colision para poder hacer colisiones pixel perfect
		self.mascara_col = pg.mask.from_surface(self.image)	



	def saltar(self):
		# como el sprite del jugador no esta en colision real con el de la plataforma (estan separados
		# por un pixel) rapidamente bajamos dos pixeles para hacerla colision y los volvemos a subir
		self.rect.y += 2
		colision = pg.sprite.spritecollide(self, self.game.plataformas, False)
		self.rect.y -= 2
		if colision and not self.saltando:
			# si esta en colison y todavia no esta saltando, comenzamos el salto
			self.saltando = True
			self.vel.y = PLAYER_SALTO


	def control_salto(self):
		# en este metodo se hace el salto controlado, cuando soltemos la tecla espacio la si
		# la velocidad del salto aun no alcanzo la del corte, la eleva hasta esta, si ya la supero (con 
		# la funcion saltar) no pasa nada
		if self.saltando:
			if self.vel.y < CORTE_SALTO:
				self.vel.y = CORTE_SALTO

		# descomentar para entender
		# print(self.vel.y)

	def pad_salto(self):
		# si toco un pad de salto uso la velocidad de mi propio salto por un plus
		self.vel.y = PLAYER_SALTO * BOOST_PAD_SALTO


	def fisica_aceleracion(self):
		# en este metodo se controla todo lo que sean fisicas, se llama siempre que mueva al jugador
		self.acel.x += self.vel.x * PLAYER_FRICCION
		self.vel += self.acel

		# descomentar para tener una idea de como esta funcionando la fisica
		# y modificar los valores en parametros para cambiar comportamiento
		#print("acelX {0}".format(self.acel.x))
		#print("velX {0}".format(self.vel.x))
		#print("velY {0}".format(self.vel.y))

		# la posicion del jugador (que es un vector2) se calcula a traves de su velocidad multiplicada
		# por el delta del juego (asi es constante en cualquier maquina ya que es independiente de la velocidad
		# de los frames) a su vez la velocidad viene calculada por el vector de aceleracion y la constante de la
		# friccion. Luego de estos calculos "tiramos" al rectangulo del sprite (lo que mueve realmente el sprite)
		# dependiendo de esa posicion y de las coliciones (siempre hay que "mover" ese rectangulo por colisiones ultimo
		# o se pueden generar comportamientos extraños como meterse en las paredes)
		self.pos += self.vel * self.game.dt
		self.rect.x = self.pos.x
		colision_plataforma(self, self.game.plataformas, "x")
		self.rect.y = self.pos.y
		colision_plataforma(self, self.game.plataformas, "y")


	def acelerar(self):
		# metodo para cuando el jugador toca un item de acelerador, utiliza la aceleracion propia mas un plus
		# tener en cuenta si conviene siempre acelerar hacia la izquierda, la aceleracion hacia la derecha genera
		# comportamientos molestos. Solo hace falta cambiar en el sentido "I" el valor "-"
		if self.sentido == "D":
			self.acel.x = PLAYER_ACEL * BOOST_ACELERADOR
		elif self.sentido == "I":
			self.acel.x = -(PLAYER_ACEL * BOOST_ACELERADOR)

		self.fisica_aceleracion()

	def lastimar(self, danio):
		# metodo en desuso pero se deja por si en algun momento se le quiere volver a dar puntos de vida
		# al player. En este momento del desarrollo el daño viene dado por la quita de tiempo. Solo basta con 
		# agregar un atributo "vida" y descomentar
		pass
		#self.vida -= danio

	

	def update(self):
		self.animar()		
		self.acel = vec2(0, GRAVEDAD)

		# para hacer el respawn siempre arriba de una plataforma hay que chequear siempre que la vel sea 0
		# (quiere decir que esta en el piso) y tomar su pos en x (restandole un par de casilleros dependiendo
		# el sentido del jugador asi evitamos los bordes) y diviendolo por el tamaño del tile para transformarlo
		# en filas y columnas y poder pasarlo al mapeador

		if self.vel.y == 0:
			if self.sentido == "D":
				self.col = self.pos.x / TAMAÑO_TILE - 2
				self.fila = (self.pos.y / TAMAÑO_TILE) - 2
			elif self.sentido == "I":
				self.col = self.pos.x / TAMAÑO_TILE + 2
				self.fila = (self.pos.y / TAMAÑO_TILE) - 2

		# aca controlamos la teclas que se pueden spamear (izq, derecha y la aceleracion o dash)
		# el control de teclas del tipo KUP y KDOWN controlamos desde el flujo principal del juego
		# al igual que los sonidos porque de otra manera generaban comportamientos indeseados

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
		self.cargar_imagenes()
		self.image = self.cuadros_idle[0]
		self.transformar(self.image)
		self.rect = self.image.get_rect()
		self.vel = vec2(0, 0)
		self.acel = vec2(0, 0)
		self.pos = vec2(x, y) * TAMAÑO_TILE
		self.rect.center = self.pos
		self.acel = vec2(0, 0)
		self.vivo = True
		self.idle = True
		

	def transformar(self, imagen):
		# para que los personajes sean mas grandes que el player (el doble) escalamos todas las imagenes
		# al utilizarlas, para eso creamos este metodo y lo usamos cada vez que asignamos una imagen
		self.image = pg.transform.scale(imagen, (TAMAÑO_TILE_BOTARAÑA, TAMAÑO_TILE_BOTARAÑA))

	def cargar_imagenes(self):
		self.cuadros_idle = [self.game.spritesheet_araña.get_imagen(132, 396, 64, 64),
							self.game.spritesheet_araña.get_imagen(132, 330, 64, 64),
							self.game.spritesheet_araña.get_imagen(132, 264, 64, 64),
							self.game.spritesheet_araña.get_imagen(132, 198, 64, 64)]


		self.cuadros_caminar_d = [self.game.spritesheet_araña.get_imagen(0, 396, 64, 64),
								self.game.spritesheet_araña.get_imagen(0, 330, 64, 64),
								self.game.spritesheet_araña.get_imagen(0, 264, 64, 64),
								self.game.spritesheet_araña.get_imagen(0, 198, 64, 64)]	

		self.cuadros_caminar_i = [self.game.spritesheet_araña.get_imagen(0, 132, 64, 64),
								self.game.spritesheet_araña.get_imagen(66, 132, 64, 64),
								self.game.spritesheet_araña.get_imagen(66, 66, 64, 64),
								self.game.spritesheet_araña.get_imagen(66, 0, 64, 64)]

		self.cuadros_correr_d = [self.game.spritesheet_araña.get_imagen(198, 198, 64, 64),
								self.game.spritesheet_araña.get_imagen(198, 132, 64, 64),
								self.game.spritesheet_araña.get_imagen(198, 66, 64, 64),
								self.game.spritesheet_araña.get_imagen(198, 0, 64, 64)]

		self.cuadros_correr_ii = [self.game.spritesheet_araña.get_imagen(264, 0, 64, 64),
								self.game.spritesheet_araña.get_imagen(198, 396, 64, 64),
								self.game.spritesheet_araña.get_imagen(198, 330, 64, 64),
								self.game.spritesheet_araña.get_imagen(198, 264, 64, 64)]

		self.cuadros_correr_i = []
		for cuadro in self.cuadros_correr_ii:
			self.cuadros_correr_i.append(pg.transform.flip(cuadro, True, False))				

		
		self.cuadro_muerte = self.game.spritesheet_araña.get_imagen(132, 66, 64, 64)


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

		self.cuadro_muerte.set_colorkey(NEGRO)
		
		


	def animar(self):
		# el metodo de animacion funciona igual que en el player solo cambian ciertos aspectos como
		# el estar vivo o no, o en idle o no
		if not self.vivo:
			self.image = self.cuadro_muerte
			self.transformar(self.image)
		else:
			este_instante = pg.time.get_ticks()
			if self.idle:
				if este_instante - self.ultimo_update > ACTUALIZACION_CUADROS:
					self.ultimo_update = este_instante
					self.cuadro_actual = (self.cuadro_actual + 1) % len(self.cuadros_idle)
					self.image = self.cuadros_idle[self.cuadro_actual]
					self.transformar(self.image)
			else:
				if este_instante - self.ultimo_update > ACTUALIZACION_CUADROS:
					self.ultimo_update = este_instante
					self.cuadro_actual = (self.cuadro_actual + 1) % len(self.cuadros_correr_d)
					if self.vel.x > 0 and self.vel.x <= 500:
						#print(self.vel.x)
						self.image = self.cuadros_caminar_d[self.cuadro_actual]
						self.transformar(self.image)				
					elif self.vel.x > 500:
						#print(self.vel.x)
						self.image = self.cuadros_correr_d[self.cuadro_actual]
						self.transformar(self.image)
					elif self.vel.x < 0 and self.vel.x >= -500:
						#print(self.vel.x)
						self.image = self.cuadros_caminar_i[self.cuadro_actual]
						self.transformar(self.image)
					elif self.vel.x < -500:
						#print(self.vel.x)
						self.image = self.cuadros_correr_i[self.cuadro_actual]
						self.transformar(self.image)

		# mascara de colision
		self.mascara_col = pg.mask.from_surface(self.image)

	def morir(self):
		# cuando se muere lo dejamos quieto y cambiamos su cuadro
		self.vel.x = 0
		self.vivo = False
		self.animar()



	def update(self):
		self.animar()
		self.acel = vec2(0, GRAVEDAD)

		if self.pos.y > 1800:
			self.kill()

		# para el comportamiento de la botaraña queremos que este en idle hasta que "detecte" al
		# jugador, para eso creamos una variable y calculamos constantemente la distancia entre ella y
		# el jugador, como importa la distancia en X calculamos el radio de deteccion sobre ese eje y sobre
		# el Y solo calculamos que mientras este en +/-70 (casi sobre el mismo eje X) se mueva
		# La araña se mueve de una manera similar al jugador pero sin friccion, por lo cual le cuesta mas
		# frenar y "patina"
		# descomentar para entender como esta funcionando la deteccion

		dist_obj = self.pos - self.game.player.pos
		#print(self.pos)
		#print(dist_obj[1])
		if (abs(dist_obj[0]) < choice(RADIO_DETECCION)) and (abs(dist_obj[1]) < 70) and self.vivo:
			#print("detectado")
			if dist_obj[0] > 0:             
				self.acel.x -= choice(VEL_BOT)
			else:
				self.acel.x += choice(VEL_BOT)
			self.idle = False
		else:
			self.acel.x = 0				
			#print("no detectado")

		self.vel += self.acel
		self.pos += self.vel * self.game.dt
		self.rect.x = self.pos.x
		colision_plataforma(self, self.game.plataformas, "x")
		self.rect.y = self.pos.y
		colision_plataforma(self, self.game.plataformas, "y")
		if self.vel.x != 0:
			self.idle = False
		else:
			self.idle = True
		


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
		self.transformar(self.image)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TAMAÑO_TILE
		self.rect.y = y * TAMAÑO_TILE
		# puede iniciar moviendose a izq
		# o a derecha 50/50 prob		
		self.vx = choice(VEL_AV)
		if randrange(100) < 50:
			self.vx *= -1
		self.iniciox = self.rect.x
		self.movimimiento = choice(MOV_AV)
		self.vivo = True

	def transformar(self, imagen):
		self.image = pg.transform.scale(imagen, (64, 64))

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
			self.transformar(self.image)
		else:
			if este_instante - self.ultimo_update > ACTUALIZACION_CUADROS_ENEMIGOS:
					self.ultimo_update = este_instante
					self.cuadro_actual = (self.cuadro_actual + 1) % len(self.cuadros_correr_d)
					if self.vx != 0:				
						if self.vx > 0:
							self.image = self.cuadros_correr_d[self.cuadro_actual]
							self.transformar(self.image)
						else:
							self.image = self.cuadros_correr_i[self.cuadro_actual]
							self.transformar(self.image)
					elif self.vx == 0:
						self.image = self.cuadros_idle[self.cuadro_actual]
						self.transformar(self.image)

		# mascara de colision
		self.mascara_col = pg.mask.from_surface(self.image)
	

	def update(self):
		# el antivirus se mueve de manera igual para cada instancia pero seguramente de manera
		# distinta entre instancias. Su rango y velocidad de movimiento viene dado por el choice de
		# dos listas (una para cada cosa). En este metodo lo que calculamos es que al llegar al limite
		# de su rango de movimiento, se vuelva en la direccion contraria.
		# se podria considerar que se tome un momento en idle al centro del rango de movimiento
		self.animar()
		self.rect.x += self.vx
		vel = self.vx
		if ((self.rect.x - self.iniciox) > self.movimimiento) or ((self.rect.x - self.iniciox) < - self.movimimiento):
			self.vx *= -1