from manim import *

class MovingPointAndLine(Scene):
    def construct(self):
        start_point = Dot(LEFT * 2, color=BLUE)
        moving_point = Dot(RIGHT * 2, color=RED)
        line = Line(start_point.get_center(), moving_point.get_center(), color=YELLOW)

        self.add(start_point, moving_point, line)

        def update_line(line):
            line.put_start_and_end_on(start_point.get_center(), moving_point.get_center())

        line.add_updater(update_line)

        self.play(moving_point.animate.move_to(UP * 2 + RIGHT * 2), run_time=3)
        self.play(moving_point.animate.move_to(DOWN * 2 + LEFT * 3), run_time=3)
        self.play(moving_point.animate.move_to(ORIGIN), run_time=3)
        self.wait()