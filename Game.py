import pygame
import tmx
from src.Player import Player
from src.SpriteLoop import SpriteLoop
from src.LevelCounter import LevelCounter


class Game(object):
    def __init__(self, screen, counter):
        self.screen = screen
        self.counter = counter
    
    def fadeOut(self):
        """Animate the screen fading to black for entering a new area"""
        clock = pygame.time.Clock()
        blackRect = pygame.Surface(self.screen.get_size())
        blackRect.set_alpha(100)
        blackRect.fill((0,0,0))
        # Continuously draw a transparent black rectangle over the screen
        # to create a fadeout effect
        for i in range(0,5):
            clock.tick(15)
            self.screen.blit(blackRect, (0,0))  
            pygame.display.flip()
        clock.tick(15)
        screen.fill((255,255,255,50))
        pygame.display.flip()
        
    def initArea(self, mapFile):
        """Load maps and initialize sprite layers for each new area"""
        self.tilemap = tmx.load(mapFile, screen.get_size())
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        # Initializing other animated sprites
        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px,cell.py), cell, self.objects)
        # In case there is no sprite layer for the current map
        except KeyError:
            pass
        else:
            self.tilemap.layers.append(self.objects)
        # Initializing player sprite
        startCell = self.tilemap.layers['triggers'].find('playerStart')[0]
        self.player = Player((startCell.px, startCell.py), 
                             startCell['playerStart'], self.players)
        self.tilemap.layers.append(self.players)
        self.tilemap.set_focus(self.player.rect.x, self.player.rect.y)

            
    def main(self):
        clock = pygame.time.Clock()
        self.initArea(self.counter.getcurrentlevel() + '.tmx')
        
        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.tilemap.update(dt, self)
            screen.fill((0,0,0))
            self.tilemap.draw(self.screen)
            pygame.display.flip()




if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("PyDash")
    pygame.display.set_icon(pygame.image.load('sprites/icon.png'))
    Game(screen, LevelCounter()).main()