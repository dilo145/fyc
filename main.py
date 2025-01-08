import arcade
from views.main_menu_view import MainMenuView
from models.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False, center_window=True)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()