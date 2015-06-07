"""
Module implementing stone object, its behaviour, physics and looks
"""

__author__ = 'Kedam'
import pygame
from random import randint

# pylint: disable=no-member
# code is secure in case that object is not a string


class Stone(pygame.sprite.Sprite):
    """Stone class object"""

    def __init__(self, items, rect, game):
        self.cells = items
        self.rect = rect
        self.game = game
        self.moving = False
        self.gone = False
        self.sidemovement = 0
        self.direction = ''
        self.timer = 0

    def __contains__(self, item):
        if item in self.cells:
            return True
        return False

    def __repr__(self):
        return str(self.cells) + str(self.rect)

    def move(self, direction):
        """Moves object in [x,y] direction"""
        for item in self.cells:
            item.px += direction[0]
            item.py += direction[1]
            item.x = item.px / 8
            item.y = item.py / 8
        self.rect = self.rect.move(direction[0], direction[1])

    def checkifstillrolling(self):
        """Checks if object is still rolling, updates move after"""
        if self.timer > 0:
            print self.timer
            print self.direction
            if self.timer < 2:
                if self.direction == 'lu':
                    self.moveleft()
                    return
                elif self.direction == 'ru':
                    self.moveright()
                    return
                else:

                    self.timer = 0
                    self.direction = ''
                    self.moving = False
                    self.game.player.locked = False
                    return
            else:

                self.timer = 0
                self.direction = ''
                self.moving = False
                self.game.player.locked = False
                return

    def update(self):
        """Updates state of object"""
        if self.gone:
            pass

        self.checkifstillrolling()

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
                (resultright.__class__.__name__ != 'str' and resultright.moving) \
                or (rect_up.__class__.__name__ != 'str' and rect_up.moving) \
                or (rect_up_left.__class__.__name__ != 'str' and rect_up_left.moving) \
                or (rect_up_right.__class__.__name__ != 'str' and rect_up_right.moving) \
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
        newrect = newrect.move(0, 4)

        self.updatesideways(rectleft, rectright, newrect)

        # Check gravity
        self.checkgravity(newrect)

        self.checksolid()

    def updatesideways(self, rectleft, rectright, newrect):
        """Checks if object has to fall or not"""
        decision = randint(0, 1)

        if decision == 1:
            if self.checkitem(rectright) == "Empty":
                rect_down_right = rectright.move(0, 64)
                if self.checkitem(rect_down_right) == "Empty":
                    result = self.checkitem(newrect)
                    if not result.__class__.__name__ == 'str':
                        if not result.moving and not self.moving:
                            self.moving = True
                            self.direction = 'r'
                            self.move((16, 0))
        elif decision == 0:
            if self.checkitem(rectleft) == "Empty":
                rect_down_left = rectleft.move(0, 64)
                if self.checkitem(rect_down_left) == "Empty":
                    result = self.checkitem(newrect)
                    if not result.__class__.__name__ == 'str':
                        if not result.moving and not self.moving:
                            self.moving = True
                            self.direction = 'l'
                            self.move((-16, 0))

    def checksolid(self):
        """Check solid factor of stone"""
        rect = self.game.player.rect.copy()
        rect.x += 1
        rect.width = 62
        if self.rect.colliderect(rect):
            if self.game.player.orient == "left":
                self.game.player.rect.x += self.game.player.movementspeed
                if self.rect.y == rect.y:
                    self.moveleft()
                    self.direction = 'lu'
            elif self.game.player.orient == "right":
                self.game.player.rect.x -= self.game.player.movementspeed
                if self.rect.y == rect.y:
                    self.moveright()
                    self.direction = 'ru'
            elif self.game.player.orient == "up":
                self.game.player.rect.y += self.game.player.movementspeed
            elif self.game.player.orient == "down":
                self.game.player.rect.y -= self.game.player.movementspeed

    def checkgravity(self, newrect):
        """Checks what object has to do in case of gravity"""
        if self.checkitem(newrect) == "Empty":
            self.moving = True
            self.move((0, 4))
            self.direction = 'd'
        else:
            if self.moving == True and \
                    newrect.colliderect(self.game.player.rect) and \
                            self.direction == 'd' and \
                            self.game.player.orient != "up":
                self.game.music.stopbg()
                self.game.music.deathsound()
                self.game.death()
                self.game.fadeout()
                self.game.startlevel(self.game.counter.get_current_level() + '.tmx')
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
                or len(self.game.tilemap.layers['triggers'].collide(inp, 'solid')) > 0:
            return "World"

        if inp.colliderect(self.game.player.rect):
            return "Player"

        return "Empty"

    def moveleft(self):
        """Moves item and player to left"""
        if self.timer > 0:
            self.timer += 1
            self.move((-8, 0))
            self.game.player.rect.x -= 8
        else:
            rect = self.rect.copy().move(-8, 0)
            if self.checkitem(rect) == "Empty" or self.checkitem(rect) == "Player":
                self.moving = True
                self.move((-8, 0))
                self.game.player.rect.x -= 8
                self.timer = 1
                self.game.player.locked = True

    def moveright(self):
        """Moves item and player to right"""
        if self.timer > 0:
            self.timer += 1
            self.move((8, 0))
            self.game.player.rect.x += 8
        else:
            rect = self.rect.copy().move(8, 0)
            if self.checkitem(rect) == "Empty" or self.checkitem(rect) == "Player":
                self.moving = True
                self.move((8, 0))
                self.game.player.rect.x += 8
                self.timer = 1
                self.game.player.locked = True
