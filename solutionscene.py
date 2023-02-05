from manim import *

class IntroScene(Scene):
    def construct(self):
        title = Tex("Can a ", "linear transformation ", "$T: $", "$\\mathbb{R}^2$",
                "$\\to$", "$\\mathbb{R}^3$", " be ", "onto?", color=WHITE)
        self.add(title)
        self.wait(1)

        und1 = Underline(title[1], color=YELLOW)
        self.play(Write(und1))
        self.play(FadeOut(und1), run_time=0.5)

        self.wait(1)

        und2 = Underline(title[7], color=YELLOW)
        self.play(Write(und2))
        self.play(FadeOut(und2), run_time=0.5)

        self.play(title.animate.to_edge(UP), run_time=1)

        nope = Text("No.", color=RED, font_size=56)

        self.play(FadeIn(nope, shift=UP))
        self.wait(0.5)
        self.play(FadeOut(nope, shift=UP), run_time=0.5)

        appliedVecEq = MathTex(r'T\left ( \begin{bmatrix} x \\ y \end{bmatrix} \right )',
                               r' = ', r'x \cdot ',
                               r'T\left ( \begin{bmatrix} 1 \\ 0 \end{bmatrix} \right )',
                               r' + ', r'y \cdot ',
                               r'T\left ( \begin{bmatrix} 0 \\ 1 \end{bmatrix} \right )')

        self.play(FadeOut(title, shift=UP), FadeIn(appliedVecEq))

        rect2 = SurroundingRectangle(appliedVecEq[3], color=YELLOW)
        rect3 = SurroundingRectangle(appliedVecEq[6], color=YELLOW)

        self.play(LaggedStart(Write(rect2), Write(rect3), lag_ratio=0.35))
        self.play(FadeOut(rect2, rect3), run_time=0.5)

        assign1 = MathTex(r'T\left ( \begin{bmatrix} 1 \\ 0 \end{bmatrix} \right )', r' = ',
                          r'\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}')
        assign2 = MathTex(r'T\left ( \begin{bmatrix} 0 \\ 1 \end{bmatrix} \right )', r' = ',
                          r'\begin{bmatrix} 2 \\ 0 \\ -1 \end{bmatrix}')
        assigns = Group(assign1, assign2).arrange(DOWN)

        self.play(TransformMatchingTex(appliedVecEq, assigns))
        self.play(assign1[2].animate.set_color(PINK), assign2[2].animate.set_color(GREEN))
        self.wait(1)

        colmVecs = Group(MathTex(r'\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}', color=PINK),
                         MathTex(r'\begin{bmatrix} 2 \\ 0 \\ -1 \end{bmatrix}', color=GREEN)
                         ).arrange(RIGHT).to_corner(UL)

        self.play(TransformMatchingTex(assigns, colmVecs))

class SeeSpanIllistration(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70*DEGREES, theta = 0 * DEGREES)
        self.begin_ambient_camera_rotation(0.15)

        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"include_numbers": True},
            tips=False
        )

        colmVecs = Group(MathTex(r'\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}', color=PINK),
                         MathTex(r'\begin{bmatrix} 2 \\ 0 \\ -1 \end{bmatrix}', color=GREEN)
                         ).arrange(RIGHT).to_corner(UL)

        self.add_fixed_in_frame_mobjects(colmVecs)
        self.play(DrawBorderThenFill(axes))
        self.wait(1)

        dots = VGroup(
            Dot3D(axes.c2p([[1], [2], [3]]), color=PINK),
            Dot3D(axes.c2p([[2], [0], [-1]]), color=GREEN)
        )

        self.play(FadeIn(dots))
        self.wait(1)

        newV2 = Arrow3D(start=dots[0].get_center(), end=(dots[1].get_center() + dots[0].get_center()), color=GREEN)

        v1 = Arrow3D(start=axes.get_origin(), end=dots[0].get_center(), color=PINK)
        v2 = Arrow3D(start=axes.get_origin(), end=dots[1].get_center(), color=GREEN, target=newV2.copy())

        self.play(FadeIn(v1), FadeIn(v2))
        self.play(FadeOut(dots))

        self.play(MoveToTarget(v2), run_time=2)

        tip = Dot3D(dots[1].get_center() + dots[0].get_center(), color=BLUE)
        self.play(FadeIn(tip))

        path = TracedPath(tip.get_center)
        self.add(path)

        #Animation takes long time
        self.play(SeeSpan(v1, v2, tip), run_time=10)
        self.wait(2)


