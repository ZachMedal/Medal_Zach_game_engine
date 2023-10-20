# This file was created by: Zach Medal
# content from kids can code: http://kidscancode.org/blog/

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
# import random
from random import randint 
import os


vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

# game settings 
WIDTH = 360
HEIGHT = 480
FPS = 30
SCORE = 0

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5
global PLAYER_FRIC
PLAYER_FRIC = 0.3

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        if hits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
    def update(self):
        if self.kind == "moving":
            self.pos = self.rect.x
            self.rect.x = self.pos + 2
        if self.kind == "ice":
            self.image.fill(WHITE)

class Ice_plat(Platform):
    def __init__(self, x, y, w, h, kind):
        Platform.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print("Thats an ice plat")

class Mob(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind 
    def seeking(self):
        if player.rect.x > self.rect.x:
            self.rect.x +=1
        if player.rect.x > self.rect.x:
            self.rect.x -=1
        if player.rect.y > self.rect.x:
            self.rect.y +=1
        if player.rect.y > self.rect.x:
            self.rect.y +=1
    def update(self):
        self.seeking()
        

        


# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
all_mobs = pg.sprite.Group()

# instantiate classes
player = Player()
# plat = Platform(150, 300, 100, 30, "static")
# plat1 = Platform(200, 200, 100, 30, "moving")
# plat2 = Ice_plat(200, 100, 100, 30, "ice")

# add instances to groups
all_sprites.add(player) 

PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40, "normal"),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20,"bounce"),
                 (125, HEIGHT - 350, 100, 20, "moving"),
                 (350, 200, 100, 20, "normal"),
                 (175, 100, 50, 20, "normal")]


for p in PLATFORM_LIST: 
    # Instantiation of the Platform Class
    plat = Platform(*p)
    all_sprites.add(plat)
    all_platforms.add(plat)

for m in range(0,25):
    m = Mob(randint(0, WIDTH), randint(0, HEIGHT/2))
    all_sprites.add(m)
    all_mobs.add(m)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)
        
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    
    ############ Update ##############
    # update all sprites
    all_sprites.update()

    # this is what prevents the player from falling through the platform when falling down...
    if player.vel.y > 0:
            hits = pg.sprite.spritecollide(player, all_platforms, False)
            if hits:
                if hits[0].kind == "ice":
                    
                    PLAYER_FRIC == 0
                    print("i'm on an ice plat")
                    print(PLAYER_FRIC)
                player.pos.y = hits[0].rect.top
                player.vel.y = 0
                

                
    # this prevents the player from jumping up through a platform
    if player.vel.y < 0:
        hits = pg.sprite.spritecollide(player, all_platforms, False)
        if hits:
            print("ouch")
            SCORE -= 1
            if player.rect.bottom >= hits[0].rect.top - 5:
                player.rect.top = hits[0].rect.bottom
                player.acc.y = 5
                player.vel.y = 0

    ############ Draw ################
    # draw the background screen
    screen.fill(BLACK)
    # draw all sprites
    all_sprites.draw(screen)
    draw_text("Score: " + str(SCORE), 22, WHITE, WIDTH/2, HEIGHT/10)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()
