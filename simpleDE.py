import numpy as np
import matplotlib.pyplot as plt
from manim import *

# Most General
# ECS might work for arbitrary case
# Some constraints weird (like connected to ridgid rod, fixed point, ect.)

# ------------------------------------------------------
#  ________     ____   ____  _____ __  _________       ____   ____   ____ _________ _______        _________ ____  _____   ______   _____ ____  _____ _________ _________ _______    
# |_   ___ \. .'    \.|_   \|_   _|  ||  _   _  |    .'    \.|_  _| |_  _|_   ___  |_   __ \      |_   ___  |_   \|_   _|.' ___  | |_   _|_   \|_   _|_   ___  |_   ___  |_   __ \   
#   | |   \. \  .--.  \ |   \ | |  \_||_/ | | \_|   /  .--.  \ \ \   / /   | |_  \_| | |__) |       | |_  \_| |   \ | | / .'   \_|   | |   |   \ | |   | |_  \_| | |_  \_| | |__) |  
#   | |    | | |    | | | |\ \| |         | |       | |    | |  \ \ / /    |  _|  _  |  __ /        |  _|  _  | |\ \| | | |    ____  | |   | |\ \| |   |  _|  _  |  _|  _  |  __ /   
#  _| |___.' /  \--'  /_| |_\   |_       _| |_      \  \--'  /   \ ' /    _| |___/ |_| |  \ \_     _| |___/ |_| |_\   |_\ \.___]  _|_| |_ _| |_\   |_ _| |___/ |_| |___/ |_| |  \ \_ 
# |________.' \.____.'|_____|\____|     |_____|      \.____.'     \_/    |_________|____| |___|   |_________|_____|\____|\._____.' |_____|_____|\____|_________|_________|____| |___|
# ------------------------------------------------------

# Encode DE a * x'' + b * x' + c * x = k
class LinearTriplet():
    def __init__(self, a, b, c, k, x0, v0):
        self.a = a
        self.b = b
        self.c = c
        self.k = k
        
        self.x0 = x0
        self.v0 = v0
    
    def exact_solution(self):
        if self.a != 0:
            r1 = (-self.b + np.sqrt(self.b ** 2 - 4 * self.a * self.c, dtype='complex')) / (2 * self.a)
            r2 = r1.conj() 
            
            print(r1, r2)
            
            if r1 != r2:
                # A1 + A2 = x0 - k
                # r1 * A1 + r2 * A2 = v0
                # r1 * A1 + r2 * (x0 - d - A1) = v0
                # A1 = (v0 + r2 * d - r2 * x0) / (r1 - r2)
                A1 = (self.v0 + r2 * self.k - r2 * self.x0) / (r1 - r2)
                A2 = self.x0 - self.k - A1
                
                print(r1, r2, A1, A2)

                return (lambda t: A1 * np.exp(r1 * t) + A2 * np.exp(r2 * t) + self.k)
            else:
                A = self.x0 - self.k

                return (lambda t: A * np.exp(r1 * t) + self.k)

        elif self.b != 0:
            A = self.x0 - self.k
            r = -self.a / self.b
            return (lambda t: A * np.exp(r * t))

        elif self.c != 0:
            return (lambda t: self.c / self.k)
    
    def sudo_period(self):
        radical = self.b ** 2 - 4 * self.a * self.c
        if radical < 1:
            r_im = np.sqrt(radical, dtype='complex') / (2 * self.a) * 1j
            period = np.abs(2 * np.pi / r_im)

            return period
        
    def sudo_decay_constant(self):
        return -self.b / self.a / 2

def zig_zag(width=2, height=1, n=4):
    zag_length = width / (n - 1)

    first_line = Line(0 * RIGHT + height / 2 * UP, zag_length / 2 * RIGHT + height * UP)
    lines = [first_line]

    x = zag_length / 2
    is_high = True

    for i in range(n-2):
        start_y = height if is_high else 0
        end_y = 0 if is_high else height

        end_x = x + zag_length

        lines = lines + [Line(x * RIGHT + start_y * UP, end_x * RIGHT + end_y * UP)]
        x = end_x
        is_high = not is_high
    
    y = height if is_high else 0
    last_line = Line(x * RIGHT + y * UP, (x + zag_length / 2) * RIGHT + height / 2 * UP)
    lines = lines + [last_line]

    return VGroup(*lines)

class TimeMObject(Mobject):
    def __init__(self, x0, content):
        super().__init__()
        self.t = 0
        self.x = x0
        self.content = content

        self.add(content)

