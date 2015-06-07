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


MOV_SPEED = 16

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
        self.score = 0
        self.locked = False

        # Set default orientation as facing down
        self.set_sprite()

    def set_sprite(self):
        """Decides which sprite it has to use to move player"""
        # Reset player sprite to face down, then decide which one to use based on orientation
        # It simply tracks pointer to appropriate sprite
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
        # Set orientation and sprite based on key held at them moment
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
        # Nothing happened
        else:
            self.hold_time = 0
            self.step = 'rightFoot'

    def detect_collision(self, last_rect, game):
        """Checks current position for any interactable objects"""

        # Check if we encountered a solid object, if yes, do not cross it
        if len(game.tilemap.layers['triggers'].collide(self.rect, 'solid')) > 0:
            self.rect = last_rect

        # We reached entry tile, create screen fadeout, then load next level
        elif len(game.tilemap.layers['triggers'].collide(self.rect, 'entry')) > 0:
            if len(game.collectibles) == 0:
                game.counter.next_level()
                game.music.stopbg()
                game.fadeout()
                game.startlevel(game.counter.get_current_level() + '.tmx')
                return

        # We are on edible floor, destroy every cell that we encounter from layer
        elif len(game.tilemap.layers['edible floor'].collide(self.rect, 'noteaten')) > 0:
            for item in game.tilemap.layers['edible floor']\
                    .get_in_region(self.rect.left,
                                   self.rect.top,
                                   self.rect.right - 1,
                                   self.rect.bottom - 1):
                item.px = 1500
                item.py = 1500
                item.x = 255
                item.y = 255

            # Update map after
            game.tilemap.draw(game.screen)


    def update(self, time_passed, game):
        """Update player state, check if player used keys"""


        self.check_movement(time_passed)

        # If we hold button for 100ms, we enable moving
        if self.hold_time >= 100:
            self.walking = True
        last_rect = self.rect.copy()

        # Movement speed is n px/frame
        if not self.locked:
        # Move rect with mov speed
            if self.walking and self.delta_x < 64:
                if self.orient == 'up':
                    self.rect.y -= MOV_SPEED
                elif self.orient == 'down':
                    self.rect.y += MOV_SPEED
                elif self.orient == 'left':
                    self.rect.x -= MOV_SPEED
                elif self.orient == 'right':
                    self.rect.x += MOV_SPEED
                self.delta_x += MOV_SPEED

        # Detect collision after
        self.detect_collision(last_rect, game)

        # Switch to the walking sprite after 32 pixels
        if self.delta_x == 32:
            # Self.step keeps track of when to flip the sprite so that
            # The character appears to be taking steps with different feet.
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

        # Refocus the camera
        game.tilemap.set_focus(self.rect.x, self.rect.y)