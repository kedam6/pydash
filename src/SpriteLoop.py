"""
Module implementing class responsible for animating immobile sprites, may be used in final version
"""

# pylint: disable=unused-argument
# ^ needed since game is used in another file,
# just to make sure object is bound to current game
# pylint: disable=super-on-old-class
# ^ it works as requested, strange that pylint thinks it's bad
__author__ = 'Kedam'
import pygame


class SpriteLoop(pygame.sprite.Sprite):
    """A simple looped animated sprite."""
    def __init__(self, location, cell, *groups):
        super(SpriteLoop, self).__init__(*groups)
        self.image = pygame.image.load(cell['src'])  # Image used to animate
        self.default_image = self.image.copy()  # Default image
        self.width = int(cell['width'])
        self.height = int(cell['height'])
        self.rect = pygame.Rect(location, (self.width, self.height))  # How much space used
        self.frames = int(cell['frames'])  # How many frames it has
        self.frame_count = 0
        self.mspf = int(cell['mspf'])  # Milliseconds per frame
        self.time_count = 0

    def update(self, time_passed, game):
        """Updates state of animation, simply switches image on command"""

        self.time_count += time_passed
        if self.time_count > self.mspf:
            # Advance animation to the appropriate frame
            self.image = self.default_image.copy()
            self.image.scroll(-1*self.width*self.frame_count, 0)
            self.time_count = 0

            # Frame count in range [0;self.frame)
            self.frame_count += 1
            if self.frame_count == self.frames:
                self.frame_count = 0

    def get_frame_count(self):
        """Gets frame count"""
        return self.frame_count
