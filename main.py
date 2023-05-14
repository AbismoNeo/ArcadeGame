import random
import pygame
from pygame.locals import *
import sys

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
        self.pos = MATRIZ((10, 580))  # MIN y MAX posiciones del jugador
        self.vel = MATRIZ(0,0) #Velocidad
        self.acc = MATRIZ(0,0) #Aceleracion
        self.jumping = False
    def MOVER(self):
        self.acc = MATRIZ(0,0.5)
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
        # if self.pos.y > ALTO:
        #     self.pos.y = 0
        # if self.pos.y < 0:
        #     self.pos.y = ALTO
        self.rect.midbottom = self.pos
        ####### AQUI SI SALIMOS DE LA VENTANA VOLVEMOS A EL LADO OPUESTO #####

    def SALTAR(self):
        COLISION = pygame.sprite.spritecollide(self, PLATAFORMAS, False)
        if COLISION and not self.jumping:
            self.jumping = True
            self.vel.y = -15
    
    def CANCELA_SALTO(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def ACTUALIZAR(self):
        COLISION = pygame.sprite.spritecollide(P1,PLATAFORMAS, False)
        if P1.vel.y > 0:
            if COLISION:
                self.vel.y = 0
                self.pos.y = COLISION[0].rect.top + 1  

class PLATAFORMA(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.surf = pygame.Surface((ANCHO, 20))
        # self.surf.fill((255,0,0))
        # self.rect = self.surf.get_rect(center = (ANCHO/2, ALTO - 10))
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,ANCHO-10), random.randint(0, ALTO-30)))
    def MOVER(self):
        pass

def plat_gen():
    while len(PLATAFORMAS) < 7 :
        width = random.randrange(50,100)
        p  = PLATAFORMA()             
        p.rect.center = (random.randrange(0, ANCHO - width), random.randrange(-50, 0))
        PLATAFORMAS.add(p)
        all_sprites.add(p)



PT1 = PLATAFORMA()
P1 = JUGADOR()

PT1.surf = pygame.Surface((ANCHO, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (ANCHO/2, ALTO - 10))

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

PLATAFORMAS = pygame.sprite.Group()
PLATAFORMAS.add(PT1)

for x in range(random.randint(5, 6)):
    pl = PLATAFORMA()
    PLATAFORMAS.add(pl)
    all_sprites.add(pl)

##############################################
############### CICLO DEL JUEGO ##############
##############################################

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.SALTAR()
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                P1.CANCELA_SALTO() 
        

    if P1.rect.top <= ALTO / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in PLATAFORMAS:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= ALTO:
                plat.kill()

    VENTANA.fill((0,0,0))
    P1.ACTUALIZAR()
    plat_gen()

    for entity in all_sprites:
        VENTANA.blit(entity.surf, entity.rect)
        entity.MOVER()


    pygame.display.update()
    FramePerSec.tick(FPS)

##############################################
############### CICLO DEL JUEGO ##############
##############################################
