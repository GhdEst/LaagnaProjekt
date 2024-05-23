import math
import pygame as pg
from settings import *
from map import *

FOV = (math.pi / 4)

class Enemy:
    def __init__(self, game, pos, speed, attack_distance, damage):
        self.game = game
        self.pos = pg.Vector2(pos)  # Ensure pos is a pg.Vector2
        self.speed = speed
        self.attack_distance = attack_distance
        self.damage = damage
        self.attack_cooldown = attack_cooldown
        self.last_attack_time = 0
        self.alive = True
        self.health = 100

    def update(self):
        if self.alive:
            self.move_towards_player()
            self.check_attack()

    def move_towards_player(self):
        player_pos = pg.Vector2(self.game.player.pos)  # Ensure player_pos is a pg.Vector2
        direction = (player_pos - self.pos).normalize()
        next_pos = self.pos + direction * self.speed * self.game.delta_time


        if not self.check_collision(next_pos):
            self.pos = next_pos

    def check_collision(self, next_pos):
        map_x, map_y = int(next_pos.x), int(next_pos.y)
        if self.game.map.World_map.get((map_x, map_y)) == 1:
            return True
        return False

    def check_attack(self):
        if self.pos.distance_to(pg.Vector2(self.game.player.pos)) < self.attack_distance:
            self.attack()

    def attack(self):
        self.game.player.health -= self.damage
        print(f"Player health: {self.game.player.health}")

        player_pos = pg.Vector2(self.game.player.pos)
        direction = (self.pos - player_pos).normalize()
        self.pos += direction * self.attack_distance / 2

    def draw(self):
        if self.alive:
            player = self.game.player
            player_pos = pg.Vector2(player.pos)  # Ensure player_pos is a pg.Vector2
            dx = self.pos.x - player_pos.x
            dy = self.pos.y - player_pos.y
            distance = math.sqrt(dx * dx + dy * dy)
            angle = math.atan2(dy, dx) - player.angle

            if angle < -math.pi:
                angle += 2 * math.pi
            if angle > math.pi:
                angle -= 2 * math.pi

            if not -FOV / 2 < angle < FOV / 2:
                return

            if not self.is_visible(player, distance):
                return

            projected_height = min(int(RES[1] / (distance * math.cos(angle))), RES[1])

            screen_x = int(RES[0] / 2 + angle * RES[0] / FOV)
            top = int(RES[1] / 2 - projected_height / 2)
            bottom = int(RES[1] / 2 + projected_height / 2)

            enemy_size = 200
            screen_pos = (screen_x, bottom - enemy_size)
            pg.draw.rect(self.game.screen, (255, 0, 0), (screen_pos, (enemy_size / 2, enemy_size)))

    def is_visible(self, player, distance):
        ray_x, ray_y = player.pos
        enemy_x, enemy_y = self.pos
        angle = math.atan2(enemy_y - ray_y, enemy_x - ray_x)
        
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        for i in range(int(distance)):
            ray_x += cos_angle
            ray_y += sin_angle
            if self.game.map.World_map.get((int(ray_x), int(ray_y))) == 1:
                return False
        return True

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
