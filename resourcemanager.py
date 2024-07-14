import os
import pygame
import xml.etree.ElementTree as ET

# root path
ROOT_PATH = os.path.dirname(__file__)

# Assets folder
spritesheet_path = os.path.join(ROOT_PATH, os.path.join("assets", "spritesheets"))
fonts_path = os.path.join(ROOT_PATH, os.path.join("assets", "fonts"))
sounds_path = os.path.join(ROOT_PATH, os.path.join("assets", "sounds"))
backgrounds_path = os.path.join(ROOT_PATH, os.path.join("assets", "backgrounds"))


class ResourceManager:
    _instance = None

    def get_instance():
        if ResourceManager._instance is None:
            ResourceManager._instance = ResourceManager()
        return ResourceManager._instance

    def __init__(self):
        if ResourceManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            try:
                ResourceManager._instance = self
                self._backgrounds = self.load_backgrounds()
                self._sprites = self.load_sprite()
                self._fonts = self.load_fonts()
                self._sound = None
            except Exception as e:
                print(f"An error occurred: {e}")

    def load_sprite(self) -> dict:
        sprites = {}
        tree = ET.parse(os.path.join(spritesheet_path, "simpleSpace_sheet.xml"))
        root = tree.getroot()
        sprite_sheet = pygame.image.load(
            os.path.join(spritesheet_path, "simpleSpace_sheet.png")
        ).convert_alpha()

        for sub_texture in root.findall("SubTexture"):
            name = sub_texture.get("name")
            x = int(sub_texture.get("x"))
            y = int(sub_texture.get("y"))
            width = int(sub_texture.get("width"))
            height = int(sub_texture.get("height"))

            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(sprite_sheet, (0, 0), (x, y, width, height))
            sprites[name.replace(".png", "")] = sprite

        return sprites

    def load_fonts(self) -> dict:
        fonts_dict = {}
        # Walk through the folder
        for root, _, files in os.walk(fonts_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                fonts_dict[filename.replace(".ttf", "")] = full_path

        return fonts_dict

    def load_backgrounds(self) -> dict:
        bg_rs_dict = {}
        # Walk through the folder
        for root, _, files in os.walk(backgrounds_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                bg_rs_dict[filename.replace(".png", "")] = pygame.image.load(
                    full_path
                ).convert_alpha()

        return bg_rs_dict

    def _get_sounds(self) -> dict:
        sounds_dict = {}
        # Walk through the folder
        for root, _, files in os.walk(sounds_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                sounds_dict[filename.replace(".ogg", "")] = pygame.mixer.Sound(
                    full_path
                )

        return sounds_dict

    # Public methods
    def get_sprite(self, name) -> pygame.surface.Surface:
        if name not in self._sprites.keys():
            raise KeyError("this key {name} doesn't exist")
        return self._sprites[name]

    def get_fonts(self, name, size) -> pygame.font.Font:
        font = pygame.font.Font(self._fonts[name], size)
        return font

    def get_backgrounds(self, name) -> pygame.surface.Surface:
        if name in self._backgrounds.keys():
            return self._backgrounds[name]

    def get_sounds(self, name) -> pygame.mixer.Sound:
        return self._get_sounds[name]
