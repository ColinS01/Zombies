import pygame
import os

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

class Character(pygame.sprite.Sprite):
 
    def __init__(self):
        super(Character, self).__init__()
        self.image = pygame.image.load(os.path.join('Assets', 'army_dude.png'))
        self.body = self.image.get_rect()
        
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.vx = 0
        self.pos = vec((0, 0))
        
        self.x_pos = 150
        self.y_pos = 400
        
        self.health = 3
        self.stamina = 100
        self.bullets = []
        self.super_energy = 50
        self.move_speed = 10
        
    def shoot(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            bullet = pygame.Rect(self.x_pos + 20, self.y_pos + 28, 10, 5)
            self.bullets.append(bullet)
            for bullet in self.bullets:
                bullet.x += BUL_VEL
                pygame.draw.rect(WIN, RED, bullet)
                if bullet.x > SCREEN_WIDTH:
                   self.bullets.clear()
                
        # make bullets not laser gun
        # create collision with zombies

    
    def movement(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            self.acc.x = -ACC
            self.image = pygame.transform.flip(pygame.image.load(os.path.join('Assets', 'army_dude.png')), flip_x= True, flip_y= False)
            
            # add stamina dectriment for movement

        if keys_pressed[pygame.K_d]:
            self.acc.x = ACC
            self.image = pygame.image.load(os.path.join('Assets', 'army_dude.png'))

            
        self.acc.x += self.vel.x * FRIC
        self.vel = self.acc
        self.x_pos += self.vel.x + .5 * self.acc.x
        
        if self.pos.x > SCREEN_WIDTH:
            self.x_pos = 0
        if self.pos.x < 0:
            self.x_pos = SCREEN_WIDTH
        
            

class Zombie(object):
    def __init__(self):
        pass
    
    def move():
        pass
    
    def hit(self):
        pass

def draw_screen():
    BG = pygame.image.load(os.path.join('Assets', 'background.png'))
    WIN.blit(BG, (0, 0))

def main():
    run = True
    clock = pygame.time.Clock()
    player = Character()
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                pygame.quit()
        
                    
        draw_screen()
        player.movement()
        player.shoot()
        WIN.blit(player.image, (player.x_pos, player.y_pos))  
        pygame.display.update()         


    main()
    
if __name__ == '__main__':
    main()