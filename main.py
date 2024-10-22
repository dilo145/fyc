import arcade
from game.game_view import GameView

def main():
    # Création de la fenêtre du jeu
    window = arcade.Window(GameView.SCREEN_WIDTH, GameView.SCREEN_HEIGHT, "Mon Jeu de Café")
    
    # Lancer la première vue du jeu
    game_view = GameView()
    game_view.setup()  # Initialiser le jeu
    window.show_view(game_view)
    
    # Lancer la boucle de jeu
    arcade.run()

if __name__ == "__main__":
    main()