"""
Level counter class, it simply counts what level we are at.
Increases that counter if needed. Currently it's range [1;4]
"""

__author__ = 'Kedam'

import os


class LevelCounter(object):
    """LevelCounter class"""

    def __init__(self):
        self.count = 1

    def next_level(self):
        """Increases level counter"""
        self.count = ((self.count + 1) % 5)
        if self.count == 0:
            self.count = 1

    def get_current_level(self):
        """Gets current level counter with maps prefix to make it look better"""
        print self.count
<<<<<<< HEAD
        return 'maps/' + str(self.count)
=======
        return os.path.join('maps', str(self.count))
>>>>>>> 4f13cae1977be74d418cb8d3caa2cf0020c64cd7
