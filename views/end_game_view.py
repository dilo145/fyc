import arcade

class EndGameView(arcade.View):
    def __init__(self, is_win, score=0):
        super().__init__()
        self.is_win = is_win
        self.score = score

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        window_width = self.window.width
        window_height = self.window.height

        if self.is_win:
            end_message = "You Win!"
            color = arcade.color.GREEN
            score_message = f"Final Score: {self.score}"
        else:
            end_message = "Game Over!"
            color = arcade.color.RED
            score_message = ""

        arcade.draw_text(end_message, window_width / 2, window_height / 2 + 50,
                         color, font_size=50, anchor_x="center", anchor_y="center")

        if self.is_win:
            arcade.draw_text(score_message, window_width / 2, window_height / 2,
                             arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")
        arcade.draw_text("Press ESC to return to Main Menu", window_width / 2, window_height / 2 - 50,
                         arcade.color.GRAY, font_size=20, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from views.main_menu_view import MainMenuView  # Local import to avoid circular dependency
            menu_view = MainMenuView()
            self.window.show_view(menu_view)