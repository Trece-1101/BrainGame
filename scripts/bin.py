def colision_plataforma(sprite, grupo, dir, jug):
		# metodo para detectar colision con cualquier plataforma. spritexollide any chequea
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
				saltando = True				
		if dir == "y":
			colision = pg.sprite.spritecollide(sprite, grupo, False)
			if colision:
				if sprite.vel.y > 0:
					# colision en el sentido y moviendose de arriba para abajo (cayendo y+)
					# mi posicion y (mi cabeza) tiene que ser el techa de la plataforma menos mi
					# altura (= mis pies)
					sprite.pos.y = colision[0].rect.top - sprite.rect.height
				if sprite.vel.y < 0:					
					# colision en el sentido y moviendose de abajo para arriba (saltando y-)
					# mi posicion de y (mi cabeza) tiene que ser el fondo de la plataforma
					sprite.pos.y = colision[0].rect.bottom
				if jug:
					saltando = False
				else:
					saltando = True
				#sprite.saltando = False
				sprite.vel.y = 0
				sprite.rect.y = sprite.pos.y