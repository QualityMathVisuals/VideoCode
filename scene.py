from manim import *

class IntroScene(Scene):
    def construct(self):
        title = Tex("Can a linear transformation ", "$T: $", "$\\mathbb{R}^2$",
                    "$\\to$", "$\\mathbb{R}^3$", " be onto?", color=WHITE)

        self.play(Write(title), run_time=1)
        self.wait(2)

        ax = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": True}
        ).add_coordinates()
        ax.to_edge(DL)
        arw = Arrow(start=LEFT, end=RIGHT)
        arw.next_to(ax, RIGHT, buff=1.2)

        eq = MathTex(r'f: ', r'\mathbb R^2', r' \to ', r'\mathbb R^3')
        eq.next_to(arw, UP, buff=1)

        out = Matrix([[0.00], [0.00], [0.00]])
        out.to_edge(RIGHT, buff=1.5)

        dot = Dot().set_color(YELLOW)
        dot.move_to(ax.get_origin())

        self.play(DrawBorderThenFill(ax), FadeIn(arw), ReplacementTransform(title, eq), FadeIn(out), FadeIn(dot))
        self.wait(1)

        inputLabel = Tex('Input', color=YELLOW, opacity=0.8).next_to(ax, UP, buff=0.2).shift(LEFT * 2.4)
        outputLabel = Tex('Output', color=BLUE, opacity=0.8).next_to(out, UP, buff=1.3).shift(LEFT * 0.2)
        self.play(Write(inputLabel), Write(outputLabel))

        fLabel = MathTex(r'\begin{bmatrix} x \\ y \end{bmatrix} \mapsto \begin{bmatrix} x \\ y \\ 0 \end{bmatrix}')
        fLabel.next_to(arw, DOWN, buff=0.7)

        self.play(FadeIn(fLabel))
        self.wait(0.5)

        out.add_updater(lambda matrix:
                        out.become(Matrix(self.inclusion(np.around(ax.point_to_coords(dot.get_center()), decimals=1))))
                        .to_edge(RIGHT, buff=1.5)
                        )

        trace = ParametricFunction(self.traceScribble, t_range=[0, PI])
        trace.move_to(ax.get_origin())

        rect1 = SurroundingRectangle(ax,color=YELLOW)

        self.play(LaggedStart(MoveAlongPath(dot, trace, rate_func=linear), Write(rect1),
                              lag_ratio=0.5, run_time=4))
        self.play(FadeOut(rect1, run_time=0.5))

        gLabel = MathTex(
            r'\begin{bmatrix} x \\ y \end{bmatrix} \mapsto \begin{bmatrix} xy \\ x^2 \\ y^2 \end{bmatrix}')
        gLabel.next_to(arw, DOWN, buff=0.7)

        eq2 = MathTex(r'g: ', r'\mathbb R^2', r' \to ', r'\mathbb R^3')
        eq2.move_to(eq)

        self.play(ReplacementTransform(fLabel, gLabel), ReplacementTransform(eq, eq2))
        self.wait(0.5)

        out.clear_updaters()
        out.add_updater(lambda matrix:
                        out.become(Matrix(np.around(self.nonLinear(ax.point_to_coords(dot.get_center())), decimals=1)))
                        .to_edge(RIGHT, buff=1.5)
                        )

        rect2 = SurroundingRectangle(out,color=BLUE)

        self.play(MoveAlongPath(dot, trace, rate_func=linear), run_time=4)
        self.wait(0.5)
        out.clear_updaters()
        # Cut to 3Dpart1 in editing. 10 seconds + 0.5 second delay
        self.play(FadeOut(out, arw, gLabel, dot, inputLabel, outputLabel),
                  eq2.animate.center().to_edge(UP), ax.animate.center().to_edge(DOWN))

        rect = Rectangle(height=ax.height, width=ax.width)
        rect.center()
        rect.set_fill(color=[BLUE, YELLOW], opacity=0.5)

        self.play(DrawBorderThenFill(rect), FadeOut(eq2))
        self.wait(1)

    def traceScribble(self, t):
        return np.array((np.sin(2 * t), np.sin(3 * t), 0))

    def inclusion(self, v):
        return [[v[0]], [v[1]], [0.00]]

    def nonLinear(self, v):
        return [[v[0] * v[1]], [v[0] * v[0]], [v[1] * v[1]]]

