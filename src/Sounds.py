__author__ = 'Kedam'
import pygame
import os


class SoundPlayer(object):

    def __init__(self):
        self.eat = pygame.mixer.Sound(os.path.join('sounds', 'select.wav'))
        self.death = pygame.mixer.Sound(os.path.join('sounds', 'death.wav'))
        self.start = pygame.mixer.Sound(os.path.join('sounds', 'start.wav'))
        self.gamebackgroundmusic = pygame.mixer.music.load(os.path.join('sounds', 'game_bg.mp3'))

    def eatsound(self):
        self.eat.play()

    def deathsound(self):
        self.death.play()

    def startsound(self):
        self.start.play()

    def playbg(self):
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.11)

    def stopbg(self):
        pygame.mixer.music.fadeout(800)
