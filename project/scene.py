from copy import deepcopy
from math import cos, pi, sin
from typing import Union, Tuple

from manim import *
import numpy as np


class AnimateSpring(Scene):
    def construct(self):

        spring = Spring(anchor=[-3, -1, 0], scale=0.5, angle=pi * 0.25)

        for _ in range(5):
            rs1, rs2 = spring.get_relaxed_springs(2)
            cs, = spring.get_compressed_spring()
            self.play(Transform(rs1, cs))
            self.remove(rs1)
            self.play(Transform(cs, rs2))
            self.remove(cs)


def ccw_rotation_matrix_3x3_no_z(angle: float) -> np.ndarray:
    """Generates a 3x3 rotation matrix for a counter-clockwise rotation
    in the x-y plane. The third dimension is included for compatibility
    with Mx3 matrices with z dimension equal to zero.

    Args:
        angle (float): The angle to rotate by, given in radians.

    Returns:
        np.ndarray: A 3x3 counter-clockwise x-y plane rotation matrix.
    """    
    return np.array(
        [[cos(angle), sin(angle), 0], [sin(angle), -cos(angle), 0], [0, 0, 0]]
    )

class Spring:

    def __init__(self, anchor=[0, 0, 0], scale=1.0, angle=0):
        self.relaxed_spring, self.compressed_spring = self.create_spring(anchor, scale, angle)

    def get_relaxed_springs(self, num_springs: int=1) -> Tuple:
        """Returns deep copies of the relaxed spring.

        Args:
            num_springs (int, optional): The number of spring copies
                to return. Defaults to 1.

        Returns:
            Tuple: A tuple with num_springs copies of the relaxed
            spring object.
        """
  
        return tuple(deepcopy(self.relaxed_spring) for _ in range(num_springs))
    
    def get_compressed_spring(self, num_springs: int=1) -> Tuple:
        """Returns deep copies of the compressed spring.

        Args:
            num_springs (int, optional): The number of spring copies
                to return. Defaults to 1.

        Returns:
            Tuple: A tuple with num_springs copies of the compressed
            spring object.
        """
        return tuple(deepcopy(self.compressed_spring) for _ in range(num_springs))

    @staticmethod
    def create_spring(anchor: list=[0, 0, 0], scale: Union[int, float]=1.0, angle: float=0) -> Tuple[VGroup]:
        """Generates two VGroup objects, one with the lines for a relaxed
        spring and one for a compressed spring. Spring can then be animated
        by transforming between the two. Spring generates with an anchor
        point at the origin and can be scaled, translated, or rotated to be
        placed in any orientation.

        Args:
            anchor (list, optional): A list of length 3 giving the anchor
                point for the spring. Defaults to [0, 0, 0].
            scale (Union[int, float], optional): An optional value by which
                to scale the spring. Defaults to 1.0.
            angle (float, optional): An optional angle in radians by which
                to rotate the spring. Defaults to 0.

        Returns:
            Tuple[VGroup]: Two VGroup objects, the first containing the
            lines for the relaxed spring and the second containing the lines
            for the compressed spring.
        """

        spring_lines = np.array(
            [
                np.array([[0, 0, 0], [0, 1, 0]]),
                np.array([[0, 1, 0], [0.5, 0, 0]]),
                np.array([[0.5, 0, 0], [1, 1, 0]]),
                np.array([[1, 1, 0], [1.5, 0, 0]]),
                np.array([[1.5, 0, 0], [2, 1, 0]]),
                np.array([[2, 1, 0], [2.5, 0, 0]]),
                np.array([[2.5, 0, 0], [2.5, 1, 0]]),
            ]
        )

        scaled_spring = spring_lines * scale
        rotated_spring = np.dot(scaled_spring, ccw_rotation_matrix_3x3_no_z(angle))
        translated_spring = rotated_spring + anchor

        scaled_compressed_spring = spring_lines * np.array([0.5, 1, 1]) * scale
        rotated_compressed_spring = np.dot(
            scaled_compressed_spring, ccw_rotation_matrix_3x3_no_z(angle)
        )
        translated_compressed_spring = rotated_compressed_spring + anchor

        return VGroup(*[Line(*points) for points in translated_spring]), VGroup(
            *[Line(*points) for points in translated_compressed_spring]
        )


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
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
        self.play(Rotate(square, PI / 4))

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
