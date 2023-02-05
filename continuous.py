import numpy as np
from manim import *
import time
from datetime import datetime

from manim.mobject.geometry.tips import ArrowTriangleFilledTip, ArrowTriangleTip
from manim.utils.rate_functions import ease_in_expo, ease_out_expo


class IntroScene(Scene):
    def construct(self):
        title = Tex(r'Can a ', 'continuous ', 'function ', r'$f$ ', r'$:$ ', r'$\mathbb R $', r'$\to $',
                    r'$\mathbb R^2$ ', r' be onto?').set_color_by_gradient(BLUE, GREEN)

        header = Tex('continuous ', 'function ', r'$f$ ', '$:$ ', r'$\mathbb R$ ', r'$\to$ ', r'$\mathbb R^2$ ')\
            .set_color_by_gradient(BLUE, GREEN)

        title.shift(UP * 1)
        self.add(title)
        und1 = Underline(title[1], color=BLUE_E)
        self.wait(3)
        self.play(Write(und1), run_time=0.5)
        self.play(FadeOut(und1), run_time=0.5)
        self.play(FadeTransformPieces(title, header), run_time=0.5)
        self.play(header.animate.to_edge(UP))

        # Underline continuous, fade text other than f:R \to R2 then change R into inline, R2 into out

        axes = Axes(
            # x-axis ranges from 0 to 1, with a  step size of 0.2
            x_range=(0, 1, 0.5),
            # y-axis ranges from -2 to 2 with a step size of 1
            y_range=(-2, 2, 1),
            # The axes will be stretched so as to match the specified
            # height and width
            y_length=5.5,
            x_length=5.5,
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config={
                "stroke_color": GREY_A,
                "stroke_width": 2,
                "include_tip": False,
                "include_numbers": True,
            },
        )
        axes.shift(RIGHT * 3 + (DOWN / 2))

        def sine_func(t):
            pt = axes.c2p(t, np.sin(4 * PI * t))
            return np.array((pt[0], pt[1], 0))

        sine_wave = ParametricFunction(sine_func, t_range=np.array([0, 1]), fill_opacity=0, color=BLUE_B)
        follow_dot = always_redraw(lambda: Dot(sine_wave.get_end(), color=BLUE_E))

        in_line = NumberLine(x_range=np.array([0, 4])).shift(LEFT * 3.5)
        tracker = ValueTracker(0)
        dot = always_redraw(lambda:
                            Dot(in_line.n2p(4 * tracker.get_value()),
                                color=BLUE_E,
                                radius=0.15,
                                fill_opacity=1)
                            )
        number = DecimalNumber(0, color=BLUE_E).next_to(dot, UP)

        number.add_updater(lambda m: m.next_to(dot, UP))
        number.add_updater(lambda m: m.set_value(((dot.get_center() - (LEFT * 3.5)) / 4)[0] + 0.5))

        seperate = ['=', '(t)', r'\sin']
        function_equation = MathTex(r'f(t) = (t, \,', r'\sin(4 \pi t))', color=BLUE_A, substrings_to_isolate=seperate)
        function_equation.next_to(in_line, DOWN, buff=1.5)

        self.play(Transform(header[4].copy(), in_line), run_time=0.5)
        self.play(Transform(header[6].copy(), axes), run_time=0.5)
        self.play(FadeIn(function_equation), run_time=0.5)
        self.play(FadeIn(dot, follow_dot, number), run_time=0.5)
        self.play(Create(sine_wave), tracker.animate.set_value(1), run_time=2.5, rate_func=linear)

        hunction_equation = VGroup(
            MathTex(r'h(t) = ', color=BLUE_A, substrings_to_isolate=seperate),
            MathTex(r'((0.5 + \sin(2 \pi t) \sin(3 \pi t)), \, \sin(2 \pi t))', color=BLUE_A,
                    substrings_to_isolate=seperate),
        ).arrange(DOWN)

        hunction_equation.next_to(in_line, DOWN, buff=1.5)

        self.play(FadeOut(sine_wave, dot, follow_dot, number),
                  TransformMatchingTex(function_equation, hunction_equation), run_time=0.5)

        def dbl_sine(t):
            pt = axes.c2p(0.5 + (0.5 * np.sin(2 * PI * t) * np.sin(3 * PI * t)), np.sin(2 * PI * t))
            return np.array((pt[0], pt[1], 0))

        dbl_sine_wave = ParametricFunction(dbl_sine, t_range=np.array([0, 1]), fill_opacity=0, color=BLUE_B)
        h_follow_dot = always_redraw(lambda: Dot(dbl_sine_wave.get_end(), color=BLUE_E))
        tracker.set_value(0)
        h_dot = always_redraw(lambda:
                              Dot(in_line.n2p(4 * tracker.get_value()),
                                  color=BLUE_E,
                                  radius=0.15,
                                  fill_opacity=1)
                              )
        h_number = DecimalNumber(0, color=BLUE_E).next_to(h_dot, UP)

        h_number.add_updater(lambda m: m.next_to(h_dot, UP))
        h_number.add_updater(lambda m: m.set_value(((h_dot.get_center() - (LEFT * 3.5)) / 4)[0] + 0.5))

        self.add(h_dot, h_follow_dot, h_number)
        self.play(Create(dbl_sine_wave), tracker.animate.set_value(1), run_time=3, rate_func=linear)

        gunction_equation = MathTex(r'g(t) = (t, \, \sin (\frac{50}{t} ))',
                                    color=BLUE_A,
                                    substrings_to_isolate=seperate)
        gunction_equation.next_to(in_line, DOWN, buff=1.5)

        self.play(FadeOut(dbl_sine_wave, h_dot, h_follow_dot, h_number),
                  TransformMatchingTex(hunction_equation, gunction_equation), run_time=0.5)

        def inv_sine_func(t):
            pt = axes.c2p(t, np.sin(50 / (t + 0.01)))
            return np.array((pt[0], pt[1], 0))

        inv_sine_wave = ParametricFunction(inv_sine_func, t_range=np.array([0, 1]), fill_opacity=0, color=BLUE_B)
        g_follow_dot = always_redraw(lambda: Dot(inv_sine_wave.get_end(), color=BLUE_E))
        g_dot = always_redraw(lambda:
                              Dot(in_line.n2p(4 * (axes.p2c(inv_sine_wave.get_end()))[0]),
                                  color=BLUE_E,
                                  radius=0.15,
                                  fill_opacity=1)
                              )
        g_number = DecimalNumber(0, color=BLUE_E).next_to(g_dot, UP)

        g_number.add_updater(lambda m: m.next_to(g_dot, UP))
        g_number.add_updater(lambda m: m.set_value(((g_dot.get_center() - (LEFT * 3.5)) / 4)[0] + 0.5))

        self.add(g_dot, g_follow_dot, g_number)
        self.play(Create(inv_sine_wave, run_time=3, rate_func=linear))

        self.wait()

