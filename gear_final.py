from manim import *
from manim.mobject.geometry.tips import *
from manim_gearbox import *
from scipy.optimize import fsolve

class gear_sum(Scene):
    def construct(self):
        m=1
        ofs = ValueTracker(0)
        Nt = ValueTracker(25)
        gear_1 = Gear(40,module=m, nppc=10, stroke_opacity=0,fill_color=BLUE_B,fill_opacity=1)
        gear_2 = Gear(int(Nt.get_value()//1),module=m, nppc=10,stroke_opacity=0,fill_color=BLUE_C,fill_opacity=1)
        def gear_updater(mob: Gear):
            newgear = Gear(int(Nt.get_value()//1),module=m, nppc=10,stroke_opacity=0,fill_color=BLUE_C,fill_opacity=1)
            mob.become(newgear)
            mob.z=newgear.z
            mob.rp = newgear.rp
            mob.rb = newgear.rb
            mob.ra = newgear.ra
            mob.rf = newgear.rf
            mob.angle_ofs = newgear.angle_ofs
            mob.pitch = newgear.pitch
            mob.pitch_angle = newgear.pitch_angle
            mob.h=newgear.h
            mob.h_a = newgear.h_a
            mob.h_f = newgear.h_f
            mob.X=newgear.X
            mob.shift(UP*mob.rp)
            mob.mesh_to(gear_1,offset=ofs.get_value())

        gear_1.shift(gear_1.rp*DOWN)
        gear_2.shift(gear_2.rp*UP)
        gear_2.mesh_to(gear_1)
        gear_2.add_updater(gear_updater)
        self.add(gear_1,gear_2)

        self.play(Rotate(gear_1,gear_1.pitch_angle*2),run_time=4)
        self.wait()
        self.play(Nt.animate.set_value(12),run_time=5,rate_func=smooth)
        self.wait()
        self.play(Rotate(gear_1, gear_1.pitch_angle * 2), run_time=4)
        self.play(Nt.animate.set_value(60), run_time=5, rate_func=smooth)
        self.wait()
        self.play(Rotate(gear_1, gear_1.pitch_angle * 2), run_time=4)
        self.wait()
        self.play(ofs.animate.set_value(0.5))
        self.wait()
        self.play(Rotate(gear_1, gear_1.pitch_angle * 2), run_time=4)
        # self.wait()