class SeeSpan(Animation):
    def __init__(self, v1: Arrow3D, v2: Arrow3D, tip: Dot3D, **kwargs):
        super().__init__(VGroup(v1, v2), **kwargs)
        self.v1 = v1
        self.v2 = v2
        self.v1Orig = np.copy(v1.get_end())
        self.v2Orig = np.copy(v2.get_end())
        self.tip = tip

    def interpolate_mobject(self, alpha: float) -> None:
        newEnd1 = self.v1Mag(alpha) * self.v1Orig
        self.v1.become(Arrow3D(self.v1.get_start(), newEnd1, color=PINK))

        newEnd2 = self.v2Mag(alpha) * self.v2Orig
        self.v2.become(Arrow3D(newEnd1, newEnd1 + newEnd2, color=GREEN))
        self.tip.move_to(newEnd2 + newEnd1)

    def v1Mag(self, t):
        x = 1 - 4 * t
        if t > 0.5:
            return 4 * t - 3
        return x

    def v2Mag(self, t):
        return np.cos(4 * PI * t)

class SeeTransformation(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"include_numbers": True},
            tips=False
        )

        rect = Rectangle(height=axes.height, width=axes.width)
        rect.center()
        rect.set_fill(color=[BLUE, YELLOW], opacity=0.5)

        v1 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[1], [0], [0]]), color=PINK,
                     target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[1], [2], [3]]), color=PINK))
        v2 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[0], [1], [0]]), color=GREEN,
                     target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[2], [0], [-1]]), color=GREEN))

        basis = VGroup(v1, v2)

        self.play(Write(axes))
        self.play(FadeIn(basis))

        self.move_camera(phi = 70 * DEGREES, theta = 45 * DEGREES, run_time=1.5)
        self.begin_ambient_camera_rotation(rate=0.15)

        surface = Surface(
            lambda u, v: axes.c2p(*self.surf(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=12,
            fill_opacity=0.6
        ).set_z_index(0)

        self.wait(1)
        self.play(FadeIn(rect))
        self.play(ReplacementTransform(rect, surface),
                  MoveToTarget(v1), MoveToTarget(v2), run_time=3)

        note = Tex(r'Image$(T) = $', r'span',
                   r'$\left ( \begin{bmatrix} 1\\2\\3 \end{bmatrix}, \begin{bmatrix} 2\\0\\-1 \end{bmatrix} \right )$', color=BLUE_B)
        self.add_fixed_in_frame_mobjects(note)
        self.remove(note)
        note.to_corner(DL)

        self.play(Write(note))

        newW2 = Arrow3D(start=axes.c2p([[1], [2], [3]]), end=axes.c2p([[3], [2], [2]]), color=GREEN).set_z_index(1)
        w1 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[1], [2], [3]]), color=PINK).set_z_index(1)
        w2 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[2], [0], [-1]]), color=GREEN, target=newW2).set_z_index(1)
        self.remove(v1, v2)
        self.add(w1, w2)

        self.play(MoveToTarget(w2))

        tip = Dot3D(newW2.get_end(), color=BLUE)

        self.play(FadeIn(tip), run_time=0.5)

        # Animation takes long time
        self.play(SeeSpan(w1, w2, tip), run_time=6, rate_func=linear)

        final = Tex(r'Image$(T) = $', r'span',
                    r'$\left ( T \left ( \begin{bmatrix} 1\\0 \end{bmatrix} \right ), T \left ( \begin{bmatrix} 0\\1 \end{bmatrix} \right ) \right )$', color=BLUE_B)
        final.to_corner(DL)
        self.add_fixed_in_frame_mobjects(final)
        self.remove(final)

        self.play(TransformMatchingTex(note, final))
        self.wait(2)

        transition = Tex(r'span',
                    r'$\left ( T \left ( \begin{bmatrix} 1\\0 \end{bmatrix} \right ), T \left ( \begin{bmatrix} 0\\1 \end{bmatrix} \right ) \right )$', color=BLUE_B)

        self.add_fixed_in_frame_mobjects(transition)
        self.remove(transition)

        self.play(FadeOut(axes, w1, w2, tip, surface))
        self.play(TransformMatchingTex(final, transition))
        self.remove(final)
        self.wait(1)

    def surf(self, u, v):
        return np.array([u + 2 * v, 2 * u, 3 * u - v])

