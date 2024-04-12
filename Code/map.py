#import pygame as pg
#
_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, 1],
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
]

#class Map:
#    def __init__(self, game) -> None:
#        self.game = game
#        self.mini_map = mini_map
#        self.World_map = {}
#        self.get_map()
#
#    def get_map(self):
#        for j, row in enumerate(self.mini_map):
#            for i, value in enumerate(row):
#                if value:
#                    self.World_map[(i, j)] = value    
#
#   def draw(self):
#      [pg.draw.rect(self.game.screen, 'lightgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
#        for pos in self.World_map] 
#"

import math
import pygame as pg
from settings import *

# Constants
FOV = math.pi / 4  # Field of View
RAYS = 100  # Number of rays to cast



class Map:
    # ... (rest of your Map class here) ...
    def __init__(self, game) -> None:
        self.game = game
        self.mini_map = mini_map
        self.World_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.World_map[(i, j)] = value    

    def raycast(self, player):
        for ray in range(RAYS):
        # Calculate the angle at which to cast this ray
            ray_angle = PLAYER_ANGLE - (FOV / 2) + (ray * FOV / RAYS)

        # Initialize the ray's position to the player's position
            ray_x, ray_y = PLAYER_POS

        # Step the ray forward until it hits a wall
            while self.World_map.get((int(ray_x), int(ray_y))) != 1:
                ray_x += math.cos(ray_angle)
                ray_y += math.sin(ray_angle)

        # Calculate the distance to the wall
            dist_to_wall = math.hypot(ray_x - PLAYER_POS[0], ray_y - PLAYER_POS[1])

        # Calculate the height of the wall slice
            wall_height = RES[1] / (dist_to_wall if dist_to_wall > 0 else 0.00001)

        # Calculate the color of the wall slice based on the distance
            color = 255 / (1 + dist_to_wall * dist_to_wall * 0.00002)
            color = (color, color, color)

        # Draw the wall slice
            pg.draw.rect(self.game.screen, color, (ray * RES[0] / RAYS, RES[1] / 2 - wall_height / 2, RES[0] / RAYS, wall_height))

    def draw(self):
        # ... (draw the map here) ...
            [pg.draw.rect(self.game.screen, 'lightgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
            for pos in self.World_map]

        
            self.raycast(self.game.player)
