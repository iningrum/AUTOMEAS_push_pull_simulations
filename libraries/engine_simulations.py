import math


class ScotchYoke:
    class Equations:
        def __init__(self, obj):
            self.self = obj
            self.radians = False

        def rad(self):
            obj = self.self
            deg = obj.angle
            return deg if self.radians else math.radians(deg)

        def velocity(self):
            obj = self.self
            r, w, sin = obj.radius, obj.rotation_acceleration, math.sin
            deg = self.rad()
            return r * w(deg) * sin(deg)

        def acceleration(self):
            obj = self.self
            r, cos = obj.radius, math.cos
            w = lambda x: math.pow(obj.rotation_acceleration(x), 2)
            deg = self.rad()
            return r * w(deg) * cos(deg)

        def dislocation(self):
            obj = self.self
            r, cos = obj.radius, math.cos
            deg = self.rad()
            return r * (1 - cos(deg))

    def __init__(self, radius, control_funct=lambda x: 0):
        self.EQ = self.Equations(self)
        self.radius = radius * 0.001  # m
        self.velocity = 0
        self.acceleration = 0  # /ms**2
        self.dislocation = 0  # mm
        self.angle = 0  # deg
        self.rotation_acceleration = control_funct
        self.RETURN_VALUE = None

    def simulate(self, angle=None):  # w is rotation acceleration
        if angle:
            self.angle = angle
        v = self.EQ.velocity()
        a = self.EQ.acceleration()
        x = self.EQ.dislocation()
        # assign values
        self.dislocation, self.velocity, self.acceleration = x * 1000, v, a
        return self.RETURN_VALUE

    def __str__(self):
        return f"Engine type is Scotch Yoke:\n" \
               f"\tradius = {self.radius} m\n" \
               f"\tangle = {self.angle} deg\n\n" \
               f"\tdislocation = {round(self.dislocation, 3)} mm\n" \
               f"\tvelocity = {round(self.velocity, 3)} m/s\n" \
               f"\tacceleration = {round(self.acceleration, 3)} m/s^2\n"


class AngledScotchYoke(ScotchYoke):
    class Equations:
        def __init__(self, obj):
            self.self = obj
            self.radians = False

        def rad(self):
            obj = self.self
            deg = obj.angle
            return deg if self.radians else math.radians(deg)

        def velocity(self):
            obj = self.self
            sin, cos, tan = math.sin, math.cos, math.tan
            r, w = obj.radius, obj.rotation_acceleration
            deg = self.rad()
            p_deg = math.radians(obj.piston_angle)
            return (r * w(deg)) * (sin(deg) + (cos(deg) / tan(p_deg)))

        def acceleration(self, v=None):
            if not v:
                v = self.velocity()
            obj = self.self
            sin, cos, tan = math.sin, math.cos, math.tan
            r = obj.radius
            deg = self.rad()
            p_deg = obj.piston_angle
            return v + r * p_deg * (sin(deg) + (cos(deg) / tan(math.radians(p_deg))))

        def dislocation(self):
            obj = self.self
            sin, cos, tan = math.sin, math.cos, math.tan
            r, p_deg = obj.radius, math.radians(obj.piston_angle)
            deg = self.rad()
            # calcualtion
            _A = 1 - cos(deg)
            _B = (r * sin(deg)) / tan(p_deg)
            return r * (_A + _B)

    def __init__(self, radius, control_function=lambda x: 0, angle=0):
        super().__init__(radius, control_function)
        self.EQ = self.Equations(self)
        self.piston_angle = angle

    def simulate(self, angle=None):  # w is rotation acceleration
        if angle:
            self.angle = angle
        pstn_angle = math.radians(self.piston_angle)
        r, v = self.radius, self.velocity
        a, x = self.acceleration, self.dislocation
        deg, w = math.radians(self.angle), self.rotation_acceleration
        # equations
        v = self.EQ.velocity()  # (r * w(deg)) * (math.sin(deg) + (math.cos(deg) / math.tan(pstn_angle)))
        a = self.EQ.acceleration(v)  # r * (w(deg) ** 2) * (math.cos(deg) - (math.sin(deg) / math.tan(pstn_angle))) + r * pstn_angle * (
        # math.sin(deg) + (math.cos(deg) / math.tan(pstn_angle)))
        x = self.EQ.dislocation() #r * (1 - math.cos(deg)) + (r * math.sin(deg)) / math.tan(pstn_angle)
        # assign values
        self.dislocation, self.velocity, self.acceleration = x * 1000, v, a
        return self.RETURN_VALUE

    def __str__(self):
        return f"{super().__str__()}\n\tangle = {self.piston_angle} [deg]\n"


class RackAndPinion:
    def __init__(self):
        pass

    def simulate(self):
        pass

    def __str__(self):
        return f"Engine type is Rack and Pinion:\n"


class DCMotor:
    def __init__(self):
        self.force = 0
        self.radius = 0
        self.angle = 0
        self.torque = 0

    def __str__(self):
        return f"Engine type is DC Motor\n"

class GearRatio:
    def r(self):
        self.ratio = self.output/self.input
        return self.r
    def t(self, T_in = None):
        if T_in:
            self.input_torque = T_in
        self.t = self.ratio*self.input_torque
        return self.output_torque
    def av(self, input_velocity):
        self.angular_velocity = input_velocity/self.r
        return self.angular_velocity
    def __init__(self, N_in, N_out, T_in = 0):
        """

        viable sizes:
            12, 14, 16, 18, 20, 24, 30, 48
        """
        self.input = N_in
        self.output = N_out
        self.input_torque = T_in
        self.ratio = self.r()
        self.output_torque = self.t()
        self.angular_velocity = 0
        self.RETURN_VALUE = lambda x: None
    def simulate(self, angular_velocity):
        self.r()
        self.t()
        self.av(angular_velocity)
        return self.RETURN_VALUE()
