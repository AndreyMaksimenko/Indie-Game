import pygame
import pickle
import os
from Scene.level import Level, Camera

class SettingsManager:
    def __init__(self, screen_width, screen_height, buttons, background_image, background_rect, screen, music, volume, difficulty='Easy'):
        self.initial_screen_width = screen_width
        self.initial_screen_height = screen_height
        self.screen = screen
        self.buttons = buttons
        self.music = music
        self.volume = volume
        self.difficulty = difficulty
        self.initial_y = self.initial_screen_height // 2 - 100
        self.button_offset = 130
        self.show_resolution_list = False
        self.resolution_list = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1920, 1080),
            (2560, 1440),
        ]
        self.selected_resolution = self.resolution_list.index((screen_width, screen_height))
        self.background_image = background_image
        self.background_rect = background_rect
        self.camera = Camera()
        self.current_volume = self.music.get_volume()
        self.new_volume = self.current_volume
        self.level = Level(self.initial_screen_width,self.initial_screen_height, self.current_volume, self.difficulty)

    def show_settings1(self):
        self.settings_open = True
        running = True
        self.settings_background_image = pygame.image.load('../main_theme/theme.jpg').convert()
        self.settings_background_rect = self.settings_background_image.get_rect()
        self.cursor_image = pygame.image.load('../graphics/cursor/cursor.png')

        while running:
            self.update_settings_background_image()
            self.screen.blit(self.settings_background_image, self.settings_background_rect)

            resolution_button = pygame.Rect(self.initial_screen_width // 2 - 100, self.initial_screen_height // 2 - 25, 200, 50)
            pygame.draw.rect(self.screen, (100, 100, 100), resolution_button)
            font = pygame.font.Font('../font/Soda.ttf', 30)
            text = font.render("Screen", True, (255, 255, 255))
            text_rect = text.get_rect(center=resolution_button.center)
            self.screen.blit(text, text_rect)

            back_button = pygame.Rect(self.initial_screen_width // 2 - 100, self.initial_screen_height - 75, 200, 50)
            pygame.draw.rect(self.screen, (100, 100, 100), back_button)
            back_text = font.render("Back", True, (255, 255, 255))
            back_text_rect = back_text.get_rect(center=back_button.center)
            self.screen.blit(back_text, back_text_rect)

            volume_slider = pygame.Rect(self.initial_screen_width // 2 - 100, self.initial_screen_height // 2 + 90, 200, 20)
            pygame.draw.rect(self.screen, (100, 100, 100), volume_slider)

            volume_text = font.render("Volume", True, (255, 255, 255))
            volume_text_rect = volume_text.get_rect(center=(volume_slider.centerx, volume_slider.top - 10))
            self.screen.blit(volume_text, volume_text_rect)

            volume_level = (self.music.get_volume() - 0.2) / 0.8
            slider_pos = (volume_slider.width - 20) * volume_level + volume_slider.left + 10
            slider_rect = pygame.Rect(slider_pos, volume_slider.top + 1, 10, volume_slider.height - 2)
            pygame.draw.rect(self.screen, (255, 255, 255), slider_rect)

            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if volume_slider.collidepoint(mouse_x, mouse_y):
                    volume_level = (mouse_x - volume_slider.left) / volume_slider.width
                    self.volume = volume_level * 0.8 + 0.2 
                    self.music.set_volume(self.volume)
                    self.update_music_volume(self.volume)

            if self.show_resolution_list:
                resolution_list_rect = pygame.Rect(resolution_button.right + 5, resolution_button.top, 200, 50 * len(self.resolution_list))
                pygame.draw.rect(self.screen, (100, 100, 100), resolution_list_rect)
                for i, resolution in enumerate(self.resolution_list):
                    resolution_rect = pygame.Rect(resolution_button.right + 10, resolution_button.top + i * 50, 200, 50)
                    pygame.draw.rect(self.screen, (150, 150, 150), resolution_rect)
                    text = font.render(f"{resolution[0]} x {resolution[1]}", True, (255, 255, 255))
                    text_rect = text.get_rect(center=resolution_rect.center)
                    self.screen.blit(text, text_rect)

                    mouse_pos = pygame.mouse.get_pos()
                    if resolution_rect.collidepoint(mouse_pos):
                        pygame.draw.rect(self.screen, (255, 255, 0), resolution_rect, 3)

            self.screen.blit(self.cursor_image, pygame.mouse.get_pos())
            pygame.mouse.set_visible(False)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if resolution_button.collidepoint(mouse_pos):
                        self.toggle_resolution_list()
                    elif back_button.collidepoint(mouse_pos):
                        self.settings_open = False
                        running = False
                    elif self.show_resolution_list:
                        for i, resolution in enumerate(self.resolution_list):
                            resolution_rect = pygame.Rect(resolution_button.right + 10, resolution_button.top + i * 50, 200, 50)
                            if resolution_rect.collidepoint(mouse_pos):
                                self.selected_resolution = i
                                self.initial_screen_width, self.initial_screen_height = self.resolution_list[i]
                                pygame.display.set_mode((self.initial_screen_width, self.initial_screen_height))
                                self.level.update_settings(self.initial_screen_width, self.initial_screen_height, self.volume)
                                self.camera.update_screen_size(self.initial_screen_width, self.initial_screen_height)
                                self.update_background_image()
                                self.toggle_resolution_list()
                                self.update_buttons_positions()
                                break

        self.settings_open = False
        pygame.mouse.set_visible(True)

    def update_music_volume(self, volume):
        self.music_volume = volume

    def update_buttons_positions(self):
        initial_y = self.initial_screen_height // 2 - 200
        button_spacing = 10
        for i, button in enumerate(self.buttons):
            button.rect.center = (self.initial_screen_width // 2, initial_y + (button.rect.height + button_spacing) * i)
            button.screen_width = self.initial_screen_width
            button.update_text_size()

    def toggle_resolution_list(self):
        self.show_resolution_list = not self.show_resolution_list
        pygame.mouse.set_visible(True)

        if self.show_resolution_list:
            self.update_buttons_positions()

    def update_settings_background_image(self):
        self.settings_background_image = pygame.transform.scale(self.settings_background_image, (self.initial_screen_width, self.initial_screen_height))

    def update_background_image(self):
        self.background_image = pygame.transform.scale(self.background_image, (self.initial_screen_width, self.initial_screen_height))
        self.screen.blit(self.background_image, self.background_rect)

    def save_settings(self, filename):
        settings_data = {
            'screen_width': self.initial_screen_width,
            'screen_height': self.initial_screen_height,
            'volume': self.volume,
            'difficulty': self.difficulty
        }
        with open(filename, 'wb') as f:
            pickle.dump(settings_data, f)

    def load_settings(self, filename):
        with open(filename, 'rb') as f:
            settings_data = pickle.load(f)
            self.initial_screen_width = settings_data['screen_width']
            self.initial_screen_height = settings_data['screen_height']
            self.volume = settings_data['volume']
            self.difficulty = settings_data.get('difficulty', 'Easy')

    def update_settings(self):
        if os.path.exists('settings_data.txt'):
           self.load_settings('settings_data.txt')
