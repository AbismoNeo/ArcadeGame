import pygame
from pygame.locals import *

pygame.init()
MATRIZ = pygame.math.Vector2  # antes "vec"  es una matriz de 2 dimensiones
ALTO = 600
ANCHO = 800
FPS = 60
FramePerSec = pygame.time.Clock()
ACEL = 0.5 # antes ACC es la acelaracion
FRIC = -0.12 # Friccion contra el piso


VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("JUEGO ARCADE")

class JUGADOR(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect(center = (10, 565))
        self.pos = MATRIZ((10, 565))  # MIN y MAX posiciones del jugador
        self.vel = MATRIZ(0,0) #Velocidad
        self.acc = MATRIZ(0,0) #Aceleracion
    def MOVER(self):
        self.acc = MATRIZ(0,0)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACEL
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACEL
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        ####### AQUI SI SALIMOS DE LA VENTANA VOLVEMOS A EL LADO OPUESTO #####
        if self.pos.x > ANCHO:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = ANCHO
        self.rect.midbottom = self.pos
        ####### AQUI SI SALIMOS DE LA VENTANA VOLVEMOS A EL LADO OPUESTO #####
class PLATAFORMA(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((ANCHO, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (ANCHO/2, ALTO - 10))

PT1 = PLATAFORMA()
P1 = JUGADOR()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

##############################################
############### CICLO DEL JUEGO ##############
##############################################

while True:
    for event in pygame.event.get():
        P1.MOVER()
        if event.type == QUIT:
            pygame.quit()
            #sys.exit()

##############################################
############### CICLO DEL JUEGO ##############
##############################################

    VENTANA.fill((0,0,0))
 
    for entity in all_sprites:
        VENTANA.blit(entity.surf, entity.rect)
 
    pygame.display.update()
    FramePerSec.tick(FPS)


