import pygame
import random
from Utils.settings import *
from pytmx.util_pygame import load_pygame
from Utils.support import *
from Graphics.sprites import Particle

class NPC(pygame.sprite.Sprite):
    def __init__(self, npc_name, pos, groups):
        super().__init__(groups)
        self.sprite_type = 'npc'
        self.import_graphics(npc_name)
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.03
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.npc_name = npc_name
        npc_info = npc_data[self.npc_name]
        self.health = npc_info['health']
        self.attack_damage = npc_info['damage']
        self.task_type = npc_info['task_type']
        self.collision_sprites = pygame.sprite.Group()
        self.z = LAYERS['main']

    def import_graphics(self, name):
        self.animations = {'idle': []}
        main_path = f'../graphics/npc/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self, dt):

        self.animate()

class NpcLayer:
    def __init__(self, all_sprites, collision_sprites):
        
        # sprite groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.npc_sprites = pygame.sprite.Group()

        self.npcs = []

        self.npc_spawned = False

        self.create_soil_grid()
        self.create_hit_rects()


    def spawn(self, player_level):
        if player_level % 2 == 0 and not self.npc_spawned:
            self.npc_()
            self.npc_spawned = True
            print('Good')
        elif player_level % 2 != 0:
            self.npc_spawned = False


    def create_soil_grid(self):
        ground = pygame.image.load('../graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles) ]
        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y , TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def npc_(self):
        possible_positions = [(rect.x // TILE_SIZE, rect.y // TILE_SIZE) for rect in self.hit_rects if 'N' and 'E' and 'C' and 'M' and 'A' and 'B' not in self.grid[rect.y // TILE_SIZE][rect.x // TILE_SIZE]]
        if possible_positions:
            x, y = random.choice(possible_positions)
            self.grid[y][x].append('N')
            self.create_npc(x, y)

    def create_npc(self, x, y):
        npc_name = random.choice(list(npc_data.keys()))
        npc = NPC(
            pos=(x * TILE_SIZE, y * TILE_SIZE), 
            groups=[self.all_sprites, self.collision_sprites, self.npc_sprites],
            npc_name=npc_name,
        )
        self.npcs.append(npc)

    def kill(self):
        for npc in self.npcs:
            Particle(npc.rect.topleft, npc.image, npc.groups()[0], LAYERS['main'], 300)
            npc.kill()
        self.npcs.clear()
        self.npc_sprites.empty()