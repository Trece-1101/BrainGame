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

# GUI
def timer(sup, x, y, pct):
	if pct < 0:
		pct = 0
	ancho = 100
	alto = 20
	relleno = pct * ancho
	borde = pg.Rect(x, y, ancho, alto)
	relleno_rect = pg.Rect(x, y, relleno, alto)
	if pct >= 0.8:
		color = ROJO
	elif pct > 0.3 and pct < 0.8:
		color = AMARILLO
	else:
		color = VERDE
	pg.draw.rect(sup, color, relleno_rect)
	pg.draw.rect(sup, BLANCO, borde, 2)



class Game():
	def __init__(self):
		# inicializar el juego
		pg.init() # inicializo el modulo pygame, obligatorio
		pg.mixer.init() # modulo de sonido
		os.environ['SDL_VIDEO_CENTERED'] = '1' # centro de la pantalla
		self.pantalla = pg.display.set_mode((ANCHO, ALTO)) # tamaño de la ventana del juego
		pg.display.set_caption(TITULO) # titulo que aparece en la ventana
		self.FPSclock = pg.time.Clock()
		self.run = True # bool para determinar si el juego (la ventana) va a seguir abierta
		self.jugando = True # bool para determinar el game_over o no
		self.fuente = pg.font.match_font(FUENTE)
		self.cargar_datos()
		self.pausado = False
		self.tiempo_final = TIEMPO_NIVEL
		self.control_tiempo = 0
		self.nivel = 3

	def cargar_datos(self):
		# metodo para cargar datos desde archivos
		self.pantalla_pausa = pg.Surface(self.pantalla.get_size()).convert_alpha()
		self.pantalla_pausa.fill((0, 0, 0, 180))

		carpeta_player = Path("gfx/Brain")
		carpeta_enemigos = Path("gfx/enemigos")
		self.carpeta_fondos = Path("gfx/fondos")
		carpeta_gfx = Path("gfx")

		#self.img_fondos = []
		#for i in range(1, 4):
		#	self.img_fondos.append(pg.image.load(os.path.join(carpeta_fondos, "{0}.png".format(i))))		

		self.img_av_idle = pg.image.load(os.path.join(carpeta_enemigos, IMG_ENEMIGOS["av_idle"])).convert_alpha()
		self.img_av_idle = pg.transform.scale(self.img_av_idle, (TAMAÑO_TILE, TAMAÑO_TILE))
		self.img_av_run1 = pg.image.load(os.path.join(carpeta_enemigos, IMG_ENEMIGOS["av_run1"])).convert_alpha()
		self.img_av_run1 = pg.transform.scale(self.img_av_run1, (TAMAÑO_TILE, TAMAÑO_TILE))
		self.img_av_muerto = pg.transform.rotate(self.img_av_idle, 180)
		#self.img_bot_idle = pg.image.load(os.path.join(carpeta_enemigos, IMG_ENEMIGOS["bot_idle"])).convert_alpha()
		#self.img_bot_idle = pg.image.load(os.path.join(carpeta_enemigos, IMG_ENEMIGOS["prueba"])).convert_alpha()
		self.img_virus = pg.image.load(os.path.join(carpeta_enemigos, IMG_ENEMIGOS["prueba2"])).convert_alpha()
		self.img_virus = pg.transform.scale(self.img_virus, (TAMAÑO_TILE, TAMAÑO_TILE))
		self.spritesheet_bot = Spritesheet(os.path.join(carpeta_gfx, SPRITESHEETS["bot"]))
		self.spritesheet_brain = Spritesheet(os.path.join(carpeta_player, SPRITESHEET_BRAIN))
		

	def cargar_nivel(self):
		carpeta_mapas = Path("mapas")
		self.mapa = Mapa(carpeta_mapas / "mapa{}.txt".format(self.nivel))
		self.mapear()


	def eventos(self):
		# metodo que maneja inputs de teclado, todo lo relacionado a ingreso de usuario
		for evento in pg.event.get():
			if evento.type == pg.QUIT:
				self.quit()
			if evento.type == pg.KEYDOWN:
				if evento.key == pg.K_ESCAPE:
					self.quit()
				if evento.key == pg.K_SPACE:
					self.player.saltar()
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
		
		self.pantalla.fill(CELESTE) # lleno la pantalla de fondo celeste

		timer(self.pantalla, 50, 10, self.control_tiempo / self.tiempo_final)

		#descomentar para ver la grilla
		#self.dibujar_grilla()

			
		for sprite in self.sprites:
			# por cada sprite que exista en el grupo principal de sprites
			self.pantalla.blit(sprite.image, self.camara.aplicar_camara(sprite))
	

		if self.pausado:
			self.pantalla.blit(self.pantalla_pausa, (0, 0))
			self.dibujar_texto("Paused", 22, ROJO, MITAD_ANCHO, MITAD_ALTO)
					
		pg.display.flip()

	def stop(self):
		# metodo para esperar el input de usuario en pantalla principal y de game_over
		esperar = True
		while esperar:
			self.FPSclock.tick(FPS)
			for evento in pg.event.get():
				if evento.type == pg.QUIT:
					esperar = False
					run = False
				if evento.type == pg.KEYUP:
					if evento.key == pg.K_ESCAPE:
						esperar = False
						run = False
					else:
						esperar = False
						run = True

		return run

	def menu_principal(self):
		# pantalla de menu principal
		#pg.mixer.music.play(loops = -1)
		self.pantalla.fill(CELESTE)
		self.dibujar_texto(TITULO, 48, BLANCO, MITAD_ANCHO, ALTO / 4)
		#self.dibujar_texto("Puntaje maximos: " + str(self.max_puntaje), 22, BLANCO, MITAD_ANCHO, ALTO * 1/3)
		self.dibujar_texto("Flechas para mover, espacio para saltar", 22, BLANCO, MITAD_ANCHO, MITAD_ALTO)
		self.dibujar_texto("Presione una tecla para continuar", 22, BLANCO, MITAD_ANCHO, ALTO * 3/4)
		pg.display.flip()
		run = self.stop()
		return run

	def game_over(self):
		# pantalla de menu para volver a jugar
		self.quit()

	def dibujar_texto(self, texto, tamaño, color, x, y, align="topleft"):
		# metodo para recibir un string y dibujarlo en pantalla
		font = pg.font.Font(self.fuente, tamaño)
		texto_surface = font.render(texto, True, color)
		texto_rect = texto_surface.get_rect()
		texto_rect.midtop = (x, y)
		self.pantalla.blit(texto_surface, texto_rect)	

	def mapear(self):
		# metodo para tomar un .txt y convertirlo en mapa
		# cargo y creo el mapa
		for fila, tiles in enumerate(self.mapa.data_mapa):
			for col, tile in enumerate(tiles):
				if tile == "1":
					Plataforma(self, col, fila)
				elif tile == "2":
					PlataformaTrampa(self, col, fila)
				elif tile == "X":
					Portal(self, col, fila)
				elif tile == "P":
					self.player = PlayerOne(self, col, fila) # inicializo al player				
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





	def nuevo_juego(self):
		# cada vez que se inicia o reinicia el juego, no la ventana
		# creacion de grupos para manejar sprites mas eficientemente
		self.sprites = pg.sprite.LayeredUpdates() # grupo para todos los sprites, con capas
		self.plataformas = pg.sprite.Group()
		self.items = pg.sprite.Group()
		self.antivirus = pg.sprite.Group()
		self.bots = pg.sprite.Group()
		self.portales = pg.sprite.Group()
		self.fondos = pg.sprite.Group()
		
		# instanciar el mapa
		#self.mapear()
		self.cargar_nivel()
		
		# instanciamos la camara con los valores del mapa que salen en la carga de datos
		self.camara = Camara(self,self.mapa.ancho, self.mapa.alto)

		# iniciamos el juego
		self.jugar()

	def update(self):
		# metodo principal que maneja colisiones, condiciones de victoria/derrota, spawns y re-spawns
		self.sprites.update()
		# la camara sigue al jugador
		self.camara.update(self.player)

		#print(self.player.pos.y)

		self.control_tiempo = pg.time.get_ticks()
		#print(self.control_tiempo)
		if self.tiempo_final - self.control_tiempo <= 0:
			print("tiempo: {0} -- tiempofinal: {1} -- timeout".format(self.control_tiempo, self.tiempo_final))
			self.jugando = False

		if self.player.pos.y > 2000:
			print("caida")
			self.nuevo_juego()

		colision_portal = pg.sprite.spritecollide(self.player, self.portales, False)
		if colision_portal:
			for portal in colision_portal:
				if abs(self.player.rect.centerx - portal.rect.centerx) < 20:
					self.nivel += 1
					self.tiempo_final += TIEMPO_NIVEL					
					self.nuevo_juego()

		colision_enemigo_bot = pg.sprite.spritecollide(self.player, self.bots, True, pg.sprite.collide_mask)
		for enemigo in colision_enemigo_bot:
			if enemigo.type == "BotAraña":
				if enemigo.vivo:
					self.player.lastimar(DANIO_BOT)			


		colision_enemigo_av = pg.sprite.spritecollide(self.player, self.antivirus, False, pg.sprite.collide_mask)
		for enemigo in colision_enemigo_av:		
			if enemigo.type == "Antivirus":
				if enemigo.vivo == True:
					self.player.lastimar(DANIO_AV)

		if self.player.vida <= 0:
			#pg.time.wait(2000)
			self.jugando = False

		for av in self.antivirus:
			colision = pg.sprite.spritecollide(av, self.bots, False)
			if colision:
				av.morir()		


		colision_item = pg.sprite.spritecollide(self.player, self.items, True)
		for item in colision_item:
			if item.type == "acelerar":
				#self.sfx_boost.play()
				self.player.acelerar()
			elif item.type == "saltar":
				# insertar sonido
				self.player.pad_salto()			


	def jugar(self):
		# loop principal del juego, este metodo esta integrado por los metodos principales
		#pg.mixer.music.play(loops = -1) # musica principal del juego en loop infinito
		#self.jugando = True
		while self.jugando:			
			self.dt = self.FPSclock.tick(FPS) / 1000
			self.eventos()
			if not self.pausado:
				self.update()			
			self.dibujar()
		pg.mixer.music.fadeout(800)
		self.game_over()


Game()