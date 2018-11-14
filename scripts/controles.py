import pygame as pg

def verificar_controles():
	joysticks = []

	for i in range(0, pg.joystick.get_count()):
			joysticks.append(pg.joystick.Joystick(i))
			joysticks[-1].init()
			print("Control detectado '",joysticks[-1].get_name(),"'")

	if len(joysticks) != 0:
		return True
	else:
		return False