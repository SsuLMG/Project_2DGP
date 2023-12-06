from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time
from sdl2 import SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode
from static import *
from pico2d import *

font = None

def init():
    global image
    global running
    global logo_start_time
    global font
    image = load_image('baseball.png')
    font = load_font('ENCR10B.TTF', 100)
    running = True
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global running
    global logo_start_time
    if get_time() - logo_start_time >= 5.0:
        logo_start_time = get_time()
        game_framework.quit()

def draw():
    global font
    clear_canvas()
    image.draw(1172/2, 764/2, 1172, 764)
    if Define.instance.score < 5000:
        font.draw(1172/2 - 200, 764/2 - 25, f'Bad Score:', (255, 255, 0))
        font.draw(1172/2 - 200, 764/2 - 100, f'{Define.instance.score:02d}', (255, 255, 0))
    else:
        font.draw(1172 / 2 - 200, 764 / 2 - 25, f'Great Score:', (255, 255, 0))
        font.draw(1172 / 2 - 200, 764 / 2 - 100, f'{Define.instance.score:02d}', (255, 255, 0))

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()