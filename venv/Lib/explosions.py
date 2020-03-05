from graphics import *

class Explosion():
    def __init__(self, point):
        self.targets = []
        #circle up, down, left, right
        self.targets.extend([Target(point), Target(point), Target(point), Target(point)])


    def update(self):
        if self.targets[0].active:
            self.targets[0].circle.y += 0.1
            self.targets[0].circle.move(0, 0.1)
        else:
            self.targets[0].circle.undraw()

        if self.targets[1].active:
            self.targets[1].circle.y -= 0.1
            self.targets[1].circle.move(0, -0.1)
        else:
            self.targets[1].circle.undraw()

        if self.targets[2].active:
            self.targets[2].circle.x -= 0.1
            self.targets[2].circle.move(-0.1, 0)
        else:
            self.targets[2].circle.undraw()

        if self.targets[3].active:
            self.targets[3].circle.x += 0.1
            self.targets[3].circle.move(0.1, 0)
        else:
            self.targets[3].circle.undraw()


class Target():
    def __init__(self, point):
        self.circle = Circle(point, 10)
        self.active = False
        self.circle.setFill('white')