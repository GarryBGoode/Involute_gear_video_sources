from manim import *
from manim.mobject.geometry.tips import *
from manim_gearbox import *
from scipy.optimize import fsolve

class Potato(VMobject):
    def __init__(self,**kwargs):
        self.r = 1
        self.rnd_dev = 0.2
        self.point_target_num = 5
        super().__init__(**kwargs)

    def generate_points(self):
        phi = 0
        ret = np.empty((0, 3))
        while phi<TAU:
            rad = self.r*(1+np.random.normal(0,self.rnd_dev))
            point = np.array([np.cos(phi)*rad,np.sin(phi)*rad,0])
            point = np.reshape(point, (1, 3))
            phi = phi + (TAU/self.point_target_num * (1+np.random.uniform(low=-self.rnd_dev,high=self.rnd_dev)))
            ret = np.concatenate((ret,point),0)
        self.set_points_as_corners(ret)
        #closing the shape
        self.add_line_to(ret[0].copy())
        self.make_smooth()


class Gear_construct(MovingCameraScene):
    def construct(self):
        gear1 = Gear(40,module=0.8,h_f=1.05,h_a=1, stroke_width=2,nppc=10)
        # gear1.rotate(gear1.pitch_angle/4)
        Pitch_circle_base = Circle(radius=gear1.rp,arc_center=gear1.get_center(),stroke_width=2,
                              num_components=20)
        Pitch_circle = DashedVMobject(Pitch_circle_base,num_dashes=40*7)
        Base_circle =  Circle(radius=gear1.rb,arc_center=gear1.get_center(),stroke_width=2,
                              num_components=20, color=YELLOW)
        Dedendum_circle = Circle(radius=gear1.rf,arc_center=gear1.get_center(),stroke_width=2,
                                 num_components=20)
        Addendum_circle = Circle(radius=gear1.ra,arc_center=gear1.get_center(),stroke_width=2,
                                 num_components=20)


        tooth_involute = VMobject(stroke_opacity=1,stroke_color=ORANGE,stroke_width=3)
        tooth_involute.points = involute_point_gen(np.linspace(0,0.7,10), gear1.rb)
        tooth_involute.rotate(-gear1.angle_ofs-gear1.pitch_angle/4+gear1.pitch_angle*gear1.z/4,about_point=ORIGIN)
        tooth_involute.shift(DOWN*gear1.rp)



        gear2  = gear1.copy()
        grp1 = VGroup(Pitch_circle,Base_circle,Dedendum_circle,Addendum_circle,gear1)
        grp2 = VGroup(gear2,Pitch_circle.copy(),Base_circle.copy())
        grp2.shift(UP*gear1.rp)
        grp2.rotate(gear1.pitch_angle/2)
        grp1.shift(DOWN*gear1.rp)

        invo_grp_1 = VGroup()
        invo_grp_1.add(tooth_involute.rotate(-gear1.pitch_angle,about_point=gear1.get_center()))
        invo_grp_1.add(tooth_involute.copy().rotate(gear1.pitch_angle, about_point=gear1.get_center()))
        invo_grp_1.add(tooth_involute.copy().rotate(2*gear1.pitch_angle, about_point=gear1.get_center()))

        invo_grp_2 = invo_grp_1.copy().rotate(PI, axis=UP,about_point=gear1.get_center())

        loa_start = gear1.get_center() + rotate_vector(gear1.rb*UP,gear1.alpha*DEGREES)
        loa_end = gear2.get_center() + rotate_vector(gear2.rb*DOWN,gear1.alpha*DEGREES)
        loa_start[2]=0.0
        loa_end[2] = 0.0
        LOA = Line(start = loa_start,
                   end =loa_end,
                   color=TEAL)

        # self.add(grp1)

        self.play(FadeIn(gear1))
        self.wait()
        self.play(FadeIn(Base_circle))
        self.wait()
        self.play(Create(invo_grp_1), run_time=3)
        self.play(Create(invo_grp_2), run_time=3)
        self.wait()
        self.play(FadeOut(invo_grp_1),FadeOut(invo_grp_2))


        self.play(FadeIn(Addendum_circle),FadeIn(Dedendum_circle))
        self.wait()
        self.play(FadeIn(Pitch_circle))
        self.wait()
        self.play(FadeOut(Addendum_circle), FadeOut(Dedendum_circle))
        self.play(FadeIn(grp2))
        self.wait()
        self.play(gear1.animate.set_stroke(opacity=0.5),gear2.animate.set_stroke(opacity=0.5))
        self.play(Create(LOA))
        Line_tan = Line(start=LEFT*5,end=RIGHT*5,color=TEAL)
        Alpha_angle = Angle(LOA,Line_tan,other_angle=True,radius=2.55,quadrant=(-1,-1),color=TEAL)
        self.wait()
        self.play(Create(Line_tan))
        self.play(FadeIn(Alpha_angle))
        self.wait()

        self.play(FadeOut(LOA),FadeOut(Line_tan),FadeOut(Alpha_angle))

        pitch_arc = Arc(radius=gear1.rp,
                        arc_center=gear1.get_center(),
                        start_angle=PI/2-gear1.pitch_angle/4,
                        angle=gear1.pitch_angle,
                        color=TEAL
                        )

        self.play(Create(pitch_arc))
        self.wait()
        #
        # self.play(FadeOut(grp2))
        #
        # equ1 = MathTex(r'module = \frac{pitch}{\pi}')
        # equ1.shift(UP*2)
        # self.add(equ1)



