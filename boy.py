import math

from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_SPACE


def space_down(e): # e = event
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def time_out_5(e): # 한번 만들어보는 5초 이벤트 타임아웃
    return e[0] == 'TIME_OUT' and e[1] == 5.0
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
        self.table = {
            Sleep: {space_down: Idle}, # Sleep에서 space_down일경우 Idle로 감 -> handle_event에서 변환해야 함
            Idle: {time_out: Sleep} #time_out event를 발생시키지 않음 
        }
        pass
    def start(self):
        self.cur_state.enter(self.boy)
        pass
    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items(): # self의 테이블의 현재상태(sleep)에서의 itmes에서의 내용이 출력
            if check_event(e):
                self.cur_state.exit(self.boy) #다음 상태로 가기 전 exit진행
                self.cur_state = next_state #다음 상태로 바꿈
                self.cur_state.enter(self.boy) # 다음 상태에서의 entry action 수행
                return True
        return False # 들어온 이벤트에 대해 다음 상태로 못감을 반환 / 디버깅에 대해 유리함

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
        print(event)
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()