from manim import *
from copy import deepcopy
import math

class AnimateSpring(Scene):
    def construct(self):

        anchor = [-3, 0, 0]

        # relaxed_spring = VGroup(*[Line(*points) for points in all_points])
        relaxed_spring = create_spring(anchor, 1, math.pi *0)
        # compress_spring(relaxed_spring)
        # compressed_spring = VGroup(*[Line(*points*np.array([0.5, 1, 1])) for points in all_points])
        compressed_spring = create_spring(anchor, 0.5, math.pi *0)
        rs1 = deepcopy(relaxed_spring)

        self.play(Transform(rs1, compressed_spring))
        self.remove(rs1)
        self.play(Transform(deepcopy(compressed_spring), relaxed_spring))
    

def create_spring(anchor, scale, angle):

    anchor = np.array(anchor)

    all_points = [
        np.array([anchor, anchor + np.array([scale * math.sin(angle), -scale * math.cos(angle), 0])]),
        # np.array([anchor + np.array([scale, 0, 0]), anchor + np.array([2*scale, -2*scale, 0])]),
        # np.array([anchor + np.array([2*scale, -2*scale, 0]), anchor + np.array([3*scale, 0, 0])]),
        # np.array([anchor + np.array([3*scale, 0, 0]), anchor + np.array([4*scale, -2*scale, 0])]),
        # np.array([anchor + np.array([4*scale, -2*scale, 0]), anchor + np.array([5*scale, 0, 0])]),
        # np.array([anchor + np.array([5*scale, 0, 0]), anchor + np.array([5*scale, -2*scale, 0])]),
    ]

    return VGroup(*[Line(*points) for points in all_points])


def compress_spring(spring_object):
    print(spring_object.get_top(), spring_object.get_left())



class SquareToCircle(Scene):
    def construct(self):
        circle =  Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.8)
        square.flip(RIGHT)  # flip horizontally
        square.rotate(-3 * TAU / 8)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class CreatingMobjects(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.wait(1)
        self.remove(circle)
        self.wait(1)


class Shapes(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        circle.shift(LEFT)
        square.shift(UP)
        triangle.shift(RIGHT)

        self.add(circle, square, triangle)
        self.wait(1)

class MobjectPlacement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        # place the circle two units left from the origin
        circle.move_to(LEFT * 2)
        # place the square to the left of the circle
        square.next_to(circle, LEFT)
        # align the left border of the triangle to the left border of the circle
        triangle.align_to(circle, LEFT)

        self.add(circle, square, triangle)
        self.wait(1)


class MobjectStyling(Scene):
    def construct(self):
        circle = Circle().shift(LEFT)
        square = Square().shift(UP)
        triangle = Triangle().shift(RIGHT)

        circle.set_stroke(color=GREEN, width=20)
        square.set_fill(YELLOW, opacity=1.0)
        triangle.set_fill(PINK, opacity=0.5)

        self.add(circle, square, triangle)
        self.wait(1)


class MobjectZOrder(Scene):
    def construct(self):
        circle = Circle().shift(LEFT)
        square = Square().shift(UP)
        triangle = Triangle().shift(RIGHT)

        circle.set_stroke(color=GREEN, width=20)
        square.set_fill(YELLOW, opacity=1.0)
        triangle.set_fill(PINK, opacity=0.5)

        self.add(triangle, square, circle)
        self.wait(1)


class SomeAnimations(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # some animations display mobjects, ...
        self.play(FadeIn(square))

        # ... some move or rotate mobjects around...
        self.play(Rotate(square, PI/4))

        # some animations remove mobjects from the screen
        self.play(FadeOut(square))

        self.wait(1)


class ApplyMethodExample(Scene):
    def construct(self):
        square = Square().set_fill(RED, opacity=1.0)
        self.add(square)

        # animate the change of color
        self.play(ApplyMethod(square.set_fill, WHITE))
        self.wait(1)

        # animate the change of position
        self.play(ApplyMethod(square.shift, UP))
        self.wait(1)
