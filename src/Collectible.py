__author__ = 'Kedam'
import pygame
from random import randint



class Collectible(pygame.sprite.Sprite):

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
        for cell in self.cells:
            cell.px = -1000
            cell.py = -1000
            cell.x = -100
            cell.y = -100
            self.gone = True
            self.rect = None

        self.game.music.eatsound()
        self.game.player.score += 1
        print 'Score: ', self.game.player.score

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
        newrect = newrect.move(0, 8)

        # Eaten
        if self.rect.colliderect(self.game.player.rect):
            print 'omnom', self.rect, 'rect', self.game.player.rect.move(-1, -1), 'player'
            self.eaten()
            try:
                self.game.collectibles.remove(self)
                return
            except ValueError:
                print 'meh'


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
            self.move((0, 8))
        else:
            if self.moving == True and newrect.colliderect(self.game.player.rect) and self.game.player.orient != "up":
                self.game.music.stopbg()
                self.game.music.deathsound()
                self.game.player.die(self.game)
                self.game.death()
                self.game.fadeout()
                self.game.startlevel(self.game.counter.get_current_level() + '.tmx')
            else:
                self.moving = False

    def checkitem(self, inp):
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