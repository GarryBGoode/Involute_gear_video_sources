from manim import *
from manim_gearbox import *
import numpy as np
from scipy.optimize import fsolve
# from Gear_mobject import involute_func
# from Gear_mobject import invo_height_func


def involute_func(t, r, a=0):
    '''
    Returns the x-y-z values of the involute function.
    t: input angle
    r: base circle radius
    a: offset angle
    '''
    def involute_val(val):
        x = r * (np.cos(val) + (val-a) * np.sin(val-a))
        y = r * (np.sin(val) - (val-a) * np.cos(val-a))
        z = 0
        return np.array((x,y,z))
    if hasattr(t, '__iter__'):
        ret = np.empty((0,3))
        for u in t:
            point = involute_val(u)
            point = np.reshape(point,(1,3))
            ret = np.concatenate((ret,point),0)
        return ret
    else:
        return involute_val(t)

def involute_deriv_func(t,r,a=0):
    def diff_val(val):
        x = r * (-np.sin(val) + (val - a) * np.cos(val - a) + np.sin(val - a))
        y = r * (np.cos(val) + (val - a) * np.sin(val - a) - np.cos(val - a))
        z = 0
        return np.array((x,y,z))
    if hasattr(t, '__iter__'):
        ret = np.empty((0, 3))
        for u in t:
            point = diff_val(u)
            point = np.reshape(point,(1,3))
            ret = np.concatenate((ret,point),0)
        return ret
    else:
        return diff_val(t)

def involute_point_gen(t,r,a=0):
    end_points = involute_func(t,r,a)
    diff_points = involute_deriv_func(t,r,a)
    out_points = np.empty((0,3))
    for i in range(len(t)-1):
        t_ratio =  (t[i+1]-t[i]) / 3
        point1 = end_points[i,:]
        point2 = end_points[i+1,:]
        anchor_1 = point1 + diff_points[i,:] * t_ratio
        anchor_2 = point2 - diff_points[i+1,:] * t_ratio
        out_points = np.append(out_points,[end_points[i,:],anchor_1,anchor_2, end_points[i+1,:]],axis=0)

    return out_points

class Involute_test(MovingCameraScene):
    def construct(self):
        trange = np.linspace(0,PI,5)
        points = involute_point_gen(trange,1)
        invo_curve = VMobject(stroke_width=1)
        invo_curve.points=points
        invo_curve_2 = ParametricFunction(lambda t: involute_func(t,1),
                                          t_range=[0,PI,PI/23],stroke_color=RED,
                                          stroke_width=2)
        self.add(invo_curve_2,invo_curve)
        for i in range(points.shape[0]):
            self.add(Point(points[i,:],color=GREEN))
        for i in range(invo_curve_2.points.shape[0]):
            self.add(Point(invo_curve_2.points[i,:],color=BLUE))



