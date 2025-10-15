import pygame
import time
import random

# 1. Inicializar Pygame
pygame.init()

# 2. Configurar la pantalla
fuente = pygame.font.Font(None, 36)
ancho_pantalla = 1550
alto_pantalla = 810
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("vs the demon")

# 3. Cargar el sprite
try:
    heroe_imagen = pygame.image.load("Michael.png")
    enemy_imagen = pygame.image.load("Perrito.png")
    calle_imagen = pygame.image.load("la  calle laaaaarga V2.jpg")
    calle_imagen = pygame.transform.scale(calle_imagen, (ancho_pantalla, alto_pantalla))
except pygame.error as e:
    print(f"Error al cargar la imagen: {e}")
    pygame.quit()
    exit()

# 4. Obtener el rectángulo de la imagen para posicionarla
heroe_rect = heroe_imagen.get_rect()
heroe_rect.center = (ancho_pantalla // 2, alto_pantalla // 2)

# Crear varios enemigos en los bordes
cantidad_enemigos = 5
enemigos = []
for _ in range(cantidad_enemigos):
    rect = enemy_imagen.get_rect()
    borde = random.choice(['top', 'bottom', 'left', 'right'])
    if borde == 'top':
        rect.x = random.randint(0, ancho_pantalla - rect.width)
        rect.y = 0
    elif borde == 'bottom':
        rect.x = random.randint(0, ancho_pantalla - rect.width)
        rect.y = alto_pantalla - rect.height
    elif borde == 'left':
        rect.x = 0
        rect.y = random.randint(0, alto_pantalla - rect.height)
    elif borde == 'right':
        rect.x = ancho_pantalla - rect.width
        rect.y = random.randint(0, alto_pantalla - rect.height)
    enemigos.append(rect)

#definir velocidad del personaje
velocidad = 1
velocidad_enemigo = 0.0009
nivel = int(velocidad_enemigo)

# 5. Bucle principal del juego
corriendo = True
while corriendo:
    nivel = int(velocidad_enemigo)
    if nivel == 10:
        corriendo = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
    teclas = pygame.key.get_pressed()

    #movimiento del personaje principal
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_a]:
        heroe_rect.x -= velocidad
        velocidad_enemigo += 0.0009
    if teclas[pygame.K_LEFT] or teclas[pygame.K_d]:
        heroe_rect.x += velocidad
        velocidad_enemigo += 0.0009
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        heroe_rect.y -= velocidad
        velocidad_enemigo += 0.0009
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        heroe_rect.y += velocidad
        velocidad_enemigo += 0.0009

    #Si el jugador toca a cualquier enemigo, pierde
    for enemy_rect in enemigos:
        if heroe_rect.colliderect(enemy_rect):
            corriendo = False

    #movimiento de los enemigos hacia el héroe
    for enemy_rect in enemigos:
        if heroe_rect.x > enemy_rect.x:
            enemy_rect.x += int(velocidad_enemigo)
        if heroe_rect.x < enemy_rect.x:
            enemy_rect.x -= int(velocidad_enemigo)
        if heroe_rect.y > enemy_rect.y:
            enemy_rect.y += int(velocidad_enemigo)
        if heroe_rect.y < enemy_rect.y:
            enemy_rect.y -= int(velocidad_enemigo)

    #límites del mapa para el héroe
    if heroe_rect.x + 32 > ancho_pantalla:
        heroe_rect.x = ancho_pantalla - 32
    if heroe_rect.x <= 0:
        heroe_rect.x = 0
    if heroe_rect.y + 32 > alto_pantalla:
        heroe_rect.y = alto_pantalla - 32
    if heroe_rect.y <= 0:
        heroe_rect.y = 0

    if nivel == velocidad:
        velocidad += 1

    # 6. Dibujar en la pantalla
    pantalla.blit(calle_imagen, (0, 0))  # Fondo estirado
    pantalla.blit(heroe_imagen, heroe_rect)
    for enemy_rect in enemigos:
        pantalla.blit(enemy_imagen, enemy_rect)

    # 7. Actualizar la pantalla
    pygame.display.flip()

# 8. Salir de Pygame
if nivel == 10:
    time.sleep(2)
pygame.quit()
print("Game Over")
print("Nivel", nivel)
if nivel == 10:
    print("¡¡¡Ganaste!!!")