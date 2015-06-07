"""
Module implementing sounds in game, also music during stages
"""

__author__ = 'Kedam'
import pygame
import os
import src.Options


class SoundPlayer(object):
    """Class implementing sound handling"""
    def __init__(self):
        self.eat = pygame.mixer.Sound(os.path.join('sounds', 'select.wav'))
        self.death = pygame.mixer.Sound(os.path.join('sounds', 'death.wav'))
        self.start = pygame.mixer.Sound(os.path.join('sounds', 'start.wav'))
        self.gamebackgroundmusic = pygame.mixer.music.load(os.path.join('sounds', 'game_bg.mp3'))

    def eatsound(self):
        """Plays eat sound file"""
        self.eat.set_volume(src.Options.CONFIG.soundvolume)
        if src.Options.CONFIG.soundon:
            self.eat.play()

    def deathsound(self):
        """Plays death sound file"""
        self.death.set_volume(src.Options.CONFIG.soundvolume)
        if src.Options.CONFIG.soundon:
            self.death.play()

    def startsound(self):
        """Plays start sound file"""
        self.start.set_volume(src.Options.CONFIG.soundvolume)
        if src.Options.CONFIG.soundon:
            self.start.play()

    def playbg(self):
        """Plays background music"""
        if src.Options.CONFIG.musicon:
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(src.Options.CONFIG.musicvolume)

    def stopbg(self):
        """Stops background music while fading out"""
        pygame.mixer.music.fadeout(800)