BACKGROUND_COLOR = BLUE
FOREGROUND_COLOR = BLUE_C

class ContinuousSurjectionScene(Scene):
    def construct(self):
        self.add_coord_plane(animate=True)
        self.add_label(r'Onto', animate=True)

        def oscillating_function(t):
            return np.array((t - 9, 5 * np.sin(50 * t), 0))

        dot, path, t_param = self.add_moving_dot(oscillating_function, t_range=[0, 18], animate=True)
        self.draw_flash_then_fade(dot, path, FOREGROUND_COLOR, t_param, 18)

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
        self.play(Create(path), t_param.animate.set_value(intersection_t), rate_func=linear, run_time=5)
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

class LineWidthScene(Scene):
    def construct(self):
        def scribble_func(t):
            return np.array((t, np.sin(t) + np.cos(9 * t), 0))

        t_param = ValueTracker(0)

        scribble = always_redraw(lambda: ParametricFunction(scribble_func,
                                                            t_range=[0, 2],
                                                            stroke_color=BLUE_C,
                                                            stroke_width=(-19 / 5) * t_param.get_value() + 5)
                                 .scale(2 + (20 * t_param.get_value())).center())

        axes = always_redraw(lambda: Axes(
            x_range=(-10, 10, 1),
            y_range=(-10, 10, 1),
            x_length=15,
            y_length=15
        ).scale(2 + (20 * t_param.get_value())))

        dot = always_redraw(lambda: Dot(
                                        color=BLUE_C,
                                        stroke_width= (-19 / 5) * t_param.get_value() + 5))

        self.play(Create(scribble), FadeIn(dot), DrawBorderThenFill(axes))
        self.play(t_param.animate.set_value(1), run_time=7)