class DifferentCasesScene(ThreeDScene):
    def construct(self):

        transitionEq = MathTex("\\textrm{span} \\left ( T \\left ( \\begin{bmatrix} 1\\\\0 \\end{bmatrix} \\right ), T \\left ( \\begin{bmatrix} 0\\\\1 \\end{bmatrix} \\right ) \\right )", color=BLUE_B)

        self.add_fixed_in_frame_mobjects(transitionEq)
        self.wait(0.5)
        self.play(transitionEq.animate.to_corner(UL))

        case1 = MathTex("\\textrm{span} \\left ( T \\left ( \\begin{bmatrix} 1\\\\0 \\end{bmatrix} \\right ), T \\left ( \\begin{bmatrix} 0\\\\1 \\end{bmatrix} \\right ) \\right ) = \\left ( \\begin{bmatrix} 1\\\\2\\\\3 \\end{bmatrix}, \\begin{bmatrix} 2\\\\0\\\\-1 \\end{bmatrix} \\right )", color=BLUE_B)
        self.add_fixed_in_frame_mobjects(case1)
        self.remove(case1)
        case1.to_corner(UL)
        self.play(ReplacementTransform(transitionEq, case1))

        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"include_numbers": True},
            tips=False
        )

        axes.shift(DOWN)

        rect = Rectangle(height=axes.height, width=axes.width)
        rect.center()
        rect.set_fill(color=[BLUE, YELLOW], opacity=0.5)
        rect2 = rect.copy()

        self.set_camera_orientation(phi = 70 * DEGREES, theta = 45 * DEGREES)
        self.begin_ambient_camera_rotation(0.15)
        self.play(DrawBorderThenFill(axes))

        v1 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[1], [0], [0]]), color=PINK,
                     target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[1], [2], [3]]), color=PINK))
        v2 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[0], [1], [0]]), color=GREEN,
                     target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[2], [0], [-1]]), color=GREEN))

        surface = Surface(
            lambda u, v: axes.c2p(*self.surf(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=12,
            fill_opacity=0.6
        )

        self.play(FadeIn(v1, v2))
        self.play(MoveToTarget(v1), MoveToTarget(v2))
        self.play(FadeIn(surface))

        self.wait(2)
        self.play(FadeOut(axes, v1, v2, surface), case1.animate.center())
        self.wait(0.5)

        case2 = MathTex("\\textrm{span} \\left ( T \\left ( \\begin{bmatrix} 1\\\\0 \\end{bmatrix} \\right ), T \\left ( \\begin{bmatrix} 0\\\\1 \\end{bmatrix} \\right ) \\right ) = \\left ( \\begin{bmatrix} 1\\\\2\\\\3 \\end{bmatrix}, \\begin{bmatrix} 1\\\\2\\\\3 \\end{bmatrix} \\right )", color=BLUE_B)
        self.add_fixed_in_frame_mobjects(case2)
        self.remove(case2)
        self.play(ReplacementTransform(case1, case2))

        self.wait(0.5)

        w1 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[1], [0], [0]]), color=PINK,
                     target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[0.5], [1], [1.5]]), color=PINK))
        w2 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[0], [1], [0]]), color=GREEN,
                     target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[0.5], [1], [1.5]]), color=GREEN))

        self.play(case2.animate.to_corner(UL), FadeIn(axes, w1, w2))
        self.wait()
        self.play(MoveToTarget(w1), MoveToTarget(w2))
        self.wait(1)

        whiteArr = Arrow3D(start=axes.get_origin(), end=axes.c2p([[0.5], [1], [1.5]]), color=WHITE,
                           target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[-0.5], [-1], [-1.5]]), color=WHITE))
        self.remove(w1, w2)
        self.add(whiteArr)

        tip = Dot3D(axes.c2p([[0.5], [1], [1.5]]), color=BLUE,
                    target=Dot3D(axes.c2p([[-0.5], [-1], [-1.5]]), color=BLUE))

        self.play(FadeIn(tip), run_time=0.5)
        self.play(MoveToTarget(whiteArr), MoveToTarget(tip), run_time=1)

        whiteArr2 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[-0.5], [-1], [-1.5]]), color=WHITE,
                           target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[0.5], [1], [1.5]]), color=WHITE))
        tip2 = Dot3D(axes.c2p([[-0.5], [-1], [-1.5]]), color=BLUE,
                    target=Dot3D(axes.c2p([[0.5], [1], [1.5]]), color=BLUE))

        self.remove(whiteArr, tip)
        self.add(whiteArr2, tip2)
        self.play(MoveToTarget(whiteArr2), MoveToTarget(tip2), run_time=1)

        u1 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[1], [0], [0]]), color=PINK,
                     target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[0.5], [1], [1.5]]), color=PINK))
        u2 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[0], [1], [0]]), color=GREEN,
                     target=Arrow3D(start=axes.get_origin(), end=axes.c2p([[0.5], [1], [1.5]]), color=GREEN))

        self.play(FadeOut(whiteArr2, tip2))
        self.play(FadeIn(u1, u2, rect))

        line = Surface(
            lambda u, v: axes.c2p(*self.line(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=8,
            fill_opacity=0.6
        )

        self.play(MoveToTarget(u1), MoveToTarget(u2), ReplacementTransform(rect, line))
        self.wait(3)

        self.play(FadeOut(axes, u1, u2, line), case2.animate.center())

        case3 = MathTex("\\textrm{span} \\left ( T \\left ( \\begin{bmatrix} 1\\\\0 \\end{bmatrix} \\right ), T \\left ( \\begin{bmatrix} 0\\\\1 \\end{bmatrix} \\right ) \\right ) = \\left ( \\begin{bmatrix} 0\\\\0\\\\0 \\end{bmatrix}, \\begin{bmatrix} 0\\\\0\\\\0 \\end{bmatrix} \\right )", color=BLUE_B)

        self.add_fixed_in_frame_mobjects(case3)
        self.remove(case3)

        self.play(ReplacementTransform(case2, case3))
        self.play(case3.animate.to_corner(UL))

        k1 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[1], [0], [0]]), color=PINK)
        k2 = Arrow3D(start=axes.get_origin(), end=axes.c2p([[0], [1], [0]]), color=GREEN)

        originPoint = Dot3D(axes.get_origin(), color=PINK)
        self.play(FadeIn(axes, k1, k2))
        self.play(ReplacementTransform(VGroup(k1, k2), originPoint))
        self.wait(2)

        self.play(FadeIn(rect2))
        self.play(ReplacementTransform(rect2, originPoint.copy()))
        self.wait(2)

    def surf(self, u, v):
        return np.array([u + 2 * v, 2 * u, 3 * u - v])

    def line(self, u, v):
        t = u + v
        return np.array([t, 2 * t, 3 * t])

