import pygame
from Utils.settings import *
from Utils.support import *
from pytmx.util_pygame import load_pygame
import uuid
from Entities.animals import ChickenTile, CowTile

class HouseTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, hitbox, name, id):
        super().__init__(groups)
        self.image  = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['main']
        self.hitbox = hitbox
        self.name = name
        self.id = id

    def get_state(self):
        return {
            'pos': self.rect.topleft,
            'name': self.name,
            'id': self.id,
            'tile_type': 'chickenhouse'
        }

    @classmethod
    def from_state(cls, state, surfs):
        pos = state['pos']
        tile_type = state['tile_type']
        surf = surfs[tile_type]
        hitbox = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
        return cls(
            pos=pos,
            surf=surf,
            groups=[],
            hitbox=hitbox,
            name=state['name'],
            id=state['id']
        )
    
class CowHouseTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, hitbox, name, id):
        super().__init__(groups)
        self.image  = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['main']
        self.hitbox = hitbox
        self.name = name
        self.id = id

    def get_state(self):
        return {
            'pos': self.rect.topleft,
            'name': self.name,
            'id': self.id,
            'tile_type': 'cowhouse'
        }

    @classmethod
    def from_state(cls, state, surfs):
        pos = state['pos']
        tile_type = state['tile_type']
        surf = surfs[tile_type]
        hitbox = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
        return cls(
            pos=pos,
            surf=surf,
            groups=[],
            hitbox=hitbox,
            name=state['name'],
            id=state['id']
        )
    