class Gear_module(MovingCameraScene):
    def construct(self):
        m = 0.2
        gear1 = Gear(10, module=m,fill_color=BLUE_A,fill_opacity=1,stroke_opacity=0,nppc=10)
        gear2 = Gear(20, module=m,fill_color=BLUE_B,fill_opacity=1,stroke_opacity=0,nppc=10)
        gear3 = Gear(32, module=m,fill_color=BLUE_C,fill_opacity=1,stroke_opacity=0,nppc=10)
        gear1.shift(LEFT*4)
        # gear2.shift(LEFT)
        gear3.shift(RIGHT*4)
        #
        gear1.mesh_to(gear2)
        gear3.mesh_to(gear2)

        rack12 = Rack(10,module=m,h_a=1,h_f=1,
                      stroke_color=RED,stroke_width=2)
        # remove last 2 curves
        rack12.points = rack12.points[:-12,:]
        rack12.rotate(PI, about_point=rack12.get_center())
        rack12.shift(gear1.get_center() + RIGHT * gear1.rp)

        rack23 = rack12.copy().shift(gear2.rp*2*RIGHT)
        rack12.rotate(PI, about_point=rack12.get_center())

        anim_base = ValueTracker(0)

        def gear_update_plus(mob:Gear):
            mob.rotate(anim_base.get_value() * mob.pitch_angle - mob.get_angle())

        def gear_update_minus(mob:Gear):
            mob.rotate(-anim_base.get_value() * mob.pitch_angle - mob.get_angle() + mob.pitch_angle/2)

        def rack_update_plus(mob: Rack):
            mob.shift(UP * (anim_base.get_value() * mob.pitch - mob.get_center()[1]))

        def rack_update_minus(mob: Rack):
            mob.shift(UP * (-anim_base.get_value() * mob.pitch - mob.get_center()[1]))

        gear1.add_updater(gear_update_minus)
        gear2.add_updater(gear_update_plus)
        gear3.add_updater(gear_update_minus)

        rack12.add_updater(rack_update_minus)
        rack23.add_updater(rack_update_plus)

        gear0 = Gear(20,module=m, cutout_teeth_num=19,stroke_width=2).rotate(PI/2)
        self.camera.frame.save_state()
        gear01 = gear0.copy()
        self.play(Create(gear0))
        self.wait(0.5)
        self.play(self.camera.frame.animate.scale(gear0.m*4 / 9).move_to(UP*gear0.rp))
        self.wait(0.5)
        pitch_arc = Arc(start_angle=PI/2-gear0.pitch_angle/2,
                        angle=gear0.pitch_angle,
                        radius=gear0.rp,
                        color=RED,
                        stroke_width=1)
        pitch_arc.add_tip(tip_shape=ArrowTriangleFilledTip,tip_length=gear0.m/3.5)
        pitch_arc.add_tip(tip_shape=ArrowTriangleFilledTip, tip_length=gear0.m / 3.5,at_start=True)
        # Arrow

        Dimension_line_1 = Line(start=UP*gear0.rf*0.9, end=UP*gear0.ra*1.1,stroke_width=1, color=RED)
        Dimension_line_1.rotate(-gear0.pitch_angle/2,about_point=gear0.get_center())
        Dim_line_grp = VGroup(Dimension_line_1,Dimension_line_1.copy().rotate(gear0.pitch_angle,about_point=gear0.get_center()))

        self.play(gear0.animate.set_stroke(opacity=0.5, family=False))
        self.play(Create(Dim_line_grp),Create(pitch_arc))
        self.wait()
        pi_m = MathTex(r"\pi m",color=RED,stroke_width=0.1).scale(m)
        pitch_t = MathTex(r"p",color=RED,stroke_width=0.1).scale(m)
        pi_m.next_to(pitch_arc,UP,buff=m*0.1)
        pitch_t.next_to(pitch_arc, DOWN, buff=m * 0.1)

        self.play(Write(pi_m,stroke_width=0.05))
        self.play(Write(pitch_t, stroke_width=0.05))
        self.wait(1.5)
        self.play(Unwrite(pi_m,stroke_width=0.05),Unwrite(pitch_t,stroke_width=0.05))

        H_a_arrow = Arrow(start=UP*gear0.rp,end=UP*gear0.ra,stroke_width=1,color=RED)
        H_d_arrow = Arrow(start=UP*gear0.rp,end=UP*gear0.rf,stroke_width=1,color=RED)

        m1 = MathTex(r"1m",color=RED,stroke_width=0.1)
        m1.scale(m)
        m1.next_to(H_a_arrow,LEFT,buff=m*0.1)


        m12 = MathTex(r"1.2m",color=RED,stroke_width=0.1)
        m12.scale(m)
        m12.next_to(H_d_arrow,RIGHT,buff=m*0.1)


        self.play(Create(H_a_arrow))
        self.play(Write(m1,stroke_width=0.05))
        self.wait()
        self.play(Create(H_d_arrow))
        self.play(Write(m12,stroke_width=0.05))

        self.wait()

        self.play(Uncreate(H_d_arrow),
                  Uncreate(H_a_arrow),
                  Uncreate(pitch_arc),
                  Unwrite(m1,stroke_width=0.05),
                  Unwrite(m12,stroke_width=0.05))
        self.play(gear0.animate.set_stroke(opacity=1,family=False))


        self.play(self.camera.frame.animate.scale(0.7/(gear0.m*3 / 9)).move_to(DOWN*0.8))
        t=0
        tres = fsolve(lambda t: smooth(t) - (1) / 21, 0)
        t=tres[0]
        for i in range(18):
            gear0.match_points(Gear(20,module=m, cutout_teeth_num=19-i-1))
            gear0.rotate(-(20-i-1)/2*gear0.pitch_angle-PI/2)
            new_Dim_line = Dimension_line_1.copy().rotate((2+i)*gear0.pitch_angle, about_point=gear0.get_center())
            self.add(gear0)
            self.add(new_Dim_line)
            Dim_line_grp.add(new_Dim_line)
            tres = fsolve(lambda t: smooth(t)-(i+2)/21,t*0.9)
            dt = (tres[0]-t)*4
            dt = 2 / 18
            self.wait(dt*1)
            t = tres[0]
        gear0.match_points(Gear(20, module=m, cutout_teeth_num=0))

        gear0.rotate(PI / 2)
        self.add(gear0)
        self.wait()

        asd=1.5
        pitch_circle = DashedVMobject(Circle(radius=gear0.rp,stroke_width=1, fill_color=RED,stroke_color=RED),num_dashes=60)
        dp_dim_lines = VGroup(
            Line(start=gear0.get_center()+gear0.rp*(RIGHT+DOWN*asd),
                 end=gear0.get_center()+gear0.rp*(RIGHT),
                 stroke_width=3, fill_color=RED,stroke_color=RED),
            Line(start=gear0.get_center() + gear0.rp * (LEFT + DOWN * asd),
                 end=gear0.get_center() + gear0.rp * LEFT,
                 stroke_width=3, fill_color=RED,stroke_color=RED),
            Line(end=gear0.get_center()+gear0.rp*(RIGHT+DOWN*asd),
                 start=gear0.get_center() + gear0.rp * (LEFT + DOWN * asd),
                 stroke_width=3, fill_color=RED,stroke_color=RED
                 ).add_tip(tip_shape=ArrowTriangleFilledTip, tip_length=gear0.m).add_tip(
                tip_shape=ArrowTriangleFilledTip, tip_length=gear0.m,at_start=True)
        )
        self.play(Create(pitch_circle))
        self.play(Create(dp_dim_lines))
        self.wait()
        dia_tex = MathTex(r"\pi d_p = z p ",color=RED)
        dia_tex2 = MathTex(r"\pi d_p = z \pi m ")
        dia_tex3 = MathTex(r"d_p=z m")
        tex_grp = VGroup(dia_tex,dia_tex2,dia_tex3)
        tex_grp.next_to(dp_dim_lines[2],UP,buff=0).scale(0.8).set_color(RED).set_stroke(width=0.5)

        self.play(Write(dia_tex,stroke_width=1))
        self.wait()
        self.play(dia_tex.animate.become(dia_tex2))
        self.wait()
        self.play(dia_tex.animate.become(dia_tex3))
        self.wait()
        self.play(Unwrite(dia_tex,stroke_width=1))
        self.play(Uncreate(Dim_line_grp),Uncreate(dp_dim_lines),Uncreate(pitch_circle))
        # self.remove(Dimension_line_1)
        self.wait()
        self.play(self.camera.frame.animate.scale(9/self.camera.frame.height).
                  shift(-1*self.camera.frame.get_center()+RIGHT*2))
        # self.camera.frame.restore()


        # self.add(gear0)
        #
        self.play(DrawBorderThenFill(VGroup(gear1,gear2,gear3)))
        self.play(FadeOut(gear0))
        asd=1.5
        dp_dim_lines = VGroup(
            Line(start=gear1.get_center() + gear0.rp * (DOWN * asd),
                 end=gear1.get_center(),
                 stroke_width=3, fill_color=RED, stroke_color=RED),
            Line(start=gear2.get_center() + gear0.rp * (DOWN * asd),
                 end=gear2.get_center(),
                 stroke_width=3, fill_color=RED, stroke_color=RED),
            Line(end=gear1.get_center() + gear0.rp * (DOWN * asd),
                 start=gear2.get_center() + gear0.rp * (DOWN * asd),
                 stroke_width=3, fill_color=RED, stroke_color=RED
                 ).add_tip(tip_shape=ArrowTriangleFilledTip, tip_length=gear0.m).add_tip(
                tip_shape=ArrowTriangleFilledTip, tip_length=gear0.m, at_start=True)
        )

        dia_tex4 = MathTex(r"d_{12} = m \frac{z_1 + z_2}{2} ", color=RED).next_to(dp_dim_lines[2],UP,buff=0).scale(0.8)
        self.play(Create(dp_dim_lines))
        self.play(Write(dia_tex4))
        self.wait()
        self.play(Uncreate(dp_dim_lines),Unwrite(dia_tex4))

        # self.add(gear1,gear2,gear3)
        self.play(anim_base.animate.set_value(2),run_time=4)
        self.play(anim_base.animate.set_value(0), run_time=4)
        self.play(Create(rack12),Create(rack23))
        # self.add(rack12,rack23)
        self.play(anim_base.animate.set_value(2), run_time=4)
        self.play(anim_base.animate.set_value(0), run_time=4)
        self.play(self.camera.frame.animate.scale((gear2.m * 4 / 9)).move_to(gear2.get_center()+gear2.rp*RIGHT))
        self.play(rack23.animate.set_stroke(width=1,opacity=0.7,family=False))
        self.play(anim_base.animate.set_value(2), run_time=15)



