'''Todos los creditos de la musica pertenecen a Juhani Junkala -- juhani.junkala@musician.org'''

# main para ejecutar el juego
from scripts.game import *
from scripts.parametros import *
from scripts.menus import *

def main():
	g = Game() # creando una instancia de la clase juego
	while g.run:
		# mientras que el atributo run sea verdadero el juego se va a mostrar (la ventana)
		#g.run = g.menu_principal() # menu principal, puede devolver false
		g.nuevo_juego() # este es el metodo que maneja todo el juego, desde aca se llama al juego nuevo
		g.run = g.game_over() # menu para decidir si terminar o reiniciar partida

if __name__ == "__main__":
	main()