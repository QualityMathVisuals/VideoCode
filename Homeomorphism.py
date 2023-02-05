from manim import *
import random

from QualityMathVis_Utils import ArrowDoubleEnded3D, CoffeeMug

BACKGROUND_COLOR = BLUE
FOREGROUND_COLOR = BLUE_C
RESOLUTION = 25


class DonutToCoffeeScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)

        self.display_exchange_objects()

    def display_exchange_objects(self):
        torus = Torus(major_radius=1.8, minor_radius=0.5, resolution=RESOLUTION,
                      checkerboard_colors=[PINK, LIGHT_BROWN])
        torus.shift(LEFT * 3)
        torus1 = torus.copy()

        coffee_mug = CoffeeMug(resolution=RESOLUTION)
        coffee_mug.scale(1.2)
        coffee_mug.shift(RIGHT * 3)
        self.play(Write(torus), Write(coffee_mug))
        self.wait(2)
        self.play(ReplacementTransform(torus, coffee_mug))
        self.wait(1)
        self.play(ReplacementTransform(coffee_mug, torus1))
        self.wait(2)
        self.play(FadeOut(torus1))


class ScribbleInBoxScene(ZoomedScene):
    def construct(self):
        # Create NumberPlane as background
        plane = NumberPlane(
            x_range=(-10, 10, 2),
            y_range=(-10, 10, 2),
            x_length=15,
            y_length=15,
            tips=True,
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            }
        ).set_opacity(0.8)

        self.play(DrawBorderThenFill(plane), run_time=0.5)

        # Create white box
        box = Rectangle(height=4, width=4, stroke_width=5).set_color([MAROON, ORANGE])

        self.play(Create(box), run_time=0.5)

        step_size = 0.001
        num_calls = int(1 / step_size)
        choice = []
        random.seed(100)
        random_vals = []
        for i in range(num_calls):
            if i < num_calls // 2:
                random_vals.append(random.random() * -0.05 - 1.45)
            else:
                random_vals.append(random.random() * 0.05 + 1.45)

        for _ in range(num_calls + 1):
            choice.append(random_vals[random.randint(0, num_calls - 1)])

        # Define parametric function for nearly space filling curve
        def space_filling_curve(t):
            j = int(t / step_size)
            y = choice[j]
            if t < 0.5:
                x = (4.4 * t) - 2
            elif 0.5 <= t <= 0.52:
                x = (4 * (t - 0.02 + (0.02 * ((t - 0.5) / 0.02))) - 2)
                y = 0.02 * choice[j]
            else:
                x = 4 * t - 2
            return x * RIGHT + y * UP

        t_param = ValueTracker(0)
        # Create nearly space filling curve
        curve = always_redraw(lambda:
                              ParametricFunction(space_filling_curve,
                                                 t_range=(0, 1, step_size),
                                                 color=MAROON,
                                                 stroke_width=3 - 2.6 * t_param.get_value())
                              )

        middle_part = ParametricFunction(space_filling_curve,
                                         t_range=(0.5, 0.52, step_size),
                                         color=GOLD,
                                         stroke_width=3 - 2.3 * 1,
                                         z_index=2)

        self.play(Create(curve), run_time=4)

        # Flash red and fade out
        self.activate_zooming(animate=True)
        self.play(t_param.animate.set_value(1))
        self.play(FadeIn(middle_part))
        self.wait(3.5)


class BriefOverviewScene(Scene):
    def construct(self):
        leading_question = VGroup(Tex(r'1. Can a ', r'continuous', r' function', r' from ',
                                      r'$\mathbb R \to \mathbb R^2$'), Tex(r' be ', r' onto', r' and ', r'one-to-one?')) \
            .arrange(DOWN, aligned_edge=LEFT).set_color_by_gradient(ORANGE, MAROON, BLUE, GREEN).to_edge(LEFT,
                                                                                                         buff=1).shift(
            UP * 3)
        two = Tex('2. Invertibility').set_color_by_gradient(ORANGE, MAROON, BLUE, GREEN).to_edge(LEFT, buff=1)
        topology_fin = Tex('3. Topology').set_color_by_gradient(ORANGE, MAROON, BLUE, GREEN).to_edge(LEFT,
                                                                                                     buff=1).shift(
            DOWN * 3)

        self.play(Write(leading_question), run_time=2)

        underlines = [
            Underline(leading_question[0][1], color=GOLD),
            Underline(leading_question[0][2], color=GOLD),
            Underline(leading_question[0][4], color=GOLD),
            Underline(leading_question[1][1], color=GOLD),
            Underline(leading_question[1][3], color=GOLD),
        ]

        for i in range(len(underlines)):
            self.play(Write(underlines[i], run_time=0.5))

        self.wait(2)
        self.play(FadeOut(*underlines), run_time=0.5)

        self.play(Write(two))
        self.wait(4)

        self.play(Write(topology_fin))
        self.wait(4)

        self.play(FadeOut(two, topology_fin), leading_question.animate.scale(1.3).center())
        self.wait(1.5)
        self.play(Indicate(leading_question[0][4]))
        self.wait(2)
        self.play(Indicate(leading_question[1][1]))
        self.play(Indicate(leading_question[1][3]))
        self.wait()


