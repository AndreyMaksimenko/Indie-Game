import pygame
from Utils.settings import *
from Utils.support import import_folder
from Graphics.sprites import Generic
from random import randint, choice

class DayChange:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)
        self.direction = -1  # -1 for day to night, 1 for night to day

    def display(self, dt):
        for index, value in enumerate(self.end_color):
            if self.direction == -1:  # Transitioning from day to night
                if self.start_color[index] > value:
                    self.start_color[index] -= 2 * dt
                else:
                    self.start_color[index] = value  # Clamp to target color
            elif self.direction == 1:  # Transitioning from night to day
                if self.start_color[index] < 255:
                    self.start_color[index] += 2 * dt
                else:
                    self.start_color[index] = 255  # Clamp to target color

        # Check if the transition is complete to switch direction
        if self.direction == -1 and self.start_color == list(self.end_color):
            self.direction = 1  # Switch to transitioning from night to day
        elif self.direction == 1 and self.start_color == [255, 255, 255]:
            self.direction = -1  # Switch to transitioning from day to night

        self.full_surf.fill(self.start_color)
        self.display_surface.blit(self.full_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class Drop(Generic):
    def __init__(self, surf, pos,  moving, groups, z):
        
        # загальне налаштування
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # рух
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(100, 300)
            
    def update(self, dt):
        # пересування
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        # timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('../graphics/rain/drops/')
        self.rain_floor = import_folder('../graphics/rain/floor/')
        self.floor_w, self.floor_h = pygame.image.load('../graphics/world/ground.png').get_size()

    def create_floor(self):
        Drop(surf = choice(self.rain_floor),
             pos = (randint(0,self.floor_w), randint(0,self.floor_h)), 
             moving = False, 
             groups = self.all_sprites, 
             z = LAYERS['rain floor'])

    def create_drops(self):
        Drop(surf = choice(self.rain_drops),
             pos = (randint(0,self.floor_w), randint(0,self.floor_h)), 
             moving = True, 
             groups = self.all_sprites, 
             z = LAYERS['rain drops'])

    def update(self):
        self.create_floor()
        self.create_drops()