class CubeExample(ThreeDScene):
    def construct(self):

        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"include_numbers": True},
            tips=False
        )

        rect = Rectangle(height=axes.height, width=axes.width)
        rect.center()
        rect.set_fill(color=[BLUE, YELLOW], opacity=0.5)

        self.add(axes)
        self.set_camera_orientation(phi = 70 * DEGREES, theta = 45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)

        cube = Cube(6, fill_color=[BLUE, DARK_BLUE])

        self.play(FadeIn(rect), run_time=0.5)
        self.play(FadeTransform(rect, cube))
        self.wait(3)

class TransitionScene(Scene):
    def construct(self):
        title = Tex("Can a", " linear transformation ", "$T: $", "$\\mathbb{R}^2$",
                "$\\to$", "$\\mathbb{R}^3$", " be onto?", color=WHITE)

        self.add(title.to_edge(UP, buff=2))
        title1 = Tex("A", " linear transformation ", "$T: $", "$\\mathbb{R}^2$",
                "$\\to$", "$\\mathbb{R}^3$", " be onto?", color=WHITE).to_edge(UP, buff=2)
        title2 = Tex("A", " linear transformation ", "$T: $", "$\\mathbb{R}^2$",
                     "$\\to$", "$\\mathbb{R}^3$", " cannot", " be onto?", color=WHITE).to_edge(UP, buff=2)
        self.wait(1.5)
        self.play(TransformMatchingTex(title, title1), run_time=1)
        self.play(TransformMatchingTex(title1, title2), run_time=1)
        self.wait(1.5)

        assign1 = MathTex(r'\begin{bmatrix} 1 \\ 0 \end{bmatrix} \mapsto \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}')
        assign2 = MathTex(r'\begin{bmatrix} 0 \\ 1 \end{bmatrix} \mapsto \begin{bmatrix} 2 \\ 0 \\ -1 \end{bmatrix}')
        assign3 = MathTex(r'\begin{matrix} ? \\ ? \end{matrix} \mapsto \begin{bmatrix} ? \\ ? \\ ? \end{bmatrix}')
        gp = VGroup(assign1, assign2, assign3).arrange(DOWN)
        gp.center()

        self.play(FadeOut(title2, shift=UP), Write(assign1), Write(assign2))
        self.wait(2)

        basisR3 = MathTex(r'\left \{ \begin{bmatrix} 1\\0\\0 \end{bmatrix}, \begin{bmatrix} 0\\1\\0 \end{bmatrix}, \begin{bmatrix} 0\\0\\1 \end{bmatrix} \right \}')
        basisR3Label = MathTex(r'\mathbb R^3')
        basisR3.to_edge(DOWN, buff=1)
        basisR3Label.next_to(basisR3, DOWN)

        self.play(Write(basisR3), Write(basisR3Label))
        self.wait(1)
        self.play(FadeOut(basisR3Label, basisR3))

        self.play(Write(assign3))
        self.wait(3.5)

        bsign1 = MathTex(r'\begin{bmatrix} 1 \\ 0 \end{bmatrix} \mapsto \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}')
        bsign2 = MathTex(r'\begin{bmatrix} 0 \\ 1 \end{bmatrix} \mapsto \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}')
        bsign3 = MathTex(r'\begin{matrix} ? \\ ? \end{matrix} \mapsto \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}')
        gp2 = VGroup(bsign1, bsign2, bsign3).arrange(DOWN)
        gp2.center()

        self.play(TransformMatchingTex(gp, gp2))
        self.wait(1)