class FunctionExamplesScene(Scene):
    def construct(self):
        poly = MathTex(r'f(x) = x^2 + 1').scale(1.2).to_edge(UP, buff=1.5)
        self.play(Write(poly), run_time=1)
        self.wait(0.5)

        inputs = range(-1, 3)

        poly_sends = []
        for i in inputs:
            send = VGroup(
                Integer(i),
                Arrow(start=LEFT, end=RIGHT).set_color([ORANGE, MAROON]),
                Integer(i * i + 1)
            ).arrange(RIGHT).space_out_submobjects(1).center()
            poly_sends.append(send)

        maps_to = VGroup(*poly_sends).arrange(DOWN).space_out_submobjects(2).shift(DOWN)
        for mapping in maps_to:
            self.play(Write(mapping), run_time=0.5)

        self.wait(2)
        new_title = MathTex(r'f:', r'A', r' \to', r' B').scale(1.2).to_edge(UP, buff=1.5)
        self.play(FadeOut(maps_to))
        self.play(TransformMatchingTex(poly, new_title))
        self.wait()
        fin_title = MathTex(r'f:', r'[0, 1]', r' \to ', r'[0, 1]^2').move_to(new_title)

        self.play(TransformMatchingTex(new_title, fin_title), run_time=1)

        axes = Axes(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            y_length=5.5,
            x_length=5.5,
            axis_config={
                "stroke_color": GREY_A,
                "stroke_width": 2,
                "include_tip": False,
                "include_numbers": True,
            },
        )
        axes.shift(RIGHT * 3 + (DOWN / 2))
        in_line = NumberLine(x_range=np.array([0, 1]), length=4, tip_length=0.4).shift(LEFT * 3.5)

        def spiral(t):
            pt = axes.c2p(t * np.cos(4 * PI * t), t * t * np.sin(4 * PI * t))
            return np.array((pt[0], pt[1], 0))

        spiral_curve = ParametricFunction(spiral, t_range=np.array([0, 1]),
                                          fill_opacity=0,
                                          color=ORANGE,
                                          stroke_opacity=0.9)
        follow_dot = always_redraw(lambda: Dot(spiral_curve.get_end(), color=MAROON))

        self.play(TransformFromCopy(fin_title[1], in_line))
        self.play(TransformFromCopy(fin_title[3], axes))
        in_line = NumberLine(x_range=np.array([0, 1]), length=4, tip_length=0.4, include_numbers=True).shift(LEFT * 3.5)

        tracker = ValueTracker(0)
        dot = always_redraw(lambda:
                            Dot(in_line.n2p(tracker.get_value()),
                                color=MAROON,
                                radius=0.1,
                                fill_opacity=1)
                            )
        arrow = always_redraw(lambda:
                              Arrow(start=UP, end=DOWN).next_to(dot, UP).set_color([ORANGE, MAROON])
                              )
        number = DecimalNumber(0, color=ORANGE).next_to(arrow, UP)

        number.add_updater(lambda m: m.next_to(arrow, UP))
        number.add_updater(lambda m: m.set_value(in_line.p2n(dot.get_center())))

        function_equation = MathTex(r'f', r'(t) = (', r't \cos(4 \pi t), \,', r't^2\sin(4 \pi t)', ')', color=BLUE_A)
        function_equation.next_to(in_line, DOWN, buff=1.5)

        self.play(FadeIn(dot, arrow, number, function_equation), fin_title.animate.shift(UP))
        self.add(follow_dot)
        self.play(Create(spiral_curve), tracker.animate.set_value(1), run_time=4)
        self.wait(1)
        self.play(FadeOut(follow_dot, spiral_curve))

        gunction_equation = MathTex(r'g', r'(t) = (', r'2 \sin(2.6 \pi t), \,', r'\sin(2.8 \pi t)\sin(4 \pi t)', ')',
                                    color=BLUE_A)
        gunction_equation.next_to(in_line, DOWN, buff=1.5).scale(0.8)

        self.play(TransformMatchingTex(function_equation, gunction_equation))

        def continuous_func(t):
            x = 2 * np.sin(1.3 * TAU * t)
            y = 2 * np.sin(1.4 * TAU * t) * np.sin(2 * TAU * t)
            pt = axes.c2p(x, y)
            return np.array((pt[0], pt[1], 0))

        random.seed(10)
        random_inputs = [random.random() for _ in range(200)]
        # Plot the outputs
        dots = [Dot(
            continuous_func(random_inputs[i]), color=MAROON, radius=0.05
        ) for i in range(len(random_inputs))]

        for i in range(15):
            tracker.set_value(random_inputs[i])
            self.play(FadeIn(dots[i]), run_time=0.05)

        for i in range(15, len(random_inputs)):
            tracker.set_value(random_inputs[i])
            self.play(FadeIn(dots[i]), run_time=0.01)

        tracker.set_value(0)
        curve = ParametricFunction(continuous_func, t_range=(0, 1), color=ORANGE)
        self.play(Create(curve), tracker.animate.set_value(1), run_time=4)
        self.wait(2)


class TopologicalContinuityScene(ThreeDScene):
    def construct(self):
        def path_on_sphere_1(t):
            x = 1.095 * np.cos(t)
            y = (1.095 * np.sin(t)) - (1.095 * np.cos(t))
            z = 1.264 * np.sin(t)
            return np.array((x, y, z))

        def path_on_plane_1(t):
            return np.array((1.2 * np.cos(t), 1.2 * np.sin(t), 0))

        def path_on_sphere_2(t):
            x = 1.1 * np.cos(1.1 * t)
            y = 1.05 * (np.sin(1.1 * t) - np.cos(1.3 * t))
            z = 1.1 * np.sin(1.3 * t)
            return np.array((x, y, z))

        def path_on_plane_2(t):
            p = path_on_sphere_2(t)
            return np.array((p[0], p[1], 0))

        sphere, label, axes = self.transition()
        self.show_func_on_sphere(sphere, path_on_sphere_1, axes, path_on_plane_1)
        self.show_func_on_sphere(sphere, path_on_sphere_2, axes, path_on_plane_2, t_range=[0, 11 * PI])
        self.transition_out(sphere, label, axes)

    def transition(self):
        t_param = ValueTracker(-2)
        real_func = MathTex(r'f: ', r'\mathbb R', r' \to ', r'\mathbb R^2').scale(1.5).to_edge(UP)
        top_func = MathTex(r'f: ', r'S', r' \to ', r'\mathbb R^2').scale(1.5).to_edge(UP)
        real_func_example = always_redraw(lambda:
                                          MathTex(r'f(', int(t_param.get_value()), r') = (',
                                                  int(t_param.get_value()), ', ', int((t_param.get_value() ** 2)), ')')
                                          .next_to(real_func, DOWN))
        number_line = NumberLine(
            x_range=(-2, 2),
            length=4,
            include_tip=True,
            tip_width=0.2,
            tip_height=0.2,
            include_numbers=True,
        )
        number_line.next_to(real_func_example, DOWN).shift(LEFT * 2 + DOWN * 2)

        axes = Axes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            x_length=4,
            y_length=4,
            axis_config={"tip_width": 0.2,
                         "tip_height": 0.2},
            tips=True,
        )
        axes.next_to(real_func_example, DOWN).shift(RIGHT * 3)

        trace = ParametricFunction(lambda t: axes.c2p(np.array([[t], [t * t]])),
                                   t_range=[-2, 2], color=FOREGROUND_COLOR)
        dot = always_redraw(lambda:
                            Dot(number_line.n2p(t_param.get_value()), color=FOREGROUND_COLOR))

        self.add_fixed_in_frame_mobjects(real_func, top_func, real_func_example, number_line, axes, dot, trace)
        self.remove(trace, top_func)

        self.wait(0.5)
        self.play(Create(trace), t_param.animate.set_value(2), rate_func=linear, run_time=2)
        self.play(FadeOut(dot, trace, real_func_example))

        sphere = Sphere(radius=2, z_index=0,
                        checkerboard_colors=[FOREGROUND_COLOR, WHITE]).shift((DOWN * 4) + (IN * 2) + (LEFT * 2))
        number_line_2 = number_line.copy()
        self.remove_fixed_in_frame_mobjects(number_line_2)
        self.remove(number_line_2)
        number_line_2.move_to(sphere)

        self.set_camera_orientation(phi=70 * DEGREES, theta=20 * DEGREES)
        self.play(FadeTransform(number_line, number_line_2), rate_func=exponential_decay, run_time=0.2)
        self.remove(number_line)
        self.play(ReplacementTransform(number_line_2, sphere), Transform(real_func, top_func))
        self.play(Rotate(sphere, PI / 2), rate_func=linear, run_time=3)

        return sphere, top_func, axes

    def show_func_on_sphere(self, sphere, sphere_trace_func, axes, plot_trace_func, t_range=[0, TAU]):
        sphere_trace = ParametricFunction(sphere_trace_func, t_range=t_range, color=ORANGE, stroke_width=3, z_index=1)
        sphere_trace.move_to(sphere)

        plot_trace_func = ParametricFunction(plot_trace_func, t_range=t_range, color=ORANGE)
        self.add_fixed_in_frame_mobjects(plot_trace_func)
        self.remove(plot_trace_func)
        plot_trace_func.move_to(axes)

        self.play(Create(sphere_trace), Create(plot_trace_func), run_time=2)
        self.play(FadeOut(sphere_trace, plot_trace_func), run_time=0.5)

    def transition_out(self, sphere, label, axes):
        self.play(FadeOut(sphere, shift=IN), FadeOut(label, shift=UP), FadeOut(axes, shift=RIGHT), run_time=0.5)


