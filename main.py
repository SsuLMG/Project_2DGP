from pico2d import open_canvas, delay, close_canvas
import game_framework
from static import *

import title_mode as start_mode

d = Define()

open_canvas(1172, 764)

game_framework.run(start_mode)

close_canvas()