class LineTransitionScene(Scene):
    def construct(self):
        label = MathTex(r'f: ', r'\mathbb R', r' \to ', r'\mathbb R', r'^2').to_edge(UP, buff=2).scale(1.3)
        #onto_label = Text(r'Onto', gradient=[BLUE_A, BLUE_B]).next_to(label, LEFT, buff=2)
        finite_label = MathTex(r'f: ', r'[0, 1]', r' \to ', r'[0, 1]', r'^2').move_to(label)
        label_explinations = [
            Text(r'Number line', gradient=[RED, ORANGE]).next_to(label[1], UP, aligned_edge=RIGHT, buff=1).shift(LEFT),
            Text(r'Coordinate plane', gradient=[RED, ORANGE]).next_to(label[3], UP, aligned_edge=LEFT, buff=1).shift(RIGHT),
            Text(r'Line Segment', gradient=[BLUE, GREEN]).next_to(finite_label[1], UP, aligned_edge=RIGHT, buff=1).shift(LEFT),
            Text(r'Square', gradient=[BLUE, GREEN]).next_to(finite_label[3], UP, aligned_edge=LEFT, buff=1).shift(RIGHT),
        ]

        small_lines = [
            Line(start=label[1].get_center(), end=label_explinations[0].get_center(), stroke_width=2)
                .scale(0.5).set_color(color=[RED, ORANGE]),
            Line(start=label[3].get_center(), end=label_explinations[1].get_center(), stroke_width=2)
                .scale(0.5).set_color(color=[RED, ORANGE]),
            Line(start=finite_label[1].get_center(), end=label_explinations[2].get_center(), stroke_width=2)
                .scale(0.5).set_color(color=[BLUE, GREEN]),
            Line(start=finite_label[3].get_center(), end=label_explinations[3].get_center(), stroke_width=2)
                .scale(0.5).set_color(color=[BLUE, GREEN]),
        ]

        line = NumberLine(
            x_range=[-2, 2],
            length=14,
            stroke_color=FOREGROUND_COLOR,
            stroke_width=6,
            tip_width=0.5,
            tip_height=0.5,
            include_tip=False,
        ).set_color_by_gradient(PURPLE_B, MAROON_B, BLUE_C, TEAL_C, YELLOW_C, GREEN_C, LIGHT_BROWN)
        line.next_to(label, DOWN, buff=2)

        line_labels = [
            MathTex(r'\mathbb R').set_color_by_gradient(RED, ORANGE).scale(1.3).next_to(line, DOWN),
            MathTex(r'[0, 1]').set_color_by_gradient(BLUE, GREEN).scale(1.3).next_to(line, DOWN),
        ]

        self.play(Create(line), Write(label), Write(line_labels[0]))
        #self.play(Write(onto_label))
        self.wait()
        self.play(Write(label_explinations[0]), Create(small_lines[0]))
        self.play(Write(label_explinations[1]), Create(small_lines[1]))
        self.wait()
        self.play(
            FadeOut(label_explinations[0], label_explinations[1], small_lines[0], small_lines[1], run_time=0.5),
            ReplacementTransform(line_labels[0], line_labels[1]),
            TransformMatchingTex(label, finite_label),
            ScaleInPlace(line, 0.5),
        )
        self.wait(0.5)
        self.play(Write(label_explinations[2]), Create(small_lines[2]))
        self.play(Write(label_explinations[3]), Create(small_lines[3]))
        self.wait()
        self.play(FadeOut(label_explinations[2], label_explinations[3], line_labels[1], line, finite_label,
                          small_lines[2], small_lines[3]))


class ScribblePlane(Scene):
    def construct(self):

        self.add_coord_plane(animate=True)

        def scribble_func(t):
            if t <= 0.33:
                return np.array((0, -t * 2, 0))
            if t <= 0.66:
                return np.array(((t - 0.33) * 2, -0.33 * 2, 0))
            return np.array((0.33 * 2, 2 * (t - 0.66) - (0.33 * 2), 0))

        rect = Rectangle(width=5, height=5, fill_opacity=0, stroke_width=5, color=WHITE).center()

        tracker = ValueTracker(0)

        scribble = always_redraw(lambda:
                                 ParametricFunction(scribble_func,
                                                    t_range=[0, 1],
                                                    stroke_color=BLUE_C,
                                                    stroke_width=5 - (4 * tracker.get_value())).scale(5).center()
                                 )

        self.play(Create(rect), run_time=0.5)
        self.play(Create(scribble), run_time=3)
        self.play(tracker.animate.set_value(1))
        self.wait()

    def add_coord_plane(self, animate=False):
        number_plane = NumberPlane(
            x_range=(-10, 10, 2),
            y_range=(-10, 10, 2),
            x_length=15,
            y_length=15,
            tips=True,
            background_line_style={
                "stroke_color": BACKGROUND_COLOR,
                "stroke_width": 0.5,
                "stroke_opacity": 0.6
            }
        )

        if animate:
            self.play(Write(number_plane), run_time=1)
        else:
            self.add(number_plane)

        return number_plane