def checkmark_on_label_animation(label):
    tex_template = TexTemplate()
    tex_template.add_to_preamble(r'\usepackage{amssymb}')
    checkmark = Tex(r'\checkmark', color=GREEN_B, tex_template=tex_template).scale(1.5)
    checkmark.next_to(label, RIGHT)

    return Succession(Write(checkmark), FadeOut(checkmark, run_time=0.5))


def cross_on_label_animation(label):
    cross = Tex(r'$\times$', color=RED_B).scale(1.5)
    cross.next_to(label, RIGHT)

    return Succession(Write(cross), FadeOut(cross, run_time=0.5))


class ContinuousSurjectionScene(Scene):
    def construct(self):
        self.add_coord_plane(animate=True)
        cont_label = self.add_label(r'Continuous', animate=True)
        onto_label = self.add_label(r'Onto', animate=False)
        self.remove(onto_label)

        def continuous_func(t):
            x = np.sin(1.3 * t)
            y = np.sin(1.4 * t) * np.sin(2 * t)
            return np.array((3 * x, 3 * y, 0))

        dot, path, t_param = self.add_moving_dot(continuous_func, t_range=[0, TAU], animate=True)
        self.draw_flash_then_fade(dot, path, FOREGROUND_COLOR, t_param, TAU)
        self.play(Transform(cont_label, onto_label))

        def oscillating_function(t):
            return np.array(((t - 9) / 2, 2 * np.sin(50 * t), 0))

        dot, path, t_param = self.add_moving_dot(oscillating_function, t_range=[0, 18], animate=False)
        self.draw_flash_then_fade(dot, path, FOREGROUND_COLOR, t_param, 18)

        self.wait(2)

    def add_coord_plane(self, animate=False):
        number_plane = NumberPlane(
            x_range=(-10, 10, 2),
            y_range=(-10, 10, 2),
            x_length=15,
            y_length=15,
            tips=True,
            background_line_style={
                "stroke_color": BACKGROUND_COLOR,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            }
        )

        if animate:
            self.play(Write(number_plane), run_time=1)
        else:
            self.add(number_plane)

        return number_plane

    def add_moving_dot(self, func, t_range=[0, 1], animate=False):
        t_param = ValueTracker(0)
        path = ParametricFunction(func, t_range=t_range, color=FOREGROUND_COLOR, stroke_width=4)

        dot = always_redraw(lambda:
                            Dot(func(t_param.get_value()), color=FOREGROUND_COLOR, z_index=1))
        if animate:
            self.play(FadeIn(dot), run_time=0.5)
        else:
            self.add(dot)

        return dot, path, t_param

    def draw_flash_then_fade(self, dot, path, color_choice, t_param, intersection_t, additional_animations=None):
        self.play(Create(path), t_param.animate.set_value(intersection_t), rate_func=linear, run_time=1.5)
        if additional_animations is None:
            self.play(VGroup(dot, path).animate.set_color(color_choice), rate_func=there_and_back, run_time=0.5)
        else:
            color_ani = AnimationGroup(VGroup(dot, path).animate.set_color(color_choice), rate_func=there_and_back,
                                       run_time=0.5)
            self.play(color_ani, additional_animations)
            path.set_color(FOREGROUND_COLOR)
            dot.set_color(FOREGROUND_COLOR)

        self.play(FadeOut(dot, path), run_time=0.5)

    def add_label(self, str_label, animate=False):
        label = Text(str_label, gradient=[BLUE_A, BLUE_B], z_index=2).scale(1.5)
        label.to_edge(DL, buff=1)
        if animate:
            self.play(Write(label), run_time=0.5)
        else:
            self.add(label)

        return label


class ContinuousOverlapScene(ContinuousSurjectionScene):
    def construct(self):
        self.add_coord_plane(animate=False)
        onto_label = self.add_label(r'Onto', animate=False)
        oto_label = self.add_label(r'One-to-one', animate=False)
        self.remove(oto_label)
        self.play(ReplacementTransform(onto_label, oto_label))
        oto_label_check_animation = checkmark_on_label_animation(oto_label)
        oto_label_cross_animation = cross_on_label_animation(oto_label)

        intersection_t = 1.52097

        def intersecting_scribble_1(t):
            x = np.sin(2 * t) * np.sin(2.8 * t) * np.sin(4 * t)
            y = np.sin(2 * t) * np.sin(2.9 * t) * np.sin(1 * t)
            return np.array((5 * x, 6 * y, 0))

        dot, path, t_param = self.add_moving_dot(intersecting_scribble_1, t_range=[0, intersection_t], animate=True)
        self.draw_flash_then_fade(dot, path, RED_B, t_param, intersection_t, oto_label_cross_animation)

        stop_t = PI

        def nonintersecting_scribble_2(t):
            x = t * np.cos(13 * t)
            y = t * np.sin(13 * t)
            return np.array((x, y, 0))

        dot, path, t_param = self.add_moving_dot(nonintersecting_scribble_2, t_range=[0, stop_t], animate=True)
        self.draw_flash_then_fade(dot, path, GREEN_B, t_param, stop_t, oto_label_check_animation)

        intersection_t = 1.9194

        def intersecting_scribble_2(t):
            x = np.sin(t) * np.sin(1.6 * t) * np.sin(7 * t)
            y = np.sin(1.4 * t) * np.sin(2.3 * t) * np.sin(3.1 * t)
            return np.array((5 * x, 5 * y, 0))

        dot, path, t_param = self.add_moving_dot(intersecting_scribble_2, t_range=[0, intersection_t], animate=True)
        self.draw_flash_then_fade(dot, path, RED_B, t_param, intersection_t, oto_label_cross_animation)

        stop_t = TAU

        def nonintersecting_scribble_1(t):
            x = t
            y = np.sin(8 * t) * np.sin(9 * t)
            return np.array((x - (stop_t / 2), 3 * y, 0))

        dot, path, t_param = self.add_moving_dot(nonintersecting_scribble_1, t_range=[0, stop_t], animate=True)
        self.draw_flash_then_fade(dot, path, GREEN_B, t_param, stop_t, oto_label_check_animation)


class CombinationTransitionScene(Scene):
    def construct(self):
        combination_term = Tex(r'continuous $\qquad$', r'onto $\qquad$', r'one-to-one $\qquad$').to_edge(UP)

        # Have video clips in the middle here underneath the word

        function = MathTex(r'f \, : \, \mathbb R \, \, \to \, \, \mathbb R^2').to_edge(DOWN)

        self.play(FadeIn(combination_term[0], shift=DOWN), run_time=0.75)
        self.play(FadeIn(combination_term[1], shift=DOWN), run_time=0.75)
        self.play(FadeIn(combination_term[2], shift=DOWN), run_time=0.75)
        self.play(FadeIn(function, shift=UP), run_time=1.25)
        cross = MathTex(r'\times', color=RED_B, z_index=1).scale(30)
        self.wait()
        self.play(Write(cross))
        self.wait()


class CloseToSurjectionScene(ContinuousSurjectionScene):
    def construct(self):
        label = self.add_label(r'Does not exist', animate=False)
        label.set_color_by_gradient(RED_B, RED_A)
        label.set_z_index(1)

        self.add_coord_plane(animate=True)

        def attempting_to_surject(t):
            return np.array((t - 10, 10 * np.sin(99 * t), 0))

        dot, path, t_param = self.add_moving_dot(attempting_to_surject, t_range=[0, 20], animate=False)
        self.draw_flash_then_fade(dot, path, FOREGROUND_COLOR, t_param, 20)


