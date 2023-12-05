import random

from pico2d import *

import ending_title_mode
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
from static import *
import ending_title_mode
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
    global score
    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    hitter = Hitter()
    game_world.add_object(hitter, 1)

    pitcher = Pitcher()
    game_world.add_object(pitcher, 1)

    fielderList = []
    fielder = Fielder()
    game_world.add_object(fielder, 1)
    fielderList.append(fielder)

    fielder_2b = Fielder_2b()
    game_world.add_object(fielder_2b, 1)
    fielderList.append(fielder_2b)

    fielder_ss = Fielder_ss()
    game_world.add_object(fielder_ss, 1)
    fielderList.append(fielder_ss)

    fielder_3b = Fielder_3b()
    game_world.add_object(fielder_3b, 1)
    fielderList.append(fielder_3b)

    fielder_lf = Fielder_lf()
    game_world.add_object(fielder_lf, 1)
    fielderList.append(fielder_lf)

    fielder_cf = Fielder_cf()
    game_world.add_object(fielder_cf, 1)
    fielderList.append(fielder_cf)

    fielder_rf = Fielder_rf()
    game_world.add_object(fielder_rf, 1)
    fielderList.append(fielder_rf)

    for f in fielderList:
        game_world.add_collision_pair('fielder:hitball',f, None)




def finish():
    game_world.clear()
    pass


def update():
    global health
    game_world.update()
    game_world.handle_collisions()
    if Define.instance.health == 0:
        game_framework.change_mode(ending_title_mode)

def draw():
    global score
    global health
    clear_canvas()
    game_world.render()
    grass.font.draw(50, 50, f'{Define.instance.score:02d}', (255, 255, 0))
    grass.font.draw(100, 50, f'{Define.instance.health:02d}', (255, 255, 0))
    update_canvas()

def pause():
    pass

def resume():
    pass