class Involute_1(MovingCameraScene):
    def construct(self):
        r=1
        inv_a_max = 3*PI/2
        inv_a = ValueTracker(0)
        rot_inv_a = ValueTracker(0)
        rot_val = ValueTracker(0)
        shifter = ValueTracker(0.0)

        num_invo_points = 16

        Center1 = Circle(0.01, color=WHITE, fill_opacity=0, stroke_opacity=0)
        Center1.add_updater(lambda mob: mob.match_points(Circle(0.01).shift(RIGHT * shifter.get_value())))
        hole=Union(Circle(r/4,
                          fill_color=WHITE,
                          fill_opacity=1,
                          stroke_opacity=0),
                   Square(side_length=r/8,
                          fill_color=WHITE,
                          fill_opacity=1,
                          stroke_opacity=0
                          ).shift(RIGHT*r/4))
        Circ_ref = Cutout(Circle(r),hole,fill_color=WHITE,fill_opacity=1,stroke_opacity=0)


        def shift_rot_updater(mob):
            mob.shift(Center1.get_center())
            mob.rotate(rot_val.get_value(),about_point=Center1.get_center())

        Circ_main = Circ_ref.copy()
        Circ_main.add_updater(lambda mob: mob.match_points(Circ_ref.copy()))
        Circ_main.add_updater(shift_rot_updater)


        invo_curve = VMobject()
        t_range = np.linspace(0, inv_a.get_value(), num_invo_points)
        invo_curve.points = involute_point_gen(t_range,r)
        def invo_updater(mob):
            t_range = np.linspace(0,inv_a.get_value(),num_invo_points)
            mob.points = involute_point_gen(t_range,r)

        invo_curve.add_updater(invo_updater)
        invo_curve.add_updater(shift_rot_updater)

        EndPoint = Circle(0.05, color=RED, fill_color=RED, fill_opacity=1,
                          arc_center=involute_func(rot_inv_a.get_value(),r))
        EndPoint.add_updater(lambda mob: mob.move_to(involute_func(rot_inv_a.get_value(),r)))
        EndPoint.add_updater(shift_rot_updater)
        # EndPoint.add_updater(lambda mob: mob.move_to(invo_curve.point_from_proportion(1)))
        Startpoint = Circle(0.05, color=BLUE, fill_color=BLUE, fill_opacity=1)
        Startpoint.add_updater(lambda mob: mob.move_to(involute_func(0,r)))
        Startpoint.add_updater(shift_rot_updater)




        rope_arc = Arc(r, rot_inv_a.get_value(), inv_a_max - rot_inv_a.get_value(), stroke_opacity=0)
        TLine = Line(end=np.array([r * np.cos(rot_inv_a.get_value()), r * np.sin(rot_inv_a.get_value()), 0]),
                     start=involute_func(rot_inv_a.get_value(),r), stroke_opacity=0)
        Rope_base = VMobject(stroke_color=GOLD_E,stroke_opacity=1, stroke_width=10)
        Rope_base.points = np.append(rope_arc.points,TLine.points,axis=0)
        def Rope_base_updater(mob):
            arc = Arc(r, rot_inv_a.get_value(), inv_a_max - rot_inv_a.get_value())
            line = Line(end=np.array([r * np.cos(rot_inv_a.get_value()), r * np.sin(rot_inv_a.get_value()), 0]),
                         start=involute_func(rot_inv_a.get_value(), r))
            mob.points = np.append(line.points,arc.points,axis=0)
        Rope_base.add_updater(Rope_base_updater)
        Rope_base.add_updater(shift_rot_updater)

        Rope = DashedVMobject(Rope_base,num_dashes=20,dashed_ratio=0.9)
        for mob in Rope.submobjects:
            mob.updaters = []
        def Rope_upater(mob):
            Rope_base.update()
            dashmob =DashedVMobject(Rope_base, num_dashes=20, dashed_ratio=0.9)
            for i in range(len(mob.submobjects)):
                mob.submobjects[i].points = dashmob.submobjects[i].points
        Rope.add_updater(Rope_upater)
        Rope.update()


        # add base
        self.add(Center1,Circ_main, invo_curve, Startpoint, Rope, EndPoint)

        # roll out
        self.play(rot_inv_a.animate.set_value(inv_a_max),
                  inv_a.animate.set_value(inv_a_max), run_time=2)
        self.wait(1)

        self.play(rot_inv_a.animate.set_value(1.2),
                  inv_a.animate.set_value(1.2), run_time=2)

        #shift left, display equation
        # self.play(shifter.animate.set_value(-2*r))

        invo_text = MathTex(r'\begin{bmatrix}x(\phi)\\y(\phi)\end{bmatrix}', '=',
                        r'r\begin{bmatrix}cos(\phi) \\ sin(\phi)\end{bmatrix}', '+',
                        r'r\phi\begin{bmatrix} sin(\phi) \\ - cos(\phi)\end{bmatrix}')

        invo_text.next_to(Circ_main,DOWN,aligned_edge=UP,buff=r+0.25)
        invo_text.scale(0.5)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.5).shift(0.5*DOWN))





        self.play(Write(invo_text))
        radius_arr = Arrow(start=Circ_main.get_center(),
                           end=[r*np.cos(rot_inv_a.get_value()),r*np.sin(rot_inv_a.get_value()),0],
                           color=WHITE,
                           buff=0,
                           stroke_width=4,
                           tip_length=0.2)
        baseline = Line(start=Circ_main.get_center(),
                        end=Circ_main.get_center()+RIGHT*r,
                        color=WHITE,
                        stroke_width=4)
        tangent_arr = Arrow(end=invo_curve.get_end(),
                           start=[r*np.cos(rot_inv_a.get_value()),r*np.sin(rot_inv_a.get_value()),0],
                           color=WHITE,
                           buff=0,
                           stroke_width=4,
                           tip_length=0.2)

        phi_angle = Angle(baseline,radius_arr,radius=0.5*r)
        phi_text = MathTex(r'\phi').scale(0.5).next_to(phi_angle,buff=0.1)

        EndPoint.z_index=30
        Startpoint.z_index=29
        self.play(Circ_main.animate.set_fill(opacity=0),Rope.animate.set_stroke(opacity=0.5))
        self.play(Create(VGroup(radius_arr,baseline,tangent_arr,phi_angle)))
        self.play(Write(phi_text))

        self.wait()

        framebox1 = SurroundingRectangle(invo_text[2], buff=.1)
        framebox2 = SurroundingRectangle(invo_text[4], buff=.1)
        self.play(
            Create(framebox1),
            radius_arr.animate.set_color(YELLOW)
        )
        self.wait()
        self.play(
            ReplacementTransform(framebox1, framebox2),
            radius_arr.animate.set_color(WHITE),
            tangent_arr.animate.set_color(YELLOW)
        )
        self.wait()
        self.play(
            tangent_arr.animate.set_color(WHITE),
            Uncreate(framebox2)
        )
        self.wait()

        self.play(Unwrite(invo_text), Unwrite(phi_text),
                  Uncreate(baseline),Uncreate(radius_arr),Uncreate(tangent_arr),
                  Uncreate(phi_angle))

        self.play(Circ_main.animate.set_fill(opacity=1), Rope.animate.set_stroke(opacity=1))

        self.play(Restore(self.camera.frame))



        self.wait(1)
        self.play(rot_inv_a.animate.set_value(0),
                  inv_a.animate.set_value(0), run_time=2)
        self.wait(1)
        self.play(rot_val.animate.set_value(PI/4))
        self.play(rot_val.animate.set_value(-PI+PI/4),
                  inv_a.animate.set_value(PI),
                  rot_inv_a.animate.set_value(PI),
                  run_time=2)
        self.wait(1)
        self.play( rot_val.animate.set_value(0 + PI / 4),
                   rot_inv_a.animate.set_value(0),
                   inv_a.animate.set_value(0),
                   run_time=2)

        self.wait(1)
        self.play(shifter.animate.set_value(-r*2),
                  rot_val.animate.set_value(PI / 3))

