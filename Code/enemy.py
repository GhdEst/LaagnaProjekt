import math
import pygame as pg

class Enemy:
    def __init__(self, game, pos, speed, attack_distance, damage):
        self.game = game
        self.pos = pg.Vector2(pos)
        self.speed = speed
        self.attack_distance = attack_distance
        self.damage = damage
        self.alive = True
        self.health = 100

    def update(self):
        if self.alive:
            self.move_towards_player()
            self.check_attack()

    def move_towards_player(self):
        player_pos = self.game.player.pos
        direction = (player_pos - self.pos).normalize()
        self.pos += direction * self.speed * self.game.delta_time

    def check_attack(self):
        if self.pos.distance_to(self.game.player.pos) < self.attack_distance:
            self.attack()

    def attack(self):
        # Inflict damage to the player
        self.game.player.health -= self.damage
        print(f"Player health: {self.game.player.health}")

    def draw(self):
        if self.alive:
            screen_pos = (int(self.pos.x * self.game.tile_size), int(self.pos.y * self.game.tile_size))
            pg.draw.circle(self.game.screen, (255, 0, 0), screen_pos, 10)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
