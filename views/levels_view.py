import arcade
import os

class LevelsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.levels_folder = "./assets/sprites/levels"
        self.levels = self.get_levels()
        self.selected_level = 0
        self.animation_timer = 0
        self.scale_direction = 1
        self.scale_factor = 1.0
        self.game_start = arcade.load_sound("./assets/sounds/game_start.mp3")


    def get_levels(self):
        levels = []
        for file_name in os.listdir(self.levels_folder):
            if file_name.endswith(".tmx"):
                levels.append(file_name)
        return levels

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

    def on_draw(self):
        self.clear()
        window_width = self.window.width
        window_height = self.window.height

        # Draw the title
        arcade.draw_text("Select Level", window_width / 2, window_height - 100,
                         arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")

        # Draw instructions
        arcade.draw_text("Use LEFT/RIGHT/UP/DOWN arrows to navigate and ENTER to select", window_width / 2, window_height - 150,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center", anchor_y="center")

        # Draw level options in a grid
        levels_per_row = 5
        row_height = 50
        col_width = 200
        start_x = window_width / 2 - (levels_per_row - 1) * col_width / 2
        start_y = window_height / 2 + (len(self.levels) // levels_per_row) * row_height / 2

        for index, level in enumerate(self.levels):
            level_name = f"Level {index + 1}"
            color = arcade.color.RED if index == self.selected_level else arcade.color.WHITE
            scale = self.scale_factor if index == self.selected_level else 1.0
            row_number = index // levels_per_row
            col_number = index % levels_per_row
            position_x = start_x + col_number * col_width
            position_y = start_y - row_number * row_height
            arcade.draw_text(level_name, position_x, position_y,
                             color, font_size=30 * scale, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        levels_per_row = 5
        if key == arcade.key.LEFT:
            self.selected_level = (self.selected_level - 1) % len(self.levels)
        elif key == arcade.key.RIGHT:
            self.selected_level = (self.selected_level + 1) % len(self.levels)
        elif key == arcade.key.UP:
            self.selected_level = (self.selected_level - levels_per_row) % len(self.levels)
        elif key == arcade.key.DOWN:
            self.selected_level = (self.selected_level + levels_per_row) % len(self.levels)
        elif key == arcade.key.ENTER:
            from views.my_game import MyGame  # Local import to avoid circular dependency
            game_view = MyGame(self.selected_level)
            arcade.play_sound(self.game_start)
            game_view.setup()
            self.window.show_view(game_view)

    def on_update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer > 0.1:
            self.animation_timer = 0
            self.scale_factor += 0.1 * self.scale_direction
            if self.scale_factor >= 1.2 or self.scale_factor <= 1.0:
                self.scale_direction *= -1