class SpaceFillingCurveScene(ZoomedScene):
    def construct(self):
        self.image_frame_stroke_width = 2
        self.zoomed_display_height = 5
        self.zoomed_display_width = 5
        order = 8
        hilbertCurves = []
        hilbert_label = []
        for i in range(order + 1):
            timestamp = datetime.fromtimestamp(time.time())
            print('Generating curve ', (i + 1), ' TIMESTAMP: ', timestamp)
            curve = self.hilbertCurve(order=i + 1)
            curve.center().shift(UP * 0.5)
            hilbertCurves.append(curve)
            hilbert_label.append(MathTex(r'H_', str(i + 1), r': [0, 1] \to [0, 1]^2')
                                 .to_edge(DOWN).shift(RIGHT).scale(0.7))

        number_line = NumberLine(x_range=[0, 1], include_numbers=True)
        number_line.next_to(hilbert_label[0], LEFT, buff=1)
        tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(number_line.n2p(tracker.get_value()), color=BLUE_E))

        transformations = []
        for i in range(order):
            timestamp = datetime.fromtimestamp(time.time())
            print('Generating transform animation ', (i + 1), ' TIMESTAMP: ', timestamp)
            transformations.append(TransformMatchingShapes(hilbertCurves[i], hilbertCurves[i + 1],
                                                           transform_mismatches=True))

        self.clear()
        self.play(Create(hilbertCurves[0]), Write(hilbert_label[0], run_time=0.4), FadeIn(number_line, run_time=0.4))
        for i in range(4):
            self.play(FadeOut(hilbertCurves[i]), run_time=0.5)
            tracker.set_value(0)
            self.add(dot)
            dot_animation = AnimationGroup(tracker.animate.set_value(1), rate_func=linear, run_time=0.5 * (i + 1))
            self.play(TransformMatchingTex(hilbert_label[i], hilbert_label[i + 1], run_time=0.5),
                      Create(hilbertCurves[i + 1], run_time=0.5 * (i + 1)),
                      dot_animation
                      )
            self.play(FadeOut(dot), run_time=0.5)

        self.activate_zooming(animate=True)
        for i in range(4, order):
            self.play(transformations[i])
            self.wait(1)

        self.wait(1)

        tracker = ValueTracker(8)
        self.clear()
        relabel = AnimationGroup(hilbert_label[order].animate.scale(1.75).center().shift(UP * 2),
                                 hilbertCurves[order].animate.scale(0.6).center().shift(DOWN + (RIGHT * 2)),
                                 number_line.animate.scale(1.75).center().shift((LEFT * 3) + DOWN)
                                 )
        self.add(hilbertCurves[order], hilbert_label[order], number_line)
        self.play(relabel)

        changing_label = hilbert_label[order].copy()
        changing_label.add_updater(lambda l: l.become(MathTex(r'H_{', str(int(tracker.get_value())),
                                                              r'}: [0, 1] \to [0, 1]^2')
                                                      .scale(1.2).move_to(l)))

        self.remove(hilbert_label[order])
        self.add(changing_label)

        self.play(tracker.animate.set_value(100), run_time=1)

        final_label = MathTex(r'H_{', r'\infty', r'}: [0, 1] \to [0, 1]^2').scale(1.2).move_to(hilbert_label[order])
        numberLabels = Group(MathTex('0').align_to(hilbertCurves[order], DOWN).shift(DOWN * 0.5),
                             MathTex('1').align_to(hilbertCurves[order], UP),
                             MathTex('1').align_to(hilbertCurves[order], RIGHT).shift(DOWN * 3))

        self.play(TransformMatchingTex(changing_label, final_label), FadeIn(numberLabels), run_time=0.5)
        # ValueTracker 0 to 1. represented by dot on dumber line. then measure 1/number of lines in hilbercurve. use them as spacings. all lines inat time t shine white\\
        arrow = Arrow(start=[-1, 0, 0], end=[1, 0, 0], tip_shape=ArrowTriangleFilledTip, stroke_width=3, color=BLUE_E)
        arrow.shift(DOWN + (LEFT * 0.5))

        detailed_box = VGroup(hilbertCurves[order], *numberLabels)

        self.play(number_line.animate.shift(LEFT),
                  detailed_box.animate.shift(RIGHT),
                  FadeIn(arrow))

        self.play(FadeOut(detailed_box))

        rect = Rectangle(height=5.5, width=5.5, fill_opacity=0.9) \
            .scale(0.6).move_to(hilbertCurves[order].get_center())
        rect.set_fill(color=[BLUE, YELLOW])

        self.play(TransformFromCopy(number_line, rect), FadeIn(numberLabels))
        self.wait()
        self.play(FadeOut(number_line, arrow, final_label, shift=LEFT), rect.animate.center(), FadeOut(numberLabels),
                  run_time=0.6)
        leftCornerDot = Dot(rect.get_corner(UL), color=GREEN_E)
        rightCornerDot = Dot(rect.get_corner(UR), color=RED_E)
        self.play(FadeIn(leftCornerDot, run_time=0.5))
        self.play(FadeIn(rightCornerDot, run_time=0.5))
        self.wait(0.5)
        # Show connection scene

    def hilbertCurve(self, order=1, x_initial=0, y_initial=0,
                     colors=[PURPLE_B, MAROON_B, BLUE_C, TEAL_C, YELLOW_C, GREEN_C, LIGHT_BROWN]):
        segment_length = 5 / (2 ** order)
        stroke_width = (-3 / 7) * order + (31 / 7)
        segments = VGroup()

        directions = self.hilbert(level=order)
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
            segments.add(Line(start=prevCenter, end=endPt, stroke_width=stroke_width))
            prevCenter = endPt

        segments.set_color_by_gradient(*colors)

        return segments

    def hilbert(self, level=1, direction='UP'):
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
                directions.extend(self.hilbert(level - 1, 'UP'))
                directions.append('RIGHT')
                directions.extend(self.hilbert(level - 1, 'LEFT'))
                directions.append('DOWN')
                directions.extend(self.hilbert(level - 1, 'LEFT'))
                directions.append('LEFT')
                directions.extend(self.hilbert(level - 1, 'DOWN'))
            if direction == 'RIGHT':
                directions.extend(self.hilbert(level - 1, 'DOWN'))
                directions.append('LEFT')
                directions.extend(self.hilbert(level - 1, 'RIGHT'))
                directions.append('UP')
                directions.extend(self.hilbert(level - 1, 'RIGHT'))
                directions.append('RIGHT')
                directions.extend(self.hilbert(level - 1, 'UP'))
            if direction == 'UP':
                directions.extend(self.hilbert(level - 1, 'LEFT'))
                directions.append('DOWN')
                directions.extend(self.hilbert(level - 1, 'UP'))
                directions.append('RIGHT')
                directions.extend(self.hilbert(level - 1, 'UP'))
                directions.append('UP')
                directions.extend(self.hilbert(level - 1, 'RIGHT'))
            if direction == 'DOWN':
                directions.extend(self.hilbert(level - 1, 'RIGHT'))
                directions.append('UP')
                directions.extend(self.hilbert(level - 1, 'DOWN'))
                directions.append('LEFT')
                directions.extend(self.hilbert(level - 1, 'DOWN'))
                directions.append('DOWN')
                directions.extend(self.hilbert(level - 1, 'LEFT'))
        return directions