class SpanAll3DSpace(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"include_numbers": True},
            tips=True
        ).add_coordinates()

        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)

        self.play(Write(axes), run_time=0.5)

        i = Arrow3D(start=axes.get_origin(), end=axes.c2p([[1], [0], [0]]),
                    color=PINK)
        j = Arrow3D(start=axes.get_origin(), end=axes.c2p([[0], [1], [0]]),
                    target=Arrow3D(start=axes.c2p([[1], [0], [0]]), end=axes.c2p([[1], [1], [0]]), color=GREEN),
                    color=GREEN)
        k = Arrow3D(start=axes.get_origin(), end=axes.c2p([[0], [0], [1]]),
                    target=Arrow3D(start=axes.c2p([[1], [1], [0]]), end=axes.c2p([[1], [1], [1]]), color=YELLOW),
                    color=YELLOW)
        gp = VGroup(i, j, k)
        self.play(FadeIn(gp))
        self.play(MoveToTarget(j), MoveToTarget(k))

        tip = Dot3D(axes.c2p([[1], [1], [1]]))
        self.play(FadeIn(tip), running_time = 0.5)

        self.play(SeeSpan3D(i, j, k, tip), run_time=8)
        self.wait(2)

class ExpansionScene(Scene):
    def construct(self):
        r3transformation = Tex(r'$T: \mathbb R^3 \to \mathbb R^3$').shift(UP)

        self.add(r3transformation)

        basisR3 = MathTex(r'\left \{ \begin{bmatrix} 1\\0\\0 \end{bmatrix}, \begin{bmatrix} 0\\1\\0 \end{bmatrix}, \begin{bmatrix} 0\\0\\1 \end{bmatrix} \right \}')
        basisR3.next_to(r3transformation, DOWN, buff=1.5)
        basisR3Label = Tex(r'Basis for $\mathbb R^3$').next_to(basisR3, DOWN)

        self.play(FadeIn(basisR3, shift=UP))
        self.play(Write(basisR3Label))

        self.wait(2)
        self.play(FadeOut(basisR3Label, r3transformation, run_time=0.5))

        assign1 = MathTex(r'\begin{bmatrix} 1\\0\\0 \end{bmatrix} \mapsto ', r'\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}')
        assign2 = MathTex(r'\begin{bmatrix} 0\\1\\0 \end{bmatrix} \mapsto ', r'\begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}')
        assign3 = MathTex(r'\begin{bmatrix} 0\\0\\1 \end{bmatrix} \mapsto ', r'\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}')
        gp = VGroup(assign1, assign2, assign3).arrange(DOWN)
        gp.center()

        self.play(Transform(basisR3, gp, replace_mobject_with_target_in_scene=True))
        self.wait(2)

        surr1 = SurroundingRectangle(assign1[1], color=YELLOW)
        surr2 = SurroundingRectangle(assign2[1], color=YELLOW)
        surr3 = SurroundingRectangle(assign3[1], color=YELLOW)

        self.play(LaggedStart(Write(surr1, run_time=0.5),
                  Write(surr2, run_time=0.5),
                  Write(surr3, run_time=0.5), lag_ratio=0.33))

        self.play(FadeOut(surr1, surr2, surr3))

        general = Tex(r'$T: \mathbb R$', r'$^n$', r'$ \to \mathbb R$', r'$^m$').shift(UP)
        self.play(ReplacementTransform(gp, general))
        self.wait(3)

        surr4 = SurroundingRectangle(general[3])
        surr5 = SurroundingRectangle(general[1])

        self.play(Write(surr4), run_time=0.5)
        self.play(FadeOut(surr4))
        self.play(Write(surr5), run_time=0.5)
        self.play(FadeOut(surr5))

        label1 = Tex('$T$ cannot be onto')
        label2 = Tex('if').next_to(label1, DOWN)
        label3 = Tex('$n < m$').next_to(label2, DOWN)

        self.play(Write(label1), run_time=0.5)
        self.play(Write(label2), run_time=0.5)
        self.play(Write(label3), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(label1, label2, label3))

        label = Tex(r'Onto?').center()
        bigger = Tex(r'$T: \mathbb R$', r'$^9$', r'$ \to \mathbb R$', r'$^{11}$')
        smaller = Tex(r'$T: \mathbb R$', r'$^{11}$', r'$ \to \mathbb R$', r'$^{9}$')
        mid = Tex(r'$T: \mathbb R$', r'$^{2}$', r'$ \to \mathbb R$', r'$^{999}$')

        gp2 = VGroup(label, bigger, smaller, mid).arrange(DOWN)
        gp2.center()

        self.play(ReplacementTransform(general, gp2))
        self.wait(2)

        check1 = Tex(r'$\times$', color=RED).next_to(bigger, RIGHT)
        check2 = Tex(r'$\checkmark$', color=GREEN).next_to(smaller, RIGHT)
        check3 = Tex(r'$\times$', color=RED).next_to(mid, RIGHT)

        self.play(Write(check1))
        self.play(Write(check2))
        self.play(Write(check3))
        self.wait(6)