class Function3DImageScene2(ThreeDScene):
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

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": True}
        ).add_coordinates()

        rect = Rectangle(height=axes.height, width=axes.width)
        rect.center()
        rect.set_fill(color=[BLUE, YELLOW], opacity=0.5)

        self.add(rect, plane)

        self.move_camera(phi = 70 * DEGREES, theta = 45 * DEGREES, run_time=1.5)
        self.begin_ambient_camera_rotation(rate=0.15)

        self.play(FadeOut(plane), Write(axes))

        surface = Surface(
            lambda u, v: axes.c2p(*self.surf(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=12,
            fill_opacity=0.6
        )

        self.play(Transform(rect, surface), run_time=3)
        self.wait(2)

        defImage = Tex(r'Image of $g$', color=BLUE).shift(DOWN * 3 + RIGHT * 5)

        self.add_fixed_in_frame_mobjects(defImage)
        self.play(Write(defImage))
        self.wait(6)

    def composition(self, t):
        return np.array([np.sin(2 * t) * np.sin(3 * t), np.sin(2 * t) * np.sin(2 * t), np.sin(3 * t) * np.sin(3 * t)])

    def surf(self, u, v):
        return np.array([u * v, u * u, v * v])


class LinearTransformation(Scene):
    def construct(self):
        title = Tex("Can a ", "linear transformation ", "$T: $", "$\\mathbb{R}^2$",
                    "$\\to$", "$\\mathbb{R}^3$", " be onto?", color=WHITE)

        self.play(Write(title.to_edge(UP)))

        underline = Underline(title[1], color=YELLOW)

        self.play(Write(underline))
        self.play(FadeOut(underline), run_time=0.5)

        self.play(FadeOut(title))

        #subTitle = Tex("For any ", r'$\begin{bmatrix} x_1 \\ y_1 \end{bmatrix}$,'
                                   #r'$\begin{bmatrix} x_2 \\ y_2 \end{bmatrix}$', " in ", r'$\mathbb R^2$', " and ",
                                   #r'$c \in \mathbb R$', ":")
        additiveLaw = MathTex(r'T\left (\begin{bmatrix} x_1 \\ y_1 \end{bmatrix}\right ) +'
                              r'T\left (\begin{bmatrix} x_2 \\ y_2 \end{bmatrix}\right ) ='
                              r'T\left (\begin{bmatrix} x_1 \\ y_1 \end{bmatrix} +'
                              r' \begin{bmatrix} x_2 \\ y_2 \end{bmatrix}\right )')
        multiplicativeLaw = MathTex(r'c \cdot T\left (\begin{bmatrix} x_1 \\ y_1 \end{bmatrix}\right ) '
                                    r'= T\left (\begin{bmatrix} cx_1 \\ cy_1 \end{bmatrix} \right )')

        group = VGroup(additiveLaw, multiplicativeLaw).arrange(DOWN).space_out_submobjects()
        group.center()

        self.play(Write(group))
        self.wait(2)
        self.play(FadeOut(group))

        coordinatePlane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": True},
            tips=True
        )
        coordinatePlane.to_edge(LEFT)
        coordinatePlaneLabel = Tex('Input Space').next_to(coordinatePlane, UP, buff=0.1)

        self.play(Write(coordinatePlane), Write(coordinatePlaneLabel))

        coords = Matrix([[0.00], [0.00]])
        coords.shift(RIGHT * 3 + UP * 2)

        dot = Dot().set_color(YELLOW)
        dot.move_to(coordinatePlane.get_origin())

        coords.add_updater(lambda matrix:
                           coords.become(Matrix(
                               np.around(self.id(coordinatePlane.point_to_coords(dot.get_center())), decimals=1)))
                           .shift(RIGHT * 3 + UP * 2)
                           .set_row_colors(GREEN_C, PINK)
                           )

        plus1 = MathTex(r' + ')
        plus1.next_to(coords, DOWN, buff=1.1)
        plus1.shift(RIGHT * 0.3)

        xVec = Matrix([[0.00], [0.00]]).next_to(plus1, LEFT)
        yVec = Matrix([[0.00], [0.00]]).next_to(plus1, RIGHT)

        xVec.add_updater(lambda m:
                         xVec.become(Matrix([[coordinatePlane.p2c(dot.get_center())[0].__round__(1)], [0.00]]))
                         .next_to(plus1, LEFT)
                         .set_row_colors(GREEN_C, WHITE)
                         )

        yVec.add_updater(lambda m:
                         yVec.become(Matrix([[0.00], [coordinatePlane.p2c(dot.get_center())[1].__round__(1)]]))
                         .next_to(plus1, RIGHT)
                         .set_row_colors(WHITE, PINK)
                         )

        equal1 = MathTex(r'= ')
        equal1.next_to(xVec, LEFT, buff=1.3)

        plus2 = MathTex(r' + ')
        plus2.next_to(plus1, DOWN, buff=1.5)

        unitxVec = Matrix([[1.0], [0.0]])
        unitxVec.next_to(plus2, LEFT)

        unityVec = Matrix([[0.0], [1.0]])
        unityVec.next_to(plus2, RIGHT, buff=1.2)

        xVal = DecimalNumber(num_decimal_places=1, color=GREEN_C).next_to(unitxVec, LEFT, buff=0.1)
        xVal.add_updater(lambda x: xVal.set_value(coordinatePlane.p2c(dot.get_center())[0].__round__(1))
                         .next_to(unitxVec, LEFT, buff=0.1)
                         )

        yVal = DecimalNumber(num_decimal_places=1, color=PINK).next_to(unityVec, LEFT, buff = 0.1)
        yVal.add_updater(lambda y: yVal.set_value(coordinatePlane.p2c(dot.get_center())[1].__round__(1))
                         .next_to(unityVec, LEFT, buff = 0.1)
                         )

        equal2 = MathTex(r'= ')
        equal2.next_to(unitxVec, LEFT, buff=1.3)

        lines = coordinatePlane.get_lines_to_point(dot.get_center())
        lines.add_updater(lambda l:
                          lines.become(coordinatePlane.get_lines_to_point(dot.get_center()))
                          )

        self.play(FadeIn(dot, lines, coords), Write(equal1), Write(xVec), Write(plus1), Write(yVec),
                  Write(equal2), Write(xVal), Write(unitxVec), Write(plus2), Write(yVal), Write(unityVec))

        randomPath = ParametricFunction(self.randomPath, t_range=[0, PI], fill_opacity=0).set_color(RED)
        randomPath.shift(LEFT * 3.6)

        self.play(MoveAlongPath(dot, randomPath), run_time=12)

        vecEq = MathTex(r'\begin{bmatrix} x \\ y \end{bmatrix}', r' = ', r'x \cdot ',
                        r'\begin{bmatrix} 1 \\ 0 \end{bmatrix}',
                        r' + ', r'y \cdot ', r'\begin{bmatrix} 0 \\ 1 \end{bmatrix}')
        vecEq.center()

        self.play(FadeOut(dot, equal1, xVec, yVec, plus1))
        self.play(FadeOut(coordinatePlane, coordinatePlaneLabel, shift=LEFT),
                  ReplacementTransform(VGroup(coords, equal2, unitxVec, xVal, yVal, plus2, unityVec), vecEq)
                  )
        self.wait(2)

        appliedVecEq = MathTex(r'T\left ( \begin{bmatrix} x \\ y \end{bmatrix} \right )',
                               r' = ', r'x \cdot ',
                               r'T\left ( \begin{bmatrix} 1 \\ 0 \end{bmatrix} \right )',
                               r' + ', r'y \cdot ',
                               r'T\left ( \begin{bmatrix} 0 \\ 1 \end{bmatrix} \right )')

        self.play(ReplacementTransform(vecEq, appliedVecEq))
        self.wait(2)

        rect1 = SurroundingRectangle(appliedVecEq[0], color=YELLOW)
        rect2 = SurroundingRectangle(appliedVecEq[3], color=YELLOW)
        rect3 = SurroundingRectangle(appliedVecEq[6], color=YELLOW)

        self.play(Write(rect1))
        self.play(FadeOut(rect1), run_time=0.5)
        self.play(LaggedStart(Write(rect2), Write(rect3), lag_ratio=0.35))
        self.play(FadeOut(rect2, rect3), run_time=0.5)

        basisR2 = MathTex(r'\left \{ \begin{bmatrix} 1\\0 \end{bmatrix}, \begin{bmatrix} 0\\1 \end{bmatrix} \right \}')
        basisR2Label = Tex(r'Basis for $\mathbb R^2$').next_to(basisR2, DOWN)

        self.play(ReplacementTransform(appliedVecEq, basisR2))
        self.play(FadeIn(basisR2Label))
        self.wait(1.5)

        ex1 = MathTex(r'\begin{bmatrix} 1 \\ 0 \end{bmatrix} \mapsto \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}')
        ex2 = MathTex(r'\begin{bmatrix} 0 \\ 1 \end{bmatrix} \mapsto \begin{bmatrix} 2 \\ 0 \\ -1 \end{bmatrix}')
        gp = VGroup(ex1, ex2).arrange(DOWN)
        gp.center()

        self.play(ReplacementTransform(Group(basisR2, basisR2Label), gp))
        self.wait(1.5)

        appliedVecEq = MathTex(r'T\left ( \begin{bmatrix} x \\ y \end{bmatrix} \right )',
                               r' = ', r'x \cdot ',
                               r'T\left ( \begin{bmatrix} 1 \\ 0 \end{bmatrix} \right )',
                               r' + ', r'y \cdot ',
                               r'T\left ( \begin{bmatrix} 0 \\ 1 \end{bmatrix} \right )')
        appliedVecEq.center().shift(RIGHT)

        comb = MathTex(r'T\left ( \begin{bmatrix} x \\ y \end{bmatrix} \right )',
                               r' = ', r'x \cdot ',
                               r'\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}',
                               r' + ', r'y \cdot ',
                               r'\begin{bmatrix} 2 \\ 0 \\ -1 \end{bmatrix}').center().shift(RIGHT)

        finaleq = MathTex(r'T\left ( \begin{bmatrix} x \\ y \end{bmatrix} \right )',
                               r' = ',
                               r'\begin{bmatrix} x + 2y \\ 2x \\ 3x - y \end{bmatrix}').center().shift(RIGHT)

        self.play(gp.animate.to_corner(UL).scale(0.5), FadeIn(appliedVecEq, shift=DOWN))
        self.wait(1.5)
        self.play(ReplacementTransform(appliedVecEq, comb))
        self.wait(1.5)
        self.play(Transform(comb, finaleq))
        self.wait(3)

    def randomPath(self, t):
        return np.array([np.sin(2 * t) + np.sin(3 * t), np.sin(3 * t), 0])

    def id(self, v):
        return [[v[0]], [v[1]]]

class Function3DImageScene3(ThreeDScene):
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
        rect.move_to(axes.get_origin())
        rect.set_fill(color=[BLUE, YELLOW], opacity=0.5)

        self.add(rect)

        self.set_camera_orientation(phi = 70 * DEGREES, theta = 45 * DEGREES, run_time=1.5)
        self.begin_ambient_camera_rotation(rate=0.15)

        self.play(Write(axes))

        surface = Surface(
            lambda u, v: axes.c2p(*self.surf(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=12,
            fill_opacity=0.6
        )

        self.play(Transform(rect, surface), run_time=3)
        self.wait(8)
        like = Tex(r'$<3$ for the solution').to_edge(DOWN, buff=1.5)
        self.add_fixed_in_frame_mobjects(like)
        self.play(Write(like))
        self.wait(3)

    def surf(self, u, v):
        return np.array([u + 2 * v, 2 * u, 3 * u - v])


class Function3DImageScene4(ThreeDScene):
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
        rect.move_to(axes.get_origin())
        rect.set_fill(color=[BLUE, YELLOW], opacity=0.5)

        label = Tex('An onto function', color=BLUE).to_corner(DL)

        self.add(rect)
        self.add_fixed_in_frame_mobjects(label)
        self.set_camera_orientation(phi = 70 * DEGREES, theta = 45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)

        self.play(Write(axes), run_time=0.5)

        cube = Cube(6, fill_color=[BLUE, DARK_BLUE])

        self.play(FadeTransform(rect, cube), run_time=1.5)
        self.wait(2)

class Onto(Scene):
    def construct(self):
        title = Tex("Can a ", "linear transformation ", "$T: $", "$\\mathbb{R}^2$",
                    "$\\to$", "$\\mathbb{R}^3$", " be ", "onto?", color=WHITE)

        self.play(Write(title.to_edge(UP)))

        underline = Underline(title[7], color=BLUE)

        self.play(Write(underline))
        self.play(FadeOut(underline), run_time=0.5)

        defOnto = Tex(r'Image of $T = \mathbb R^3$', color=BLUE)

        self.play(Write(defOnto))
        self.wait(2)

class Thumbnail(Scene):
    def construct(self):
        title = Tex('Quality Math Visuals')
        title.center()
        self.add(title)