class FiniteFunctionScene(ThreeDScene):
    def construct(self):
        self.next_section("Intro", skip_animations=True)
        onto_label = self.add_label(r'Onto')
        oto_label = self.add_label(r'One-to-one')
        oto_onto_label = self.add_label(r'Onto and One-to-one')
        self.remove(onto_label, oto_label, oto_onto_label)

        self.set_camera_orientation(phi=70 * DEGREES, theta=20 * DEGREES)
        self.begin_ambient_camera_rotation(0.15)

        self.add_axes(True)
        in_dots = self.add_random_points(color=GREEN_B, box_length=1.5, animate=False)
        in_dots.shift(RIGHT * 3)
        out_dots = self.add_random_points(color=RED_B, box_length=1.5, animate=False)
        out_dots.shift(LEFT * 3)

        self.remove(in_dots, out_dots)
        self.play(Create(in_dots), run_time=2)
        self.wait(0.5)
        self.play(Create(out_dots), run_time=2)
        self.wait()
        arrows = self.get_random_arrows(in_dots, out_dots)

        # self.show_example_dots(in_dots, out_dots)
        self.play(Create(arrows), run_time=4)
        self.wait(2)
        self.play(FadeOut(arrows, in_dots, out_dots), run_time=0.5)

        self.next_section("Oto and Onto", skip_animations=True)
        self.show_onto_example(onto_label)
        self.play(FadeOut(onto_label, run_time=0.5), FadeIn(oto_label))
        self.show_oto_example(oto_label)

        self.next_section("Bijection", skip_animations=False)
        self.play(Create(in_dots), Create(out_dots))
        self.play(Create(arrows), run_time=2)
        self.play(FadeOut(oto_label, run_time=0.5), FadeIn(oto_onto_label))
        self.play(AnimationGroup(*[MoveToTarget(arrow) for arrow in arrows]), run_time=2)
        self.wait()
        self.play(Indicate(out_dots))
        self.play(Indicate(in_dots))
        self.wait()
        self.play(
            *[arrow.animate.set_color_by_gradient(BLUE, GREEN).show_start_arrow() for arrow in arrows],
        )
        self.wait()
        self.interchange_dots(in_dots, out_dots)
        self.wait(5)

    def add_label(self, str, animate=False):
        label = Text(str, gradient=[BLUE_A, BLUE_B], z_index=2).scale(1.5)
        label.to_edge(DL, buff=1)

        self.add_fixed_in_frame_mobjects(label)
        self.remove(label)

        if animate:
            self.play(Write(label), run_time=0.5)
        else:
            self.add(label)

        return label

    def show_checkmark_on_label(self, label):
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r'\usepackage{amssymb}')
        checkmark = Tex(r'\checkmark', color=GREEN_B, tex_template=tex_template).scale(2.5)
        checkmark.next_to(label, RIGHT)
        self.add_fixed_in_frame_mobjects(checkmark)
        self.remove(checkmark)

        self.play(Succession(Write(checkmark), FadeOut(checkmark, run_time=0.5)))

    def show_cross_on_label(self, label):
        cross = Tex(r'$\times$', color=RED_B).scale(2.5)
        cross.next_to(label, RIGHT)
        self.add_fixed_in_frame_mobjects(cross)
        self.remove(cross)

        self.play(Succession(Write(cross), FadeOut(cross, run_time=0.5)))

    def add_axes(self, animate=False):
        axes = ThreeDAxes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            z_range=(-5, 5),
            x_length=7,
            y_length=7,
            z_length=7,
            tips=True,
            axis_config={"tip_width": 0.2,
                         "tip_height": 0.2},
        )

        if animate:
            self.play(DrawBorderThenFill(axes))
        else:
            self.add(axes)

        return axes

    def add_random_points(self, num_dots=10, center=np.array((0, 0, 0)), color=WHITE, box_length=2, animate=False):
        dots = VGroup()
        random.seed(10)
        for i in range(num_dots):
            x = random.uniform(-1 * box_length, box_length)
            y = random.uniform(-1 * box_length, box_length)
            z = random.uniform(-1 * box_length, box_length)
            center_C = center + np.array((x, y, z))
            dots.add(Dot3D(center_C, color=color))

        if animate:
            self.play(Create(dots), run_time=0.5)
        else:
            self.add(dots)

        return dots

    def get_random_arrows(self, in_dots, out_dots, color=FOREGROUND_COLOR):
        n = len(in_dots)
        arrows = VGroup()
        for i in range(n):
            o = random.randint(0, n - 1)
            strt = in_dots[i].get_center()
            end = out_dots[o].get_center()
            end_tgt = out_dots[i].get_center()

            arrow_to_add = ArrowDoubleEnded3D(
                start=strt,
                end=end,
                color=color,
                show_start_arrow=False,
                target=ArrowDoubleEnded3D(start=strt, end=end_tgt, color=color, show_start_arrow=False).scale(0.9)
            ).scale(0.9)

            arrows.add(arrow_to_add)

        return arrows

    def show_example_dots(self, in_dots, out_dots):
        first_three_in = []
        first_three_out = []
        sample_batch = 3
        for i in range(sample_batch):
            first_three_in.append(in_dots[i].copy())
            first_three_out.append(out_dots[i].copy())

        self.add(*first_three_in)
        self.play(FadeOut(in_dots, out_dots), run_time=0.5)

        for i in range(len(first_three_in)):
            self.play(ReplacementTransform(first_three_in[i], first_three_out[i], run_time=1.5))

        self.play(FadeIn(in_dots, out_dots), run_time=0.5)
        self.remove(*first_three_out)

    def show_onto_example(self, label, num_in_dots=3, num_out_dots=3):
        in_dots = self.add_random_points(num_dots=num_in_dots, color=GREEN_B, box_length=1.5, animate=False)
        in_dots.shift(RIGHT * 3)
        out_dots = self.add_random_points(num_dots=num_out_dots, color=RED_B, box_length=1.5, animate=False)
        out_dots.shift(LEFT * 3)

        arrows = VGroup()
        for i in range(num_in_dots):
            arrows.add(
                Arrow3D(
                    start=in_dots[i].get_center(),
                    end=out_dots[random.randint(0, num_out_dots - 2)].get_center(),
                    color=FOREGROUND_COLOR,
                    target=Arrow3D(
                        start=in_dots[i].get_center(),
                        end=out_dots[i].get_center(),
                        color=FOREGROUND_COLOR
                    ).scale(0.9)
                ).scale(0.9)
            )

        self.play(Create(in_dots), Create(out_dots))
        self.play(Write(label))
        self.play(Create(arrows))
        self.show_cross_on_label(label)
        self.wait(0.5)
        self.play(AnimationGroup(*[MoveToTarget(arrow) for arrow in arrows]))
        self.show_checkmark_on_label(label)
        self.wait(0.5)
        self.play(FadeOut(arrows, in_dots, out_dots))

    def show_oto_example(self, label, num_in_dots=3, num_out_dots=5):
        in_dots = self.add_random_points(num_dots=num_in_dots, color=GREEN_B, box_length=1.5, animate=False)
        in_dots.shift(RIGHT * 3)
        out_dots = self.add_random_points(num_dots=num_out_dots, color=RED_B, box_length=1.5, animate=False)
        out_dots.shift(LEFT * 3)

        arrows = VGroup()
        for i in range(num_in_dots):
            arrows.add(Arrow3D(start=in_dots[i].get_center(),
                               end=out_dots[0].get_center(),
                               color=FOREGROUND_COLOR,
                               target=Arrow3D(start=in_dots[i].get_center(),
                                              end=out_dots[i].get_center(),
                                              color=FOREGROUND_COLOR).scale(0.9)).scale(0.9))

        self.play(FadeIn(in_dots, out_dots))
        self.play(Create(arrows))
        self.show_cross_on_label(label)
        self.wait(0.5)
        self.play(AnimationGroup(*[MoveToTarget(arrow) for arrow in arrows]))
        self.show_checkmark_on_label(label)
        self.wait(0.5)
        self.play(FadeOut(arrows, in_dots, out_dots))

    def interchange_dots(self, in_dots, out_dots):
        green_move = AnimationGroup(
            *[in_dots[i].animate.move_to(out_dots[i].get_center()) for i in range(len(in_dots))]
        )
        red_move = AnimationGroup(*[out_dots[i].animate.move_to(in_dots[i].get_center()) for i in range(len(out_dots))])

        self.play(green_move, red_move, run_time=2)
        green_move = AnimationGroup(
            *[in_dots[i].animate.move_to(out_dots[i].get_center()) for i in range(len(in_dots))]
        )
        red_move = AnimationGroup(*[out_dots[i].animate.move_to(in_dots[i].get_center()) for i in range(len(out_dots))])
        self.play(green_move, red_move, run_time=2)


