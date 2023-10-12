import math

from pico2d import load_image

class Sleep:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        print('눕다')
    @staticmethod
    def exit(boy):
        print('Idle Exit')
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('드르렁')
    @staticmethod
    def draw(boy): # 눕힐때 clip.cop을 이용해서 회전할 경우엔 세워진 이미지를 눕히려면 계산해야함, 이미 눕힌 이미지는 계산 필요 x
                   # 즉, 미리 계산해서 가능하면 미리 계산해서 그 결과를 실행시간에 사용하는 것이 필요 계산결과가 동일한 경우 코드 재활용 함
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                      math.pi / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        pass

class Idle:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        print('Idle Enter')
    @staticmethod
    def exit(boy):
        print('Idle Exit')
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('Idle Do')
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass
class StateMactine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Sleep
        pass
    def start(self):
        self.cur_state.enter(self.boy)
        pass
    def update(self):
        self.cur_state.do(self.boy)
        pass
    def draw(self):
        self.cur_state.draw(self.boy)
        pass

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMactine(self)
        self.state_machine.start()

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()