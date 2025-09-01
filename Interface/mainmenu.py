import pygame
import sys
import pickle
import os
from pygame.locals import *
from Utils.settings import *
from Scene.level import Level
from Interface.overlay import *
from Interface.Button import Button
from Utils.settingsmanager import SettingsManager

class MainMenu:
    def __init__(self):
        self.initial_screen_width = SCREEN_WIDTH
        self.initial_screen_height = SCREEN_HEIGHT
   
        self.music = pygame.mixer.Sound('../audio/main_menu.wav')
        self.music.set_volume(VOLUME)
        self.music.play(loops=-1)
        self.current_volume = self.music.get_volume()
        self.initial_y = self.initial_screen_height // 2 - 100
        self.button_offset = 130
        self.buttons = [
            Button('New Game', (self.initial_screen_width // 2, self.initial_y), self.initial_screen_width),
            Button('Load Game', (self.initial_screen_width // 2, self.initial_y + self.button_offset), self.initial_screen_width),
            Button('Settings', (self.initial_screen_width // 2, self.initial_y + self.button_offset * 2), self.initial_screen_width),
            Button('Exit', (self.initial_screen_width // 2, self.initial_y + self.button_offset * 3), self.initial_screen_width),
        ]
        self.background_image = pygame.image.load('../main_theme/theme.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.initial_screen_width, self.initial_screen_height))
        self.background_rect = self.background_image.get_rect()
        self.screen = pygame.display.set_mode((self.initial_screen_width, self.initial_screen_height))
        self.s = SettingsManager(self.initial_screen_width, self.initial_screen_height,self.buttons,self.background_image, self.background_rect, self.screen, self.music, self.current_volume, 'Easy')
        self.difficulty = self.s.difficulty
        self.running = False
        self.cursor_image = pygame.image.load('../graphics/cursor/cursor.png')
        self.cursor_rect = self.cursor_image.get_rect()
        self.clock = pygame.time.Clock()
        self.settings_open = False

    def draw(self):
        self.s.update_background_image()
        for button in self.buttons:
            button.draw(self.screen)
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (255, 255, 0), button.rect, 3)
        pygame.mouse.set_visible(False)
        self.s.update_buttons_positions()
        self.screen.blit(self.cursor_image, pygame.mouse.get_pos())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        return button.text
        return None
    

    def show_difficulty_menu(self):
        self.difficulty_buttons = [
            Button('Easy', (self.initial_screen_width // 2, self.initial_y), self.initial_screen_width),
            Button('Medium', (self.initial_screen_width // 2, self.initial_y + self.button_offset), self.initial_screen_width),
            Button('Hard', (self.initial_screen_width // 2, self.initial_y + self.button_offset * 2), self.initial_screen_width),
        ]
        selecting_difficulty = True
        while selecting_difficulty:
            self.screen.blit(self.background_image, self.background_rect)
            for button in self.difficulty_buttons:
                button.draw(self.screen)
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (255, 255, 0), button.rect, 3)
            pygame.mouse.set_visible(False)
            self.screen.blit(self.cursor_image, pygame.mouse.get_pos())
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.difficulty_buttons:
                        if button.rect.collidepoint(mouse_pos):
                            return button.text

    def start_level(self, dt, difficulty):
     self.music.stop()
     self.running = True
     self.level = Level(self.initial_screen_width, self.initial_screen_height, self.current_volume, difficulty)
     self.level.music_sound(self.music, self.current_volume)
     game_menu = GameMenu(self.initial_screen_width, self.initial_screen_height, self.music, self.current_volume, self.background_image, self.background_rect, self.screen, self.cursor_image, self.cursor_rect, self.clock)
     paused = False

     while self.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                paused = not paused
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.level.player.show_tasks = not self.level.player.show_tasks

        if paused:
            game_menu.draw()
            action = game_menu.handle_events()
            if action == 'Resume':
                paused = False
            elif action == 'Save Game':
                self.level.save_player_state('player_state.txt')
                self.level.soil_layer.save_plants()
                self.level.building_layer.save_objects_chicken()
                self.level.building_layer.save_objects_cow()
                paused = False
            elif action == 'Load Game':
                self.level.load_player_state('player_state.txt')
                self.level.soil_layer.load_plants()
                self.level.building_layer.load_objects_chicken()
                self.level.building_layer.load_objects_cow()
                paused = False
            elif action == 'Settings':
                game_menu.show_settings()
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif action == 'Exit':
                pygame.quit()
                sys.exit()

        else:
            dt = self.clock.tick() / 1000
            self.level.run(dt)

        pygame.display.update()


    def load_level(self, dt, difficulty):
     self.music.stop()
     self.running = True
     self.level = Level(self.initial_screen_width, self.initial_screen_height, self.current_volume, difficulty)
     self.level.load_player_state('player_state.txt')
     self.level.building_layer.load_objects_chicken()
     self.level.building_layer.load_objects_cow()
     self.level.soil_layer.load_plants()
     self.level.music_sound(self.music, self.current_volume)
     game_menu = GameMenu(self.initial_screen_width, self.initial_screen_height, self.music, self.current_volume, self.background_image, self.background_rect, self.screen, self.cursor_image, self.cursor_rect, self.clock)
     paused = False

     while self.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                paused = not paused
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.level.player.show_tasks = not self.level.player.show_tasks

        if paused:
            game_menu.draw()
            action = game_menu.handle_events()
            if action == 'Resume':
                paused = False
            elif action == 'Save Game':
                self.level.save_player_state('player_state.txt')
                self.level.soil_layer.save_plants()
                self.level.building_layer.save_objects_chicken()
                self.level.building_layer.save_objects_cow()
                paused = False
            elif action == 'Load Game':
                self.level.load_player_state('player_state.txt')
                self.level.soil_layer.load_plants()
                self.level.building_layer.load_objects_chicken()
                self.level.building_layer.load_objects_cow()
                paused = False
            elif action == 'Settings':
                game_menu.show_settings()
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif action == 'Exit':
                pygame.quit()
                sys.exit()

        else:
            dt = self.clock.tick() / 1000
            self.level.run(dt)

        pygame.display.update()

    def load_game(self, filename):
        with open(filename, 'rb') as f:
             player_state = pickle.load(f)
             print('Load')
        return player_state
    
    def load(self):
        if os.path.exists('settings_data.txt'):
            self.s.load_settings('settings_data.txt')

    def show_settings(self):
        self.s.show_settings1()
        self.s.save_settings('settings_data.txt')



class GameMenu():
    def __init__(self, screen_width, screen_height, music, volume, background_image, background_rect, screen, cursor_image, cursor_rect, clock):
        self.initial_screen_width = screen_width
        self.initial_screen_height = screen_height
        self.music = music
        self.current_volume = volume
        self.music.set_volume(self.current_volume)
        self.initial_y = self.initial_screen_height // 2 - 100
        self.button_offset = 130
        self.buttons = [
            Button('Resume', (self.initial_screen_width // 2, self.initial_y), self.initial_screen_width),
            Button('Save Game', (self.initial_screen_width // 2, self.initial_y + self.button_offset), self.initial_screen_width),
            Button('Load Game', (self.initial_screen_width // 2, self.initial_y + self.button_offset * 2), self.initial_screen_width),
            Button('Settings', (self.initial_screen_width // 2, self.initial_y + self.button_offset * 3), self.initial_screen_width),
            Button('Exit', (self.initial_screen_width // 2, self.initial_y + self.button_offset * 4), self.initial_screen_width),
        ]
        self.background_image = background_image
        self.background_rect = background_rect
        self.screen = screen
        self.running = True
        self.cursor_image = cursor_image
        self.cursor_rect = cursor_rect
        self.clock = clock
        self.settings_open = False
        self.s = SettingsManager(self.initial_screen_width, self.initial_screen_height, self.buttons, self.background_image, self.background_rect, self.screen, self.music, self.current_volume)

    def draw(self):
        self.s.update_background_image()
        for button in self.buttons:
            button.draw(self.screen)
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (255, 255, 0), button.rect, 3)
        pygame.mouse.set_visible(False)
        self.s.update_buttons_positions()
        self.screen.blit(self.cursor_image, pygame.mouse.get_pos())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        return button.text
        return None

    def load(self):
        if os.path.exists('settings_data.txt'):
            self.s.load_settings('settings_data.txt')

    def show_settings(self):
        self.s.show_settings1()
        self.s.save_settings('settings_data.txt')












