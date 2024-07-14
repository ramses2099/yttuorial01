import pygame
from constants import *
from resourcemanager import ResourceManager
from objects import Laser

class Player(pygame.sprite.Sprite):

    def __init__(self, res_manager: ResourceManager, *groups: pygame.sprite.Group):
       super().__init__(groups)
       self.groups = groups
       self.res_manager = res_manager
       self.image =  self.res_manager.get_sprite('ship_J')
       self.position = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 64)
       # rect    
       self.rect = self.image.get_frect(center = self.position)
       self.direction = pygame.math.Vector2()
       # interval time   
       self.can_shoot = True
       self.laser_shoot_time = 0
       self.cooldown_duration = 400
       
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
       
    def update(self, dt):
        keys = pygame.key.get_pressed()
        # direction
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])        
        # normalize direction    
        self.direction = self.direction.normalize() if self.direction else self.direction           
        self.rect.center += self.direction * PLAYER_SPEED * dt        
        # keys for space key
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(self.res_manager, self.rect.midtop, 0, self.groups)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()
    
    