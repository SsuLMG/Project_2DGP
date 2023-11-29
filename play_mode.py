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
from fielder_2b import Fielder_2b
from fielder_ss import Fielder_ss
from fielder_3b import Fielder_3b
from fielder_lf import Fielder_lf
from fielder_cf import Fielder_cf
from fielder_rf import Fielder_rf
from hitball import HitBall
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

    fielder_2b = Fielder_2b()
    game_world.add_object(fielder_2b, 1)

    fielder_ss = Fielder_ss()
    game_world.add_object(fielder_ss, 1)

    fielder_3b = Fielder_3b()
    game_world.add_object(fielder_3b, 1)

    fielder_lf = Fielder_lf()
    game_world.add_object(fielder_lf, 1)

    fielder_cf = Fielder_cf()
    game_world.add_object(fielder_cf, 1)

    fielder_rf = Fielder_rf()
    game_world.add_object(fielder_rf, 1)


    hitball = HitBall()
    game_world.add_collision_pair('fielder:hitball', None, hitball)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass



