import pygame, os, sys, random
from constants import *


class Game:
    def __init__(self):
        pygame.init()
                
        self.load_text()
        self.load_sound()
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.drwa_screen = pygame.Surface(DRAW_SCREEN_SIZE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.dt = 1
        
        self.game()
    
    def load_text(self):
        self.textures = {}
        for image in os.listdir("images/"):
            texture = pygame.image.load("images/" + image)
            self.textures[image.replace(".png", "")] = texture
    
    def load_sound(self):
        self.sounds = {}
        pygame.mixer.init()
        for sound in os.listdir("sounds/"):
            file = pygame.mixer.Sound("sounds/" + sound)
            self.sounds[file.replace(".ogg", "")] = file
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
    
    def close(self):
        pygame.quit()
        sys.exit(0)
    
    def game(self):
        
        while True:
            # input event
            self.check_events()
            
            # draw
            self.draw()
            self.refresh_screen()
    
    def draw(self):
        pass
    
    
    
    def refresh_screen(self):
        scaled = pygame.transform.scale(self.drwa_screen, SCREEN_SIZE)
        self.screen.blit(scaled, (0, 0))
        pygame.displayx.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000
    
if __name__ == "__main__":
    Game()