import matplotlib.pyplot as plt
import numpy as np
import utils, sys, re, os, argparse, datetime
from math import pi

# Perform basic statistical analysis on arrays
def analyze(towrap, phase, amplitude):
    wrap = pi
    if towrap:
        p = np.unwrap(phase, wrap)
    else:
        p = phase
    return "{: 8.3f}, {: 8.3f}, {: 8.3f}, {: 8.3f}, {: 8.3f}, {: 8.3f}, {: 8.3f}, {: 8.3f}".format(
            np.amin(p), np.amax(p), np.average(p), np.median(p),
            np.amin(amplitude), np.amax(amplitude), np.average(amplitude), np.median(amplitude))

#
#
#
parser = argparse.ArgumentParser(description='Preprocess LW data')
parser.add_argument('--idir', help='input directory', required=True)
parser.add_argument('--odir', help='output directory', required=True)
parser.add_argument('--unwrap', '-u', help='unwrap phase', action='store_true')
parser.add_argument('--amin', '-a', help='minimum accepted amplitude', type=float, default = -1000.0)
args = parser.parse_args()

utils.checkdirs(args)

stnfd = {}
for stn in utils.stations:
    stnfd[stn] = open(os.path.join(args.odir, stn + '.sta'), 'a')
    stnfd[stn].write("# Run date: {}\n".format(datetime.datetime.now()))
    stnfd[stn].write("# Unwrap phases: {}\n".format(args.unwrap))
    stnfd[stn].write("# Minimum accepted amplitude: {}\n".format(args.amin))
    stnfd[stn].write("# date,  phase_min (rad), phase_max (rad), phase_avg (rad), phase_med (rad), ampl_min, ampl_max, ampl_avg, ampl_med\n")

for root, dirs, files in os.walk(args.idir):
    for file in sorted(files):
        y, m, d, h, min = utils.date_from_string(file)
        data = utils.readfile(os.path.join(root, file))
        print("{}".format(file))
        for stn in utils.stations:
            t, a, p = utils.removebadamplnan(data, stn, args.amin, 0.0, 24.0)
            res = analyze(args.unwrap, p, a)
            stnfd[stn].write("{:02d}{:02d}{:02d}, {}\n".format(y, m, d, res))
