import pygame
import random
import time
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.x = 50
        self.y = 363
        self.surf = pygame.Surface((37, 46))
        self.surf.fill((55, 55, 55))
        self.surf = pygame.image.load('./images/dino0.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.jumpCount = 12
        self.isjump = False

    def update(self, pressed_keys):
        if self.isjump == False :
            if pressed_keys[K_SPACE]:
                self.isjump = True
        else:
            if self.jumpCount >= -12:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount**2 * 0.1 * neg
                self.rect = self.surf.get_rect(center=(self.x, self.y))
                self.jumpCount -= 1
            else:
                self.isjump = False
                self.jumpCount = 12
            
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super(Ground, self).__init__()
        self.x = 400
        self.y = 390
        self.surf = pygame.Surface((800,118))
        self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load('./images/1x-horizon.png').convert()
        self.rect = self.surf.get_rect(center=(self.x, self.y))

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.Surface((50, 20))
        self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load("./images/1x-cloud.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT/4)
            )
        )
        self.speed = 2
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((10, 30))
        self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load('./images/obs1.png').convert()
        self.rect = self.surf.get_rect(center = (800,363))     
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
          
clock = pygame.time.Clock()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 400)

ADDCLOUD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCLOUD, 4000)

player = Player()
ground = Ground()
cloud = Cloud()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ground)

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

running = True

while running:
    
    for event in pygame.event.get():
        score_value += 1
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False
            
        if event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
            
        if event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    
    screen.fill((0, 0, 0))

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    enemies.update()
    clouds.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    show_score(100, 100)
    
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pygame.display.flip()

    clock.tick(30)


pygame.quit()
