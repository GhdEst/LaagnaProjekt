from settings import *
import pygame as pg
import math
import map

class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.health = 1000000
        self.shoot_cooldown = 1300  # Cooldown time between shots in milliseconds
        self.last_shot_time = 0


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
        if keys[pg.K_SPACE]:
            self.shoot()

    def shoot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_cooldown:
            self.last_shot_time = current_time
            ray_x, ray_y = self.pos
            ray_angle = self.angle

            for _ in range(100):  # Number of steps in the raycast
                ray_x += math.cos(ray_angle)
                ray_y += math.sin(ray_angle)

                map_x, map_y = int(ray_x), int(ray_y)
                if self.game.map.World_map.get((map_x, map_y)) == 1:
                    break

                for enemy in self.game.map.enemies:
                    if enemy.alive and enemy.pos.distance_to((ray_x, ray_y)) < 10:
                        enemy.take_damage(40)
                        return


    def draw(self):
        pass

    def update(self):
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)