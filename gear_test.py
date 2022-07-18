import bezier as bz
from manim import *
import numpy as np
from manim_gearbox import *
# from Gear_mobject import *
from scipy.optimize import fsolve
import bezier as bz
from collections.abc import Iterable


MY_BLUE: str ="#001439"
# WHITE: str = "#FFFFFF"

z = 22;

m = 0.2
pitch = m*PI
rp = m*z/2
# magic number for standard gears
h = 2.25 * m

alpha = 25
rb = rp * np.cos(alpha * DEGREES)
#

class gear_test(MovingCameraScene):
    def construct(self):
        gear1=Gear(20,stroke_color=WHITE,stroke_width=1.5, stroke_opacity=0, fill_color=WHITE,fill_opacity=0.5)
        gear2=Gear(40,
                   stroke_color=RED,stroke_width=1.5,stroke_opacity=0,
                   inner_teeth=True,fill_color=RED,fill_opacity=1,h_a=0.7)
        # gear1.rotate(-gear1.rp_tooth_ofs)
        # gear2.rotate(-gear2.rp_tooth_ofs)
        circ = Circle(gear2.ra+0.3)

        gear3 = Difference(circ,gear2)
        gear2.shift((gear2.rp + gear1.rp) * RIGHT)
        gear3.shift((-gear2.rp+gear1.rp*0)*RIGHT)
        gear3.set_fill(color=RED,opacity=1)
        gear3.set_stroke(opacity=0)
        gear1.shift(-gear1.rp*RIGHT)
        # circ2 = Circle(2)
        # cyclo = ParametricFunction(lambda t: epi_cycloid_func(2,0.5,t), t_range=[0,TAU])
        # cyclo2 = ParametricFunction(lambda t: hypo_cycloid_func(2, 0.5, t), t_range=[0, TAU])

        self.add(gear1)
        # self.add(gear2)
        # self.add(gear3)
        self.camera.frame.set(width=3)
        # self.play(Rotate(gear1, PI / 10, rate_func=linear), Rotate(gear2, -PI / 10 / 3, rate_func=linear), run_time=4)
        self.play(Rotate(gear1, PI / 10, rate_func=linear), Rotate(gear3, PI / 10 / 2, rate_func=linear), run_time=4)

        asd=SVGMobject
#         cgear1 = Gear_cycloid(20,0.2*20/2,0.25,0.2,h_a=1,h_f=1,stroke_width=0.25,stroke_opacity=0,fill_color=WHITE,fill_opacity=0.5)
#         cgear2 = Gear_cycloid(40,0.2*40/2,0.2,0.25,h_a=1,h_f=1,stroke_width=0.25,stroke_opacity=0,fill_color=RED,fill_opacity=0.5)
#         cgear1.shift(cgear1.rp*LEFT)
#         cgear2.shift(cgear2.rp*RIGHT)
#         # circ3 = Circle(2)
#         # circ4 = Circle(1.8)
#         # circ5 = Circle(2.2)
#         # self.add(circ2,cyclo,cyclo2)
#         self.add(cgear1,cgear2)
#         self.play(Rotate(cgear1, PI / 10, rate_func=linear), Rotate(cgear2, -PI / 10 / 2, rate_func=linear), run_time=4)



class planet_test(MovingCameraScene):
    def construct(self):
        sungear=Gear(40,stroke_color=WHITE,stroke_width=1.5, stroke_opacity=0, fill_color=WHITE,fill_opacity=0.5)
        planetgear=Gear(20,
                   stroke_color=RED,stroke_width=1.5,stroke_opacity=0,
                   inner_teeth=False,fill_color=RED,fill_opacity=1)
        outgear = Gear(80,inner_teeth=True, h_a=0.7)
        ringgear = Difference(Circle(radius=outgear.rp+0.5),outgear,
                              stroke_opacity=0,
                              fill_color=BLUE_A, fill_opacity=1
                              )

        sungear.shift(LEFT*sungear.rp)
        planetgear.shift(RIGHT*planetgear.rp)
        planet_grp = VGroup()
        Center_Point = ORIGIN+(LEFT*sungear.rp)
        for i in range(6):
            planet_grp.add(planetgear.copy().rotate(
                about_point=Center_Point,
                angle= i*60*DEGREES
            ).rotate(angle=i*60*sungear.z/planetgear.z*DEGREES))
        ringgear.shift(LEFT*sungear.rp)


        Sun_rot = ValueTracker(0)
        Ring_rot = ValueTracker(0)
        Sun2 = sungear.copy()
        Ring2 = ringgear.copy()
        Sun2.add_updater(lambda mob: mob.match_points(sungear.copy().rotate(angle=Sun_rot.get_value())))
        Ring2.add_updater(lambda mob: mob.match_points(ringgear.copy().rotate(angle=Ring_rot.get_value())))
        planet2 = planet_grp.copy()
        def planet_updater(mob):
            omega1 = (-Sun_rot.get_value()*sungear.z + Ring_rot.get_value()*outgear.z) / planetgear.z / 2
            omega2 = (Sun_rot.get_value()*sungear.z + Ring_rot.get_value()*outgear.z) / 2 / (sungear.z+planetgear.z)
            for i in range(6):
                mob_loc = planet_grp[i].copy()
                mob_loc.rotate(angle=omega2,about_point=Center_Point)
                mob_loc.rotate(angle=(omega1-omega2))
                mob.submobjects[i].match_points(mob_loc)
        planet2.add_updater(planet_updater)
        # for mob in planet_grp:
        #     mob.add_updater(planet_updater)

        self.add(Sun2, Ring2, planet2)

        self.play(Sun_rot.animate.set_value(PI),run_time=10,rate_func=rate_functions.ease_in_out_cubic)
        # self.play((Sun_rot.animate.set_value(0)),run_time=2)

        self.play(Ring_rot.animate.set_value(-0.5*PI ), run_time=10,rate_func=rate_functions.ease_in_out_cubic)
        # self.wait(2)
        # self.play((Ring_rot.animate.set_value(0)), run_time=2)


