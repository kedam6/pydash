__author__ = 'Kedam'
import pygame
from random import randint
import src.Player

class Stone(pygame.sprite.Sprite):

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
        for item in self.cells:
            item.px += direction[0]
            item.py += direction[1]
            item.x = item.px / 8
            item.y = item.py / 8
        self.rect = self.rect.move(direction[0], direction[1])

    def update(self):
        if self.gone:
            pass
        if self.timer > 0:
            print self.timer
            print self.direction
            if self.timer < 4:
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


        rectright = self.rect.copy().move(64, 0)
        rectleft = self.rect.copy().move(-64, 0)

        resultleft = self.checkitem(rectright)
        resultright = self.checkitem(rectleft)

        rectup = self.rect.copy().move(0, -64)
        rectUL = self.rect.copy().move(-64, -64)
        rectUR = self.rect.copy().move(64, -64)

        rectup = self.checkitem(rectup)
        rectUL = self.checkitem(rectUL)
        rectUR = self.checkitem(rectUR)

        if (resultleft.__class__.__name__ != 'str' and resultleft.moving ) or \
                (resultright.__class__.__name__ != 'str' and resultright.moving )\
                or (rectup.__class__.__name__ != 'str' and rectup.moving)\
                or (rectUL.__class__.__name__ != 'str' and rectUL.moving )\
                or (rectUR.__class__.__name__ != 'str' and rectUR.moving )\
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

        # Eaten


        decision = randint(0, 1)

        if decision == 1:
            if self.checkitem(rectright) == "Empty":
                rectDR = rectright.move(0,64)
                if self.checkitem(rectDR) == "Empty":
                    result = self.checkitem(newrect)
                    if not result.__class__.__name__ == 'str':
                        if not result.moving and not self.moving:
                            self.moving = True
                            self.direction = 'r'
                            self.move((16, 0))
        elif decision == 0:
            if self.checkitem(rectleft) == "Empty":
                rectDL = rectleft.move(0,64)
                if self.checkitem(rectDL) == "Empty":
                    result = self.checkitem(newrect)
                    if not result.__class__.__name__ == 'str':
                        if not result.moving and not self.moving:
                            self.moving = True
                            self.direction = 'l'
                            self.move((-16, 0))


        #Check gravity
        if self.checkitem(newrect) == "Empty":
            self.moving = True
            self.move((0, 4))
            self.direction = 'd'
        else:
            if self.moving == True and newrect.colliderect(self.game.player.rect) and self.direction == 'd':
                self.game.music.stopbg()
                self.game.music.deathsound()
                self.game.death()
                self.game.fadeout()
                self.game.startlevel(self.game.counter.get_current_level() + '.tmx')
            self.moving = False

        rect = self.game.player.rect.copy()
        rect.x = rect.x + 1
        rect.width = 62
        if self.rect.colliderect(rect) and self.rect.y == rect.y:
            if self.game.player.orient == "left":
                self.game.player.rect.x += src.Player.MOV_SPEED
                self.moveleft()
                self.direction = 'lu'
            elif self.game.player.orient == "right":
                self.game.player.rect.x -= src.Player.MOV_SPEED
                self.moveright()
                self.direction = 'ru'
            elif self.game.player.orient == "up":
                self.game.player.rect.y += src.Player.MOV_SPEED
            elif self.game.player.orient == "down":
                self.game.player.rect.y -= src.Player.MOV_SPEED

    def checkitem(self, inp):
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
        if self.timer > 0:
            self.timer += 1
            self.move((-4, 0))
            self.game.player.rect.x -= 4
        else:
            rect = self.rect.copy().move(-4, 0)
            if self.checkitem(rect) == "Empty" or self.checkitem(rect) == "Player":
                self.moving = True
                self.move((-4, 0))
                self.game.player.rect.x -= 4
                self.timer = 1
                self.game.player.locked = True

    def moveright(self):
        if self.timer > 0:
            self.timer += 1
            self.move((4, 0))
            self.game.player.rect.x += 4
        else:
            rect = self.rect.copy().move(4, 0)
            if self.checkitem(rect) == "Empty" or self.checkitem(rect) == "Player":
                self.moving = True
                self.move((4, 0))
                self.game.player.rect.x += 4
                self.timer = 1
                self.game.player.locked = True