import arcade
from views.my_game import MyGame
from models.constants import *
import time

class LoadingView(arcade.View):
    def __init__(self, level=0):
        super().__init__()
        self.level = level
        self.loading_done = False
        self.game_view = None
        self.progress = 0
        self.dots = ""
        self.dot_timer = 0
        self.loading_tasks = [
            "Loading assets",
            "Preparing level",
            "Setting up player",
            "Initializing physics",
            "Almost ready"
        ]
        self.current_task = 0
        self.load_started = False

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        window_width = self.window.width
        window_height = self.window.height

        arcade.draw_text(GAME_TITLE, window_width/2, window_height/2 + 100,
                        arcade.color.WHITE, 60, anchor_x="center", font_name="Arial")

        loading_text = f"{self.loading_tasks[self.current_task]}{self.dots}"
        arcade.draw_text(loading_text, window_width/2, window_height/2,
                        arcade.color.LIGHT_GRAY, 20, anchor_x="center")

        bar_width = 400
        bar_height = 20
        bar_x = window_width/2 - bar_width/2
        bar_y = window_height/2 - 50

        arcade.draw_rectangle_filled(bar_x + bar_width/2, bar_y,
                                   bar_width, bar_height,
                                   arcade.color.DARK_GRAY)

        progress_width = bar_width * (self.progress / 100)
        if progress_width > 0:
            arcade.draw_rectangle_filled(bar_x + progress_width/2, bar_y,
                                       progress_width, bar_height,
                                       arcade.color.ELECTRIC_BLUE)

        arcade.draw_text(f"{int(self.progress)}%",
                        window_width/2, bar_y - 30,
                        arcade.color.WHITE, 14, anchor_x="center")

    def load_game_assets(self):
        self.game_view = MyGame(self.level)
        self.game_view.setup()
        self.progress = 100
        self.loading_done = True

    def on_update(self, delta_time):
        if not self.load_started:
            self.load_started = True
            self.load_game_assets()
            return

        self.dot_timer += delta_time
        if self.dot_timer >= 0.5:
            self.dot_timer = 0
            self.dots = "." * ((len(self.dots) + 1) % 4)

        if self.loading_done and self.game_view:
            self.window.show_view(self.game_view)
