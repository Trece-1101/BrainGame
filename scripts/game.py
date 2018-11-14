# clase principal que almacena todo el juego
import pygame as pg
import os
import random
from pathlib import Path
from scripts.parametros import *
from scripts.personajes import *
from scripts.tiles import *
from scripts.camara import *
from scripts.item import *
from scripts.menus import *
from scripts.controles import *
from scripts.fondos import *

# GUI
def gui(pantalla, x, y, pct, color_lleno, color_medio, color_vacio, texto):
	if pct < 0:
		pct = 0
	elif pct > 100:
		pct = 100
	ancho = 100
	alto = 40
	relleno = pct * ancho
	borde = pg.Rect(x, y, ancho, alto)
	relleno_rect = pg.Rect(x, y, relleno, alto)
	if pct >= 0.8:
		color = color_lleno
	elif pct > 0.3 and pct < 0.8:
		color = color_medio
	else:
		color = color_vacio
	pg.draw.rect(pantalla, color, relleno_rect)
	pg.draw.rect(pantalla, BLANCO, borde, 2)
	dibujar_texto(pantalla, texto, 18, NEGRO, x + 55, y + 45)


class Game():
	def __init__(self):
		# inicializar el juego
		pg.init() # inicializo el modulo pygame, obligatorio
		pg.mixer.init() # modulo de sonido
		os.environ['SDL_VIDEO_CENTERED'] = '1' # centro de la pantalla
		self.pantalla = pg.display.set_mode((ANCHO, ALTO)) # tamaño de la ventana del juego
		pg.display.set_caption(TITULO) # titulo que aparece en la ventana
		self.FPSclock = pg.time.Clock()
		#self.run = True # bool para determinar si el juego (la ventana) va a seguir abierta
		iniciar = menu(self.pantalla, self.FPSclock)
		self.run = iniciar[0]	
		#self.run = menu_principal(self.pantalla, self.FPSclock)
		self.jugando = True # bool para determinar el game_over o no	
		self.fuente = pg.font.match_font(FUENTE)
		#self.fondos = []	
		self.cargar_datos()
		self.pausado = False
		self.tiempo_inicio = pg.time.get_ticks()
		self.tiempo_final = TIEMPO_NIVEL * iniciar[1]
		self.control_tiempo = 0		
		self.c_niveles = 1
		if verificar_controles():
			self.j = pg.joystick.Joystick(0)
		

	def cargar_datos(self):
		# metodo para cargar datos desde archivos
		# imagenes			

		# spritesheet_completo			
		self.spritesheet = Spritesheet(os.path.join(CARPETA_IMAGENES, SPRITESHEET))

		# fondos
		'''self.fondos = []
		for f in FONDOS:
			self.fondos.append(os.path.join(CARPETA_IMAGENES, FONDOS[f]))

		self.fondo = random.choice(self.fondos)	'''

		# sonidos
		self.carpeta_sonidos = Path("sfx")

		# acciones
		self.sonido_salto = pg.mixer.Sound(os.path.join(self.carpeta_sonidos, SFX["salto"]))		
		self.sonido_lastimado = pg.mixer.Sound(os.path.join(self.carpeta_sonidos, SFX["lastimado"]))
		self.sonido_muerteNPC = pg.mixer.Sound(os.path.join(self.carpeta_sonidos, SFX["lastimados_npc"]))
		self.sonido_portal = pg.mixer.Sound(os.path.join(self.carpeta_sonidos, SFX["portal"]))
		# tiempo
		self.sonido_tiempo_limite = pg.mixer.Sound(os.path.join(self.carpeta_sonidos, SFX["tiempo_limite"]))		
		# items
		self.sonido_salto_boost = pg.mixer.Sound(os.path.join(self.carpeta_sonidos, SFX["salto_boost"]))
		self.sonido_boost = pg.mixer.Sound(os.path.join(self.carpeta_sonidos, SFX["boost"]))
		self.sonido_combotron = pg.mixer.Sound(os.path.join(self.carpeta_sonidos, SFX["combotron"]))
		self.sonido_tiempotron = pg.mixer.Sound(os.path.join(self.carpeta_sonidos, SFX["tiempotron"]))
	

		# crear una secuencia de 10 niveles aleatorios
		# 3 faciles
		# 3 medios
		# 3 dificilesf
		# 1 final

		self.sec_niveles = []
		x = 0
		while x < 3:
			nivel = random.randint(1, 5)
			if nivel not in self.sec_niveles:
				self.sec_niveles.append(nivel)	
				x += 1
		x = 0		

		while x < 3:
			nivel = random.randint(6, 10)
			if nivel not in self.sec_niveles:
				self.sec_niveles.append(nivel)	
				x += 1
		x = 0	

		while x < 3:
			nivel = random.randint(11, 15)
			if nivel not in self.sec_niveles:
				self.sec_niveles.append(nivel)	
				x += 1

		nivel = random.randint(16, 17)
		self.sec_niveles.append(nivel)
		#print(self.sec_niveles)
				

	def cargar_nivel(self, nivel):
		carpeta_mapas = Path("mapas")
		#self.mapa = Mapa(carpeta_mapas / "nivel{}.txt".format(nivel))
		self.mapa = Mapa(carpeta_mapas / "nivel4.txt")
		#print(nivel)
		self.mapear()

	def musica_random(self):
		pg.mixer.music.load(os.path.join(self.carpeta_sonidos, random.choice(SFX["musica"])))
		pg.mixer.music.play(loops=-1)


	def eventos(self):
		# metodo que maneja inputs de teclado, todo lo relacionado a ingreso de usuario
		for evento in pg.event.get():
			if evento.type == pg.QUIT:
				self.quit()
			if evento.type == pg.KEYDOWN:
				if evento.key == pg.K_ESCAPE:
					sys.exit(0)
				if evento.key == pg.K_SPACE:
					self.sonido_salto.play()
					self.player.saltar()
				if evento.key == pg.K_LSHIFT:
					self.sonido_boost.play()
				if evento.key == pg.K_p:
					self.pausado = not self.pausado
			if evento.type == pg.KEYUP:
				if evento.key == pg.K_SPACE:
					self.player.control_salto()
			

	def dibujar_grilla(self):
		for x in range(0, ANCHO, TAMAÑO_TILE):
			pg.draw.line(self.pantalla, NEGRO, (x, 0), (x, ALTO))

		for y in range(0, ALTO, TAMAÑO_TILE):
			pg.draw.line(self.pantalla, NEGRO, (0, y), (ANCHO, y))


	def dibujar(self):
		# metodo que maneja el dibujo en pantalla de todas las cosas
		pg.display.set_caption("{:.2f}".format(self.FPSclock.get_fps()))


		self.pantalla.blit(self.img_fondo, self.img_fondo_rect)
		
		#self.pantalla.fill(CELESTE) # lleno la pantalla de fondo celeste
		#fondo = pygame.image.load(choice(self.fondos)).convert()

		pct_scan = self.control_tiempo / self.tiempo_final
		if pct_scan > 0.9:
			self.sonido_tiempo_limite.play()
		pct_scan_mod = str(round(pct_scan * 100, 1))
		pct_stamina = self.player.stamina / 100
		gui(self.pantalla, 50, 10, pct_scan, ROJO, AMARILLO, VERDE, "Escaneando {0} %".format(pct_scan_mod))
		gui(self.pantalla, 50, 100, pct_stamina, VERDE, AMARILLO, ROJO, "Stamina {0}".format(self.player.stamina))

		#descomentar para ver la grilla
		#self.dibujar_grilla()

		

		for sprite in self.sprites:
			# por cada sprite que exista en el grupo principal de sprites
			self.pantalla.blit(sprite.image, self.camara.aplicar_camara(sprite))
	


		if self.pausado:		
			self.pantalla.blit(pantalla_pausa(self.pantalla), (0,0))
			
					
		pg.display.flip()


	def mapear(self, colPlayer = 0, filaPlayer = 0):
		# metodo para tomar un .txt y convertirlo en mapa
		# cargo y creo el mapa
		for fila, tiles in enumerate(self.mapa.data_mapa):
			for col, tile in enumerate(tiles):
				if tile == "1":
					PlataformaCentro(self, col, fila)
				elif tile == "0":
					PlataformaExtremoI(self, col, fila)
				elif tile == "2":
					PlataformaExtremoD(self, col, fila)
				elif tile == "5":
					PlataformaTrampaCentro(self, col, fila)
				elif tile == "4":
					PlataformaTrampaI(self, col, fila)
				elif tile == "6":
					PlataformaTrampaD(self, col, fila)
				elif tile == "X":
					Portal(self, col, fila)
				elif tile == "P":
					if colPlayer == 0 and filaPlayer == 0:
						self.player = PlayerOne(self, col, fila) # inicializo al player
						print(self.player.pos.x , " -- ", self.player.pos.y)
						print(col, fila)
					else:
						self.player = PlayerOne(self, colPlayer, filaPlayer)
						self.player.stamina = self.respawn_stamina		
				elif tile == "B":
					Botaraña(self, col, fila)
				elif tile == "V":
					Antivirus(self, col, fila)				
				elif tile == "A":
					if random.randrange(100) < PROB_ACELERADOR:
						Acelerador(self, col, fila)
				elif tile == "S":
					if random.randrange(100) < PROB_PAD_SALTO:
						PadSalto(self, col, fila)
				elif tile == "C":
					if random.randrange(100) < PROB_COMBOTRON:
						Combotron(self, col, fila)
				elif tile == "T":
					if random.randrange(100) < PROB_TIEMPOTRON:
						Tiempotron(self, col, fila)

	
	def reiniciar_sprites(self):
		self.sprites = pg.sprite.LayeredUpdates() # grupo para todos los sprites, con capas
		self.plataformas = pg.sprite.Group()
		self.items = pg.sprite.Group()
		self.antivirus = pg.sprite.Group()
		self.bots = pg.sprite.Group()
		self.portales = pg.sprite.Group()
		self.fondos = pg.sprite.Group()


	def nuevo_juego(self):
		# cada vez que se inicia o reinicia el juego, no la ventana
		# creacion de grupos para manejar sprites mas eficientemente
		self.reiniciar_sprites()

		# musica
		self.musica_random()

		# fondo
		self.fondo = os.path.join(CARPETA_IMAGENES, random.choice(FONDO))
		self.img_fondo = pg.image.load(self.fondo)
		self.img_fondo_rect = self.img_fondo.get_rect()	
			
		# instanciar el mapa
		self.cargar_nivel(self.sec_niveles[0])

		
		# instanciamos la camara con los valores del mapa que salen en la carga de datos
		self.camara = Camara(self,self.mapa.ancho, self.mapa.alto)

		# iniciamos el juego
		self.jugar()

	def respawn(self):
		self.reiniciar_sprites()
		self.mapear(self.player.col, self.player.fila)


	def update(self):
		# metodo principal que maneja colisiones, condiciones de victoria/derrota, spawns y re-spawns
		self.sprites.update()
		# la camara sigue al jugador
		self.camara.update(self.player)


		self.control_tiempo = pg.time.get_ticks() - self.tiempo_inicio
		#print(self.control_tiempo)
		#print(self.tiempo_final)
		if self.tiempo_final - self.control_tiempo <= 0:
			#print("tiempo: {0} -- tiempofinal: {1} -- timeout".format(self.control_tiempo, self.tiempo_final))
			self.jugando = False


		if self.player.pos.y > 2000:
			#print("caida")
			self.respawn_stamina = self.player.stamina
			self.respawn()



		# colision con el portal para pasar de nivel
		colision_portal = pg.sprite.spritecollide(self.player, self.portales, False)
		if colision_portal:
			for portal in colision_portal:
				if abs(self.player.rect.centerx - portal.rect.centerx) < 20:
					if self.c_niveles < 10:
						#print("niveles_jugados {0}".format(self.c_niveles))
						self.sonido_portal.play()
						self.c_niveles += 1
						self.tiempo_final += TIEMPO_NIVEL
						self.sec_niveles.pop(0)				
						self.nuevo_juego()
					else:
						print("ganaste")
						sys.exit(0)


		# colision con botaraña, quita segundos
		colision_enemigo_bot = pg.sprite.spritecollide(self.player, self.bots, False)
		for enemigo in colision_enemigo_bot:
			if enemigo.type == "BotAraña":
				if enemigo.vivo:					
					self.sonido_lastimado.play()
					enemigo.morir()
					self.tiempo_final -= DANIO_BOT			


		# colision con el antivirus, segundos
		colision_enemigo_av = pg.sprite.spritecollide(self.player, self.antivirus, False, pg.sprite.collide_mask)
		for enemigo in colision_enemigo_av:		
			if enemigo.type == "Antivirus":
				if enemigo.vivo == True:
					self.sonido_lastimado.play()
					enemigo.morir()									
					self.tiempo_final -= DANIO_AV

		# colision entre el anvivirus y la botaraña, muere el antivirus
		for av in self.antivirus:
			colision = pg.sprite.spritecollide(av, self.bots, False)
			if colision and av.vivo:
				self.sonido_muerteNPC.play()
				av.morir()		


		# colision con los distintos items
		colision_item = pg.sprite.spritecollide(self.player, self.items, True)
		for item in colision_item:
			if item.type == "acelerar":
				self.sonido_boost.play()
				self.player.acelerar()
			elif item.type == "saltar":
				self.sonido_salto_boost.play()
				self.player.pad_salto()
			elif item.type == "combotron":
				self.sonido_combotron.play()
				self.player.stamina += BOOST_COMBOTRON
				if self.player.stamina > 100:
					self.player.stamina = 100
			elif item.type == "tiempotron":
				self.sonido_tiempotron.play()
				self.tiempo_final += BOOST_TIEMPOTRON



	def game_over(self):
		res = menu_game_over(self.pantalla, self.FPSclock)
		return res		



	def jugar(self):
		# loop principal del juego, este metodo esta integrado por los metodos principales
		pg.mixer.music.play(loops = -1) # musica principal del juego en loop infinito
		while self.jugando:			
			self.dt = self.FPSclock.tick(FPS) / 1000
			self.eventos()
			if not self.pausado:
				self.update()			
			self.dibujar()
		pg.mixer.music.fadeout(800)
		