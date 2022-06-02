import math
import sys

from tqdm import tqdm
from libraries import engine_simulations
import numpy
class ScotchYoke:
    def radius_sweep(self, rs, control_signal, pstn_angle = 90):
        # control_signal(r) -> ctrl(deg)
        engine = []
        angled = False
        v, a, x, w = [], [], [], []
        if pstn_angle == 90:
            engine = engine_simulations.ScotchYoke
        else:
            angled = True
            engine = engine_simulations.AngledScotchYoke
        # generate objects
        engines = [engine(r, control_signal(r/1000)) if not angled else engine(r, control_signal(r/1000), pstn_angle) for r in rs]
        with tqdm(total = len(rs), file = sys.stdout) as pbar:
            pbar.set_description_str("Radius sweep job")
            for engine in engines:
                engine.RETURN_VALUE = lambda: (engine.velocity, engine.acceleration, engine.dislocation, engine.rotation_acceleration(engine.angle))
                _v, _a, _x, _w= zip(*[engine.simulate(deg)() for deg in numpy.arange(0.0, 360.0, 0.01)])
                _ = [max(val) for val in [_v, _a, _x, _w] ]
                _v, _a, _x, _w = _
                v.append(_v)
                a.append(_a)
                x.append(_x)
                w.append(_w)
                pbar.update(1)
        return v, a, x, w, rs
    def piston_angle_sweep(self, angles, r, control_signal):
        # control_signal(angle) -> control_signal(deg)
        # remember about dividing r/1000! in control_signal
        # 150 - 30 MIGHT be sensible
        engine = engine_simulations.AngledScotchYoke
        v, a, x, w = [], [], [], []
        engines = [engine(r, control_signal(math.radians(ang)), ang) for ang in angles]
        with tqdm(total = len(angles), file = sys.stdout) as pbar:
            pbar.set_description_str("Angle sweep job")
            for engine in engines:
                engine.RETURN_VALUE = lambda: (engine.velocity, engine.acceleration, engine.dislocation, engine.rotation_acceleration(engine.angle))
                _v, _a, _x, _w = zip(*[engine.simulate(deg)() for deg in numpy.arange(0.0, 360.0, 0.01)])
                _ = [max(val) for val in [_v, _a, _x, _w]]
                _v, _a, _x, _w = _
                v.append(_v)
                a.append(_a)
                x.append(_x)
                w.append(_w)
                pbar.update(1)
            return v, a, x, w, angles
    def degree_sweep(self, ds, control_signal, radius, pstn_angle = 90):
        angled = pstn_angle!=90
        engine = engine_simulations.AngledScotchYoke if angled else engine_simulations.ScotchYoke
        engine = engine(radius, control_signal, pstn_angle) if angled else engine(radius, control_signal)
        engine.RETURN_VALUE = lambda: (
        engine.velocity, engine.acceleration, engine.dislocation, engine.rotation_acceleration(math.radians(engine.angle)))
        v,a,x,w = zip(*[engine.simulate(deg)() for deg in ds])
        return v,a,x,w,ds

