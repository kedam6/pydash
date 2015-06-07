"""
Module starting a game. It shows menu,
also it is responsible for loading maps and visual effects such as fadeout.
"""

import sys
import pygame
import src.Options
from src import tmx
from src import Player
from src import LevelCounter
from src import GameMenu
from src import Collectible
from src import Stone
from src import SoundPlayer

# pylint: disable=no-member
# pygame has these members, just pycharm doesnt see them
# pylint: disable=too-many-function-args
# pylint thinks that a single pygame.Rect object is too large for constructor
# pylint: disable=unused-variable
# pylint thinks that iterator in for loop is useless, it is not


class Game(object):
    """Game class, it runs whole game"""

    def __init__(self, outerscreen, counter):
        self.screen = outerscreen
        self.counter = counter
        self.tilemap = None
        self.players = None
        self.objects = None
        self.player = None
        self.collectibles = []
        self.stones = []
        self.music = SoundPlayer()

    def fadeout(self):
        """Animate the screen fading to black for entering a new area"""

        # Get screen options, fill with black
        clock = pygame.time.Clock()

        self.music.startsound()

        blackrect = pygame.Surface(self.screen.get_size())
        blackrect.set_alpha(100)
        blackrect.fill((0, 0, 0))

        # Start changing color to make an illusion of animation
        for i in range(0, 20):
            clock.tick(20)
            self.screen.blit(blackrect, (0, 0))
            pygame.display.flip()

        myfont = pygame.font.SysFont("Arial", 80)
        label = myfont.render("Level " + str(self.counter.count), 1, (255, 255, 0))
        textpos = label.get_rect()
        textpos.centerx = blackrect.get_rect().centerx
        textpos.centery = blackrect.get_rect().centery
        self.screen.blit(label, textpos)
        pygame.display.flip()

        pygame.time.wait(1000)

        blackrect = pygame.Surface(self.screen.get_size())
        blackrect.set_alpha(50)
        blackrect.fill((0, 0, 0))

        # Start changing color to make an illusion of animation
        for i in range(1, 20):
            clock.tick(20)
            self.screen.blit(blackrect, (0, 0))
            pygame.display.flip()

        # Then release color
        clock.tick(15)
        SCREEN.fill((255, 255, 255, 50))
        pygame.display.flip()

        self.music.playbg()

    def death(self):
        """Animate screen after death"""
        # Get screen options, fill with black
        clock = pygame.time.Clock()
        redrect = pygame.Surface(self.screen.get_size())
        redrect.set_alpha(100)
        redrect.fill((255, 0, 0))

        # Start changing color to make an illusion of animation
        for i in range(0, 5):
            clock.tick(20)
            print i
            self.screen.blit(redrect, (0, 0))
            pygame.display.flip()

        # Then release color
        clock.tick(15)
        SCREEN.fill((255, 255, 255, 50))
        pygame.display.flip()

    def startlevel(self, map_filename):
        """Load maps and initialize sprite layers for each new area"""

        self.tilemap = tmx.load(map_filename, SCREEN.get_size())
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        self.collectibles = []
        self.stones = []



        for i, cell in self.tilemap.layers['items'].cells.items():
            if 'collectible' in cell.tile.properties and cell.tile.properties['collectible'] == 2:
                items = [cell,
                         self.tilemap.layers['items'].cells[(cell.x + 1, cell.y)],
                         self.tilemap.layers['items'].cells[(cell.x, cell.y + 1)],
                         self.tilemap.layers['items'].cells[(cell.x + 1, cell.y + 1)]]
                self.collectibles.append(
                    Collectible(items, pygame.Rect(cell.px, cell.py, 64, 64), self)
                    )
            elif 'stone' in cell.tile.properties and cell.tile.properties['stone'] == 2:
                items = [cell,
                         self.tilemap.layers['items'].cells[(cell.x + 1, cell.y)],
                         self.tilemap.layers['items'].cells[(cell.x, cell.y + 1)],
                         self.tilemap.layers['items'].cells[(cell.x + 1, cell.y + 1)]]
                self.stones.append(Stone(items, pygame.Rect(cell.px, cell.py, 64, 64), self))

        # Initialize player sprite
        # Get player's start position, the first one from (0,0)
        startcell = self.tilemap.layers['triggers'].find('playerStart')[0]
        self.player = Player((startcell.px, startcell.py), startcell['playerStart'], self.players)
        # Update with new layer, get player inside that layer and focus on player at all cost
        self.tilemap.layers.append(self.players)
        self.tilemap.set_focus(self.player.rect.x, self.player.rect.y)

    def main(self):
        """Method responsible for running game"""

        # Start loading level from tmx file
        clock = pygame.time.Clock()
        self.fadeout()
        self.startlevel(self.counter.get_current_level() + '.tmx')

        # Game loop
        while True:
            timepassed = clock.tick(60)

            # Await event from user to close level
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.music.stopbg()
                    return

            # Update map status
            self.tilemap.update(timepassed, self)
            SCREEN.fill((0, 0, 0))
            for item in self.collectibles:
                item.update()
            for item in self.stones:
                item.update()
            self.tilemap.draw(self.screen)
            pygame.display.flip()


if __name__ == '__main__':
    # Prepare screen of game to be shown, set resolution, name and icon
    pygame.init()
    SCREEN = pygame.display.set_mode(
        [(640, 480), (800, 600), (1024, 768)][src.Options.CONFIG.resolution],
        0,
        32)
    pygame.display.set_caption("PyDash")
    pygame.display.set_icon(pygame.image.load('sprites/icon.png'))
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()

    # Prepare menu for being shown and run it
    GameMenu(SCREEN,
             {'Start': Game(SCREEN, LevelCounter()).main,
              'Options': src.Options.main,
              'Quit': sys.exit}).run()
