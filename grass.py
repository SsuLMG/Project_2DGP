from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('stadium.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1172/2, 764/2)
        #self.image.draw(1200, 30)


#1172 x 1093