"""
Module implementing collectible item in game, it has physics, presentation
Also can kill player if its hit when falling
"""


__author__ = 'Kedam'
import pygame
from random import randint

# pylint: disable=no-member
# code is secure in case that object is not a string

class Collectible(pygame.sprite.Sprite):
    """Collectible class, implements all collectible item needs"""

    def __init__(self, items, rect, game):
        self.cells = items
        self.rect = rect
        self.game = game
        self.moving = False
        self.gone = False
        self.sidemovement = 0
        self.direction = ''

    def __contains__(self, item):
        if item in self.cells:
            return True
        return False

    def __repr__(self):
        return str(self.cells) + str(self.rect)

    def eaten(self):
        """Behaviour after item is eaten by player"""
        for cell in self.cells:
            cell.px = -1000
            cell.py = -1000
            cell.x = -100
            cell.y = -100
            self.gone = True
            self.rect = None

        self.game.music.eatsound()
        self.game.player.score += 1

    def move(self, direction):
        """Move item by [x,y] direction"""
        for item in self.cells:
            item.px += direction[0]
            item.py += direction[1]
            item.x = item.px / 8
            item.y = item.py / 8
        self.rect = self.rect.move(direction[0], direction[1])


    def update(self):
        """Update state of collectible in game"""
        if self.gone:
            pass

        rectright = self.rect.copy().move(64, 0)
        rectleft = self.rect.copy().move(-64, 0)

        resultleft = self.checkitem(rectright)
        resultright = self.checkitem(rectleft)

        rect_up = self.rect.copy().move(0, -64)
        rect_up_left = self.rect.copy().move(-64, -64)
        rect_up_right = self.rect.copy().move(64, -64)

        rect_up = self.checkitem(rect_up)
        rect_up_left = self.checkitem(rect_up_left)
        rect_up_right = self.checkitem(rect_up_right)

        if (resultleft.__class__.__name__ != 'str' and resultleft.moving) or \
                (resultright.__class__.__name__ != 'str' and resultright.moving)\
                or (rect_up.__class__.__name__ != 'str' and rect_up.moving)\
                or (rect_up_left.__class__.__name__ != 'str' and rect_up_left.moving)\
                or (rect_up_right.__class__.__name__ != 'str' and rect_up_right.moving)\
                and self.checkitem(self.rect.copy().move(0, 1)) != "Empty":
            pass

        if self.direction == 'l' or self.direction == 'r':
            if self.direction == 'l':
                self.move((-16, 0))
            elif self.direction == 'r':
                self.move((16, 0))

            self.sidemovement += 1
            if self.sidemovement == 3:
                self.sidemovement = 0
                self.direction = ''
                self.moving = False
            return

        newrect = self.rect.copy()
        newrect = newrect.move(0, 8)

        # Eaten
        self.checkifeaten()

        # Then check if it can fall sideways
        self.updatefallingsideways(rectleft, rectright, newrect)

        # Check gravity
        self.updategravity(newrect)

    def checkifeaten(self):
        """Checks if user is inside this objects rectangle, if it is it calls eaten method"""
        if self.rect.colliderect(self.game.player.rect):
            self.eaten()
            try:
                self.game.collectibles.remove(self)
                return
            except ValueError:
                print 'meh'

    def updatefallingsideways(self, rectleft, rectright, rectdown):
        """Checks if its possible to fall sideways, if it is do that at random"""
        decision = randint(0, 1)

        if decision == 1:
            if self.checkitem(rectright) == "Empty":
                rect_down_right = rectright.move(0, 64)
                if self.checkitem(rect_down_right) == "Empty":
                    result = self.checkitem(rectdown)
                    if not result.__class__.__name__ == 'str':
                        if not result.moving and not self.moving:
                            self.moving = True
                            self.direction = 'r'
                            self.move((16, 0))
        elif decision == 0:
            if self.checkitem(rectleft) == "Empty":
                rect_down_left = rectleft.move(0, 64)
                if self.checkitem(rect_down_left) == "Empty":
                    result = self.checkitem(rectdown)
                    if not result.__class__.__name__ == 'str':
                        if not result.moving and not self.moving:
                            self.moving = True
                            self.direction = 'l'
                            self.move((-16, 0))

    def updategravity(self, newrect):
        """Updates horizontal movement for item"""
        if self.checkitem(newrect) == "Empty":
            self.moving = True
            self.move((0, 8))
        else:
            if self.moving == True and\
                    newrect.colliderect(self.game.player.rect) and self.game.player.orient != "up":
                self.game.music.stopbg()
                self.game.music.deathsound()
                self.game.death()
                self.game.fadeout()
                self.game.startlevel(self.game.counter.get_current_level() + '.tmx')
            else:
                self.moving = False

    def checkitem(self, inp):
        """Checks what is in inp rectangle in game, background is assumed as empty
        Player and world objects are marked as world
        Stones and collectibles are just represented by themselves
        """
        for i in self.game.collectibles:
            if inp.colliderect(i.rect) and i != self:
                return i

        for i in self.game.stones:
            if inp.colliderect(i.rect) and i != self:
                return i

        if len(self.game.tilemap.layers['edible floor'].collide(inp, 'noteaten')) > 0 \
                or inp.colliderect(self.game.player.rect) \
                or len(self.game.tilemap.layers['triggers'].collide(inp, 'solid')) > 0:
            return "World"

        #if self.rect.colliderect(inp):
        #    return "Empty"

        return "Empty"