class ExtensionToR2Scene(SpaceFillingCurveScene):
    def construct(self):
        axes = Axes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            x_length=10,
            y_length=10,
            tips=True
        ).set_z_index(0)

        rectangles = [
            Rectangle(height=5.5, width=5.5, fill_opacity=0.9, fill_color=[BLUE, YELLOW]).scale(
                0.6).center().set_z_index(4),
            Rectangle(height=2, width=2, fill_opacity=0.9, fill_color=[BLUE, YELLOW]).center().set_z_index(3),
            Rectangle(height=4, width=4, fill_opacity=0.9, fill_color=[RED, ORANGE]).center().set_z_index(2),
            Rectangle(height=6, width=6, fill_opacity=0.9, fill_color=[PURPLE, BLUE]).center().set_z_index(1),
            Rectangle(height=8, width=8),
        ]

        curves = [
            self.hilbertCurve(order = 4, colors=[BLUE, YELLOW]).scale((2 / 5)).center().set_z_index(3),
            self.hilbertCurve(order = 5, colors=[RED, ORANGE]).scale((4 / 5)).center().set_z_index(2),
            self.hilbertCurve(order = 6, colors=[PURPLE, BLUE]).scale((6 / 5)).center().set_z_index(1),
        ]

        left_corner_dots = [Dot(rectangles[i].get_corner(UL), color=GREEN_E, z_index=5) for i in range(4)]
        right_corner_dots = [Dot(rectangles[i].get_corner(UR), color=RED_E, z_index=5) for i in range(4)]

        self.add(rectangles[0], left_corner_dots[0], right_corner_dots[0])

        function_labels = [
            MathTex(r'H:[0, 1] \to', r' [', r'-1', r',', r' 1', r']^2').next_to(rectangles[0], DOWN),
            MathTex(r'H:[0, 1] \to', r' [', r'-1', r',', r' 1', r']^2').next_to(axes, DOWN, buff=-1.75).shift(LEFT * 4),
            MathTex(r'H:[0, 1] \to', r' [', r'-2', r',', r' 2', r']^2').next_to(axes, DOWN, buff=-1.75).shift(LEFT * 4),
            MathTex(r'H:[0, 1] \to', r' [', r'-3', r',', r' 3', r']^2').next_to(axes, DOWN, buff=-1.75).shift(LEFT * 4),
            MathTex(r'H:[0, 2] \to', r' [', r'-2', r',', r' 2', r']^2').next_to(axes, DOWN, buff=-1.75).shift(LEFT * 4),
            MathTex(r'H:[0, 3] \to', r' [', r'-3', r',', r' 3', r']^2').next_to(axes, DOWN, buff=-1.75).shift(LEFT * 4),
            MathTex(r'H:[0, \infty] \to', r' (', r'-\infty', r',', r' \infty', r')^2').scale(1.5)
        ]
        self.play(Write(function_labels[0]), FadeOut(left_corner_dots[0], right_corner_dots[0]), run_time=0.5)

        self.play(TransformMatchingTex(function_labels[0], function_labels[1]),
                  FadeTransform(rectangles[0], rectangles[1]), run_time=0.5)

        self.play(Write(axes), run_time=0.5)

        lines = [
            Line(start=right_corner_dots[1].get_center(), end=left_corner_dots[2].get_center(), z_index=6).set_color([BLUE, YELLOW]),
            Line(start=right_corner_dots[2].get_center(), end=left_corner_dots[3].get_center(), z_index=6).set_color([RED, ORANGE]),
            Line(start=right_corner_dots[3].get_center(), end=rectangles[4].get_corner(UL), z_index=6).set_color([PURPLE, BLUE]),
        ]
        """
        self.play(Create(lines[0]), run_time=0.5)
        self.play(Create(lines[1]), run_time=0.5)


        self.play(FadeOut(left_corner_dots[2], left_corner_dots[3],
                          right_corner_dots[1], right_corner_dots[2], right_corner_dots[3],
                          lines[0], lines[1], rectangles[3], rectangles[2]))
        self.play(TransformMatchingTex(function_labels[3], function_labels[1]))
        """
        self.play(FadeOut(rectangles[1]))
        self.play(FadeIn(left_corner_dots[1]), run_time=0.5)
        self.play(Create(curves[0]), run_time=1.5)
        self.play(Create(lines[0]))
        self.play(VGroup(left_corner_dots[1], lines[0], curves[0]).animate.set_opacity(0.2), run_time=0.2)
        self.play(TransformMatchingTex(function_labels[1], function_labels[4], run_time=0.5), Create(curves[1],
                                                                                                     run_time=2.5))
        self.play(Create(lines[1]))
        self.play(VGroup(lines[1], curves[1]).animate.set_opacity(0.2), run_time=0.2)
        self.play(TransformMatchingTex(function_labels[4], function_labels[5]), Create(curves[2], run_time=3.5))
        self.play(Create(lines[2]))
        self.play(lines[1].animate.set_opacity(1), run_time=0.5)
        self.play(curves[1].animate.set_opacity(1), run_time=0.5)
        self.play(lines[0].animate.set_opacity(1), run_time=0.5)
        self.play(VGroup(curves[0], left_corner_dots[1]).animate.set_opacity(1), run_time=0.5)

        self.play(*[ReplacementTransform(curves[i], rectangles[i + 1]) for i in range(len(curves))])
        self.wait(2)
        self.play(FadeOut(function_labels[5], left_corner_dots[1]),
                  FadeOut(rectangles[1], rectangles[2], rectangles[3], lines[0], lines[1], lines[2], axes))

        template = TexTemplate().add_to_preamble(r"\usepackage{amssymb}")
        label = [
            Tex(r'$H: \mathbb R \to \mathbb R$', r'$^2$'),
            Tex(r'Onto', '?').shift(DOWN),
            Tex(r'Onto', '!').shift(DOWN),
            Tex(r'$H: \mathbb R \to \mathbb R$', r'$^3$')
        ]
        check = Tex(r'\checkmark', tex_template=template, color=GREEN_C).next_to(label[2], RIGHT)

        self.play(FadeIn(label[0], shift=UP), run_time=0.5)
        self.play(FadeIn(label[1], shift=UP), run_time=0.5)
        self.wait()
        self.play(TransformMatchingTex(label[1], label[2]), Write(check))
        self.wait()
        self.play(TransformMatchingTex(label[0], label[3]))
        self.wait()


