F = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],    
    [1, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, 1],
    [1, F, F, 1, 1, 1, 1, F, F, F, 1, 1, 1, F, F, F, F, F, F, F, F, 1],
    [1, F, F, F, F, F, 1, F, F, F, F, F, 1, F, F, F, F, F, F, F, F, 1],
    [1, F, F, F, F, F, 1, F, F, F, F, F, 1, F, F, F, F, F, F, F, F, 1],
    [1, F, F, 1, 1, 1, 1, F, F, F, F, F, F, F, F, F, F, F, F, F, F, 1],
    [1, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, 1],
    [1, F, F, F, 1, F, F, F, 1, F, F, F, F, F, F, F, F, F, F, F, F, 1],
    [1, F, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, F, F, F, F, F, F, F, F, 1],
    [1, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, 1],
    [1, F, F, 1, 1, 1, 1, F, F, F, 1, 1, 1, F, F, F, F, F, F, F, F, 1],
    [1, F, F, F, F, F, 1, F, F, F, F, F, 1, F, F, F, F, F, F, F, F, 1],
    [1, F, F, F, F, F, 1, F, F, F, F, F, 1, F, F, F, F, F, F, F, F, 1],
    [1, F, F, 1, 1, 1, 1, F, F, F, F, F, F, F, F, F, F, F, F, F, F, 1],
    [1, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, 1],
    [1, F, F, F, 1, F, F, F, 1, F, F, F, F, F, F, F, F, F, F, F, F, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

import math
import random
import pygame as pg
from settings import *
from enemy import Enemy

FOV = (math.pi / 4)
RAYS = 100
EPSILON = 1e-6

class Map:
    def __init__(self, game) -> None:
        self.game = game
        self.mini_map = mini_map
        self.World_map = {}
        self.enemies = [Enemy(game, (5, 5), speed=0.0005, attack_distance=1.05, damage=10, attack_cooldown=1000)]
        self.get_map()
        self.spawn_enemies()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.World_map[(i, j)] = value    

    def raycast(self, player):
        wall_slices = []
        
        for ray in range(RAYS):
            ray_angle = player.angle - (FOV / 2) + (ray * FOV / RAYS)
            ray_angle = ray_angle % (2 * math.pi)

            ray_x, ray_y = player.pos
            map_x, map_y = int(ray_x), int(ray_y)

            delta_dist_x = abs(1 / (math.cos(ray_angle) + EPSILON))
            delta_dist_y = abs(1 / (math.sin(ray_angle) + EPSILON))

            if math.cos(ray_angle) < 0:
                step_x = -1
                side_dist_x = (ray_x - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1.0 - ray_x) * delta_dist_x

            if math.sin(ray_angle) < 0:
                step_y = -1
                side_dist_y = (ray_y - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y + 1.0 - ray_y) * delta_dist_y

            hit = False
            while not hit:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1

                if self.World_map.get((map_x, map_y)) == 1:
                    hit = True

            if side == 0:
                dist_to_wall = (map_x - ray_x + (1 - step_x) / 2) / math.cos(ray_angle)
            else:
                dist_to_wall = (map_y - ray_y + (1 - step_y) / 2) / math.sin(ray_angle)

            wall_height = RES[1] / (dist_to_wall if dist_to_wall > 0 else 0.00001)
            color_intensity = max(min(255 / (dist_to_wall if dist_to_wall > 0 else 0.00001), 255), 0)
            color = (color_intensity, color_intensity, color_intensity)
            x = ray * RES[0] / RAYS

            wall_slices.append((x, RES[1] / 2 - wall_height / 2, RES[1] / 2 + wall_height / 2, color))

        for i in range(len(wall_slices) - 1):
            x1, y1_top, y1_bottom, color1 = wall_slices[i]
            x2, y2_top, y2_bottom, color2 = wall_slices[i + 1]
            top_polygon = [(x1, y1_top), (x2, y2_top), (x2, y1_top), (x1, y1_top)]
            bottom_polygon = [(x1, y1_bottom), (x2, y1_bottom), (x2, y2_bottom), (x1, y1_bottom)]
            pg.draw.polygon(self.game.screen, color1, top_polygon)
            pg.draw.polygon(self.game.screen, color1, bottom_polygon)

    def spawn_enemies(self):
        possible_positions = [(x, y) for y in range(len(self.mini_map)) for x in range(len(self.mini_map[y])) if self.mini_map[y][x] == False]
        if possible_positions:
            spawn_pos = random.choice(possible_positions)
            self.enemies.append(Enemy(self.game, pg.Vector2(spawn_pos), 0.005, 1.05, 10, 1000))  # Ensure spawn_pos is a pg.Vector2

    def update(self):
        for enemy in self.enemies:
            enemy.update()

    def draw(self):
        self.raycast(self.game.player)
        for enemy in self.enemies:
            enemy.draw()