class DefineInvertibleFuncScene(Scene):
    def construct(self):
        invertible = Tex(r'Invertible').set_color_by_gradient(ORANGE, MAROON_A).scale(1.5).shift(UP * 2)
        in_text = Tex(r'Input').scale(1.5).shift(LEFT * 3)
        out_text = Tex(r'Output').scale(1.5).shift(RIGHT * 3)
        arrow = DoubleArrow(start=LEFT * 1, end=RIGHT * 1, color=MAROON_A).scale(2)
        arrow_lbl = MathTex(r'f').scale(2).next_to(arrow, DOWN).set_color(MAROON_A)
        oto_onto = Tex(r'One to one and onto').set_color_by_gradient(ORANGE, MAROON_A).scale(1.5).shift(DOWN * 2)
        self.play(Write(invertible))
        self.play(DrawBorderThenFill(arrow), DrawBorderThenFill(arrow_lbl), Write(in_text), Write(out_text))
        self.wait(1)
        self.play(Write(oto_onto))
        self.wait(1)
        self.play(in_text.animate.shift(RIGHT * 6), out_text.animate.shift(LEFT * 6), rate_func=there_and_back,
                  run_time=2)
        self.wait(1)


class TransitionToContinuousBijectionScene(Scene):
    def construct(self):
        leading_question = VGroup(
            Tex(r'1. Can a ', r'continuous', r' function', r' from ', r'$\mathbb R \to \mathbb R^2$', r' be '),
            Tex(r'one-to-one', r' and ', r'onto?'),
        ).arrange(DOWN, aligned_edge=LEFT).set_color_by_gradient(ORANGE, MAROON, BLUE, GREEN).to_edge(LEFT).shift(RIGHT)
        isolated_terms = VGroup(
            Tex('continuous').set_color_by_gradient(ORANGE, MAROON, BLUE),
            leading_question[1].copy()
        ).arrange(RIGHT).scale(1.4)
        new_term = Tex(r'invertible').scale(1.4)
        new_term.set_color_by_gradient(TEAL, GREEN).move_to(isolated_terms[1])

        self.play(Write(leading_question), run_time=2)
        self.wait()
        self.play(TransformMatchingTex(leading_question, isolated_terms))

        unds = [
            Underline(isolated_terms[0], color=GOLD),
            Underline(isolated_terms[1][0], color=GOLD),
            Underline(isolated_terms[1][2], color=GOLD),
        ]

        self.play(Write(unds[0]), run_time=0.5)
        self.play(FadeOut(unds[0]), run_time=0.5)
        self.play(Write(unds[1]), run_time=0.5)
        self.play(FadeOut(unds[1]), run_time=0.5)
        self.play(Write(unds[2]), run_time=0.5)
        self.play(FadeOut(unds[2]), run_time=0.5)
        self.play(TransformMatchingTex(VGroup(*isolated_terms[1:]), new_term), run_time=1.25)
        self.wait(2)


class HomeomorphicExamplesScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(0.15)

        self.go_through_fun_shapes()
        self.go_through_torus_examples()

    def go_through_fun_shapes(self):
        sphere = Sphere(radius=3, checkerboard_colors=[GREEN_A, GREEN_C], resolution=20)
        cube = Cube(side_length=6)
        cone = Cone(base_radius=3, height=6, checkerboard_colors=[RED_C, ORANGE], resolution=20).center()
        prism = Prism(dimensions=[7, 3, 5], sheen_factor=20, sheen_direction=RIGHT, fill_color=PURPLE_B)

        self.play(DrawBorderThenFill(sphere))
        self.play(ReplacementTransform(sphere, cube))
        self.wait()
        self.play(ReplacementTransform(cube, cone))
        self.wait()
        self.play(ReplacementTransform(cone, prism))
        self.wait()
        self.play(FadeOut(prism))

    def go_through_torus_examples(self):
        torus = [
            Torus(major_radius=2, minor_radius=0.8, checkerboard_colors=[GREEN_B, BLUE]),
            Torus(major_radius=1, minor_radius=0.2, checkerboard_colors=[GOLD, YELLOW_A]),
            Torus(major_radius=3, minor_radius=1, checkerboard_colors=[LIGHT_PINK, PURPLE])
                .rotate_about_origin(60 * DEGREES, axis=RIGHT + OUT + UP),
        ]
        self.play(Create(torus[0]))
        self.wait()
        self.play(ReplacementTransform(torus[0], torus[1]))
        self.wait()
        self.play(ReplacementTransform(torus[1], torus[2]))
        self.wait()
        self.play(FadeOut(torus[2]))


