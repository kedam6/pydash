__author__ = 'Kedam'


class LevelCounter():

    def __init__(self):
        self.count = 1

    def nextlevel(self):
        self.count = ((self.count + 1) % 5)
        if self.count == 0:
            self.count = 1

    def getcurrentlevel(self):
        print self.count
        return str(self.count)