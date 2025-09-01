import pygame
from Utils.settings import *

class Button:
    def __init__(self, text, pos, screen_width):
        self.image = pygame.image.load('../graphics/buttons/button.png')
        self.text = text
        self.screen_width = screen_width
        self.font_size = int(36 * self.screen_width / SCREEN_WIDTH)
        self.font = pygame.font.Font('../font/Soda.ttf', 30)
        self.text_image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.text_rect = self.text_image.get_rect(center=self.rect.center)

    def update_text_size(self):
        self.font_size = int(36 * self.screen_width / SCREEN_WIDTH)
        self.font = pygame.font.Font('../font/Soda.ttf', 30)
        self.text_image = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_image, self.text_rect)