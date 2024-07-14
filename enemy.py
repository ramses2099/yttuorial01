import pygame
import random
from constants import *
from resourcemanager import ResourceManager

class Enemy(pygame.sprite.Sprite):

    def __init__(self, res_manager: ResourceManager):
       pygame.sprite.Sprite.__init__(self)
       
       # images 
       self.res_manager = res_manager
       self.arr_images = ["enemy_A","enemy_B","enemy_C","enemy_D","enemy_E"]
       self.name_image = random.choice(self.arr_images)
       
       self.image =  self.res_manager.get_sprite(self.name_image)
              
       # position random
       self.x = random.randint(64, SCREEN_SIZE[0])
       self.y = random.randint(0, 10)
       
       # rect    
       self.rect = self.image.get_frect(center = (self.x, self.y))
       
    def update(self, dt):
        #  move
        self.rect.y += ENEMY_SPEED * dt
    
    