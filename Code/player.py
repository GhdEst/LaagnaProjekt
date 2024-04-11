from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        pass

    def update(self):
        self.movement()