class SpaceFillingCurve3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.25)

        order = 5
        hilbertCurves = []
        for i in range(order):
            timestamp = datetime.fromtimestamp(time.time())
            print('Generating curve ', (i + 1), ' TIMESTAMP: ', timestamp)
            curve = self.hilbert3DCurve(order=i + 1)
            curve.center()
            hilbertCurves.append(curve)

        self.play(Create(hilbertCurves[0]))
        for i in range(order - 1):
            self.play(FadeOut(hilbertCurves[i]))
            self.play(Create(hilbertCurves[i + 1], run_time=2.5 + (1.5 * i)))

        self.wait(2)

    def hilbert3DCurve(self, order=1, x_initial=0, y_initial=0):
        segment_length = 5 / (2 ** order)
        stroke_width = (-3 / 7) * order + (31 / 7)
        segments = VGroup()

        directions = self.hilbert3D(order=order)
        prevCenter = np.array((x_initial, y_initial, 0.))

        for direct in directions:
            dirTranslate = UP
            if direct == 'LEFT':
                dirTranslate = LEFT
            if direct == 'RIGHT':
                dirTranslate = RIGHT
            if direct == 'DOWN':
                dirTranslate = DOWN
            if direct == 'IN':
                dirTranslate = IN
            if direct == 'OUT':
                dirTranslate = OUT

            endPt = np.copy(prevCenter + (segment_length * dirTranslate))
            segments.add(Line3D(start=prevCenter, end=endPt, stroke_width=stroke_width, resolution=2))
            prevCenter = endPt

        segments.set_color_by_gradient(PURPLE_B, MAROON_B, BLUE_C, TEAL_C, YELLOW_C, GREEN_C, LIGHT_BROWN)

        return segments

    def hilbert3D(self, order=1, cup_case=0):
        # Each cup is 7 directions, which contains 8 cubes.
        # To subdivide, we preserve all directions in starting cup,
        # BUT, we add 8 cups at each corner, which cup we add depends
        # on what we start with
        cups = [
            ['OUT', 'UP', 'IN', 'RIGHT', 'OUT', 'DOWN', 'IN'],  # 0
            ['OUT', 'DOWN', 'IN', 'LEFT', 'OUT', 'UP', 'IN'],  # 1
            ['IN', 'UP', 'OUT', 'LEFT', 'IN', 'DOWN', 'OUT'],  # 2
            ['IN', 'DOWN', 'OUT', 'RIGHT', 'IN', 'UP', 'OUT'],  # 3
            ['OUT', 'RIGHT', 'IN', 'UP', 'OUT', 'LEFT', 'IN'],  # 4
            ['OUT', 'LEFT', 'IN', 'DOWN', 'OUT', 'RIGHT', 'IN'],  # 5
            ['IN', 'LEFT', 'OUT', 'UP', 'IN', 'RIGHT', 'OUT'],  # 6
            ['IN', 'RIGHT', 'OUT', 'DOWN', 'IN', 'LEFT', 'OUT'],  # 7
            ['RIGHT', 'UP', 'LEFT', 'OUT', 'RIGHT', 'DOWN', 'LEFT'],  # 8
            ['LEFT', 'DOWN', 'RIGHT', 'OUT', 'LEFT', 'UP', 'RIGHT'],  # 9
            ['UP', 'LEFT', 'DOWN', 'IN', 'UP', 'RIGHT', 'DOWN'],  # 10
            ['RIGHT', 'DOWN', 'LEFT', 'IN', 'RIGHT', 'UP', 'LEFT']  # 11
        ]
        if order == 1:
            return cups[cup_case]
        else:
            if cup_case == 0:
                sequence_of_cup_cases = [8, 4, 4, 3, 3, 5, 5, 10]
            elif cup_case == 1:
                sequence_of_cup_cases = [9, 5, 5, 2, 2, 4, 4, 11]
            elif cup_case == 2:
                sequence_of_cup_cases = [10, 6, 6, 1, 1, 7, 7, 8]
            elif cup_case == 3:
                sequence_of_cup_cases = [11, 7, 7, 0, 0, 6, 6, 9]
            elif cup_case == 4:
                sequence_of_cup_cases = [8, 0, 0, 6, 6, 1, 1, 11]
            elif cup_case == 5:
                sequence_of_cup_cases = [9, 1, 1, 7, 7, 0, 0, 10]
            elif cup_case == 6:
                sequence_of_cup_cases = [10, 2, 2, 4, 4, 3, 3, 9]
            elif cup_case == 7:
                sequence_of_cup_cases = [11, 3, 3, 5, 5, 2, 2, 8]
            elif cup_case == 8:
                sequence_of_cup_cases = [0, 4, 4, 9, 9, 7, 7, 2]
            elif cup_case == 9:
                sequence_of_cup_cases = [1, 5, 5, 8, 8, 6, 6, 3]
            elif cup_case == 10:
                sequence_of_cup_cases = [6, 2, 2, 11, 11, 0, 0, 5]
            elif cup_case == 11:
                sequence_of_cup_cases = [3, 7, 7, 10, 10, 4, 4, 1]

            build = []
            cup = cups[cup_case]
            for i in range(8):
                subCube = self.hilbert3D(order=order - 1, cup_case=sequence_of_cup_cases[i])
                build.extend(subCube)
                if i != 7:
                    build.append(cup[i])

            return build