class ScrollingVectorScene(Scene):
    def construct(self):
        vector = MathTex("\\begin{bmatrix} 1\\\\4\\\\4\\\\6\\\\5\\\\2\\\\1\\\\0\\\\9\\\\7\\\\3\\\\1\\\\4\\\\2\\\\6\\\\9\\\\8\\\\0\\\\7\\\\0\\\\7\\\\3\\\\6\\\\9\\\\1\\\\4\\\\4\\\\6\\\\5\\\\2\\\\1\\\\0\\\\9\\\\7\\\\3\\\\1\\\\4\\\\2\\\\6\\\\9\\\\8\\\\0\\\\7\\\\0\\\\7\\\\3\\\\6\\\\9\\\\1\\\\4\\\\4\\\\6\\\\5\\\\2\\\\1\\\\0\\\\9\\\\7\\\\3\\\\1\\\\4\\\\2\\\\6\\\\9\\\\8\\\\0\\\\7\\\\0\\\\7\\\\3\\\\6\\\\9\\\\4\\\\4\\\\6\\\\5\\\\2\\\\1\\\\0\\\\9\\\\7\\\\3\\\\1\\\\4\\\\2\\\\6\\\\9\\\\8\\\\0\\\\7\\\\0\\\\7\\\\3\\\\6\\\\9\\\\1\\\\4\\\\4\\\\6\\\\5\\\\2\\\\1\\\\0\\\\9\\\\7\\\\3\\\\1\\\\4\\\\2\\\\6\\\\9\\\\8\\\\0\\\\7\\\\0\\\\7\\\\3\\\\6\\\\9\\\\1\\\\4\\\\4\\\\6\\\\5\\\\2\\\\1\\\\0\\\\9\\\\7\\\\3\\\\1\\\\4\\\\2\\\\6\\\\9\\\\8\\\\0\\\\7\\\\0\\\\7\\\\3\\\\6\\\\9\\\\4\\\\4\\\\6\\\\5\\\\2\\\\1\\\\0\\\\9\\\\7\\\\3\\\\1\\\\4\\\\2\\\\6\\\\9\\\\8\\\\0\\\\7\\\\0\\\\7\\\\3\\\\6\\\\9\\\\1\\\\4\\\\4\\\\6\\\\5\\\\2\\\\1\\\\0\\\\9\\\\7\\\\3\\\\1\\\\4\\\\2\\\\6\\\\9\\\\8\\\\0\\\\7\\\\0\\\\7\\\\3\\\\6\\\\9\\\\1\\\\4\\\\4\\\\6\\\\5\\\\2\\\\1\\\\0\\\\9\\\\7\\\\3\\\\1\\\\4\\\\2\\\\6\\\\9\\\\8\\\\0\\\\7\\\\0\\\\7\\\\3\\\\6\\\\9 \\end{bmatrix}", font_size=96)
        vector.to_edge(UP)
        self.add(vector)
        self.play(vector.animate.to_edge(DOWN), run_time=12)
        self.wait(2)

