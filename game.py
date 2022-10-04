import pygame
import os
import random
from pygame.locals import *
import sys

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
BUL_VEL = 10
FPS = 60
ACC = 1
FRIC = -0.10
RED = (255, 0, 0)
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombies')
vec = pygame.math.Vector2    
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super(Character, self).__init__()
        self.image = pygame.image.load(os.path.join('Assets', 'army_dude.png'))
        self.body = self.image.get_rect()
        
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.vx = 0
        self.pos = vec((0, 0))
        
        self.pos.x = 500
        self.pos.y = 400
        
        self.health = 3
        self.stamina = 100
        self.bullets = []
        self.super_energy = 50
        self.move_speed = 10
        self.player_level = 1
        self.direction = 1
        
    def movement(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            self.acc.x = -ACC
            self.direction = -1
            self.image = pygame.transform.flip(pygame.image.load(os.path.join('Assets', 'army_dude.png')), flip_x= True, flip_y= False)
            
        if keys_pressed[pygame.K_d]:
            self.acc.x = ACC
            self.direction = 1
            self.image = pygame.image.load(os.path.join('Assets', 'army_dude.png'))

            
        self.acc.x += self.vel.x * FRIC
        self.vel.x = self.acc.x
        self.pos.x += self.vel.x + .5 * self.acc.x
        
        if self.pos.x > SCREEN_WIDTH:
            self.x_pos = 0
        if self.pos.x < 0:
            self.x_pos = SCREEN_WIDTH
            
    def update(self):
        self.body.center = (self.pos.x, self.pos.y)
            
    def create_bullet(self):
        return Bullet(self.pos.x, self.pos.y, self.direction)
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, direction):
        super().__init__()
        self.direction = direction
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center = (x_pos + 20, y_pos + 30))
            
    def update(self):
        self.rect.x += BUL_VEL * self.direction

class Zombie(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets', 'zombie.png'))
        self.rect = self.image.get_rect()     
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        
        self.direction = direction
        
        self.vel.x = random.randint(2,6) / 2  # Randomized velocity of the generated enemy
        
        
        # Sets the intial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 400
        if self.direction == 1:
            self.pos.x = SCREEN_WIDTH
            self.pos.y = 400
            
    def movement(self):
        # Causes the enemy to change directions upon reaching the end of screen    
        if self.pos.x >= (SCREEN_WIDTH-20):
            self.direction = 1
            self.image = pygame.image.load(os.path.join('Assets', 'zombie.png'))
            
        elif self.pos.x <= 0:
            self.direction = 0
            self.image = pygame.transform.flip(self.image, flip_x = True, flip_y = False)
            
           # Updates position with new values     
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
        
        self.rect.center = self.pos # Updates rect
        
    def render(self):
        WIN.blit(self.image, (self.pos.x, self.pos.y))
        self.movement()



class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 1
        self.stage_enemies = []
        self.stage = 1
        for x in range(1, 21):
                self.stage_enemies.append(int((x ** 2 / 2) + 1))
    
    def world(self):
        pygame.time.set_timer(self.enemy_generation, 2000)
        self.battle = True
        
    def stage_handler(self):
        self.world()
        
    def next_stage(self):  # Code for when the next stage is clicked            
      self.stage += 1
      self.enemy_count = 0
      print("Stage: "  + str(self.stage))
      pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage)) 
             

           
def draw_screen():
    BG = pygame.image.load(os.path.join('Assets', 'background.png'))
    WIN.blit(BG, (0, 0))
    

def main():
    run = True
    direction = 0
    round = 1
    zombie_count = 0
    clock = pygame.time.Clock()
    player = Character()
    player_group.add(player)
    handler = EventHandler()
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_group.add(player.create_bullet())
            
            if event.type == handler.enemy_generation:
                if handler.enemy_count < handler.stage_enemies[player.stage - 1]:
                    enemy = Zombie()
                    zombie_group.add(enemy)
                    handler.enemy_count += 1
                    
            if handler.battle == True and len(zombie_group) == 0:
                handler.next_stage()
        
        handler.stage_handler()
          
        draw_screen()
        
        for entity in zombie_group:
            entity.update()
            entity.movement()
            entity.render()
        
            
        player.movement()
        
        bullet_group.update()
        player_group.update()
        
        bullet_group.draw(WIN)
        WIN.blit(player.image, (player.pos.x, player.pos.y))
        
    

        pygame.display.update()         


    main()
    
if __name__ == '__main__':
    main()