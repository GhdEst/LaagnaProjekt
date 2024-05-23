import random
import pygame as pg
import sys
from settings import *
from map import *
from player import *
from render import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 24)
        self.delta_time = 1
        self.new_game()
        self.renderer = Renderer(self)
        self.map = Map(self)
        self.bullets = []

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)

    def update(self):
        self.player.update()
        self.map.update()  # Update the map, which updates enemies
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        self.screen.fill('White')
        self.map.draw()
        self.player.draw()

    def check_events(self):
         for event in pg.event.get():
              if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                   pg.quit()
                   sys.exit()

    def run(self):
            while True:
                 self.check_events()
                 self.update()
                 self.draw()
                 self.renderer.render()
                 
                 pg.display.flip()

if __name__ == '__main__':
     game = Game()
     game.run()
