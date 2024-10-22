import arcade
from game.player import Player
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SCALING

class GameView(arcade.View):
    SCREEN_WIDTH = SCREEN_WIDTH
    SCREEN_HEIGHT = SCREEN_HEIGHT

    def __init__(self):
        super().__init__()
        self.player = None
        self.physics_engine = None

    def setup(self):
        """Configuration initiale du jeu (niveau 1)."""
        # Créer le joueur (tasse de café)
        self.player = Player("assets/sprites/user.jpg", PLAYER_SCALING)
        
        # Créer un sol (plateau simple) pour tester
        self.wall_list = arcade.SpriteList()
        wall = arcade.SpriteSolidColor(800, 50, arcade.color.DARK_BROWN)
        wall.center_x = 400
        wall.center_y = 25
        self.wall_list.append(wall)

        # Initialisation de la physique (la tasse et les murs)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)

    def on_draw(self):
        """Méthode qui dessine tous les éléments à l'écran."""
        arcade.start_render()

        # Dessiner le joueur (tasse de café) et les murs
        self.wall_list.draw()
        self.player.draw()

    def on_key_press(self, key, modifiers):
        """Gestion des touches pressées."""
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Arrête le mouvement quand la touche est relâchée."""
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0

    def update(self, delta_time):
        """Met à jour les positions et la logique du jeu."""
        self.physics_engine.update()
        self.player.update()