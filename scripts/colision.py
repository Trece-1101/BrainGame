import pygame as pg


def colision_x(sprite, grupo):
    colision = pg.sprite.spritecollide(sprite, grupo, False)
    if colision:
        if sprite.vel.x >= 0:
            # colision en el sentido x moviendose de izq a derecha
            # mi posicion de x tiene que ser la izq de la plataforma menos el ancho
            # de mi rectangulo de colision
            sprite.pos.x = colision[0].rect.left - sprite.rect.width
        else:
            # colision en el sentido x moviendose de derecha a izquierda
            # mi posicion de x tiene que ser la derecha de la plataforma
            sprite.pos.x = colision[0].rect.right
        sprite.vel.x = 0
        sprite.rect.x = sprite.pos.x


def colision_y(sprite, grupo):
    colision = pg.sprite.spritecollide(sprite, grupo, False)
    if colision:
        if sprite.vel.y >= 0:
            # colision en el sentido y moviendose de arriba para abajo (cayendo y+)
            # mi posicion y (mi cabeza) tiene que ser el techa de la plataforma menos mi
            # altura (= mis pies)
            sprite.pos.y = colision[0].rect.top - sprite.rect.height
            for plataforma in colision:
                if plataforma.type == "trampa" and sprite.type == "player":
                    plataforma.pisada = True
        else:
            # colision en el sentido y moviendose de abajo para arriba (saltando y-)
            # mi posicion de y (mi cabeza) tiene que ser el fondo de la plataforma
            sprite.pos.y = colision[0].rect.bottom
        # si el sprite que colisiona es el del jugador volvemos su atributo saltando a False
        if sprite.type == "player":
            sprite.saltando = False
        sprite.vel.y = 0
        sprite.rect.y = sprite.pos.y


def colision_plataforma(sprite, grupo, dir):
    # funcion para detectar colision con cualquier plataforma. spritexollide chequea
    # colision entre un sprite (sprite del player o enemigo) vs una coleccion/grupo (game.plataformas)
    # False para que no desaparezca al colisionar
    # Devuelve una lista que contiene los sprites de un grupo que colisionan con el sprite
    # Esta como una funcion y no como parte de una clase ya que se requiere que dos clases distintas la
    # utilicen (player y un tipo de enemigo). Considerar crear una super clase y hacer herencia.
    # descomentar al final para entender
    if dir == "x":
        colision_x(sprite, grupo)
    elif dir == "y":
        colision_y(sprite, grupo)

    #print("direccion {0} -- colision {1} -- sprite {2} -- grupo {3}".format(dir, colision, sprite, grupo))
