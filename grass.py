from pico2d import *

class Grass:
    enter_sound = None

    def __init__(self):
        self.image = load_image('stadium.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.enter_sound = load_wav('enter_sound.wav')
        self.enter_sound.set_volume(32)
        self.enter_sound.play()

    def update(self):
        pass

    def draw(self):
        self.image.draw(1172/2, 764/2)
        #self.image.draw(1200, 30)





#1172 x 1093
