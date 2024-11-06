import arcade

# --- Constants
SCREEN_TITLE = "CoFyc"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

CHARACTER_SCALING = 0.32
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
ANIMATION_INTERVAL = 0.2  # Time in seconds between frame switches

class MainMenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """ Render the screen """
        self.clear()

        window_width = self.window.width
        window_height = self.window.height

        arcade.draw_text("CoFyc", window_width / 2, window_height / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")
        arcade.draw_text("Press ENTER to start", window_width / 2, window_height / 2 - 50,
                         arcade.color.GRAY, font_size=20, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        """ Start the game when the player presses ENTER """
        if key == arcade.key.ENTER:
            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)

class EndGameView(arcade.View):
    """ End game view """

    def __init__(self, is_win, score=0):
        super().__init__()
        self.is_win = is_win  # True if the game is won, False if it's game over
        self.score = score  # Score at the end of the game

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Render the end screen """
        self.clear()
        window_width = self.window.width
        window_height = self.window.height

        # Display different text based on whether it's a win or game over
        if self.is_win:
            end_message = "You Win!"
            color = arcade.color.GREEN
            score_message = f"Final Score: {self.score}"
        else:
            end_message = "Game Over!"
            color = arcade.color.RED
            score_message = ""  # No score display if it's a game over

        arcade.draw_text(end_message, window_width / 2, window_height / 2 + 50,
                         color, font_size=50, anchor_x="center", anchor_y="center")

        # Draw the score if the game is won
        if self.is_win:
            arcade.draw_text(score_message, window_width / 2, window_height / 2,
                             arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")
        arcade.draw_text("Press ESC to return to Main Menu", window_width / 2, window_height / 2 - 50,
                         arcade.color.GRAY, font_size=20, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        """ Handle key press on end screen """
        if key == arcade.key.ESCAPE:
            menu_view = MainMenuView()
            self.window.show_view(menu_view)

class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.camera_sprites = None
        self.camera_gui = None
        self.score = 0
        self.left_key_down = False
        self.right_key_down = False
        self.off_ground_time = 0
        self.fall_threshold = 1.0
        self.player_images = [
            "./assets/sprites/resources/coffeeAnimation1.png",
            "./assets/sprites/resources/coffeeAnimation2.png"
        ]
        self.current_image = 0
        self.animation_timer = 0  # Timer to control animation speed

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        map_name = "./assets/sprites/levels/map_level_1.tmx"
        layer_options = {
            "ground": {"use_spatial_hash": True},
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        self.score = 0
        self.player_sprite = arcade.Sprite(self.player_images[self.current_image], CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["ground"]
        )

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()
        self.scene.draw()
        self.camera_gui.use()
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)

    def update_player_speed(self):
        self.player_sprite.change_x = 0
        if self.left_key_down and not self.right_key_down:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_key_down and not self.left_key_down:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True
        self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
        self.update_player_speed()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera_sprites.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera_sprites.viewport_height / 2)
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        self.camera_sprites.move_to((screen_center_x, screen_center_y))

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.animation_timer += delta_time

        if self.left_key_down or self.right_key_down:
            if self.animation_timer >= ANIMATION_INTERVAL:
                self.current_image = (self.current_image + 1) % 2
                self.player_sprite.texture = arcade.load_texture(self.player_images[self.current_image])
                self.animation_timer = 0

        coffee_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["coffee"])
        sugar_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["sugar"])
        developer_hit = arcade.check_for_collision_with_list(self.player_sprite, self.scene["developer"])
        if len(developer_hit) > 0:
            end_view = EndGameView(is_win=True, score=self.score)
            self.window.show_view(end_view)

        # Track time off ground
        if not self.physics_engine.can_jump():
            self.off_ground_time += delta_time
            # Trigger game over if off ground for too long
            if self.off_ground_time > self.fall_threshold:
                end_view = EndGameView(is_win=False, score=self.score)
                self.window.show_view(end_view)
        else:
            # Reset off-ground time if player is on ground
            self.off_ground_time = 0

        # Process item collisions
        for coffee in coffee_hit_list:
            coffee.remove_from_sprite_lists()
            self.score += 1

        for sugar in sugar_hit_list:
            sugar.remove_from_sprite_lists()
            self.score -= 1

        # Update camera
        self.center_camera_to_player()

    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
