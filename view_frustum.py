from manim import *
import numpy as np

class NBVVisualization(Scene):
    def create_entropy_animation(scene):
        # LaTeX formula
        formula = MathTex(
            r"I_v(x) = -p(x)\log_2(p(x)) - (1-p(x))\log_2(1-p(x))",
            font_size=36
        ).to_edge(UP)

        # Create axes
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1.2, 0.2],
            x_length=8,
            y_length=4,
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.2, 0.2)}
        ).shift(DOWN * 0.5)

        # Axis labels
        x_label = axes.get_x_axis_label("p(x)")
        y_label = axes.get_y_axis_label("I_v(x)")

        # Entropy function
        def entropy(p):
            if p <= 0 or p >= 1:
                return 0
            return -p * np.log2(p) - (1-p) * np.log2(1-p)

        # Plot the function
        graph = axes.plot(
            lambda x: entropy(x) if 0 < x < 1 else 0,
            x_range=[0.001, 0.999],
            color=YELLOW
        )

        # Sliding point
        t_tracker = ValueTracker(0.1)
        point = always_redraw(lambda: Dot(
                                  axes.c2p(t_tracker.get_value(), entropy(t_tracker.get_value())),
                                  color=RED,
                                  radius=0.08
                              ))

        # Point coordinates text
        coords = always_redraw(lambda: MathTex(
                                   f"({t_tracker.get_value():.2f}, {entropy(t_tracker.get_value()):.2f})",
                                   font_size=24
                               ).next_to(point, UR, buff=0.1))

        # Animations
        scene.play(Write(formula))
        scene.play(Create(axes), Write(x_label), Write(y_label))
        scene.play(Create(graph))
        scene.play(Create(point), Write(coords))

        # Animate sliding point
        scene.play(t_tracker.animate.set_value(0.9), run_time=4, rate_func=linear)
        scene.play(t_tracker.animate.set_value(0.1), run_time=4, rate_func=linear)
        scene.play(t_tracker.animate.set_value(0.5), run_time=2)

        scene.wait(2)

        scene.play(
            Uncreate(point),
            Unwrite(coords),
            Uncreate(graph),
            Uncreate(axes),
            Unwrite(x_label),
            Unwrite(y_label),
            Unwrite(formula)
        )

    def construct(self):
        # Camera position and parameters
        camera_pos = np.array([-4, 0, 0])
        view_angle = PI/6  # 60 degrees total
        view_distance = 6
        num_rays = 8  # Number of rays representing pixel resolution

        # Create camera point
        camera_point = Dot(camera_pos, color=BLUE, radius=0.1)
        camera_label = Text("Camera", font_size=20).next_to(camera_point, DOWN)

        # Calculate view cone boundaries
        half_angle = view_angle / 2
        direction = np.array([1, 0, 0])  # pointing right

        # View cone boundary lines
        upper_boundary = Line(
            camera_pos,
            camera_pos + view_distance * np.array([np.cos(half_angle), np.sin(half_angle), 0]),
            color=BLUE,
            stroke_width=2
        )
        lower_boundary = Line(
            camera_pos,
            camera_pos + view_distance * np.array([np.cos(-half_angle), np.sin(-half_angle), 0]),
            color=BLUE,
            stroke_width=2
        )

        # Create view cone area (filled)
        view_cone_points = [
            camera_pos,
            camera_pos + view_distance * np.array([np.cos(half_angle), np.sin(half_angle), 0]),
            camera_pos + view_distance * np.array([np.cos(-half_angle), np.sin(-half_angle), 0])
        ]
        view_cone = Polygon(*view_cone_points, color=BLUE, fill_opacity=0.1, stroke_width=0)

        # Generate uniform rays (representing camera pixels)
        rays = VGroup()
        ray_angles = np.linspace(-half_angle, half_angle, num_rays)

        for angle in ray_angles:
            ray_end = camera_pos + view_distance * np.array([np.cos(angle), np.sin(angle), 0])
            ray = Line(camera_pos, ray_end, color=YELLOW, stroke_width=1, stroke_opacity=0.7)
            rays.add(ray)

        # Generate voxels (green boxes) inside view cone
        visible_voxels = VGroup()
        hit_voxels = VGroup()  # Voxels that intersect with rays

        # Define voxel positions inside the view cone
        voxel_positions = [
            np.array([0, 0, 0]),
            np.array([0, 0.5, 0]),
            np.array([0.5, 0.5, 0]),
            np.array([0.5, 0, 0]),
            np.array([0.5, -0.5, 0]),
            np.array([0.5, -1, 0]),
            np.array([0.5, 1, 0]),
            np.array([1, 1, 0]),
            np.array([0, 0.5, 0]),
            np.array([0.5, 1.5, 0]),
            np.array([1, 0.5, 0]),
            np.array([-0.5, 0, 0]),
            np.array([0, -0.5, 0]),
            np.array([0, -1, 0]),
            np.array([-0.5, -1.5, 0]),
            np.array([0,  -1.5, 0]),
            np.array([0.5,  -1.5, 0]),
            np.array([1,  -1.5, 0]),
        ]

        # Check which voxels are hit by rays
        hit_positions = []
        for pos in voxel_positions:
            # Check if voxel is roughly aligned with any ray
            vec_to_voxel = pos - camera_pos
            angle_to_voxel = np.arctan2(vec_to_voxel[1], vec_to_voxel[0])

            # Check if this angle is close to any ray angle
            is_hit = False
            for ray_angle in ray_angles:
                if abs(angle_to_voxel - ray_angle) < 0.05:  # tolerance for intersection
                    is_hit = True
                    break

            if is_hit:
                hit_positions.append(pos)

        # Create voxels
        for pos in voxel_positions:
            voxel = Square(side_length=0.5, color=GREEN, fill_opacity=0.7)
            voxel.move_to(pos)

            if pos.tolist() in [p.tolist() for p in hit_positions]:
                # voxel.set_color(RED)
                hit_voxels.add(voxel)
            else:
                visible_voxels.add(voxel)

        # Generate occluded voxels outside view cone (dashed lines)
        occluded_voxels = VGroup()
        occluded_positions = [
            np.array([2, 3.5, 0]),
            np.array([3, -3, 0]),
            np.array([4, 4, 0]),
            np.array([1, -3.5, 0]),
            np.array([5, 2.5, 0]),
            np.array([0, 4, 0]),
            np.array([2, -4, 0]),
            np.array([4.5, -2.5, 0])
        ]

        for pos in occluded_positions:
            # Create dashed square by using multiple small rectangles
            voxel_outline = Square(side_length=0.3, color=GRAY, fill_opacity=0)
            voxel_outline.move_to(pos)

            # Create dashed effect by breaking the outline
            dashed_voxel = DashedVMobject(voxel_outline, num_dashes=8, color=GRAY)
            occluded_voxels.add(dashed_voxel)



        # Add legend
        legend = VGroup()
        legend_items = [
            ("Camera", BLUE),
            ("View Cone", BLUE),
            ("Uniform Rays", YELLOW),
            ("Visible Voxels", GREEN),
            ("Ray-Hit Voxels", RED),
            ("Occluded Voxels", GRAY)
        ]

        for i, (label, color) in enumerate(legend_items):
            item = VGroup()
            color_square = Square(side_length=0.2, color=color, fill_opacity=0.7)
            if label == "Occluded Voxels":
                color_square = DashedVMobject(Square(side_length=0.2, color=color, fill_opacity=0), num_dashes=4)
            text = Text(label, font_size=16, color=WHITE)
            item.add(color_square, text.next_to(color_square, RIGHT, buff=0.1))
            item.shift(DOWN * (i * 0.4 - 1.5) + RIGHT * 5)
            legend.add(item)

        # Animation sequence
        # Add title
        japanese_font = "Noto Serif CJK JP"
        title = Text("Volumetric NBV Algorithm (2D TOP Down view)", font_size=28, color=WHITE)
        title.to_edge(UP)
        jpTtitle = Text("日本語のアニメーション", font=japanese_font, font_size=48).next_to(title, DOWN, buff=0.5)
        self.play(Write(title), Write(jpTtitle))
        self.wait(0.5)
        self.play(Unwrite(title), Unwrite(jpTtitle))

        titlePart = Text("Plant (object) is represented as voxels", font_size=28, color=WHITE)
        titlePart.move_to(UP * 2.5)
        self.play(Write(titlePart))
        # Add voxels
        self.play(Create(visible_voxels), Create(hit_voxels), Create(occluded_voxels), run_time=2)
        self.wait(0.5)


        # What is a voxel part
        self.play(Unwrite(titlePart))
        titlePart = Tex(
            r"Each voxel $x$ holds an occupancy probability $p(x)$",
            font_size=28,
            color=WHITE
        )
        titlePart.move_to(UP * 2.5)
        self.play(Write(titlePart))
        smallX = Tex(
            r"$x$",
            font_size=32
        )
        smallX.move_to(RIGHT*3 + DOWN)

        arrow = Arrow(
            start=smallX.get_center(),
            end=hit_voxels[5].get_center(),
            color=WHITE
        )
        self.play(Write(smallX), Create(arrow))
        self.wait(0.5)
        text_block = MathTex(
            r"p(x) = 0 \rightarrow \text{ certainly empty} \\",
            r"p(x) = 0.5 \rightarrow \text{ uncertain} \\",
            r"p(x) = 1 \rightarrow \text{ certainly occupied}",
            font_size=32,
            color=WHITE
        ).to_edge(LEFT)
        self.play(Write(text_block))
        self.wait(1)
        self.play(Unwrite(text_block), Uncreate(arrow), Uncreate(smallX))
        self.play(Uncreate(visible_voxels), Uncreate(hit_voxels), Uncreate(occluded_voxels), run_time=2)

        # What is information gain
        self.play(Unwrite(titlePart))
        titlePart = Tex(
            r"Each voxel $x$ has an information function $I_v$",
            font_size=28,
            color=WHITE
        )
        titlePart.to_edge(UP)
        self.play(Write(titlePart))
        self.create_entropy_animation()
        self.wait(1)
        text_block = MathTex(
            r"p(x) = 0 \rightarrow \text{ certainly empty} \rightarrow I_v(x) \text{ will be lowest} \\",
            r"p(x) = 0.5 \rightarrow \text{ uncertain} \rightarrow I_v(x) \text{ will be highest} \\",
            r"p(x) = 1 \rightarrow \text{ certainly occupied} \rightarrow I_v(x) \text{ will be lowest}",
            font_size=32,
            color=WHITE
        ).to_edge(LEFT)
        self.play(Write(text_block))
        self.wait(1)
        self.play(Unwrite(text_block))

        # First Part
        self.play(Unwrite(titlePart))
        titlePart = Text("Camera is represented as a view cone", font_size=28, color=WHITE)
        titlePart.move_to(UP * 2.5)
        # Add camera
        self.play(Write(titlePart))
        self.play(Create(camera_point), Write(camera_label))
        self.wait(0.5)

        # Add view cone
        self.play(Create(view_cone), Create(upper_boundary), Create(lower_boundary))
        self.wait(0.5)
        self.wait(1)

        #Second part
        self.play(Unwrite(titlePart))
        titlePart = Text("Rays are casted from the camera origin", font_size=28, color=WHITE)
        titlePart.move_to(UP * 2)
        self.play(Write(titlePart))
        # Add rays (uniform, representing pixel resolution)
        self.play(Create(rays), run_time=2)
        self.wait(0.5)

        self.play(Unwrite(titlePart))
        titlePart = Text("Rays intersect with voxels", font_size=28, color=WHITE)
        titlePart.move_to(UP * 2)
        self.play(Write(titlePart))
        # Add voxels
        self.play(Create(visible_voxels), Create(hit_voxels), Create(occluded_voxels), run_time=2)
        self.wait(0.5)

        # Highlight ray-hit voxels

        # Add legend
        self.play(Create(legend), run_time=2)
        self.wait(2)

        # Optional: Animate ray scanning
        self.play(
            *[ray.animate.set_stroke(opacity=1, width=3) for ray in rays],
            run_time=1
        )
        self.play(
            *[ray.animate.set_stroke(opacity=0.7, width=1) for ray in rays],
            run_time=1
        )

        self.wait(3)

# To run this code, save it as a .py file and run:
# manim -pql filename.py NBVVisualization