class FlatHomeomorphismExampleScene(Scene):
    def construct(self):
        self.show_simple_shapes()
        self.show_line_examples()

    def show_simple_shapes(self):
        stk_width = 10
        circle = Circle(radius=3, stroke_width=stk_width, color=TEAL_B).scale(0.4)
        circle.to_corner(UL, buff=1)
        square = Square(side_length=6, stroke_width=stk_width, color=BLUE_B).scale(0.4)
        square.to_corner(UR, buff=1)
        triangle = Triangle(stroke_width=stk_width, color=MAROON).scale(3).scale(0.5)
        triangle.to_corner(DL, buff=1)
        rectangle = Rectangle(width=6, height=3, stroke_width=stk_width, color=PURPLE).scale(0.5)
        rectangle.to_corner(DR, buff=1)
        arrows = VGroup(
            DoubleArrow(start=circle.get_center(), end=square.get_center()).scale(0.7).set_color([TEAL_B, BLUE_B]),
            DoubleArrow(start=square.get_center(), end=rectangle.get_center()).scale(0.7).set_color([BLUE_B, MAROON]),
            DoubleArrow(start=triangle.get_center(), end=rectangle.get_center()).scale(0.7).set_color([MAROON, PURPLE]),
        )
        arrow_labels = VGroup(
            MathTex('f').set_color([TEAL_B, BLUE_B]).next_to(arrows[0], DOWN),
            MathTex('g').set_color([BLUE_B, MAROON]).next_to(arrows[1], LEFT),
            MathTex('h').set_color([MAROON, PURPLE]).next_to(arrows[2], UP),
        )

        label = Text("Continuous and Invertible", font_size=52, gradient=[TEAL, GREEN])

        self.play(DrawBorderThenFill(arrows), Write(arrow_labels), Create(circle), Create(square), Create(triangle), Create(rectangle), Write(label))
        self.wait(0.25)
        self.play(ReplacementTransform(circle, square))
        self.wait(0.25)
        self.play(ReplacementTransform(square, rectangle))
        self.wait(0.25)
        self.play(ReplacementTransform(rectangle, triangle))
        self.wait(0.25)
        self.play(FadeOut(rectangle, triangle, label, arrows, arrow_labels), run_time=0.5)

    def show_line_examples(self, segments=10, length=3):
        lines = VGroup(*[
            Line(
                start=length * (RIGHT * (i / segments)),
                end=length * (RIGHT * ((i + 1) / segments)),
                stroke_width=10,
                color=FOREGROUND_COLOR,
                target=Line(
                    start=np.array([
                        int(length * np.cos((PI / 2) * i)) * (i / segments),
                        int(length * np.sin((PI / 2) * i)) * (i / segments),
                        0
                    ]),
                    end=np.array([
                        int(length * np.cos((PI / 2) * (i + 1))) * ((i + 1) / segments),
                        int(length * np.sin((PI / 2) * (i + 1))) * ((i + 1) / segments),
                        0
                    ]),
                    stroke_width=10,
                    color=FOREGROUND_COLOR,
                )
            )
            for i in range(segments)
        ])
        lines.set_color_by_gradient(BLUE_B, YELLOW_A, GREEN)
        lines.scale(2)
        lines.center()
        lines.save_state()

        lines_2 = VGroup(*[
            Line(
                start=length * (RIGHT * (i / segments)),
                end=length * (RIGHT * ((i + 1) / segments)),
                stroke_width=10,
                color=FOREGROUND_COLOR,
                target=Line(
                    start=np.array([
                        length * (i / segments),
                        int(length * np.sin((PI / 2) * i)) * (i / segments),
                        0
                    ]),
                    end=np.array([
                        length * ((i + 1) / segments),
                        int(length * np.sin((PI / 2) * (i + 1))) * ((i + 1) / segments),
                        0
                    ]),
                    stroke_width=10,
                    color=FOREGROUND_COLOR,
                )
            )
            for i in range(segments)
        ])
        lines_2.set_color_by_gradient(BLUE_B, YELLOW_A, GREEN)
        lines_2.scale(2)
        lines_2.center()
        lines_2.save_state()

        self.play(Succession(*[Create(line, run_time=1 / segments) for line in lines]))
        self.play(*[MoveToTarget(line) for line in lines])
        self.play(lines.animate.restore())
        self.remove(lines)
        self.add(lines_2)
        self.play(*[MoveToTarget(line) for line in lines_2])
        self.play(lines_2.animate.restore())

        rect = Rectangle(width=6, height=4, fill_opacity=1, fill_color=[RED_B, ORANGE])
        self.play(ReplacementTransform(lines_2, rect))
        self.play(lines_2.animate.restore(), FadeOut(rect, run_time=0.5))

        length = length * (segments / 4)
        lines_3 = VGroup(*[
            Line(
                start=length * (RIGHT * (i / segments)),
                end=length * (RIGHT * ((i + 1) / segments)),
                stroke_width=10,
                color=FOREGROUND_COLOR,
                target=Line(
                    start=np.array([
                        int(0.5 * length * np.cos((PI / 2) * i)),
                        int(0.5 * length * np.sin((PI / 2) * i)),
                        0
                    ]),
                    end=np.array([
                        int(0.5 * length * np.cos((PI / 2) * (i + 1))),
                        int(0.5 * length * np.sin((PI / 2) * (i + 1))),
                        0
                    ]),
                    stroke_width=10,
                    color=FOREGROUND_COLOR,
                )
            )
            for i in range(4)
        ])
        lines_3.set_color_by_gradient(BLUE_B, YELLOW_A, GREEN)
        lines_3.scale(2)
        lines_3.center()
        lines_3.save_state()
        self.remove(lines_2)
        self.add(lines_3)
        self.play(*[MoveToTarget(line) for line in lines_3])
        self.play(lines_3.animate.set_color(RED_B), rate_func=there_and_back)
        discontinuity = Dot(lines_3[3].get_end(), color=RED_E, radius=0.15)
        self.play(FadeIn(discontinuity), run_time=0.5)
        self.play(Indicate(discontinuity))
        self.play(FadeOut(discontinuity), run_time=0.5)
        cross = MathTex(r'\times', color=RED_B, z_index=1).scale(30)
        self.play(Write(cross), lines_3.animate.restore())
        self.play(FadeOut(lines_3, cross))


class SphereVersusDonutScene(ThreeDScene):
    def construct(self):
        sphere = Sphere(radius=1.3, checkerboard_colors=[BLUE_B, LIGHT_GRAY], resolution=RESOLUTION).shift(1.5 * RIGHT)
        sphere_cpy = sphere.copy()
        torus_main = Torus(minor_radius=0.6, major_radius=1.3, checkerboard_colors=[LIGHT_BROWN, PINK], resolution=RESOLUTION).shift(
            2.5 * LEFT)
        torus_temp = Torus(minor_radius=0.8, major_radius=0.8, checkerboard_colors=[BLUE_B, LIGHT_GRAY], resolution=RESOLUTION)
        self.set_camera_orientation(phi=70 * DEGREES, theta=95*DEGREES)
        self.begin_ambient_camera_rotation(0.15)

        self.play(DrawBorderThenFill(torus_main))
        self.play(DrawBorderThenFill(sphere))
        self.play(FadeOut(torus_main), sphere.animate.center().scale(1.2))

        self.wait()
        self.play(ReplacementTransform(sphere, torus_temp))
        self.wait()
        self.move_camera(phi=30*DEGREES)

        red_dot = Dot3D(color=RED, radius=0.2).shift(OUT*0.3)
        self.play(FadeIn(red_dot))
        self.play(Indicate(red_dot))
        self.play(FadeOut(red_dot), run_time=0.5)
        self.play(ReplacementTransform(torus_temp, sphere_cpy))
        self.play(FadeIn(torus_main), sphere_cpy.animate.shift(2 * RIGHT))
        self.wait(3)