class gear_base(Scene):
    def construct(self):

        gear1 = Gear(12,module=0.3,stroke_opacity=0,fill_opacity=1,fill_color=WHITE)
        gear1.rotate(-gear1.pitch/gear1.rp/4)
        center = Circle(0.3)
        gear2 = Difference(gear1,center,stroke_opacity=0,fill_opacity=1,fill_color=WHITE)
        grid1 = NumberPlane()

        gear3 = Gear(8,module=0.6,
                     stroke_opacity=0, fill_opacity=1, fill_color=WHITE,
                     h_f=0.75,h_a=1.25)
        gear3.rotate(gear3.pitch_angle/4)
        self.add(gear3)

class gear_base_roll(MovingCameraScene):
    def construct(self):
        ps=0.25
        m=0.35
        gear1 = Gear(12,module=0.3,stroke_opacity=0,fill_opacity=1,fill_color=WHITE,profile_shift=ps)
        gear0 = gear1.copy()
        # gear1.rotate(-gear1.pitch/gear1.rp/4)
        center = Circle(0.3)
        gear2 = Difference(gear1,center,stroke_opacity=0,fill_opacity=1,fill_color=WHITE)
        gear3 = gear2.copy()

        # point_x = np.array([0, 0.25, 0.5, 1])
        def my_rate_func(t:float)->float:
            point_x = np.array([0, 0.25, 0.25, 1])
            point_y = np.array([0,0,1,1])
            bzx = bezier(point_x)
            bzy = bezier(point_y)
            alpha = fsolve(lambda k: bzx(k)-t,0.5)
            ret = bzy(alpha)
            return ret[0]

        self.add(gear2)
        self.wait(1)
        self.add(gear3)
        self.play(gear2.animate.shift(LEFT*(gear1.rp + ps*m +0.7)),gear3.animate.shift(RIGHT*(gear1.rp + ps*m + 0.7)),
                  run_time=1)
        # self.wait(0.2)
        gear1.shift(LEFT*(gear1.rp + ps*m))
        gear0.mesh_to(gear1,offset=-0.055)
        dist = (gear0.get_center()-gear1.get_center())*(1-1e-3)
        self.play(Rotate(gear2,gear0.get_angle()/2), Rotate(gear3,gear0.get_angle()/2),run_time=1)
        self.play(gear2.animate.shift(LEFT * (-(gear1.rp + ps*m +0.7)+dist/2)),
                  gear3.animate.shift(RIGHT * (-(gear1.rp + ps*m +0.7)+dist/2)),
                  # gear3.animate.mesh_to(gear2),
                  rate_func=rate_functions.ease_out_bounce)
        self.wait(0.2)
        self.play(Rotate(gear2, 30 * gear1.pitch_angle), Rotate(gear3, -30 * gear1.pitch_angle), run_time=8,rate_func=my_rate_func)
        #back
        # self.play(Rotate(gear3, -4 * gear1.pitch_angle), Rotate(gear2, 4 * gear1.pitch_angle), run_time=4,rate_func=rate_functions.ease_in_out_back)
        self.play(self.camera.frame.animate.scale(0.3))

        self.play(Rotate(gear3, -3.25 * gear1.pitch_angle), Rotate(gear2, 3.25 * gear1.pitch_angle), run_time=20,
                  rate_func=my_rate_func)


# with tempconfig({"quality": "medium_quality", "disable_caching": True}):
#     scene = gear_base_roll()
#     scene.render()