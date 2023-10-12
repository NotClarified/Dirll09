from pico2d import load_image

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
        self.cur_state = Idle
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