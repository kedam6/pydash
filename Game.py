"""
Module starting a game. It shows menu,
also it is responsible for loading maps and visual effects such as fadeout.
"""

import sys
import pygame
from src.lib import tmx
from src.Player import Player
from src.SpriteLoop import SpriteLoop
from src.LevelCounter import LevelCounter
from src.GameMenu import GameMenu


class Game(object):
    """Game class, it runs whole game"""

    def __init__(self, outerscreen, counter):
        self.screen = outerscreen
        self.counter = counter
        self.tilemap = None
        self.players = None
        self.objects = None
        self.player = None

    def fadeout(self):
        """Animate the screen fading to black for entering a new area"""

        # Get screen options, fill with black
        clock = pygame.time.Clock()
        blackrect = pygame.Surface(self.screen.get_size())
        blackrect.set_alpha(100)
        blackrect.fill((0, 0, 0))

        # Start changing color to make an illusion of animation
        for i in range(0, 5):
            clock.tick(20)
            print i
            self.screen.blit(blackrect, (0, 0))
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

        # Initialize potential animated objects
        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px, cell.py), cell, self.objects)
        # Turns out were missing sprites layer
        except KeyError:
            pass
        else:
            self.tilemap.layers.append(self.objects)

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
        self.startlevel(self.counter.get_current_level() + '.tmx')

        # Game loop
        while True:
            timepassed = clock.tick(70)

            # Await event from user to close level
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            # Update map status
            self.tilemap.update(timepassed, self)
            SCREEN.fill((0, 0, 0))
            self.tilemap.draw(self.screen)
            pygame.display.flip()


if __name__ == '__main__':
    # Prepare screen of game to be shown, set resolution, name and icon
    pygame.init()
    SCREEN = pygame.display.set_mode((1024, 768), 0, 32)
    pygame.display.set_caption("PyDash")
    pygame.display.set_icon(pygame.image.load('sprites/icon.png'))

    # Prepare menu for being shown
    MENU_ITEMS = ('Start', 'Options', 'Quit')
    FUNCTIONS = {'Start': Game(SCREEN, LevelCounter()).main, 'Options': sys.exit, 'Quit': sys.exit}

    # Run game, will do some backgrounds later
    GAME = GameMenu(SCREEN, FUNCTIONS.keys(), FUNCTIONS)
    GAME.run()