class ChangedQuestionScene(Scene):
    def construct(self):
        start_title = VGroup(Tex(r'Continuous and invertible '), MathTex(r'f', r':[0, 1]', r' \to ', r'[0, 1]^2'))\
            .arrange(RIGHT).set_color_by_gradient(ORANGE, MAROON, BLUE)
        arrow = DoubleArrow(start=LEFT * 2, end=RIGHT * 2).set_color([ORANGE, MAROON, BLUE])
        int_title = start_title[1].copy().center().to_edge(UP, buff=1)
        int_title_cpy = int_title.copy()
        fin_title = MathTex(r'f').next_to(arrow, DOWN)

        self.play(Write(start_title), run_time=2)
        self.wait()
        self.play(TransformMatchingTex(start_title, int_title))

        box = Rectangle(width=3.5, height=3.5, fill_opacity=1).set_color([BLUE, GREEN]).shift(RIGHT * 4)
        box_cpy = box.copy()

        in_line = NumberLine(x_range=np.array([0, 1]), length=3, tip_length=0.4).shift(LEFT * 4)
        in_line_cpy = in_line.copy()

        self.play(TransformFromCopy(int_title[1], in_line))
        self.play(TransformFromCopy(int_title[3], box))
        self.play(TransformMatchingTex(int_title, fin_title), ReplacementTransform(int_title_cpy, arrow))
        self.play(Indicate(in_line))
        self.play(Indicate(box))
        self.wait(0.5)
        self.play(ReplacementTransform(in_line, box))
        self.wait(0.5)
        self.play(ReplacementTransform(box, in_line_cpy))
        self.wait(0.5)
        self.play(FadeIn(box_cpy))
        question_marks = Tex('The same???').set_color_by_gradient(BLUE, GREEN).next_to(arrow, UP)
        self.wait(1)
        self.play(Write(question_marks))
        cross = MathTex(r'\times', color=RED_B).scale(8)
        self.wait(3)
        self.play(Write(cross))
        self.wait()
        self.play(FadeOut(cross))
        self.wait(1)

COLOR_GRAD = [PURPLE_B, MAROON_B, BLUE_C, TEAL_C, YELLOW_C, GREEN_C, LIGHT_BROWN]
ROTATION_CONSTANT = (20 * DEGREES, RIGHT + UP + OUT)


class TopologyOfLineScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=220 * DEGREES)
        self.begin_ambient_camera_rotation(0.15)

        line, plane = self.introduce_objects(animate=True)
        self.bend_line_into_loop(line, animate=False)
        self.embeded_hilbert_curves(plane, animate=False)
        self.remove_point_examples(line, plane, animate=True)

    def introduce_objects(self, animate=False):
        line_length = 6 * 0.5
        real_line = ArrowDoubleEnded3D(start=RIGHT * line_length, end=LEFT * line_length, color=FOREGROUND_COLOR)
        plane = Rectangle(width=6, height=6, fill_opacity=1, fill_color=[TEAL, GREEN])
        plane.rotate(ROTATION_CONSTANT[0], ROTATION_CONSTANT[1])
        plane.pieces = VGroup(
            *plane.get_pieces(20)
        )
        plane.add(plane.pieces)
        plane.set_shade_in_3d(True)

        if animate:
            self.play(DrawBorderThenFill(real_line), run_time=1)
            self.wait(0.5)
            self.play(FadeOut(real_line), run_time=0.5)
            self.play(DrawBorderThenFill(plane), run_time=1)
            self.wait(0.5)
            self.play(FadeOut(plane), run_time=0.5)

        return real_line, plane

    def bend_line_into_loop(self, line, animate=False):
        intersection_t = 0.747998

        def loop_func(t):
            x = np.cos(10.5 * t)
            y = 2 * np.sin(3.5 * t)
            return np.array((x, x, y))

        intersection_pt = Dot3D(loop_func(intersection_t), color=RED_B, radius=0.15, z_index=2)

        loop = ParametricFunction(loop_func, t_range=[0, 1], stroke_width=10, stroke_color=FOREGROUND_COLOR, z_index=1)

        if animate:
            self.play(Write(line))
            self.play(Create(loop, run_time=3), FadeOut(line, run_time=0.3))
            self.wait()
            self.play(FadeIn(intersection_pt))
            self.play(Indicate(intersection_pt))
            self.wait()
            self.play(FadeOut(loop, intersection_pt))

    def embeded_hilbert_curves(self, plane, animate=False):

        def hilbertCurve(order=1, x_initial=0, y_initial=0):
            segment_length = 5 / (2 ** order)
            stroke_width = (-3 / 7) * order + (31 / 7)
            segments = VGroup()

            directions = hilbert(level=order)
            prevCenter = np.array((x_initial, y_initial, 0.))

            for direct in directions:
                dirTranslate = UP
                if direct == 'LEFT':
                    dirTranslate = LEFT
                if direct == 'RIGHT':
                    dirTranslate = RIGHT
                if direct == 'DOWN':
                    dirTranslate = DOWN

                endPt = np.copy(prevCenter + (segment_length * dirTranslate))
                segments.add(Line3D(start=prevCenter, end=endPt, stroke_width=stroke_width, resolution=3))
                prevCenter = endPt

            segments.set_color_by_gradient(*COLOR_GRAD)

            return segments

        def hilbert(level=1, direction='UP'):
            directions = []
            if level == 1:
                if direction == 'LEFT':
                    directions.append('RIGHT')
                    directions.append('DOWN')
                    directions.append('LEFT')
                if direction == 'RIGHT':
                    directions.append('LEFT')
                    directions.append('UP')
                    directions.append('RIGHT')
                if direction == 'UP':
                    directions.append('DOWN')
                    directions.append('RIGHT')
                    directions.append('UP')
                if direction == 'DOWN':
                    directions.append('UP')
                    directions.append('LEFT')
                    directions.append('DOWN')
            else:
                if direction == 'LEFT':
                    directions.extend(hilbert(level - 1, 'UP'))
                    directions.append('RIGHT')
                    directions.extend(hilbert(level - 1, 'LEFT'))
                    directions.append('DOWN')
                    directions.extend(hilbert(level - 1, 'LEFT'))
                    directions.append('LEFT')
                    directions.extend(hilbert(level - 1, 'DOWN'))
                if direction == 'RIGHT':
                    directions.extend(hilbert(level - 1, 'DOWN'))
                    directions.append('LEFT')
                    directions.extend(hilbert(level - 1, 'RIGHT'))
                    directions.append('UP')
                    directions.extend(hilbert(level - 1, 'RIGHT'))
                    directions.append('RIGHT')
                    directions.extend(hilbert(level - 1, 'UP'))
                if direction == 'UP':
                    directions.extend(hilbert(level - 1, 'LEFT'))
                    directions.append('DOWN')
                    directions.extend(hilbert(level - 1, 'UP'))
                    directions.append('RIGHT')
                    directions.extend(hilbert(level - 1, 'UP'))
                    directions.append('UP')
                    directions.extend(hilbert(level - 1, 'RIGHT'))
                if direction == 'DOWN':
                    directions.extend(hilbert(level - 1, 'RIGHT'))
                    directions.append('UP')
                    directions.extend(hilbert(level - 1, 'DOWN'))
                    directions.append('LEFT')
                    directions.extend(hilbert(level - 1, 'DOWN'))
                    directions.append('DOWN')
                    directions.extend(hilbert(level - 1, 'LEFT'))
            return directions

        curves = [hilbertCurve(i + 1).rotate(ROTATION_CONSTANT[0], ROTATION_CONSTANT[1]).center() for i in range(4)]
        line = Line3D(start=LEFT * 3, end=RIGHT * 3, stroke_width=6)
        line.set_color_by_gradient(*COLOR_GRAD)
        cross = MathTex(r'\times', color=RED_B).scale(13)
        self.add_fixed_in_frame_mobjects(cross)
        self.remove(cross)

        if animate:
            self.play(Write(line))
            self.play(FadeOut(line, run_time=0.5), Create(curves[0], run_time=1))
            for i in range(len(curves) - 1):
                self.play(FadeOut(curves[i], run_time=0.5), Create(curves[i + 1], run_time=1.5 + (1 * i)))

            self.play(ReplacementTransform(curves[len(curves) - 1], plane), run_time=2)
            self.wait()
            self.play(Write(cross))
            self.play(FadeOut(cross))
            self.wait()

    def remove_point_examples(self, line, plane, animate=False):
        line.save_state()
        plane.save_state()
        line.shift(UP * 3).scale(0.8)

        if animate:
            self.play(FadeIn(line), plane.animate.shift(DOWN * 3).scale(0.8))

        removable_point_line = Dot3D(line.get_center(), color=RED_B, radius=0.15).set_z_index(6)
        removable_point_line.set_shade_in_3d(False)
        removable_point_plane = Dot3D(plane.get_center(), color=RED_B, radius=0.15).set_z_index(6)
        removable_point_plane.set_shade_in_3d(False)

        if animate:
            self.play(DrawBorderThenFill(removable_point_plane), DrawBorderThenFill(removable_point_line))
            self.play(Flash(removable_point_line), Flash(removable_point_plane))

            self.play(
                removable_point_line.animate.set_color(BLACK),
                removable_point_plane.animate.set_color(BLACK),
            )

            self.wait()
            self.play(Indicate(line))
            self.wait(3.5)
            self.play(Indicate(plane))
            self.wait(5)