class MatrixExampleScene(Scene):
    def construct(self):
        assign1 = MathTex(r'T\left ( \begin{bmatrix} 1 \\ 0 \end{bmatrix} \right ) =', r'\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}')
        assign2 = MathTex(r'T\left ( \begin{bmatrix} 0 \\ 1 \end{bmatrix} \right ) =', r'\begin{bmatrix} 2 \\ 0 \\ -1 \end{bmatrix}')
        assigns = VGroup(assign1, assign2).arrange(DOWN)
        assigns.center()

        self.play(FadeIn(assigns))
        self.wait(1)

        together1 = MathTex(r'\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}')
        together2 = MathTex(r'\begin{bmatrix} 2 \\ 0 \\ -1 \end{bmatrix}')
        together = VGroup(together1, together2).arrange(RIGHT)
        together.center()

        self.play(TransformMatchingTex(assigns, together))
        self.wait(1)

        mtrx1 = MathTex(r'\begin{bmatrix} 1 & 2 \\ 2 & 0 \\ 3 & -1 \end{bmatrix}')

        self.play(FadeTransform(together, mtrx1))
        self.wait(1)

        multipy1 = MathTex(r'\begin{bmatrix} 1 & 2 \\ 2 & 0 \\ 3 & -1 \end{bmatrix}',  r'\cdot', r'\begin{bmatrix} x \\ y \end{bmatrix}')

        self.play(TransformMatchingTex(mtrx1, multipy1))
        self.wait(1)

        self.play(multipy1.animate.shift(LEFT*2))

        multipy2 = MathTex(
            r'= x \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} + y \begin{bmatrix} 2 \\ 0 \\ -1 \end{bmatrix}')
        multipy2.next_to(multipy1, RIGHT)

        self.play(FadeIn(multipy2))
        self.wait(1)

        multipy3 = MathTex(r'= \begin{bmatrix} x \\ 2x \\ 3x \end{bmatrix} + \begin{bmatrix} 2y \\ 0 \\ -y \end{bmatrix}')
        multipy3.next_to(multipy1, RIGHT)

        self.play(ReplacementTransform(multipy2, multipy3))
        self.wait(1)

        multipy4 = MathTex(
            r'= \begin{bmatrix} x + 2y \\ 2x \\ 3x - y \end{bmatrix}')
        multipy4.next_to(multipy1, RIGHT)

        self.play(ReplacementTransform(multipy3, multipy4))
        self.wait(1)

        applyTransformation = MathTex(r'T', r'\left ( \begin{bmatrix} x \\ y \end{bmatrix} \right )', r' = ')
        applyTransformation.next_to(multipy1, LEFT)

        self.play(FadeIn(applyTransformation))
        self.wait(1)

        self.play(FadeOut(multipy4), VGroup(applyTransformation, multipy1).animate.center())
        self.wait(1)

        mtrxBij = MathTex(r'T', r' \leftrightarrow ', r'\begin{bmatrix} 1 & 2 \\ 2 & 0 \\ 3 & -1 \end{bmatrix}')
        self.play(TransformMatchingTex(VGroup(applyTransformation, multipy1), mtrxBij))
        self.wait(1)
        self.play(FadeOut(mtrxBij, shift= DOWN))


