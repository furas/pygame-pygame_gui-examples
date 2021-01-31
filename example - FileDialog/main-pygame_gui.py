
# author: Bartlomiej "furas" Burek (https://blog.furas.pl)
# date: 2021.01.29
# https://stackoverflow.com/questions/65945488/how-to-activate-pygame-screen-after-using-tkinter-directory-browser/

# --- file dialog ---
#
# https://pygame-gui.readthedocs.io/en/latest/pygame_gui.windows.html#module-pygame_gui.windows.ui_file_dialog
# https://pygame-gui.readthedocs.io/en/latest/pygame_gui.elements.html#pygame_gui.elements.ui_window.UIWindow
# https://github.com/MyreMylar/pygame_gui/blob/main/pygame_gui/windows/ui_file_dialog.py
# --- theming ---
# https://pygame-gui.readthedocs.io/en/latest/theme_guide.html
# https://pygame-gui.readthedocs.io/en/latest/theme_reference/theme_file_dialog.html
# https://pygame-gui.readthedocs.io/en/latest/theme_reference/theme_selection_list.html#theme-selection-list
# https://github.com/MyreMylar/pygame_gui_examples/tree/master/data/fonts
#
# https://github.com/MyreMylar/pygame_gui_examples/blob/master/data/themes/button_theming_test_theme.json

import pygame
import pygame_gui

# --- constants ---

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)

# --- classes ---

class DirectoryDialog(pygame_gui.windows.ui_file_dialog.UIFileDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # always allow for picking folders
        self.allow_picking_directories = True
        
        #self.enable_title_bar = False  # didn't work
        
        #self.title_bar = None
        #self.resizable = False
         
    def update_current_file_list(self):
        super().update_current_file_list()
        
        # keep only folders
        self.current_file_list = [item for item in self.current_file_list if item[1] == '#directory_list_item']
            
# --- functions ---

def open_file_dialog_1():
    global file_dialog

    # center dialog
    rect = pygame.Rect((0, 0), (SCREEN_WIDTH-200, SCREEN_HEIGHT-200))
    rect.center = screen.get_rect().center
    
    # create dialog
    file_dialog = pygame_gui.windows.ui_file_dialog.UIFileDialog(rect=rect, manager=manager, allow_picking_directories=True)
    file_dialog.resizable = False
    file_dialog.title_bar = None
    
def open_file_dialog_2():
    global file_dialog

    # center dialog
    rect = pygame.Rect((0, 0), (SCREEN_WIDTH-200, SCREEN_HEIGHT-200))
    rect.center = screen.get_rect().center
    
    # create dialog
    file_dialog = DirectoryDialog(rect=rect, manager=manager, window_title='Select Directory 2')
    file_dialog.resizable = False
    file_dialog.title_bar = None

# --- main ---

# - init -

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme.json')
#print('\n'.join(dir(manager.get_theme().get_font_dictionary())))
#print('get_default_font():', manager.get_theme().get_font_dictionary().get_default_font())
#print(manager.print_unused_fonts())
print('default_font_id:', manager.get_theme().get_font_dictionary().default_font_id)
print('default_font_info:', manager.get_theme().get_font_dictionary().default_font_info)
print('default_font_name:', manager.get_theme().get_font_dictionary().default_font_name)
print('default_font_size:', manager.get_theme().get_font_dictionary().default_font_size)
print('default_font_style:', manager.get_theme().get_font_dictionary().default_font_style)


# - objects -

# center button
rect = pygame.Rect((0, 0), (500, 50))
rect.center = screen.get_rect().center
rect.y -= 50
# create button
button_directory_1 = pygame_gui.elements.UIButton(relative_rect=rect, text='Select Directory 1', manager=manager)


rect = pygame.Rect((0, 0), (500, 50))
rect.center = screen.get_rect().center
rect.y += 50
# create button
button_directory_2 = pygame_gui.elements.UIButton(relative_rect=rect, text='Select Directory 2', manager=manager)

# - mainloop -

clock = pygame.time.Clock()
is_running = True

while is_running:

    time_delta = clock.tick(30)/1000.0

    # - events -
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:

            # handle button's events
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_directory_1:
                    open_file_dialog_1()
                elif event.ui_element == button_directory_2:
                    open_file_dialog_2()

            # handle dialog's events
            if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:        
                if event.ui_element == file_dialog:
                    print('Selected:', event.text)
                
        manager.process_events(event)

    # - updates -
    
    manager.update(time_delta)

    # - draws -
    
    screen.fill(BLACK)
    
    manager.draw_ui(screen)

    pygame.display.update()
