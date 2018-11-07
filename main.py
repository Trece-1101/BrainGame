# main para ejecutar el juego
from scripts.game import *

def main():
	g = Game() # creando una instancia de la clase juego
	while g.run:
		# mientras que el atributo run sea verdadero el juego se va a mostrar (la ventana)
		g.nuevo_juego() # este es el metodo que maneja todo el juego, desde aca se llama al juego nuevo
		g.run = g.game_over() # menu para decidir si terminar o reiniciar partida

if __name__ == "__main__":
	main()