from settings import *
import pygame as pg
import math
from map import *

class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos  
        if keys[pg.K_a]:
            dx += speed_sin  
            dy -= speed_cos  

        self.x += dx
        self.y += dy

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

        next_x = self.x + dx
        next_y = self.y + dy

        if (self.game.map.World_map.get((int(next_x), int(next_y))) != 1 and 0 <= next_x < len(self.game.map.mini_map[0]) and 0 <= next_y < len(self.game.map.mini_map)):


            self.x = next_x
            self.y = next_y


    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIDTH * math.cos(self.angle),
                      self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)