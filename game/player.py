import arcade
from game.constants import PLAYER_MOVEMENT_SPEED

class Player(arcade.Sprite):
    def __init__(self, image, scaling):
        super().__init__(image, scaling)
        self.center_x = 100  # Position de départ sur l'axe X
        self.center_y = 100  # Position de départ sur l'axe Y

    def update(self):
        """Méthode pour gérer le mouvement du joueur."""
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        # Limites de l'écran
        if self.left < 0:
            self.left = 0
        if self.right > 800:
            self.right = 800
        if self.bottom < 0:
            self.bottom = 0
        if self.top > 600:
            self.top = 600