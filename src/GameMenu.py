"""
Class handling menu used in game, all its logic and presentation
"""
__author__ = 'Kedam'

import pygame

# pylint: disable=no-member
# pylint hates me today, pygame has these members


# RGB colors used in menu
GREEN = (0, 255, 0)
YELLOW = (200, 255, 0)
BLACK = (0, 0, 0)


def set_mouse_selection(item, mouse_position):
    """Marks the MenuItem chosen by mouse"""
    if item.is_mouse_selection(mouse_position):
        item.set_font_color(YELLOW)
        item.set_bold(True)
    else:
        item.set_font_color(GREEN)
        item.set_bold(False)


class GameMenu(object):
    """GameMenu class, has list of MenuItems,
    is responsible for their behaviour and mouse/keyboard support"""

    def __init__(self, screen, items, bg_color=BLACK, font=None, font_size=30,
                 font_color=GREEN):
        # Set screen and its parameters
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        # Background color and clock for main loop
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        # Menu items and functions associated with them
        self.funcs = items
        self.items = []

        # Prepare new MenuItem based on items from
        for index, item in enumerate(items.keys()):
            menu_item = MenuItem(item, font, font_size, font_color)

            # Get total height of all items
            total_item_height = len(items.keys()) * menu_item.height

            # Place items on center of screen
            position_x = (self.scr_width / 2) - (menu_item.width / 2)
            # Place items slightly up from center of screen, one after another
            position_y = (self.scr_height - total_item_height) / 2 + \
                            index * (index + menu_item.height)  # Height between each element

            # Set its position and add it to list of menu items
            menu_item.set_position(position_x, position_y)
            self.items.append(menu_item)

        # No item selected
        self.mouse_is_visible = True
        self.cur_item = None

    def set_mouse_visibility(self):
        """Sets visibility of mouse"""
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_keyboard_selection(self, key):
        """Marks the MenuItem chosen via up and down keys"""

        # Unmark all of them to be sure
        for item in self.items:
            item.set_bold(False)
            item.set_font_color(GREEN)

        # Set new chosen item as first one if none was chosen before
        if self.cur_item is None:
            self.cur_item = 0
        # Find chosen item, do not cross list bounds
        else:
            if key == pygame.K_UP and self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        # Mark selected item
        self.items[self.cur_item].set_bold(True)
        self.items[self.cur_item].set_font_color(YELLOW)

        # Check if space or enter is pressed
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            # Run function associated with menu option
            text = self.items[self.cur_item].text
            self.funcs[text]()

    def run(self):
        """Runs screen with menu"""

        # Main loop
        while True:
            # Limit frame speed to 60 FPS
            self.clock.tick(60)

            # Get current mouse position
            mouse_position = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                # No need for mouse if we use keyboard
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(event.key)
                # Check if mouse was clicked on some menu item
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mouse_position):
                            self.funcs[item.text]()

            # Wake mouse up
            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.set_mouse_visibility()

            # Redraw the background
            self.screen.fill(self.bg_color)

            # Get selection by mouse if needed
            for item in self.items:
                if self.mouse_is_visible:
                    set_mouse_selection(item, mouse_position)
                self.screen.blit(item.label, item.position)

            # Refresh screen
            pygame.display.flip()


class MenuItem(pygame.font.Font):
    """Menu item class, just a standard text that is glowing on usage"""

    def __init__(self, text, font=None, font_size=30,
                 font_color=GREEN, (pos_x, pos_y)=(0, 0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def is_mouse_selection(self, (posx, posy)):
        """Check if (posx, posy) collides with out rectangle"""
        if (self.pos_x <= posx <= self.pos_x + self.width) and \
                (self.pos_y <= posy <= self.pos_y + self.height):
            return True
        return False

    def set_position(self, new_x, new_y):
        """Set new position"""
        self.position = (new_x, new_y)
        self.pos_x = new_x
        self.pos_y = new_y

    def set_font_color(self, rgb_tuple):
        """Set new font color"""
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
