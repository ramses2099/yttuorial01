import pygame, os, sys, random
from constants import *
from resourcemanager import ResourceManager
from scene import ManagerScene, MenuScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
                       
        self.screen = pygame.display.set_mode(SCREEN_SIZE)      
        pygame.display.set_caption(TITLE)
        
        # load resources
        self.res_manager = ResourceManager.get_instance()         
        
        # Scene Manager
        self.manager_scene = ManagerScene(MenuScene(self.res_manager))
        
        self.clock = pygame.time.Clock()
        self.dt = 0
                 
    def showFPS(self):
        fps = round(self.clock.get_fps(),2)
        text = f"{TITLE} FPS: {fps}"
        pygame.display.set_caption(text)
        
    def run(self):
         
        while True:
            # DEBUG
            if DEBUG:
                self.showFPS()            
            
            # input event
            events = pygame.event.get()
            self.manager_scene.process_events(events)
                       
            # update
            self.manager_scene.update(self.dt)
            
            # draw
            self.manager_scene.draw(self.screen)
            
            pygame.display.flip()
            self.dt = self.clock.tick(FRAMERATE) / 1000 
     

               
               
    