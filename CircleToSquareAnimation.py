from manim import *
import math
import numpy as np
from manim.utils.color.DVIPSNAMES import MAGENTA


class CircleToSquareAnimation(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(1.35)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": GREEN, "length": 5},
            tips=False
        )
        R = Dot(axes.coords_to_point(0, 0), color=ORANGE)

        scale = 1
        house_points = [
            [0 * scale, 0 * scale, 0],
            [1 * scale, 0 * scale, 0],
            [1 * scale, 1 * scale, 0],
            [0.5 * scale, 1.5 * scale, 0],
            [0 * scale, 1 * scale, 0],
            [0 * scale, 0 * scale, 0]
        ]

        robot = Polygon(*house_points[:-1], color=BLUE, fill_opacity=0.3, stroke_width=3).move_to(R.get_center())
        box_with_label = VGroup(robot, MathTex("Robot").next_to(robot, RIGHT))
        self.play(Create(box_with_label))

        self.wait()

        O = Dot(axes.coords_to_point(0, 6), color=YELLOW)
        O_label = MathTex("Goal").next_to(O, DOWN)
        self.play(FadeIn(O), Write(O_label))

        self.wait()

        G1 = Dot(axes.coords_to_point(0.2, 3), color=BLUE)
        G2 = Dot(axes.coords_to_point(3.5, 2.678), color=RED)
        Gm = always_redraw(lambda: Dot((G1.get_center() + G2.get_center()) / 2, color=GREEN))
        Gm_label = always_redraw(lambda: MathTex("G_m").next_to(Gm, RIGHT))
        G1_label = always_redraw(lambda: MathTex("G_1").next_to(G1, LEFT))
        G2_label = always_redraw(lambda: MathTex("G_2").next_to(G2, DOWN))
        circle1 = Circle(radius=0.25, color=RED).move_to(G1)
        circle2 = Circle(radius=0.25, color=RED).move_to(G2)
        self.play(Create(circle1), Create(circle2))
        self.wait()
        R_label = MathTex("R").next_to(R, UP)
        r_group = VGroup(R, R_label)
        self.play(FadeIn(R), Write(R_label))
        self.play(FadeOut(box_with_label))
        self.wait()
        self.play(Create(G1), Create(G2))
        self.play(Create(Gm))
        self.play(FadeOut(circle1), FadeOut(circle2))
        self.play(Write(G1_label), Write(G2_label))
        self.play(Create(axes))
        self.wait()

        G1R = always_redraw(lambda: Line(G1.get_center(), R.get_center()))
        G1G2 = always_redraw(lambda: Line(G1.get_center(), G2.get_center()))

        angle = always_redraw(lambda: Angle(Line(G1.get_center(), R.get_center()),
                                             Line(G1.get_center(), G2.get_center()),
                                             radius=0.5))
        theta_label = always_redraw(lambda: MathTex("\\theta").next_to(angle, 0.7 * RIGHT + 0.7 * DOWN, buff=0.1))

        def calculate_angle():
            vec_G1R = R.get_center() - G1.get_center()
            vec_G1G2 = G2.get_center() - G1.get_center()

            vec1 = vec_G1R[:2]
            vec2 = vec_G1G2[:2]

            mag1 = np.linalg.norm(vec1)
            mag2 = np.linalg.norm(vec2)

            if mag1 == 0 or mag2 == 0:
                return 0.0

            dot_product = np.dot(vec1, vec2)
            cos_angle = dot_product / (mag1 * mag2)
            cos_angle = np.clip(cos_angle, -1.0, 1.0)
            return math.degrees(math.acos(cos_angle))

        theta_value_label = always_redraw(
            lambda: MathTex(f"\\theta = {calculate_angle():.2f}°")
            .set_color(WHITE)
            .scale(0.7)
            .move_to(self.camera.frame.get_left() + RIGHT)
        )
        self.wait()
        self.play(Create(G1G2), Create(angle), Create(G1R))
        self.play(self.camera.frame.animate.move_to(G1).scale(0.5))
        self.play(Write(theta_label))
        self.play(Write(theta_value_label))
        self.wait(2)
        #
        # G1.add_updater(lambda mob: mob.shift(UP +  RIGHT))
        self.play(G1.animate.shift(0.5 * UP + 0.2 * RIGHT))
        self.wait()
        self.play(G2.animate.shift(DOWN + 0.2 * LEFT))
        self.wait()
        self.play(G2.animate.shift(LEFT))
        self.play(self.camera.frame.animate.move_to(ORIGIN + 2* LEFT).scale(1.7))
        self.wait()
        self.play(FadeOut(G1G2), FadeOut(angle), FadeOut(G1R), FadeOut(theta_label))
        self.wait()

        equation_text = MathTex("G_m = \\frac{G_1 + G_2}{2}").set_color(WHITE).scale(0.8).move_to(theta_value_label.get_center() +                                                                                                  UP + RIGHT * 0.5)
        self.play(FadeIn(Gm_label), Write(equation_text))
        self.wait(3)
        # Fade out axes and G1 and G2
        self.play(FadeOut(axes), FadeOut(G1_label), FadeOut(G2_label))
        self.wait()
        arrow_r_gm = always_redraw(lambda: Arrow(R.get_center(), Gm.get_center(), color=TEAL))
        arrow_gm_goal = always_redraw(lambda: Arrow(Gm.get_center(), O.get_center(), color=TEAL))
        self.play(Create(arrow_r_gm), Create(arrow_gm_goal))
        for _ in range(5):
            self.play(*[FadeIn(arrow_gm_goal), FadeIn(arrow_r_gm)], run_time=0.5)
            self.play(*[FadeOut(arrow_gm_goal), FadeOut(arrow_r_gm)], run_time=0.5)
        self.wait()

        #Fade in G1 and G2 label again
        self.play(FadeIn(G1_label), FadeIn(G2_label))
        D = Dot(Gm.get_center(), color=RED)
        D_label = always_redraw(lambda: MathTex("D").next_to(D, DOWN))

        self.play(Create(D), Write(D_label))
        self.wait()
        def normal_vector():
            direction = G2.get_center() - G1.get_center()
            return normalize(rotate_vector(direction, PI / 2))

        # Step 4: Create a long dashed line in the direction of the normal vector
        length = 6
        def startline():
            return Gm.get_center() - normal_vector() * length / 2

        def endline():
            return Gm.get_center() + normal_vector() * length / 2

        perp_bisector = always_redraw(lambda: DashedLine(startline(), endline(), color=RED))
        perp_path = always_redraw(lambda: Line(startline(), endline()))
        # D.move_to(perp_path.get_start())

        self.play(Create(perp_bisector))
        self.wait()

        self.play(MoveAlongPath(D, perp_path), run_time=5, rate_func=there_and_back)
        self.wait()


        D.add_updater(lambda mob: mob.move_to(startline()))
        brace = always_redraw(lambda: BraceBetweenPoints(D.get_center(), Gm.get_center()))
        label = brace.get_text("Max distance").scale(0.5)
        label.add_updater(lambda m: m.next_to(brace, DOWN))
        self.play(Create(brace), Write(label))
        self.wait()

        self.play(G2.animate.shift(RIGHT * 2 + UP))