class BuildingLayer:
    def __init__(self, all_sprites, collision_sprites, chicken_house = [], cow_house = [], chicken_relations = {}, cow_relations = {}):
        
        # sprite groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.building_sprites = pygame.sprite.Group()
        self.chicken_sprites = pygame.sprite.Group()
        self.cow_sprites = pygame.sprite.Group()

        self.building_surfs = import_folder_dict('../graphics/buildings')
        self.available_buildings = ['chickenhouse', 'cowhouse']
        self.selected_building_index = 0

        self.building_images = {
            'chickenhouse': pygame.image.load('../graphics/buildings/chickenhouse.png'),
            'cowhouse': pygame.image.load('../graphics/buildings/cowhouse.png')
        }

        self.create_soil_grid()
        self.create_hit_rects()

        self.chicken_houses = chicken_house
        self.cow_houses = cow_house
        self.max_chickens = 3
        self.max_cows = 2
        self.chicken_counts = {}
        self.cow_counts = {}

        self.chicken_relations = chicken_relations
        self.cow_relations = cow_relations

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

    
    def chicken_house(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):        
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    if 'C' not in self.grid[y][x]:
                        if 'M' not in self.grid[y][x]:
                            self.grid[y][x].append('C')
                            self.create_chicken_house()

    def cow_house(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):        
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    if 'M' not in self.grid[y][x]:
                        if 'C' not in self.grid[y][x]:
                               self.grid[y][x].append('M')
                               self.create_cow_house()

    def create_chicken_house(self):
        self.building_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'C' in cell:

                    tile_type = 'chickenhouse'
                    building_id = str(uuid.uuid4())
                    print(f"Generated building_id: {building_id}")

                    if building_id not in self.chicken_relations:
                        chicken_house = HouseTile(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE), 
                        surf = self.building_surfs[tile_type], 
                        groups = [self.all_sprites, self.building_sprites, self.collision_sprites],
                        hitbox = pygame.Rect(index_col * TILE_SIZE, index_row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                        name = 'ChickenHouse',
                        id = building_id
                        )
                        self.chicken_houses.append(chicken_house)
                        self.chicken_relations[building_id] = []
                        print(f"Added building_id: {building_id} to self.chicken_relations")
                        print(f"Saved building_id: {building_id} ")


    def create_cow_house(self):
     self.building_sprites.empty()
     for index_row, row in enumerate(self.grid):
        for index_col, cell in enumerate(row):
            if 'M' in cell:
                tile_type = 'cowhouse'
                building_cow_id = str(uuid.uuid4())
                print(f"Generated building_cow_id: {building_cow_id}")

                if building_cow_id not in self.cow_relations:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE

                    width = TILE_SIZE * 3 - 5
                    height = TILE_SIZE * 3 - 5

                    cow_house = CowHouseTile(
                        pos=(x, y),
                        surf=self.building_surfs[tile_type],
                        groups=[self.all_sprites, self.building_sprites, self.collision_sprites],
                        hitbox=pygame.Rect(x, y, width, height),
                        name='CowHouse',
                        id=building_cow_id
                    )
                    self.cow_houses.append(cow_house)
                    self.cow_relations[building_cow_id] = []
                    print(f"Added building_cow_id: {building_cow_id} to self.cow_relations")
                    print(f"Saved building_cow_id: {building_cow_id}")

    def switch_building(self):
        self.selected_building_index = (self.selected_building_index + 1) % len(self.available_buildings)
        selected_building = self.available_buildings[self.selected_building_index]
        print(f"Selected building: {selected_building}")
                    

    def save_objects_chicken(self):
        objects_data = [obj.get_state() for obj in self.chicken_houses]
        with open('objects_chicken.txt', 'wb') as f:
            pickle.dump(objects_data, f)
        print("All chicken houses have been saved.")

    def save_objects_cow(self):
        objects_data = [obj.get_state() for obj in self.cow_houses]
        with open('objects_cow.txt', 'wb') as f:
            pickle.dump(objects_data, f)
        print("All cow houses have been saved.")


    def load_objects_chicken(self):
        try:
            with open('objects_chicken.txt', 'rb') as f:
                objects_data = pickle.load(f)
                created_objects = [self.create_object_from_state_chicken(data) for data in objects_data]
            for obj in created_objects:
                obj.add(self.all_sprites, self.collision_sprites)
                if isinstance(obj, HouseTile):
                    obj.add(self.building_sprites)
                    if obj.id not in self.chicken_relations:
                        self.chicken_relations[obj.id] = []
                elif isinstance(obj, ChickenTile):
                    obj.add(self.chicken_sprites)
                    
            print("Loaded objects successfully.")
            print("Loaded ChickenHouse objects:", [obj.id for obj in self.chicken_houses if obj.name == 'ChickenHouse'])
        except FileNotFoundError:
            print("No saved objects found. Starting with an empty list.")
            self.chicken_houses = []

    def load_objects_cow(self):
     try:
        with open('objects_cow.txt', 'rb') as f:
            objects_data = pickle.load(f)
            created_objects = [self.create_object_from_state_cow(data) for data in objects_data if data['name'] in ['CowHouse', 'Cow']]
        for obj in created_objects:
            if obj is not None:
                obj.add(self.all_sprites, self.collision_sprites)
                if isinstance(obj, CowHouseTile):
                    obj.add(self.building_sprites)
                    if obj.id not in self.cow_relations:
                        self.cow_relations[obj.id] = []
                elif isinstance(obj, CowTile):
                    obj.add(self.cow_sprites)
                    
        print("Loaded objects successfully.")
        print("Loaded CowHouse objects:", [obj.id for obj in self.cow_houses if obj.name == 'CowHouse'])
     except FileNotFoundError:
        print("No saved objects found. Starting with an empty list.")
        self.cow_houses = []


    def create_object_from_state_chicken(self, state):
     if state['name'] == 'ChickenHouse':
        return HouseTile(
            pos=state['pos'],
            surf=self.building_surfs[state['tile_type']],
            groups=[self.all_sprites, self.building_sprites, self.collision_sprites],
            hitbox=pygame.Rect(*state['pos'], TILE_SIZE, TILE_SIZE),
            name=state['name'],
            id=state['id']
        )
     elif state['name'] == 'Chicken':
        return ChickenTile(
            pos=state['pos'],
            groups=[self.all_sprites, self.chicken_sprites],
            name=state['name'],
            building_id=state['building_id'],
            chicken_id=state['chicken_id'],
            fed=state['fed'],
            feed_interval=state['feed_interval'],
            last_fed_time=state['last_fed_time']
        )
     else:
        print(f"Unknown object type encountered: {state['name']}")
        return None
    
    def create_object_from_state_cow(self, state):
     if state['name'] == 'CowHouse':
        return CowHouseTile(
            pos=state['pos'],
            surf=self.building_surfs[state['tile_type']],
            groups=[self.all_sprites, self.building_sprites, self.collision_sprites],
            hitbox=pygame.Rect(*state['pos'], TILE_SIZE, TILE_SIZE),
            name=state['name'],
            id=state['id']
        )
     elif state['name'] == 'Cow':
        return CowTile(
            pos=state['pos'],
            groups=[self.all_sprites, self.chicken_sprites],
            name=state['name'],
            building_id=state['building_id'],
            cow_id=state['cow_id'],
            fed=state['fed'],
            feed_interval=state['feed_interval'],
            last_fed_time=state['last_fed_time']
        )
     else:
        print(f"Unknown object type encountered: {state['name']}")
        return None