class FinalQuestionScene(Scene):
    def construct(self):
        question = Tex(r'Can a ', 'continuous ', 'function ', r'$f$ ', r'$:$ ', r'$\mathbb R^2$', r'$ \to $',
                    r'$\mathbb R^3$', r' be onto?').set_color_by_gradient(BLUE, GREEN)
        question.shift(UP * 2)
        self.play(Write(question))
        self.wait()

        yes = Tex('Yes?', color=GREEN_C).next_to(question, DOWN, buff=1)
        self.play(FadeIn(yes, shift=UP))

        right_arr = Tex(r'$\mathbb R$', r'$ \to \, \,$',r'$\mathbb R^3$', color=GREEN_C)
        left_arr = Tex(r'$\mathbb R^2$', r'$ \to $', color=BLUE_C)
        arrs = VGroup(left_arr, right_arr).arrange(RIGHT)
        arrs.center().next_to(yes, DOWN, buff=1).scale(1.5)
        self.play(FadeIn(right_arr))
        self.play(FadeIn(left_arr))
        self.wait(2)

class EmbededLineScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=7,
            y_length=7,
            z_length=7,
            axis_config={"include_numbers": True},
            tips=True
        ).add_coordinates()
        axes.center()

        labels = [
            MathTex(r'H', r'^3', r': \mathbb R', r' \to \mathbb R', r'^3')
                .to_corner(UL, buff=1).set_color_by_gradient(LIGHT_PINK, TEAL),
            MathTex(r'f', r': \mathbb R', r'^2', r' \to \mathbb R', r'^3')
                .to_corner(UL, buff=1).set_color_by_gradient(RED, TEAL),
            MathTex(r'g', r': \mathbb R^2', r' \to \mathbb R')
                .to_corner(UL, buff=1).set_color_by_gradient(RED, PURPLE),
            MathTex(r'f', r' = ', r'H^3', r' \circ ', r'g')
                .to_corner(UL, buff=1).set_color_by_gradient(RED, TEAL),
            MathTex(r'f', r': \mathbb R', r'^2', r' \to \mathbb R', r'^3')
                .to_corner(UL, buff=1).set_color_by_gradient(RED, TEAL),
        ]

        label_explinations = [
            MathTex(r'\mathbb R', r' \to \mathbb R', r'^3')
                .next_to(labels[3][2], DOWN, aligned_edge=RIGHT, buff=1).set_color_by_gradient(LIGHT_PINK, RED),
            MathTex(r'\mathbb R^2', r' \to \mathbb R')
                .next_to(labels[3][4], DOWN, aligned_edge=LEFT, buff=1).set_color_by_gradient(RED, TEAL),
        ]

        lines_to_explinations = [
            Line(start=labels[3][2].get_center(), end=label_explinations[0].get_center(), stroke_width=3)
                .set_color([LIGHT_PINK, RED]).scale(0.5),
            Line(start=labels[3][4].get_center(), end=label_explinations[1].get_center(), stroke_width=3)
                .set_color([RED, TEAL]).scale(0.5),
        ]

        self.add_fixed_in_frame_mobjects(*labels, *label_explinations, *lines_to_explinations)
        self.remove(*labels, *label_explinations, *lines_to_explinations)

        line = Line3D(start=axes.c2p([[-5.], [0.], [0.]]), end=axes.c2p([[5.], [0.], [0.]]),
                       stroke_width=5, fill_opacity=0.5).set_color([PURPLE, BLUE])
        line1 = line.copy()
        line2 = line1.copy()
        rect = Rectangle(width=7, height=7).set_fill(color=[LIGHT_PINK, RED], opacity=0.5)
        cube = Cube(side_length=7, color=BLUE, fill_opacity=0.6)
        cube.center()
        rect.center()
        rect1 = rect.copy()
        rect2 = rect1.copy()
        rect3 = rect2.copy()

        self.set_camera_orientation(phi=70*DEGREES, theta=45*DEGREES)
        self.begin_ambient_camera_rotation(0.15)

        self.play(Create(axes), Write(labels[0]))
        self.play(FadeIn(line))
        self.wait()
        self.play(ReplacementTransform(line, cube))
        self.wait()
        self.play(FadeOut(cube), run_time=0.5)
        self.play(DrawBorderThenFill(rect), FadeOut(labels[0], run_time=0.5), FadeIn(labels[1]))
        self.wait()
        self.play(ReplacementTransform(rect, cube))
        self.wait()
        self.play(FadeOut(cube), run_time=0.5)
        self.play(FadeIn(rect1, labels[2]), FadeOut(labels[1], run_time=0.5))
        self.wait()
        self.play(ReplacementTransform(rect1, line1))
        self.wait()
        self.play(FadeOut(line1))
        self.play(FadeOut(labels[2], run_time=0.5), FadeIn(labels[3]))
        self.play(Create(rect2))
        self.play(Write(label_explinations[0]), Write(label_explinations[1]),
                  Create(lines_to_explinations[0]), Create(lines_to_explinations[1]))
        self.play(ReplacementTransform(rect2, line1))
        self.play(ReplacementTransform(line1, cube))
        self.wait(2)
        self.play(FadeOut(cube, *label_explinations, *lines_to_explinations))
        self.play(DrawBorderThenFill(rect3), FadeOut(labels[3], run_time=0.5), FadeIn(labels[4]))
        self.wait()
        self.play(ReplacementTransform(rect3, line2))
        self.play(ReplacementTransform(line2, cube))
        self.wait(2)

