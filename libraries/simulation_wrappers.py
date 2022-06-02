from libraries import experiment, plots
from colorama import Fore
import os
import matplotlib.pyplot as plt
def radius_sweep(d_range, signal, src, filename, graph_title, angle = 90):
    plt.rcParams["figure.figsize"] = (10, 10)

    def hpath(string):
        string = f"{os.path.expanduser('~')} {string}"
        return os.sep.join(string.split())

    def export_csv(path, content):
        with open(path, "w") as f:
            f.write(content)
    def get_matrix_csv(a, b, c, d, e, header):
        vals = [";".join([str(item) for item in v]) for v in zip(a, b, c, d, e)]
        vals = [header] + vals
        vals = "\n".join(vals)
        vals = vals.replace('.', ',')
        return vals

    # experiment No1 - fully controlled motion
    print(Fore.GREEN+graph_title+Fore.RESET)
    v, a, x, w, r = experiment.ScotchYoke().radius_sweep(d_range, signal, angle)
    w = [9.5493 * val for val in w]
    radius = plots.MatrixPlot(2, 2, f"Radius sweep - {graph_title}")
    radius.AddPlot(r, v, 'r', ("Max velocity for each radius", "radius [mm]", "velocity [m/s]"))
    radius.AddPlot(r, a, 'g', ("Max acceleration for each radius", "radius [mm]", "velocity [m/s^2]"))
    radius.AddPlot(r, x, 'k', ("Max displacement for each radius", "radius [mm]", "displacement [mm]"))
    radius.AddPlot(r, w, 'b', ("Max angular velocity", "radius [mm]", "required RPM [RPM]"))
    plt.subplots_adjust(hspace=0.3)
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(hpath(f"{filename}.png"))
    header = "[radius |mm],[angular velocity |RPM],[dislocation |mm],[linear velocity | m/s],[linear acceleration |m/s^2]"
    "[linear velocity |m/s]#[acceleration |m/s^2]"
    header = header.replace(',', ';')
    csv = get_matrix_csv(r, w, x, v, a, header)
    export_csv(hpath(f"{filename}.csv"), csv)

def angle_sweep(r, d_range, signal, src, filename, graph_title):
    plt.rcParams["figure.figsize"] = (10, 10)

    def hpath(string):
        string = f"{os.path.expanduser('~')} {string}"
        return os.sep.join(string.split())

    def export_csv(path, content):
        with open(path, "w") as f:
            f.write(content)
    def get_matrix_csv(a, b, c, d, e, header):
        vals = [";".join([str(item) for item in v]) for v in zip(a, b, c, d, e)]
        vals = [header] + vals
        vals = "\n".join(vals)
        vals = vals.replace('.', ',')
        return vals

    # experiment No1 - fully controlled motion
    print(Fore.GREEN+graph_title+Fore.RESET)
    v, a, x, w, pstn_angle = experiment.ScotchYoke().piston_angle_sweep(d_range, r, signal)
    w = [9.5493 * val for val in w]
    radius = plots.MatrixPlot(2, 2, f"Radius sweep - {graph_title}")
    radius.AddPlot(pstn_angle, v, 'r', ("Max velocity for each angle", "piston angle [deg]", "velocity [m/s]"))
    radius.AddPlot(pstn_angle, a, 'g', ("Max acceleration for each angle", "piston angle [deg]", "velocity [m/s^2]"))
    radius.AddPlot(pstn_angle, x, 'k', ("Max displacement for each angle", "piston angle [deg]", "displacement [mm]"))
    radius.AddPlot(pstn_angle, w, 'b', ("Max angular velocity", "piston angle [deg]", "required RPM [RPM]"))
    plt.subplots_adjust(hspace=0.3)
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(hpath(f"{filename}.png"))
    header = "[piston angle |deg],[angular velocity |RPM],[dislocation |mm],[linear velocity | m/s],[linear acceleration |m/s^2]"
    "[linear velocity |m/s]#[acceleration |m/s^2]"
    header = header.replace(',', ';')
    csv = get_matrix_csv(pstn_angle, w, x, v, a, header)
    export_csv(hpath(f"{filename}.csv"), csv)

def degree_sweep(r, d_range, signal, src, filename, graph_title, angle = 90):
    plt.rcParams["figure.figsize"] = (10, 10)

    def hpath(string):
        string = f"{os.path.expanduser('~')} {string}"
        return os.sep.join(string.split())

    def export_csv(path, content):
        with open(path, "w") as f:
            f.write(content)
    def get_matrix_csv(a, b, c, d, e, header):
        vals = [";".join([str(item) for item in v]) for v in zip(a, b, c, d, e)]
        vals = [header] + vals
        vals = "\n".join(vals)
        vals = vals.replace('.', ',')
        return vals

    # experiment No1 - fully controlled motion
    #print(Fore.GREEN+graph_title+Fore.RESET)
    v, a, x, w, deg = experiment.ScotchYoke().degree_sweep(d_range, signal, r, angle)
    w = [9.5493 * val for val in w]

    radius = plots.MatrixPlot(2, 2, f"Degree sweep - {graph_title}")
    radius.AddPlot(deg, v, 'r', ("Velocity", "piston angle [deg]", "velocity [m/s]"))
    radius.AddPlot(deg, a, 'g', ("Acceleration", "piston angle [deg]", "velocity [m/s^2]"))
    radius.AddPlot(deg, x, 'k', ("Dislocation", "piston angle [deg]", "displacement [mm]"))
    radius.AddPlot(deg, w, 'b', ("angular velocity", "piston angle [deg]", "required RPM [RPM]"))
    plt.subplots_adjust(hspace=0.3)
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(hpath(f"{filename}.png"))
    header = "[position |deg],[angular velocity |RPM],[dislocation |mm],[linear velocity | m/s],[linear acceleration |m/s^2]"
    "[linear velocity |m/s]#[acceleration |m/s^2]"
    header = header.replace(',',';')
    csv = get_matrix_csv(deg, w, x, v, a, header)
    export_csv(hpath(f"{filename}.csv"), csv)