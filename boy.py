import math

from pico2d import load_image, get_time, SDLK_a
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP


def space_down(e):  # e = event
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def a_key_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'


def right_down(e):
    print('RIGHT_DOWN')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    print('RIGHT_UP')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    print('LEFT_DOWN')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    print('LEFT_UP')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class AutoRun:
    @staticmethod
    def enter(boy, e):
        if boy.action == 0 or boy.action == 2:  # 시작시 왼쪽방향
            boy.dir, boy.action = -1, 0
        elif boy.action == 1 or boy.action == 3:  # 시작시 오른쪽 방향
            boy.dir, boy.action = 1, 1
        boy.auto_run_time = get_time()
        boy.frame = 0
        print('Auto Start')
        pass

    @staticmethod
    def exit(boy, e):
        print('Auto Exit')
        pass

    @staticmethod
    def do(boy):
        if get_time() - boy.auto_run_time > 5:  # do에서 계속 시간 체크, 5초 경과 시 handle event 발생
            boy.state_machine.handle_event(('TIME_OUT', 0))
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5 * 3  # Run의 3배 속도

        if boy.x >= 780:
            boy.dir, boy.action = -1, 0
        elif boy.x <= 30:
            boy.dir, boy.action = 1, 1
        pass

    @staticmethod
    def draw(boy):  # 소년의 속도 빨라지고, 크기 커짐, 좌우측 끝에서 방향 전환
        # 기본 boy : boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y, 100 * 1.3, 100 * 1.3)
        pass


class Sleep:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        print('눕다')

    @staticmethod
    def exit(boy, e):
        print('Idle Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('드르렁')

    @staticmethod
    def draw(boy):  # 눕힐때 clip.cop을 이용해서 회전할 경우엔 세워진 이미지를 눕히려면 계산해야함, 이미 눕힌 이미지는 계산 필요 x
        # 즉, 미리 계산해서 가능하면 미리 계산해서 그 결과를 실행시간에 사용하는 것이 필요 계산결과가 동일한 경우 코드 재활용 함
        if boy.action == 2:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                          - math.pi / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                          math.pi / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        pass


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1  # 여기서의 dir은? 방향
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class Idle:
    @staticmethod
    def enter(boy, e):
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        boy.frame = 0
        boy.start_time = get_time()  # 경과시간을 가지고 오는 함수
        print('Idle Enter')
        pass

    @staticmethod
    def exit(boy, e):
        print('Idle Exit')
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:  # do에서 계속 시간 체크, 3초 경과 시 handle event 발생
            boy.state_machine.handle_event(('TIME_OUT', 0))
        print('Idle Do')

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class StateMactine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = AutoRun
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,
                   time_out: Sleep, a_key_down: AutoRun},  # time_out event를 발생시키지 않음
            Sleep: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,
                    space_down: Idle, a_key_down: AutoRun},  # Sleep에서 space_down일경우 Idle로 감 -> handle_event에서 변환해야 함
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, a_key_down: AutoRun},
            AutoRun: {time_out: Idle, left_down: Run, right_down: Run}
        }
        pass

    def start(self):
        self.cur_state.enter(self.boy, ('START', 0))
        pass

    def handle_event(self, e):
        for check_event, next_state in self.transitions[
            self.cur_state].items():  # self의 테이블의 현재상태(sleep)에서의 itmes에서의 내용이 출력
            if check_event(e):
                self.cur_state.exit(self.boy, e)  # 다음 상태로 가기 전 exit진행 # e를 추가한 이유 enter에 e를 전달해서 필요한 작업 수행
                self.cur_state = next_state  # 다음 상태로 바꿈
                self.cur_state.enter(self.boy, e)  # 다음 상태에서의 entry action 수행
                return True
        return False  # 들어온 이벤트에 대해 다음 상태로 못감을 반환 / 디버깅에 대해 유리함

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