class Involute_2(MovingCameraScene):
    def construct(self):

        r=1
        inv_a_max = 3*PI/2
        inv_a = ValueTracker(0)
        rot_inv_a = ValueTracker(0)
        rot_val = ValueTracker(PI/3)
        shifter = ValueTracker(-2*r)

        r2=1.5
        # inv_a_max = 3*PI/2
        rot_inv_a2 = ValueTracker(0.0)
        rot_val2 = ValueTracker(PI/3)
        shifter2 = ValueTracker(r2*2)

        self.add(shifter,shifter2,inv_a,rot_inv_a,rot_inv_a2,rot_val,rot_val2)

        num_invo_points = 16

        Center1 = Circle(0.01, color=WHITE, fill_opacity=0, stroke_opacity=0)
        Center1.add_updater(lambda mob: mob.match_points(Circle(0.01).shift(RIGHT * shifter.get_value())))
        hole=Union(Circle(r/4,
                          fill_color=WHITE,
                          fill_opacity=1,
                          stroke_opacity=0),
                   Square(side_length=r/8,
                          fill_color=WHITE,
                          fill_opacity=1,
                          stroke_opacity=0
                          ).shift(RIGHT*r/4))
        Circ_ref = Cutout(Circle(r),hole,fill_color=WHITE,fill_opacity=1,stroke_opacity=0)


        def shift_rot_updater(mob):
            mob.shift(Center1.get_center())
            mob.rotate(rot_val.get_value(),about_point=Center1.get_center())

        Circ_main = Circ_ref.copy()
        Circ_main.add_updater(lambda mob: mob.match_points(Circ_ref.copy()))
        Circ_main.add_updater(shift_rot_updater)


        invo_curve = VMobject()
        t_range = np.linspace(0, inv_a.get_value(), num_invo_points)
        invo_curve.points = involute_point_gen(t_range,r)
        def invo_updater(mob):
            t_range = np.linspace(0,inv_a.get_value(),num_invo_points)
            mob.points = involute_point_gen(t_range,r)

        invo_curve.add_updater(invo_updater)
        invo_curve.add_updater(shift_rot_updater)

        EndPoint = Circle(0.05, color=RED, fill_color=RED, fill_opacity=1,
                          arc_center=involute_func(rot_inv_a.get_value(),r))
        EndPoint.add_updater(lambda mob: mob.move_to(involute_func(rot_inv_a.get_value(),r)))
        EndPoint.add_updater(shift_rot_updater)
        # EndPoint.add_updater(lambda mob: mob.move_to(invo_curve.point_from_proportion(1)))
        Startpoint = Circle(0.05, color=BLUE, fill_color=BLUE, fill_opacity=1)
        Startpoint.add_updater(lambda mob: mob.move_to(involute_func(0,r)))
        Startpoint.add_updater(shift_rot_updater)



        rope_arc = Arc(r, rot_inv_a.get_value(), inv_a_max - rot_inv_a.get_value(), stroke_opacity=0)
        TLine = Line(end=np.array([r * np.cos(rot_inv_a.get_value()), r * np.sin(rot_inv_a.get_value()), 0]),
                     start=involute_func(rot_inv_a.get_value(),r), stroke_opacity=0)
        Rope_base = VMobject(stroke_color=GOLD_E,stroke_opacity=1, stroke_width=10)
        Rope_base.points = np.append(rope_arc.points,TLine.points,axis=0)
        def Rope_base_updater(mob):
            arc = Arc(r, rot_inv_a.get_value(), inv_a_max - rot_inv_a.get_value())
            line = Line(end=np.array([r * np.cos(rot_inv_a.get_value()), r * np.sin(rot_inv_a.get_value()), 0]),
                         start=involute_func(rot_inv_a.get_value(), r))
            mob.points = np.append(line.points,arc.points,axis=0)
        Rope_base.add_updater(Rope_base_updater)
        Rope_base.add_updater(shift_rot_updater)

        Rope = DashedVMobject(Rope_base,num_dashes=20,dashed_ratio=0.9)
        for mob in Rope.submobjects:
            mob.updaters = []
        def Rope_upater(mob):
            Rope_base.update()
            dashmob =DashedVMobject(Rope_base, num_dashes=20, dashed_ratio=0.9)
            for i in range(len(mob.submobjects)):
                mob.submobjects[i].points = dashmob.submobjects[i].points
        Rope.add_updater(Rope_upater)
        Rope.update()


        Center2 = Circle(0.01, color=WHITE, fill_opacity=0, stroke_opacity=0)
        Center2.add_updater(lambda mob: mob.match_points(Circle(0.01).shift(RIGHT * shifter2.get_value())))
        Circ_ref2 = Cutout(Circle(r2), hole, fill_color=WHITE, fill_opacity=1, stroke_opacity=0)

        def shift_rot_updater2(mob):
            mob.shift(Center2.get_center())
            mob.rotate(rot_val2.get_value(),about_point=Center2.get_center())

        Circ_second = Circ_ref2.copy()
        Circ_second.add_updater(lambda mob: mob.match_points(Circ_ref2.copy()))
        Circ_second.add_updater(shift_rot_updater2)

        invo_curve2 = VMobject()
        t_range = np.linspace(0,inv_a.get_value(),num_invo_points)
        invo_curve2.points = involute_point_gen(t_range,r2)
        def invo_updater2(mob):
            t_range = np.linspace(0, inv_a.get_value(), num_invo_points)
            mob.points = involute_point_gen(t_range,r2)
        invo_curve2.add_updater(invo_updater2)
        invo_curve2.add_updater(shift_rot_updater2)

        Startpoint2 = Circle(0.05, color=BLUE, fill_color=BLUE, fill_opacity=1)
        Startpoint2.add_updater(lambda mob: mob.move_to(involute_func(0, r2)))
        Startpoint2.add_updater(shift_rot_updater2)


        Rope_base2 = VMobject(stroke_color=GOLD_E,stroke_opacity=1,stroke_width=10)
        Rope_base2.points = np.append(rope_arc.points,TLine.points,axis=0)
        def Rope_base_updater2(mob):
            arc = Arc(r2, rot_inv_a2.get_value(), inv_a_max - rot_inv_a2.get_value())
            line = Line(end=np.array([r2 * np.cos(rot_inv_a2.get_value()), r2 * np.sin(rot_inv_a2.get_value()), 0]),
                         start=involute_func(rot_inv_a2.get_value(), r2))
            mob.points = np.append(line.points,arc.points,axis=0)
        Rope_base2.add_updater(Rope_base_updater2)
        Rope_base2.add_updater(shift_rot_updater2)

        Rope2 = DashedVMobject(Rope_base2,num_dashes=20,dashed_ratio=0.9)
        for mob in Rope2.submobjects:
            mob.updaters = []
        def Rope_upater(mob):
            Rope_base2.update()
            dashmob =DashedVMobject(Rope_base2, num_dashes=20, dashed_ratio=0.9)
            for i in range(len(mob.submobjects)):
                mob.submobjects[i].points = dashmob.submobjects[i].points
        Rope2.add_updater(Rope_upater)
        Rope2.update()


        rel_dist = 2
        ref_angle1 = fsolve(lambda t: involute_height_func(t, r) - r * (rel_dist - 1), PI / 4)
        ref_angle2 = fsolve(lambda t: involute_height_func(t, r2) - r2 * (rel_dist - 1), PI / 4)

        # add base
        self.add(Center1,Circ_main, invo_curve, Startpoint, Rope, EndPoint)



        # self.play(rot_val.animate.set_value(PI/3),
        #           rot_val2.animate.set_value(PI/3),
        #           # run_time=2)
        self.play(rot_inv_a.animate.set_value(ref_angle1),
                  rot_inv_a2.animate.set_value(ref_angle1),
                  rot_val.animate.set_value(-ref_angle2 + PI / 3),
                  rot_val2.animate.set_value(-PI - (ref_angle2 - PI / 3)),
                  run_time=2
                  )

        self.add(Center2)
        # self.play()
        EndPoint.z_index = 30
        Startpoint2.z_index = 25
        self.play(DrawBorderThenFill(Circ_second),Create(Rope2),Create(Startpoint2))
        self.wait()
        # self.play(Create(rope_arc2))

        # self.play(Create(invo_curve2))

        ofs = 1.5
        self.play(rot_inv_a.animate.set_value(ref_angle1+ofs),
                  rot_val.animate.set_value(-ref_angle1 + PI / 3 - ofs),
                  rot_inv_a2.animate.set_value((ref_angle2-ofs*r/r2)),
                  rot_val2.animate.set_value(-PI - ((ref_angle2 - PI / 3)-ofs*r/r2)),
                  run_time=2
                  )
        ofs = -1.5
        self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                  rot_val.animate.set_value(-ref_angle1 + PI / 3 - ofs),
                  rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                  rot_val2.animate.set_value(-PI - ((ref_angle2 - PI / 3) - ofs * r / r2)),
                  run_time=2
                  )
        ofs = 0
        self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                  rot_val.animate.set_value(-ref_angle1 + PI / 3 - ofs),
                  rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                  rot_val2.animate.set_value(-PI - ((ref_angle2 - PI / 3) - ofs * r / r2)),
                  run_time=2
                  )

        self.wait()

        self.add(invo_curve2)
        self.play(inv_a.animate.set_value(2.5))
        for i in range(2):
            self.wait()
            ofs = 0.7
            self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                      rot_val.animate.set_value(-ref_angle1 + PI / 3 - ofs),
                      rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                      rot_val2.animate.set_value(-PI - ((ref_angle2 - PI / 3) - ofs * r / r2)),
                      run_time=2
                      )
            ofs = -0.7
            self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                      rot_val.animate.set_value(-ref_angle1 + PI / 3 - ofs),
                      rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                      rot_val2.animate.set_value(-PI - ((ref_angle2 - PI / 3) - ofs * r / r2)),
                      run_time=2
                      )
            ofs = 0
            self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                      rot_val.animate.set_value(-ref_angle1 + PI / 3 - ofs),
                      rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                      rot_val2.animate.set_value(-PI - ((ref_angle2 - PI / 3) - ofs * r / r2)),
                      run_time=2
                      )

        # zoom in
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.33))

        self.wait()


        self.play(EndPoint.animate.set_opacity(0))
        # wiggle
        ofs = 0.3
        self.play(rot_inv_a.animate.set_value(ref_angle1+ofs),
                  rot_inv_a2.animate.set_value(ref_angle2+ofs),
                  rate_func=rate_functions.wiggle,
                  run_time=2
                  )
        #
        normline = Line(start=EndPoint.get_center() - (Rope_base.points[1, :] - Rope_base.points[0, :]) / 2,
                        end=EndPoint.get_center() + (Rope_base.points[1, :] - Rope_base.points[0, :]) / 2,
                        stroke_opacity=1,
                        stroke_color=WHITE)
        tanline = Line(
            start=EndPoint.get_center() - rotate_vector(Rope_base.points[1, :] - Rope_base.points[0, :], -PI / 2) / 2,
            end=EndPoint.get_center() + rotate_vector(Rope_base.points[1, :] - Rope_base.points[0, :], -PI / 2) / 2,
            stroke_opacity=1,
            stroke_color=WHITE)
        rangle = Angle(line1=normline,line2=tanline,quadrant=(1,1),other_angle=True,color=WHITE, dot=True)

        rangle_grp = VGroup(rangle,tanline,normline)
        rangle_grp.add_updater(lambda mob: mob.move_to(EndPoint))

        self.wait()
        self.play(Create(rangle_grp))
        ofs = 0.3
        self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                  rot_val.animate.set_value(-ref_angle1 + PI / 3 - ofs),
                  rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                  rot_val2.animate.set_value(-PI - ((ref_angle2 - PI / 3) - ofs * r / r2)),
                  run_time=2
                  )

        self.wait()
        ofs = -0.3
        self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                  rot_val.animate.set_value(-ref_angle1 + PI / 3 - ofs),
                  rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                  rot_val2.animate.set_value(-PI - ((ref_angle2 - PI / 3) - ofs * r / r2)),
                  run_time=2
                  )
        self.wait()
        ofs = 0
        self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                  rot_val.animate.set_value(-ref_angle1 + PI / 3 - ofs),
                  rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                  rot_val2.animate.set_value(-PI - ((ref_angle2 - PI / 3) - ofs * r / r2)),
                  run_time=2
                  )
        self.wait()

        self.play(Uncreate(rangle_grp))

        def inv_angle_shift_updater(mob):
            dist = (shifter2.get_value()-shifter.get_value())*r/(r+r2)
            loc_ref_angle = fsolve(lambda t: involute_height_func(t, r) - (dist-r), PI / 4)
            loc_rot_angle = np.arccos(r/dist)
            mob.set_value(loc_ref_angle)

        def rot_angle_shift_updater(mob):
            dist = (shifter2.get_value()-shifter.get_value())*r/(r+r2)
            loc_ref_angle = fsolve(lambda t: involute_height_func(t, r) - (dist-r), PI / 4)
            loc_rot_angle = np.arccos(r/dist)
            mob.set_value(-loc_ref_angle+loc_rot_angle)

        def inv_angle_shift_updater2(mob):
            dist = (shifter2.get_value()-shifter.get_value())*r2/(r+r2)
            loc_ref_angle = fsolve(lambda t: involute_height_func(t, r2) - (dist-r2), PI / 4)
            loc_rot_angle = np.arccos(r2/dist)
            mob.set_value(loc_ref_angle)


        def rot_angle_shift_updater2(mob):
            dist = (shifter2.get_value()-shifter.get_value())*r2/(r+r2)
            loc_ref_angle = fsolve(lambda t: involute_height_func(t, r2) - (dist-r2), PI / 4)
            loc_rot_angle = np.arccos(r2/dist)
            mob.set_value(-PI-(+loc_ref_angle-loc_rot_angle))

        rot_inv_a.add_updater(inv_angle_shift_updater)
        rot_inv_a2.add_updater(inv_angle_shift_updater2)
        rot_val.add_updater(rot_angle_shift_updater)
        rot_val2.add_updater(rot_angle_shift_updater2)

        self.wait(1)

        ref_angle2 = fsolve(lambda t: involute_height_func(t, r) - r * (1.35 - 1), PI / 4)
        rot_angle = np.arccos(1 / 1.35)
        ofs = 0

        self.play(Restore(self.camera.frame))
        self.play(
                  shifter.animate.set_value(-1.4*r),
                  shifter2.animate.set_value(1.4 * r2),
                  run_time=2
                  )


        self.play(
            shifter.animate.set_value(-2.35 * r),
            shifter2.animate.set_value(2.35 * r2),
            run_time=2
        )

        self.wait()

        self.play(
            shifter.animate.set_value(-1.7 * r),
            shifter2.animate.set_value(1.7 * r2),
            run_time=2
        )

        self.wait()

        self.play(
            shifter.animate.set_value(-2.35 * r),
            shifter2.animate.set_value(2.35 * r2),
            run_time=2
        )

        rot_inv_a.remove_updater(inv_angle_shift_updater)
        rot_inv_a2.remove_updater(inv_angle_shift_updater2)
        rot_val.remove_updater(rot_angle_shift_updater)
        rot_val2.remove_updater(rot_angle_shift_updater2)

        rel_dist = (shifter2.get_value() - shifter.get_value()) * r / (r + r2)
        rel_dist2 = (shifter2.get_value()-shifter.get_value())*r2/(r+r2)
        ref_angle1 = fsolve(lambda t: involute_height_func(t, r) - (rel_dist-r), PI / 4)
        ref_angle2 = fsolve(lambda t: involute_height_func(t, r2) - (rel_dist2-r2), PI / 4)
        loc_rot_angle1 = np.arccos(r / rel_dist)
        loc_rot_angle2 = np.arccos(r2 / rel_dist2)

        ofs = 0.3
        self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                  rot_val.animate.set_value(-ref_angle1 + loc_rot_angle1 - ofs),
                  rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                  rot_val2.animate.set_value(-PI - ((ref_angle2 - loc_rot_angle2) - ofs * r / r2)),
                  run_time=2
                  )
        self.wait()
        ofs = -0.3
        self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                  rot_val.animate.set_value(-ref_angle1 + loc_rot_angle1 - ofs),
                  rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                  rot_val2.animate.set_value(-PI - ((ref_angle2 - loc_rot_angle2) - ofs * r / r2)),
                  run_time=2
                  )
        self.wait()
        ofs = 0
        self.play(rot_inv_a.animate.set_value(ref_angle1 + ofs),
                  rot_val.animate.set_value(-ref_angle1 + loc_rot_angle1 - ofs),
                  rot_inv_a2.animate.set_value((ref_angle2 - ofs * r / r2)),
                  rot_val2.animate.set_value(-PI - ((ref_angle2 - loc_rot_angle2) - ofs * r / r2)),
                  run_time=2
                  )
        self.wait()







class equation_test(Scene):
    def construct(self):
        # text = MathTex(
        #     "\\frac{d}{dx}f(x)g(x)=", "f(x)\\frac{d}{dx}g(x)", "+",
        #     "g(x)\\frac{d}{dx}f(x)"
        # )
        # text = MathTex(r'&x(t)\\&y(t)', '=',
        #                r'&r cos(t) \\ &r sin(t)', '+',
        #                r'&rt sin(t) \\ &-rt cos(t)')
        # text = MathTex(r' &x(t) \\ y(t)& ')
        text2 = MathTex(r'\begin{bmatrix}x(t)\\y(t)\end{bmatrix}', '=',
                        r'\begin{bmatrix}r cos(t) \\ r sin(t)\end{bmatrix}', '+',
                        r'\begin{bmatrix}rt sin(t) \\ -rt cos(t)\end{bmatrix}')
        self.play(Write(text2))
        # self.play(Write(text2))


# with tempconfig({"quality": "medium_quality", "disable_caching": True, "save_last_frame":True}):
#     scene = Involute_2()
#     scene.render()