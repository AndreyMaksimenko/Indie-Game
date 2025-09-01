import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

import pygame
from Utils.settings import *
from Interface.loadingscreen import LoadingScreen
from Interface.mainmenu import MainMenu
       
class Game:
    def __init__(self):
        pygame.init()
        self.main_menu = MainMenu() 
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Dreamworld')
        self.clock = pygame.time.Clock()
        self.loading_screen = LoadingScreen()
        self.main_menu.load()
        self.loading_complete = False
        self.in_main_menu = False

    def update_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def run_loading_screen(self):
        while not self.loading_complete:
            self.loading_complete = not self.loading_screen.handle_events()
            self.loading_screen.update(self.screen)
            pygame.display.update()

    def run_main_menu(self):
        self.in_main_menu = True
        while self.in_main_menu:
            self.screen.fill((0, 0, 0))     
            button_pressed = self.main_menu.handle_events()
            if button_pressed == 'New Game':
                difficulty = self.main_menu.show_difficulty_menu()
                dt = self.clock.tick() / 1000
                self.main_menu.start_level(dt, difficulty)
                break 
            elif button_pressed == 'Load Game':
                difficulty = self.main_menu.difficulty
                dt = self.clock.tick() / 1000
                self.main_menu.load_level(dt, difficulty)
                break 
            elif button_pressed == 'Settings':
                self.main_menu.show_settings()
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif button_pressed == 'Exit':
                pygame.quit()
                quit()
            else:
                self.main_menu.draw()
                pygame.display.update()


    def run(self):
        self.run_loading_screen()
        self.run_main_menu()


if __name__ == '__main__':
    game = Game()
    game.run()
