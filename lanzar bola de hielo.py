import pygame
import sys
import time

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Cargar imagen del proyectil
proyectil_img = pygame.image.load("Bolita de hielo.png").convert_alpha()
# cargar imagen del jugador
heroe = pygame.image.load("Michael.png").convert_alpha()
#cargar imagen del enemigo
enemigo = pygame.image.load("perrito.png").convert_alpha()

# Posición inicial del jugador
jugador_x, jugador_y = 100, HEIGHT // 2
velocidad_jugador = 5

# Barra de energía
energia_max = 100
energia = energia_max
costo_proyectil = 5

# Recarga de energía
recarga_espera = 3  # segundos
recarga_velocidad = 1  # puntos por frame
ultimo_disparo = None

# Lista para proyectiles activos
proyectiles = []

class Proyectil:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 10

    def mover(self):
        self.x += self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(proyectil_img, (self.x, self.y))

def dibujar_barra_energia(pantalla, energia, energia_max):
    barra_ancho = 200
    barra_alto = 20
    x, y = 20, 20
    # Fondo de la barra
    pygame.draw.rect(pantalla, (100, 100, 100), (x, y, barra_ancho, barra_alto))
    # Barra de energía actual
    energia_actual_ancho = int(barra_ancho * (energia / energia_max))
    pygame.draw.rect(pantalla, (0, 200, 255), (x, y, energia_actual_ancho, barra_alto))
    # Borde
    pygame.draw.rect(pantalla, (255, 255, 255), (x, y, barra_ancho, barra_alto), 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Lanzar proyectil con tecla "E" solo si hay energía suficiente
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and energia >= costo_proyectil:
                proyectiles.append(Proyectil(jugador_x, jugador_y))
                energia -= costo_proyectil
                ultimo_disparo = time.time()

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        jugador_x -= velocidad_jugador
    if keys[pygame.K_RIGHT]:
        jugador_x += velocidad_jugador
    if keys[pygame.K_UP]:
        jugador_y -= velocidad_jugador
    if keys[pygame.K_DOWN]:
        jugador_y += velocidad_jugador

    # Limitar movimiento dentro de la pantalla
    jugador_x = max(0, min(WIDTH - heroe.get_width(), jugador_x))
    jugador_y = max(0, min(HEIGHT - heroe.get_height(), jugador_y))

    # Recargar energía si han pasado 3 segundos sin disparar
    if ultimo_disparo is not None:
        if time.time() - ultimo_disparo >= recarga_espera and energia < energia_max:
            energia += recarga_velocidad
            energia = min(energia, energia_max)
    else:
        # Si nunca se ha disparado, recargar normalmente
        if energia < energia_max:
            energia += recarga_velocidad
            energia = min(energia, energia_max)

    screen.fill((30, 30, 30))
    # Dibujar jugador con sprite
    screen.blit(heroe, (jugador_x, jugador_y))

    # Dibujar barra de energía
    dibujar_barra_energia(screen, energia, energia_max)

    # Mover y dibujar proyectiles
    for proyectil in proyectiles[:]:
        proyectil.mover()
        proyectil.dibujar(screen)
        # Eliminar proyectil si sale de la pantalla
        if proyectil.x > WIDTH:
            proyectiles.remove(proyectil)

    pygame.display.flip()
    clock.tick(60)