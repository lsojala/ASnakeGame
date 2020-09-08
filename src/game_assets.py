"""
Load graphical assets for the game
"""

from PIL import Image, ImageTk

class Assets:
    def __init__(self):
        try:
            self.snake_image = Image.open("./assets/snake.png")
            self.food_image = Image.open("./assets/food.png")
        except IOError as error:
            print("<DEBUG> Loading grapics encountered an error: {}".format(error))


    def load_assets(self):
        self.snake = ImageTk.PhotoImage(self.snake_image)
        self.food = ImageTk.PhotoImage(self.food_image)