class SeeSpan3D(Animation):
    def __init__(self, v1: Arrow3D, v2: Arrow3D, v3: Arrow3D, tip: Dot3D, **kwargs):
        super().__init__(VGroup(v1, v2), **kwargs)
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v1Orig = np.copy(v1.get_end())
        self.v2Orig = np.copy(v2.get_end())
        self.v3Orig = np.copy(v3.get_end())
        self.tip = tip

    def interpolate_mobject(self, alpha: float) -> None:
        newEnd1 = self.v1Mag(alpha) * self.v1Orig
        self.v1.become(Arrow3D(self.v1.get_start(), newEnd1, color=PINK))

        newEnd2 = self.v2Mag(alpha) * self.v2Orig
        self.v2.become(Arrow3D(newEnd1, newEnd1 + newEnd2, color=GREEN))

        newEnd3 = self.v3Mag(alpha) * self.v3Orig
        self.v3.become(Arrow3D(newEnd1 + newEnd2, newEnd1 + newEnd2 + newEnd3, color=YELLOW))
        self.tip.move_to(newEnd1 + newEnd2 + newEnd3)

    def v1Mag(self, t):
        x = 1 - 4 * t
        if t > 0.5:
            return 4 * t - 3
        return x

    def v2Mag(self, t):
        return np.cos(4 * PI * t)

    def v3Mag(self, t):
        return np.cos(2 * PI * t)

class FinalScene(Scene):
    def construct(self):
        title = Tex("Can a ", "linear transformation ", "$T: $", "$\\mathbb{R}^2$",
                    "$\\to$", "$\\mathbb{R}^3$", " be ", "onto?", color=WHITE).shift(UP)
        self.play(Write(title))
        self.wait(2)

        no = Text("No", color=RED, font_size=56).shift(DOWN)
        self.play(FadeIn(no), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(no))

        title1 = Tex("Can a ", "continuous function ", "$f: $", "$\\mathbb{R}^2$",
                    "$\\to$", "$\\mathbb{R}^3$", " be ", "onto?", color=WHITE).shift(UP)
        self.play(TransformMatchingTex(title, title1))

        und = Underline(title1[1])

        self.play(Write(und))
        self.play(FadeOut(und), run_time=0.5)
        self.wait(1)

        thanks = Tex("$<3$ for the solution!", color=BLUE, font_size=56).shift(DOWN)
        self.play(Write(thanks))
        self.wait(4)

class YouAskScene(Scene):
    def construct(self):
        label = Text("You")
        Q1 = Text("?", font_size=48).rotate(45 * DEGREES).shift(UP * 2 + RIGHT)
        Q2 = Text("?", font_size=48).rotate(-30 * DEGREES).shift(LEFT * 2 + UP)
        Q3 = Text("?", font_size=48).rotate(10 * DEGREES).shift(DOWN + RIGHT)
        self.play(Write(label))
        self.wait(1)
        self.play(Write(Q1))
        self.play(Write(Q2))
        self.play(Write(Q3))
        self.wait()

class UsedInScene(Scene):
    def construct(self):
        cs = Tex('Computer Science').shift(UP * 2 + LEFT * 3)
        ml = Tex('Machine Learning').shift(UP * 2 + RIGHT * 3)
        cm = Tex('Computation').shift(DOWN * 2 + LEFT * 3)
        cp = Tex('Cryptography').shift(DOWN * 2 + RIGHT * 3)
        self.play(Write(cs), run_time = 0.85)
        self.play(Write(ml), run_time = 0.85)
        self.play(Write(cm), run_time = 0.85)
        self.play(Write(cp), run_time = 0.85)
        self.wait(2.5)
class Thumbnail(Scene):
    def construct(self):
        one = Tex(r'Image of $T: \mathbb R^2 \to \mathbb R^3$', color=BLUE_B).to_edge(DOWN, buff=1)
        self.add(one)
