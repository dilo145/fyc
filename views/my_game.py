import arcade
import os
from models.constants import *
from views.end_game_view import EndGameView

class MyGame(arcade.View):
    def __init__(self, selected_level):
        super().__init__()
        self.selected_level = selected_level
        self.levels = self.get_levels()
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
        self.animation_timer = 0
        self.in_vide = False
        self.timer_started = False

        # Load sounds
        self.coffee_sound = arcade.load_sound("./assets/sounds/coffee_dip.mp3")
        self.sugar_sound = arcade.load_sound("./assets/sounds/sugar.mp3")
        self.jump_sound = arcade.load_sound("./assets/sounds/jump.mp3")
        self.death_sound = arcade.load_sound("./assets/sounds/game_over.mp3")
        self.drinking_coffee = arcade.load_sound("./assets/sounds/drinking_coffee.mp3")
        self.background_music = arcade.load_sound("./assets/sounds/bg_music.mp3")

    def get_levels(self):
        levels = []
        levels_folder = "./assets/sprites/levels"
        for file_name in os.listdir(levels_folder):
            if file_name.endswith(".tmx"):
                levels.append(file_name)
        return levels

    def setup(self):
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        map_name = f"./assets/sprites/levels/map_level_{self.selected_level + 1}.tmx"

        layer_options = {
            "ground": {
                "use_spatial_hash": True,
                "hit_box_algorithm": "None"
            },
            "coffee": {
                "use_spatial_hash": True,
                "hit_box_algorithm": "None"
            },
            "sugar": {
                "use_spatial_hash": True,
                "hit_box_algorithm": "None"
            },
            "developer": {
                "use_spatial_hash": True,
                "hit_box_algorithm": "None"
            },
            "vide": {
                "use_spatial_hash": True,
                "hit_box_algorithm": "None"
            }
        }

        try:
            self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)

            if self.tile_map.background_color:
                arcade.set_background_color(self.tile_map.background_color)
            else:
                arcade.set_background_color(arcade.color.SKY_BLUE)

            self.scene.add_sprite_list("Player")
            self.player_sprite = arcade.Sprite(
                self.player_images[self.current_image],
                CHARACTER_SCALING
            )
            self.player_sprite.center_x = 128
            self.player_sprite.center_y = 128
            self.scene.add_sprite("Player", self.player_sprite)

            if "ground" in self.tile_map.sprite_lists:
                self.physics_engine = arcade.PhysicsEnginePlatformer(
                    self.player_sprite,
                    gravity_constant=GRAVITY,
                    walls=self.tile_map.sprite_lists["ground"]
                )
            else:
                self.physics_engine = arcade.PhysicsEnginePlatformer(
                    self.player_sprite,
                    gravity_constant=GRAVITY,
                    walls=arcade.SpriteList()
                )

        except Exception as e:
            print(f"Error loading level: {e}")
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite,
                gravity_constant=GRAVITY,
                walls=arcade.SpriteList()
            )

        self.background_music_player = arcade.play_sound(self.background_music, volume=0.2, looping=True)
        self.time_remaining = LEVEL_TIME_LIMITS.get(self.selected_level)
        self.timer_started = False

    def on_show(self):
        super().on_show()
        self.timer_started = True

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()
        self.scene.draw()
        self.camera_gui.use()
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)
        time_text = f"Time: {int(self.time_remaining)}"
        arcade.draw_text(time_text, 10, 40, arcade.csscolor.WHITE, 18)

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
                arcade.play_sound(self.jump_sound)
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

        coffee_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("coffee"))
        sugar_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("sugar"))
        developer_hit = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("developer"))
        vide_hit = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("vide"))

        if len(developer_hit) > 0:
            arcade.play_sound(self.drinking_coffee)
            if self.score >= 1:
                end_view = EndGameView(is_win=True, score=self.score, current_level=self.selected_level,
                                   total_levels=len(self.levels))
            else:
                end_view = EndGameView(is_win=False, score=self.score, current_level=self.selected_level,
                                       total_levels=len(self.levels))
            self.window.show_view(end_view)
        elif len(vide_hit) > 0:
            self.in_vide = True
        elif self.in_vide:  # If player was in "vide" and now unhit it
            arcade.stop_sound(self.background_music_player)
            arcade.play_sound(self.death_sound)
            end_view = EndGameView(is_win=False, score=self.score, current_level=self.selected_level,
                                   total_levels=len(self.levels))
            self.window.show_view(end_view)

        for coffee in coffee_hit_list:
            coffee.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.coffee_sound)

        for sugar in sugar_hit_list:
            sugar.remove_from_sprite_lists()
            self.score -= 1
            arcade.play_sound(self.sugar_sound)

        if self.timer_started:
            self.time_remaining -= delta_time
            if self.time_remaining <= 0:
                end_view = EndGameView(is_win=False, score=self.score,
                                       current_level=self.selected_level,
                                       total_levels=len(self.levels))
                self.window.show_view(end_view)

        self.center_camera_to_player()

    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))