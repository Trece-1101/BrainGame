# clase principal que almacena todo el juego
import pygame as pg
import os
from pathlib import Path
from scripts.parametros import *
from scripts.personajes import *
from scripts.tiles import *
from scripts.camara import *

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
		#pg.key.set_repeat(500, 100)

	def cargar_datos(self):
		# metodo para cargar datos desde archivos
		carpeta_mapas = Path("mapas")

		num = 0
		self.mapa = Mapa(carpeta_mapas / "mapa{}.txt".format(num))

	def eventos(self):
		# metodo que maneja inputs de teclado, todo lo relacionado a ingreso de usuario
		for evento in pg.event.get():
			if evento.type == pg.QUIT:
				self.quit()
			if evento.type == pg.KEYDOWN:
				if evento.key == pg.K_ESCAPE:
					self.quit()

	def dibujar_grilla(self):
		for x in range(0, ANCHO, TAMAÑO_TILE):
			pg.draw.line(self.pantalla, NEGRO, (x, 0), (x, ALTO))

		for y in range(0, ALTO, TAMAÑO_TILE):
			pg.draw.line(self.pantalla, NEGRO, (0, y), (ANCHO, y))

	def dibujar(self):
		# metodo que maneja el dibujo en pantalla de todas las cosas
		pg.display.set_caption("{:.2f}".format(self.FPSclock.get_fps()))
		self.pantalla.fill(CELESTE) # lleno la pantalla de fondo celeste
		self.dibujar_grilla()
		for sprite in self.sprites:
			# dibujo en pantalla todos los sprites			
			self.pantalla.blit(sprite.image, self.camara.offset(sprite))
					
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

	def dibujar_texto(self, texto, tamaño, color, x, y):
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
				elif tile == "P":
					self.player = PlayerOne(self, col, fila) # inicializo al player
				elif tile == "E":
					Enemigo(self, col, fila)

	def nuevo_juego(self):
		# cada vez que se inicia o reinicia el juego, no la ventana
		# creacion de grupos para manejar sprites mas eficientemente
		self.sprites = pg.sprite.LayeredUpdates() # grupo para todos los sprites, con capas
		self.plataformas = pg.sprite.Group()
		
		# instanciar el mapa
		self.mapear()	
		
		# instanciamos la camara
		self.camara = Camara(self.mapa.ancho, self.mapa.alto)

		# iniciamos el juego
		self.jugar()

	def update(self):
		# metodo principal que maneja colisiones, condiciones de victoria/derrota, spawns y re-spawns
		self.sprites.update()
		self.camara.update(self.player)		


	def jugar(self):
		# loop principal del juego, este metodo esta integrado por los metodos principales
		#pg.mixer.music.play(loops = -1) # musica principal del juego en loop infinito
		#self.jugando = True
		while self.jugando:			
			self.dt = self.FPSclock.tick(FPS) / 1000
			self.eventos()
			self.update()
			self.dibujar()
		pg.mixer.music.fadeout(800)


Game()