class SineGetsCloseScene(Scene):
    def construct(self):
        start_title = VGroup(Tex(r'Continuous and invertible '), MathTex(r'f', r':[0, 1]', r' \to ', r'[0, 1]^2'))\
            .arrange(RIGHT).set_color_by_gradient(ORANGE, MAROON, BLUE)
        arrow = DoubleArrow(start=LEFT * 2, end=RIGHT * 2).set_color([ORANGE, MAROON, BLUE])
        arrow_title = MathTex(r'f(t) = (t, \sin(400t))').set_color([ORANGE, MAROON, BLUE]).next_to(arrow, DOWN)
        title = start_title[1].copy().center().to_edge(UP, buff=1)

        box = Rectangle(width=3.5, height=3.5, fill_opacity=0).shift(RIGHT * 4)
        filled_box = Rectangle(width=3.5, height=3.5, fill_opacity=1).set_color([BLUE, GREEN]).move_to(box)
        cross = MathTex(r'\times', color=RED_B).scale(25)

        axes = Axes(
            x_range=(-1, 1, 1),
            y_range=(-1, 1, 1),
            y_length=3.5,
            x_length=3.5,
            axis_config={
                "stroke_color": GREY_A,
                "stroke_width": 2,
                "include_tip": False,
                "include_numbers": True,
            },
        ).move_to(box).shift(LEFT * 0.1)

        in_line = NumberLine(x_range=np.array([0, 1]), length=3, tip_length=0.4).shift(LEFT * 4)
        self.add(title, in_line, box)
        self.play(Write(arrow), Write(arrow_title))
        s = ValueTracker(0)

        def osc_func(t):
            pt = axes.c2p(2*t - 1, np.sin(400 * t))
            return np.array((pt[0], pt[1], 0))

        spiral_curve = always_redraw(lambda:
                                     ParametricFunction(osc_func, t_range=(0, 1, 0.001),
                                                        fill_opacity=0,
                                                        color=ORANGE,
                                                        stroke_opacity=0.9,
                                                        stroke_width= 2.5 - s.get_value() * 2)
                                     )
        follow_dot = always_redraw(lambda: Dot(spiral_curve.get_end(), color=MAROON))
        tracker = ValueTracker(0)
        dot = always_redraw(lambda:
                            Dot(in_line.n2p(tracker.get_value()),
                                color=MAROON,
                                radius=0.1,
                                fill_opacity=1)
                            )
        self.play(FadeIn(dot, follow_dot))
        self.play(tracker.animate.set_value(1), Create(spiral_curve), rate_func=linear, run_time=2)
        not_oto_onto = Tex(r'Close, but not one-to-one and onto.').set_color([ORANGE, MAROON]).to_edge(DOWN, buff=0.5)
        self.play(Write(not_oto_onto))
        self.wait()
        self.play(s.animate.set_value(1))
        self.wait(2)
        self.play(FadeOut(dot, follow_dot, box, arrow_title), ReplacementTransform(spiral_curve, filled_box))
        self.wait()
        self.play(Write(cross))
        self.play(FadeOut(cross, run_time=0.5))
        self.wait()


class FurtherExplorationScene(Scene):
    def construct(self):
        very_original_question = Tex(r'Can a linear transformation from $\mathbb R^2$ to $\mathbb R^3$ be onto?')
        original_question = Tex(r'Can a continuous function from $\mathbb R^2$ to $\mathbb R^3$ be onto?')
        question = Tex(
            r'Why can there never exist a one to one and onto function \\ from $\mathbb R^2$ to $\mathbb R^3$?')
        final_question_1 = Tex(r'How did our equivalence  \\ relation work? \\ How can we generalize equivalence?')
        final_question_2 = Tex(
            r'In what ways do invertible \\ continuous functions define \\ an equivalence of shapes?')

        very_original_question.to_edge(UP, buff=1).set_color_by_gradient(BLUE, GREEN)
        original_question.set_color_by_gradient(BLUE, GREEN)
        question.to_edge(DOWN, buff=1).set_color_by_gradient(BLUE, GREEN)

        arrows = [
            Arrow(start=very_original_question.get_center(), end=original_question.get_center(),
                  stroke_width=5).set_color([YELLOW, BLUE]).scale(0.5),
            Arrow(start=original_question.get_center(), end=question.get_center(), stroke_width=5).set_color(
                [YELLOW, BLUE]).scale(0.5),
        ]

        self.play(Write(very_original_question))
        self.wait()
        self.play(FadeIn(arrows[0], run_time=0.5), Write(original_question))
        self.wait()
        self.play(FadeIn(arrows[1], run_time=0.5), Write(question))
        self.wait()
        self.play(
            FadeOut(very_original_question, original_question, *arrows, run_time=0.5),
            question.animate.to_edge(UP, buff=1)
        )

        final_question_2.to_edge(LEFT, buff=1).set_color_by_gradient(GOLD, BLUE)
        final_question_1.to_corner(DR, buff=1).set_color_by_gradient(GOLD, BLUE)

        arrows = [
            Arrow(start=question.get_center(), end=final_question_1.get_center(),
                  stroke_width=5).set_color([GOLD, BLUE]).scale(0.3),
            Arrow(start=question.get_center(), end=final_question_2.get_center() + RIGHT, stroke_width=5).set_color(
                [GOLD, BLUE]).scale(0.3),
        ]

        self.wait(0.5)
        self.play(Write(arrows[1]), run_time=0.5)
        self.play(Write(final_question_2))
        self.play(Write(arrows[0]), run_time=0.5)
        self.play(Write(final_question_1))
        self.wait()
        self.play(FadeOut(question, final_question_1, final_question_2, *arrows))

        thanks_for_watching = Text(r'Thanks for watching! <3', gradient=[FOREGROUND_COLOR, TEAL]).scale(1.5)
        self.play(Write(thanks_for_watching))
        self.play(Indicate(thanks_for_watching, color=FOREGROUND_COLOR))
        self.wait(3)
