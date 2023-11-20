import random

from pico2d import *
import game_framework

import game_world
from grass import Grass
import title_mode
#from boy import Boy
from ball import Ball
from zombie import Zombie
from hitter import Hitter
from pitcher import Pitcher
from fielder import Fielder

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            hitter.handle_event(event)
            pitcher.handle_event(event)

def init():
    global grass
    global hitter
    global pitcher

    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    hitter = Hitter()
    game_world.add_object(hitter, 1)

    pitcher = Pitcher()
    game_world.add_object(pitcher, 1)

    fielder = Fielder()
    game_world.add_object(fielder, 1)
    # fill here



def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # fill here

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