class Gear_manuf(Scene):
    def construct(self):
        turn_mod = ValueTracker(0)
        gear1 = Gear(12,module=0.3,h_a=1,h_f=1.2,stroke_opacity=0)
        circ1 = Circle(gear1.ra,num_components=20,fill_color=WHITE,fill_opacity=1,stroke_opacity=0)
        rack1 = Rack(14,module=0.3,h_a=1.2,h_f=1,stroke_opacity=0,fill_opacity=1,fill_color=RED)
        rack1.rotate(PI/2, about_point=ORIGIN)
        rack1.shift(DOWN*gear1.rp)
        rack_ofs = 10*rack1.pitch
        rack1.shift(rack_ofs*LEFT)
        def rack_updater(mob:Rack):
            mob.shift(-mob.submobjects[0].points[0] * RIGHT + rack_ofs * LEFT + turn_mod.get_value() * mob.pitch * RIGHT)
        def gear_updater(mob:Gear):
            mob.rotate(mob.pitch_angle*turn_mod.get_value()-mob.get_angle())
        gear1.add_updater(gear_updater)
        rack1.add_updater(rack_updater)

        def circ_updater(mob:VMobject):
            mob.rotate(gear1.pitch_angle * turn_mod.get_value() - gear1.get_angle())
            mob.match_points(Difference(mob,rack1))

        def my_rate_func(t:float)->float:
            point_x = np.array([0, 0.2, 0.8, 1])
            point_y = np.array([0,0,1,1])
            bzx = bezier(point_x)
            bzy = bezier(point_y)
            alpha = fsolve(lambda k: bzx(k)-t,0.5)
            ret = bzy(alpha)
            return ret[0]



        circ1.add_updater(circ_updater)
        self.add(circ1,rack1,gear1)
        self.play(turn_mod.animate.set_value(14+5),run_time = 30, rate_func=my_rate_func)
#
#
# with tempconfig({"quality": "medium_quality", "disable_caching": True, "save_last_frame":True}):
#     scene = Gear_module()
#     scene.render()