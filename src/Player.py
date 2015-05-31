"""
Player class module.
Represents player's view, behaviour and movement. Also his looks.
"""

# pylint: disable=unused-argument
# ^ needed since game is used in another file,
# just to make sure object is bound to current game
# pylint: disable=super-on-old-class
# ^ it works as requested, strange that pylint thinks it's bad
# pylint: disable=no-member
# pygame has these members, just pycharm doesnt see them

__author__ = 'Kedam'
import pygame


class Player(pygame.sprite.Sprite):
    """Player class"""

    def __init__(self, location, orientation, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('sprites/player.png')
        self.image_default = self.image.copy()
        self.rect = pygame.Rect(location, (64, 64))
        self.orient = orientation
        self.hold_time = 0
        self.walking = False
        self.delta_x = 0
        self.step = 'rightFoot'
        # Set default orientation
        self.set_sprite()

    def set_sprite(self):
        """Decides which sprite it has to use to move player"""
        # Resets the player sprite sheet to its default position
        # and scrolls it to the necessary position for the current orientation
        self.image = self.image_default.copy()
        if self.orient == 'up':
            self.image.scroll(0, -64)
        elif self.orient == 'down':
            self.image.scroll(0, 0)
        elif self.orient == 'left':
            self.image.scroll(0, -128)
        elif self.orient == 'right':
            self.image.scroll(0, -192)

    def check_movement(self, time_passed):
        """Checks keyboard for pressed movement keys"""
        key = pygame.key.get_pressed()
        # Setting orientation and sprite based on key input:
        if key[pygame.K_UP]:
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.set_sprite()
                self.hold_time += time_passed
        elif key[pygame.K_DOWN]:
            if not self.walking:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.set_sprite()
                self.hold_time += time_passed
        elif key[pygame.K_LEFT]:
            if not self.walking:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.set_sprite()
                self.hold_time += time_passed
        elif key[pygame.K_RIGHT]:
            if not self.walking:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.set_sprite()
                self.hold_time += time_passed
        else:
            self.hold_time = 0
            self.step = 'rightFoot'

    def detect_collision(self, last_rect, game):
        """Checks current position for any interactable objects"""
        # Collision detection:
        # Reset to the previous rectangle if player collides
        # with anything in the foreground layer
        if len(game.tilemap.layers['triggers'].collide(self.rect, 'solid')) > 0:
            self.rect = last_rect
        # Area entry detection:
        elif len(game.tilemap.layers['triggers'].collide(self.rect, 'entry')) > 0:
            game.fadeout()
            game.counter.next_level()
            game.startlevel(game.counter.get_current_level() + '.tmx')

            return

        elif len(game.tilemap.layers['edible floor'].collide(self.rect, 'noteaten')) > 0:
            for item in game.tilemap.layers['edible floor']\
                    .get_in_region(self.rect.left,
                                   self.rect.top,
                                   self.rect.right - 1,
                                   self.rect.bottom - 1):
                item.px = 0
                item.py = 0
                item.x = 0
                item.y = 0
            game.tilemap.draw(game.screen)

    def update(self, time_passed, game):
        """Update player state, check if player used keys"""

        self.check_movement(time_passed)

        # Walking mode enabled if a button is held for 0.1 seconds
        if self.hold_time >= 100:
            self.walking = True
        last_rect = self.rect.copy()
        # Walking at 8 pixels per frame in the direction the player is facing
        if self.walking and self.delta_x < 64:
            if self.orient == 'up':
                self.rect.y -= 8
            elif self.orient == 'down':
                self.rect.y += 8
            elif self.orient == 'left':
                self.rect.x -= 8
            elif self.orient == 'right':
                self.rect.x += 8
            self.delta_x += 8

        self.detect_collision(last_rect, game)



        # Switch to the walking sprite after 32 pixels
        if self.delta_x == 32:
            # Self.step keeps track of when to flip the sprite so that
            # the character appears to be taking steps with different feet.
            if (self.orient == 'up' or self.orient == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            else:
                self.image.scroll(-64, 0)
                self.step = 'leftFoot'
        # After traversing 64 pixels, the walking animation is done
        if self.delta_x == 64:
            self.walking = False
            self.set_sprite()
            self.delta_x = 0

        game.tilemap.set_focus(self.rect.x, self.rect.y)
