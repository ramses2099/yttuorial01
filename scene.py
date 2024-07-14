import pygame, sys
from abc import abstractmethod, ABC
from resourcemanager import ResourceManager
from constants import *
from objects import *
from player import Player
from enemy import Enemy

# Base Scene class
class Scene(ABC):
    def __init__(self):
        self.next_scene = self
    
    @abstractmethod    
    def process_events(self, events):
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, dt):
        raise NotImplementedError()
    
    @abstractmethod
    def draw(self, screen):
        raise NotImplementedError()
   
# Menu Scene
class MenuScene(Scene):
    def __init__(self, res_manager: ResourceManager):
        super().__init__()
        self.res_manager = res_manager
        self.menu_items = ['Start Game','Options','Quit']
        self.selected_item = 0
        self.bg = self.res_manager.get_backgrounds('black')
        
    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                if event.key == pygame.K_RETURN:
                    if self.menu_items[self.selected_item] == 'Start Game':
                        self.next_scene = GameScene(self.res_manager)
                    elif self.menu_items[self.selected_item] == 'Options':
                        pass
                    elif self.menu_items[self.selected_item] == 'Quit':
                        pygame.quit()
                        sys.exit()
      
    def update(self, dt):
        pass
    
    def draw(self, screen):
        bg = pygame.transform.scale(self.bg,(SCREEN_SIZE[0], SCREEN_SIZE[1]))
        screen.blit(bg, (0, 0))        
        font = self.res_manager.get_fonts('kenvector_future', 74)
        text = font.render("Main Menu", True, WHITE)
        screen.blit(text, (SCREEN_SIZE[0]//2 - text.get_width()//2, SCREEN_SIZE[1]//4 - text.get_height()//2))
        
        # Create the screen
        for index, item in enumerate(self.menu_items):
            if index == self.selected_item:
                color = HIGHLIGHT_COLOR
            else:
                color = WHITE
            # text
            font_option = self.res_manager.get_fonts('kenvector_future', 22)
            text = font_option.render(item, True, color)
            text_rect = text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + index * 50))
            screen.blit(text, text_rect)
    
# Game Scene
class GameScene(Scene):
    def __init__(self, res_manager: ResourceManager):
        super().__init__()
        self.res_manager = res_manager
        self.bg = self.res_manager.get_backgrounds('black')
        self.current_level_number = 1
        #  groups
        self.all_decorator = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.meteor_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()
        
         
        # test enemy
        for e in range(2):
            self.all_sprites.add(Enemy(self.res_manager))
            
        # test start
        for s in range(5):
            Star(self.res_manager, self.all_decorator)
        
        # create custom event
        self.meteor_event = pygame.event.custom_type()
        pygame.time.set_timer(self.meteor_event, 500)       
        
        # player instance   
        self.player = Player(self.res_manager, (self.all_sprites, self.laser_group))
        
        self.bar = ShieldBar(5, 50)
    
    def showLives(self, screen):
        image = self.res_manager.get_sprite('ship_J')
        rect = image.get_rect()
        sprite = pygame.transform.scale(image, (rect.width//2, rect.height//2))
        
        font = self.res_manager.get_fonts('kenvector_future', 22) 
        lives = 3   
        lv_text = font.render(f"LIVES: {lives} - ", True, WHITE)   
        screen.blit(lv_text, (SCREEN_SIZE[0] - 190, 20))
        screen.blit(sprite, (SCREEN_SIZE[0] - 40, 20))
    
    def showPlayerPoints(self, screen):    
        points = 0 
        font = self.res_manager.get_fonts('kenvector_future', 22)   
        points_text = font.render(f"POINTS: {points}", True, WHITE)   
        screen.blit(points_text, ((SCREEN_SIZE[0]-190), 43))
     
    def showLevel(self, screen):    
        lvl = self.current_level_number
        font = self.res_manager.get_fonts('kenvector_future', 22)    
        lvl_text = font.render(f"LEVEL: {lvl}", True, WHITE)   
        screen.blit(lvl_text, (5, 15))   
     
    def collisions(self):
         # collision player and meteor
        collision_sprite = pygame.sprite.spritecollide(self.player, self.meteor_group, True)
        if collision_sprite:
            print('collition meteor')
            
            
        # collision laser and meteor
        for laser in self.laser_group:
            collition_laser = pygame.sprite.spritecollide(laser, self.meteor_group, True)
            if collition_laser:
                laser.kill()
                
    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == self.meteor_event:
                x, y = random.randint(0, SCREEN_SIZE[0]), random.randint(-200, -100)
                Meteor(self.res_manager, (x, y), (self.all_sprites, self.meteor_group))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_scene = MenuScene(self.res_manager)
      
    def update(self, dt):
        self.all_sprites.update(dt)
        # check collision
        self.collisions()
                    
    
    def draw(self, screen):
        bg = pygame.transform.scale(self.bg,(SCREEN_SIZE[0], SCREEN_SIZE[1]))
        screen.blit(bg, (0, 0))
        
        # decorator sprite
        self.all_decorator.draw(screen)
        
        # info game
        self.showLives(screen)
        self.showLevel(screen)
        self.showPlayerPoints(screen)
        self.bar.draw(screen)
        
         
        # draw all sprite
        self.all_sprites.draw(screen)
    
# Scene Manager
class ManagerScene():
    def __init__(self, start_scene: Scene):
        super().__init__()
        self.current_scene = start_scene
        
    def process_events(self, events):
        self.current_scene.process_events(events)
        if self.current_scene.next_scene != self.current_scene:
            self.current_scene = self.current_scene.next_scene
      
    def update(self, dt):
        self.current_scene.update(dt)
    
    def draw(self, screen):
        self.current_scene.draw(screen)