class FurtherQuestionsScene(Scene):
    def construct(self):
        self.next_section()
        starter = Tex(r'There ', r'exists', r' a continuous',
                      r',', r' onto', r' function $\mathbb R^2 \to \mathbb R^3$', r'.', color=BLUE_B).shift(UP * 2)
        second = Tex(r'There ', r'does ', r'not ', r'exist', r' a continuous', r',', r'\\', r' onto',
                     r' and one-to-one', r' function $\mathbb R^2 \to \mathbb R^3$', r'.', color=BLUE_B).shift(UP * 2)
        third = Tex(r'Why ', 'does ', 'there ', r'not ', r'exist', r' a continuous', r',', r'\\', r' onto',
                     r' and one-to-one', r' function $\mathbb R^2 \to \mathbb R^3$', r'?', color=BLUE_B)

        oto_lbl = Tex(r'one to one ', r' \, $\Leftrightarrow$ \,', r' non-crossing')\
            .set_color_by_gradient(BLUE, BLUE_B).scale(1.5).to_edge(DOWN, buff=1.5)

        self.play(Write(starter), run_time=2)
        self.wait(3)
        self.play(TransformMatchingTex(starter, second), run_time=2)
        self.play(Write(oto_lbl), run_time=2)
        #Show clip of hilbert curve and then connecting
        self.wait(5)
        #Before this must last 14 seconds
        self.next_section()
        self.play(FadeOut(oto_lbl))
        self.play(TransformMatchingTex(second, third))
        self.wait(1)
        thanks = Tex('Thanks for watching!', color=BLUE_C).next_to(third, DOWN, buff=1)
        self.play(Write(thanks))
        self.wait(4)
