from pico2d import *

import random
import math
import game_framework
import game_world
import play_mode

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

class Idle:

    @staticmethod
    def enter(fielder, e):
        fielder.frame = 0
        fielder.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(fielder, e):
        #if space_down(e):
        #    hitter.fire_ball()
        pass

    @staticmethod
    def do(fielder):
        fielder.frame = (fielder.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(fielder):
        if int(fielder.frame) == 0:
            fielder.image.clip_draw(0, 0, 45, 53, fielder.x, fielder.y)
        if int(fielder.frame) == 1:
            fielder.image.clip_draw(45, 0, 33, 53, fielder.x, fielder.y)
        if int(fielder.frame) == 2:
            fielder.image.clip_draw(78, 0, 42, 53, fielder.x, fielder.y)
        if int(fielder.frame) == 3:
            fielder.image.clip_draw(120, 0, 40, 53, fielder.x, fielder.y)


class StateMachine:
    def __init__(self, fielder):
        self.fielder = fielder
        self.cur_state = Idle
        self.transitions = {}

    def start(self):
        self.cur_state.enter(self.fielder, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.fielder)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.fielder, e)
                self.cur_state = next_state
                self.cur_state.enter(self.fielder, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.fielder)



class Fielder_rf:
    def __init__(self):
        self.x, self.y = 1000, 350
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('fielder.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 30

    def handle_collision(self, group, other):
        pass
