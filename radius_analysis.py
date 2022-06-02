# by Kordian Czyżewski 4EIT2, WEEIA
"""
    Scotch Yoke - radius analysis
"""
import os
import math
import sys

import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy

from libraries import simulation_wrappers

"""
    The purpose of this simulation is to find maximum values of:
        velocity [m/s]
        acceleration [m/s^2]
        displacement [mm]
        required RPM [RPM] (1 rad/s = 9.5493 RPM)
    for free and controlled motion in Scotch Yoke mechanism depending
    on wheel radius and for angled variations of said mechanism.
    
    
"""


def main():
    DEFAULT_DATA_DIR = "Desktop scotch_yoke_analysis"
    plt.rcParams["figure.figsize"] = (10, 10)

    def hpath(string):
        string = f"{os.path.expanduser('~')} {string}"
        return os.sep.join(string.split())

    if not os.path.exists(hpath(DEFAULT_DATA_DIR)):
        os.makedirs(hpath(f"{DEFAULT_DATA_DIR} regular_yoke angle_sweep"))
        os.makedirs(hpath(f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep"))
        os.makedirs(hpath(f"{DEFAULT_DATA_DIR} regular_yoke radius_sweep"))
        os.makedirs(hpath(f"{DEFAULT_DATA_DIR} angled_yoke angle_sweep"))
        os.makedirs(hpath(f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep"))
        os.makedirs(hpath(f"{DEFAULT_DATA_DIR} angled_yoke radius_sweep"))

    def signal(r):
        def angular(deg):
            sin = math.sin(deg)
            funct = lambda x: 0.8
            if abs(sin) < 0.5:
                return 0.8 / (r)
            else:
                val = abs(funct(deg) / (r * sin))
                return val if val <= 50 else 0.8 / (r)

        return angular

    def angled_signal(pstn_angle):
        def return_this(r):
            def angular(deg):
                sin = math.sin(deg)
                cos = math.cos(deg)
                tan = math.tan(pstn_angle)
                cofunct = 1 / ((sin + (cos / tan)) * r)
                if abs(sin) >= 0.5 and abs(cos) >= 0.5 and tan and abs(cofunct) <= 200 and 90<=math.degrees(deg)<=190:
                    return cofunct * 0.8
                else:
                    return 0.8 / r

            return angular

        return return_this

    def natural_signal(r):
        return lambda x: 0.8 / r

    ##
    def angle_sweep_signal(radius):
        def return_this(pstn_angle):
            def angular(deg):
                return (0.8 / (radius / 1000))

            return angular

        return return_this

    def counter_angle_sweep_signal(radius):
        radius = radius / 1000

        def return_this(pstn_angle):
            def angular(deg):
                sin = math.sin(deg)
                cos = math.cos(deg)
                tan = math.tan(pstn_angle)
                val = radius * (sin + (cos / tan))
                if sin and cos and tan and val and abs(1 / val) <= 50 and 90<=math.degrees(deg)<=190:
                    return 1 / val
                else:
                    return 0.8 / radius

            return angular

        return return_this

    def radius_sweep():
        # No1 -> radius sweep for regular SY mechanism
        simulation_wrappers.radius_sweep(range(50, 200, 1), signal, f"{DEFAULT_DATA_DIR}",
                                         f"{DEFAULT_DATA_DIR} regular_yoke radius_sweep controlled_motion",
                                         "controlled motion")
        simulation_wrappers.radius_sweep(range(50, 200, 1), natural_signal, f"{DEFAULT_DATA_DIR}",
                                         f"{DEFAULT_DATA_DIR} regular_yoke radius_sweep natural_motion",
                                         "natural motion")
        # No2 -> radius sweep for 115 angle
        simulation_wrappers.radius_sweep(range(50, 200, 1), angled_signal(115), f"{DEFAULT_DATA_DIR}",
                                         f"{DEFAULT_DATA_DIR} angled_yoke radius_sweep controlled_115",
                                         "controlled motion - angled 115", 115)
        simulation_wrappers.radius_sweep(range(50, 200, 1), natural_signal, f"{DEFAULT_DATA_DIR}",
                                         f"{DEFAULT_DATA_DIR} angled_yoke radius_sweep natural_115",
                                         "natural motion - angled 115", 115)
        # No3 -> radius sweep for 150 angle
        simulation_wrappers.radius_sweep(range(50, 200, 1), angled_signal(150), f"{DEFAULT_DATA_DIR}",
                                         f"{DEFAULT_DATA_DIR} angled_yoke radius_sweep controlled_150",
                                         "controlled motion - angled 150",
                                         150)
        simulation_wrappers.radius_sweep(range(50, 200, 1), natural_signal, f"{DEFAULT_DATA_DIR}",
                                         f"{DEFAULT_DATA_DIR} angled_yoke radius_sweep natural_150",
                                         "natural motion - angled 150", 150)

    def angle_sweep():
        # No4 -> angle sweep for natural & controlled signal
        simulation_wrappers.angle_sweep(50, range(90, 150, 1), angle_sweep_signal(50), f"{DEFAULT_DATA_DIR}",
                                        f"{DEFAULT_DATA_DIR} angled_yoke angle_sweep r50_natural", "natural motion")
        simulation_wrappers.angle_sweep(50, range(90, 150, 1), counter_angle_sweep_signal(50), f"{DEFAULT_DATA_DIR}",
                                        f"{DEFAULT_DATA_DIR} angled_yoke angle_sweep r50_controlled",
                                        "controlled motion")

        simulation_wrappers.angle_sweep(154, range(90, 150, 1), angle_sweep_signal(154), f"{DEFAULT_DATA_DIR}",
                                        f"{DEFAULT_DATA_DIR} angled_yoke angle_sweep r154_natural", "natural motion")
        simulation_wrappers.angle_sweep(154, range(90, 150, 1), counter_angle_sweep_signal(154), f"{DEFAULT_DATA_DIR}",
                                        f"{DEFAULT_DATA_DIR} angled_yoke angle_sweep r154_controlled",
                                        "controlled motion")

        simulation_wrappers.angle_sweep(200, range(90, 150, 1), angle_sweep_signal(200), f"{DEFAULT_DATA_DIR}",
                                        f"{DEFAULT_DATA_DIR} angled_yoke angle_sweep r200_natural", "natural motion")
        simulation_wrappers.angle_sweep(200, range(90, 150, 1), counter_angle_sweep_signal(200), f"{DEFAULT_DATA_DIR}",
                                        f"{DEFAULT_DATA_DIR} angled_yoke angle_sweep r200_controlled",
                                        "controlled motion")

    def degree_sweep():
        # No5 -> 0-90, 90-180, 0-360 for chosen mechanisms
        with tqdm(total=12, file=sys.stdout) as pbar:
            pbar.set_description_str("regular SY, degree sweep")
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 90.0, 0.01), lambda x: 0.8 / 0.05,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r50_natural_0_90",
                                             "natural motion")
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(90.0, 190.0, 0.01), lambda x: 0.8 / 0.05,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r50_natural_90_180",
                                             "natural motion")
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 360.0, 0.01), lambda x: 0.8 / 0.05,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r50_natural_0_360",
                                             "natural motion")
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 90.0, 0.01), lambda x: 0.8 / 0.2,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r200_natural_0_90",
                                             "natural motion")
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(90.0, 190.0, 0.01), lambda x: 0.8 / 0.2,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r200_natural_90_180",
                                             "natural motion")
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 360.0, 0.01), lambda x: 0.8 / 0.2,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r200_natural_0_360",
                                             "natural motion")
            pbar.update(1)
            # controlled movement
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 90.0, 0.01), signal(50 / 1000),
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r50_controlled_0_90",
                                             "controlled motion")
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(90.0, 190.0, 0.01), signal(50 / 1000),
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r50_controlled_90_180",
                                             "controlled motion")
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 360.0, 0.01), signal(50 / 1000),
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r50_controlled_0_360",
                                             "controlled motion")
            pbar.update(1)

            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 90.0, 0.01), signal(200 / 1000),
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r200_controlled_0_90",
                                             "controlled motion")
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(90.0, 190.0, 0.01), signal(200 / 1000),
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r200_controlled_90_180",
                                             "controlled motion")
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 360.0, 0.01), signal(200 / 1000),
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} regular_yoke degree_sweep r200_controlled_0_360",
                                             "controlled motion")
            pbar.update(1)
            plt.close("all")
        # angled 150
        with tqdm(total=12, file=sys.stdout) as pbar:
            pbar.set_description_str("angle 150, degree sweep")
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 90.0, 0.01), lambda x: 0.8 / 0.05,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r50a150_natural_0_90",
                                             "natural motion", 150)
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(90.0, 190.0, 0.01), lambda x: 0.8 / 0.05,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r50a150_natural_90_180",
                                             "natural motion", 150)
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 360.0, 0.01), lambda x: 0.8 / 0.05,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r50a150_natural_0_360",
                                             "natural motion", 150)
            pbar.update(1)

            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 90.0, 0.01), lambda x: 0.8 / 0.2,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a150_natural_0_90",
                                             "natural motion", 150)
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(90.0, 190.0, 0.01), lambda x: 0.8 / 0.2,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a150_natural_90_180",
                                             "natural motion", 150)
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 360.0, 0.01), lambda x: 0.8 / 0.2,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a150_natural_0_360",
                                             "natural motion", 150)
            pbar.update(1)
            # controlled movement
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 90.0, 0.01),
                                             counter_angle_sweep_signal(50)(math.radians(150)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r50a150_controlled_0_90",
                                             "controlled motion", 150)
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(90.0, 190.0, 0.01),
                                             counter_angle_sweep_signal(50)(math.radians(150)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r50a150_controlled_90_180",
                                             "controlled motion", 150)
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 360.0, 0.01),
                                             counter_angle_sweep_signal(50)(math.radians(150)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r50a150_controlled_0_360",
                                             "controlled motion", 150)
            pbar.update(1)

            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 90.0, 0.01),
                                             counter_angle_sweep_signal(200)(math.radians(150)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a150_controlled_0_90",
                                             "controlled motion", 150)
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(90.0, 190.0, 0.01),
                                             counter_angle_sweep_signal(200)(math.radians(150)),
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a150_controlled_90_180",
                                             "controlled motion", 150)
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 360.0, 0.01),
                                             counter_angle_sweep_signal(200)(math.radians(150)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a150_controlled_0_360",
                                             "controlled motion", 150)
            pbar.update(1)
            plt.close("all")
        # angle 115
        with tqdm(total=12, file=sys.stdout) as pbar:
            pbar.set_description_str("angle 115, degree sweep")
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 90.0, 0.01), lambda x: 0.8 / 0.05,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a115_natural_0_90",
                                             "natural motion", 115)
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(90.0, 190.0, 0.01), lambda x: 0.8 / 0.05,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a115_natural_90_180",
                                             "natural motion", 115)
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 360.0, 0.01), lambda x: 0.8 / 0.05,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a115_natural_0_360",
                                             "natural motion", 115)
            pbar.update(1)

            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 90.0, 0.01), lambda x: 0.8 / 0.2,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a115_natural_0_90",
                                             "natural motion", 115)
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(90.0, 190.0, 0.01), lambda x: 0.8 / 0.2,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a115_natural_90_180",
                                             "natural motion", 115)
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 360.0, 0.01), lambda x: 0.8 / 0.2,
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a115_natural_0_360",
                                             "natural motion", 115)
            pbar.update(1)
            # controlled movement
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 90.0, 0.01),
                                             counter_angle_sweep_signal(50)(math.radians(115)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r50a115_controlled_0_90",
                                             "controlled motion", 115)
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(90.0, 190.0, 0.01),
                                             counter_angle_sweep_signal(50)(math.radians(115)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r50a115_controlled_90_180",
                                             "controlled motion", 115)
            pbar.update(1)
            simulation_wrappers.degree_sweep(50, numpy.arange(0.0, 360.0, 0.01),
                                             counter_angle_sweep_signal(50)(math.radians(115)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r50a115_controlled_0_360",
                                             "controlled motion", 115)
            pbar.update(1)

            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 90.0, 0.01),
                                             counter_angle_sweep_signal(200)(math.radians(115)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a115_controlled_0_90",
                                             "controlled motion", 115)
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(90.0, 190.0, 0.01),
                                             counter_angle_sweep_signal(200)(math.radians(115)),
                                             f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a115_controlled_90_180",
                                             "controlled motion", 115)
            pbar.update(1)
            simulation_wrappers.degree_sweep(200, numpy.arange(0.0, 360.0, 0.01),
                                             counter_angle_sweep_signal(200)(math.radians(115)), f"{DEFAULT_DATA_DIR}",
                                             f"{DEFAULT_DATA_DIR} angled_yoke degree_sweep r200a115_controlled_0_360",
                                             "controlled motion", 115)
            pbar.update(1)

    # execution of experiments
    #radius_sweep()
    #plt.close("all")
    angle_sweep()
    plt.close("all")
    #degree_sweep()
    #plt.close("all")
    # TODO determine optimal radius and RPM


main()
# plt.show()