# Contained Interactions
# create_space_contained :: Params -> Initial State -> State Space
# space_approx :: State Space -> Delta Tiime -> State Space
# space_exact :: State Space -> Time -> State Space
# annotations :: _
# draw :: State Space -> _

# Contained

## Spring
class SpringParams():
    def __init__(self, k, m, equalibrum_x, friction=0):
        self.k = k
        self.m = m
        self.friction = friction
        self.equalibrum_x = equalibrum_x
    
    def create_space(self, x0, v0):
        return SpringStateX(self, x0, v0)
        
class SpringStateX():
    def __init__(self, params, x0, v0):
        self.params = params
        self.x = x0
        self.v = v0

        self.de = LinearTriplet(params.k / params.m, params.friction, 1, params.k/ params.m * params.xe, self.x, self.v)
    
    def exact_func(self):
        return self.de.exact_solution()
    
    def create_mobject(self, height, n):
        lines = zig_zag(self.x, height, n)
        square = Square(1).shift(.5 * UP + (self.x + .5) * RIGHT)
        object = TimeMObject(self.x, VGroup(lines, square))
        
        f = self.exact_func()

        def move_spring(spring, dt):
            x = f(spring.t).real
            dx = x - spring.x
            # print(spring.t, x)
            lines.stretch_to_fit_width(x)
            lines.shift(dx / 2 * RIGHT)
            square.shift(dx * RIGHT)

            spring.t = spring.t + dt
            spring.x = x
        
        object.add_updater(move_spring)
        return object

## Pendulum
class SAPendlum():
    def __init__(self, length, g=9.81):
        self.g = g
        self.length = length
    
    def create_space(self, theta0, omega0):
        return SAPendlumStateTheta(self, theta0, omega0)
        
class SAPendlumStateTheta():
    def __init__(self, params, theta0, omega0):
        self.params = params
        self.theta = theta0
        self.omega = omega0

        self.de = LinearTriplet(1, 0, params.g / params.length, 0, self.theta, self.omega)
    
    def exact_func(self):
        return self.de.exact_solution()
    
    def create_mobject(self):
        p = self.params.length * np.sin(self.theta) * RIGHT - self.params.length * np.cos(self.theta) * UP
        string = Line(0 * UP + 0 * RIGHT, p)
        ball = Circle(.2).move_to(p)

        object = TimeMObject(self.theta, VGroup(string, ball))
        f = self.exact_func()

        def update_pendulum(pendulum, dt):
            theta = f(pendulum.t).real
            d_theta = theta - pendulum.x

            string.rotate_about_origin(d_theta)
            ball.rotate_about_origin(d_theta)

            pendulum.t = pendulum.t + dt
            pendulum.x = theta

        object.add_updater(update_pendulum)
        return object

class SAPendulumStateXY():
    def __init__(self, theta_space):
        self.params = theta_space.params
        self.theta_space = theta_space
    
    def exact_func(self):
        f_theta = self.theta_space.exact_func()

        def fun(t):
            theta = f_theta(t)
            return (self.params.length * np.sin(theta), -self.params.length * np.cos(theta))
        
        return fun

class TestScene(Scene):
    def construct(self):
        p1 = SAPendlum(length=1)
        s1 = p1.create_space(.5, 0)
        object1 = s1.create_mobject()
        text1 = MathTex(f'T_1 = {int(s1.de.sudo_period())} s')
        text1.next_to(object1)

        p2 = SAPendlum(length=3)
        s2 = p2.create_space(.5, 0)
        object2 = s2.create_mobject()
        text2 = MathTex(f'T_2 = {int(s2.de.sudo_period())} s')
        text2.next_to(object2)
        
        self.add(object1)
        self.add(object2)
        self.add(text1)
        self.add(text2)

        self.wait(20)

def test():
    params = SpringParams(k=10, m=1, equalibrum_x=2, friction=1)
    space = params.create_space(.5, 0)
    f = space.exact_func()

    ts = np.linspace(0, 10, 1000)
    xs = f(ts)

    plt.plot(ts, xs)
    plt.show()

def test2():
    de = LinearTriplet(1,1,2,0, 1, 0)
    f = de.exact_solution()
    p = de.sudo_period()
    print(p)

    ts = np.linspace(0, 10, 1000)
    xs = f(ts)

    plt.subplot(2,1,1)
    plt.plot(ts, xs.real)
    plt.vlines([-p, 0, p], -1, 1, colors='k')
    
    plt.subplot(2,1,2)
    plt.plot(ts, xs.imag)
    plt.vlines([-p, 0, p], -1, 1, colors='k')
    plt.show()

#test2()