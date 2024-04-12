import pygame as pg
from settings import *

class Renderer:
    def __init__(self, game):
        self.game = game

    def render(self):
        # Clear the screen
        self.game.screen.fill('black')

        # Draw the map
        self.game.map.draw()

        # Draw the player
        self.game.player.draw()

        # Update the display
        pg.display.flip()