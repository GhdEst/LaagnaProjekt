_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

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
            ray_angle = self.game.player.angle - (FOV / 2) + (ray * FOV / RAYS)

        # Initialize the ray's position to the player's position
            ray_x, ray_y = self.game.player.pos

        # Step the ray forward until it hits a wall
            while self.World_map.get((int(ray_x), int(ray_y))) != 1:
                ray_x += math.cos(ray_angle)
                ray_y += math.sin(ray_angle)

        # Calculate the distance to the wall
            dist_to_wall = math.hypot(ray_x - self.game.player.pos[0], ray_y - self.game.player.pos[1])

        # Calculate the height of the wall slice
            wall_height = RES[1] / (dist_to_wall if dist_to_wall > 0 else 0.00001)

        # Calculate the color of the wall slice based on the distance
            color = 135 / (1 + dist_to_wall * dist_to_wall * 0.00002)
            color = (color, color, color)

        # Draw the wall slice
            pg.draw.rect(self.game.screen, color, (ray * RES[0] / RAYS, RES[1] / 2 - wall_height / 2, RES[0] / RAYS, wall_height))

    def draw(self):
        # ... (draw the map here) ...


        
            self.raycast(self.game.player)
