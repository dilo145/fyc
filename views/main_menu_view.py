import arcade
from models.constants import *

class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_options = ["Play", "Levels"]
        self.selected_option = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        window_width = self.window.width
        window_height = self.window.height

        arcade.draw_text(GAME_TITLE, window_width / 2, window_height / 2 + 100,
                         arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")
        arcade.draw_text("Press ENTER to select", window_width / 2, window_height / 2 - 100,
                         arcade.color.GRAY, font_size=20, anchor_x="center", anchor_y="center")

        for index, option in enumerate(self.menu_options):
            color = arcade.color.YELLOW if index == self.selected_option else arcade.color.WHITE
            arcade.draw_text(option, window_width / 2, window_height / 2 + 50 - index * 30,
                             color, font_size=30, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
        elif key == arcade.key.DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
        elif key == arcade.key.ENTER:
            if self.selected_option == 0:
                from views.loading_view import LoadingView
                loading_view = LoadingView(0)
                self.window.show_view(loading_view)
            elif self.selected_option == 1:  # Levels
                from views.levels_view import LevelsView
                levels_view = LevelsView()
                self.window.show_view(levels_view)