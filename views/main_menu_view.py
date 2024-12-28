import arcade

class MainMenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        window_width = self.window.width
        window_height = self.window.height

        arcade.draw_text("CoFyc", window_width / 2, window_height / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")
        arcade.draw_text("Press ENTER to start", window_width / 2, window_height / 2 - 50,
                         arcade.color.GRAY, font_size=20, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            from views.my_game import MyGame  # Local import to avoid circular dependency
            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)