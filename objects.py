import math
import random
import pygame
from constants import *
from resourcemanager import ResourceManager

class ShieldBar(pygame.sprite.Sprite):
  def __init__(self, x: int , y: int)->None:
    pygame.sprite.Sprite.__init__(self)
    self.bar_length: int = 200
    self.bar_height: int = 25
    self.fill: float = 200
    self.outline_rect: pygame.rect.Rect = pygame.Rect(x, y, self.bar_length, self.bar_height)
    self.fill_rect: pygame.rect.Rect = pygame.rect.Rect(x, y, self.fill, self.bar_height)
    
  def increment_bar(self, value: int)->None:
    if (self.fill < self.bar_length):
      self.fill += value
      self.fill_rect.width = int(self.fill)
  
  def decrease_bar(self, value: int)->None:
    if(self.fill >= 10):
      self.fill -= value
      self.fill_rect.width = int(self.fill)  
    
  def draw(self, screen : pygame.surface.Surface):
    pygame.draw.rect(screen, WHITE, self.outline_rect, 2)
    pygame.draw.rect(screen, GREEN, self.fill_rect)
    
    
class Star(pygame.sprite.Sprite):
  def __init__(self, res_manager: ResourceManager, groups: pygame.sprite.Group) -> None:
    super().__init__(groups)
    self.res_manager = res_manager
    self.names = ["star_large","star_medium","star_small","star_tiny"]
    self.image = res_manager.get_sprite(random.choice(self.names))
    self.rect = self.image.get_rect(center =(random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])))
  
  
class Meteor(pygame.sprite.Sprite):
  def __init__(self, res_manager: ResourceManager, pos: tuple, *groups: pygame.sprite.Group) -> None:
    super().__init__(groups)
    self.res_manager = res_manager
    self.names = ["meteor_detailedLarge","meteor_detailedSmall","meteor_large","meteor_small","meteor_squareDetailedLarge",
    "meteor_squareDetailedSmall","meteor_squareLarge","meteor_squareSmall"]
    self.image = res_manager.get_sprite(random.choice(self.names))
    self.rect = self.image.get_frect(center = pos)
    self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
    self.speed = random.randint(400, 500)

    # interval timer
    self.start_time = pygame.time.get_ticks()
    self.livetime = 3000
    
  def update(self, dt):
     self.rect.center += self.direction * self.speed * dt
     if pygame.time.get_ticks() - self.start_time >= self.livetime:
       self.kill()


class Laser(pygame.sprite.Sprite):
  def __init__(self, res_manager: ResourceManager, pos: tuple, typelaser: int, *groups: pygame.sprite.Group) -> None:
    super().__init__(groups)
    self.res_manager = res_manager
    self.names = ["effect_purple","effect_yellow"]
    self.image_trans = pygame.transform.scale(res_manager.get_sprite(self.names[typelaser]),(8,64))
    self.image = self.image_trans
    self.rect = self.image.get_frect(midbottom = pos)
    
  def update(self, dt):
    self.rect.centery -= LASER_SPEED * dt
    if self.rect.bottom < 0:
      self.kill()
    