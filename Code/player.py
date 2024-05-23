from settings import *
import pygame as pg
import math
import map
from enemy import *

class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.health = 1000000
        self.shoot_cooldown = 500  # Cooldown time between shots in milliseconds
        self.last_shot_time = 0
        self.kills = 0

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
            bullet = Bullet(self.game, self.x + math.cos(self.angle) * 30, self.y + math.sin(self.angle) * 30, self.angle)
            self.game.bullets.append(bullet)

    def draw(self):
        pass

    def update(self):
        self.movement()

        bullets_to_remove = []
        for bullet in self.game.bullets:
            distance = math.sqrt((self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2)
            if distance < BULLET_HIT_RADIUS:
                for enemy in self.game.map.enemies:
                    enemy_rect = pg.Rect(enemy.pos.x - enemy_rect / 2, enemy.pos.y - enemy_rect / 2, enemy_rect, enemy_rect)
                    if enemy_rect.colliderect(bullet.rect):
                        enemy.take_damage(BULLET_DAMAGE)
                        bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            self.game.bullets.remove(bullet)

        for bullet in self.game.bullets:
            bullet.update()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

class Bullet:
    def __init__(self, game, x, y, angle):
        self.game = game
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.alive = True
        self.rect = pg.Rect(self.x, self.y, BULLET_SIZE, BULLET_SIZE)

    def update(self):
        if self.alive:
            self.move()
            self.check_collision()

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.rect.center = (self.x, self.y)

    def check_collision(self):
        # Check collision with map or enemies
        if self.is_offscreen() or self.collides_with_enemy():
            self.alive = False

    def is_offscreen(self):
        return not RES.colliderect(self.rect)

    def collides_with_enemy(self):
        for enemy in self.game.map.enemies:
            enemy_rect = pg.Rect(enemy.pos.x - enemy_rect / 2, enemy.pos.y - enemy_rect / 2, enemy_rect, enemy_rect)
            if enemy_rect.colliderect(self.rect):
                enemy.take_damage(BULLET_DAMAGE)
                return True
        return False

    def draw(self):
        pg.draw.rect(self.game.screen, BULLET_COLOR, self.rect)

    def should_remove(self):
        return not self.alive
