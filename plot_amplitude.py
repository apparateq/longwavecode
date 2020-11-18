import matplotlib.pyplot as plt
import numpy as np
import utils, argparse, os, sys
from math import pi

marker_style='-'  # default plot type is lines

#
#
#
parser = argparse.ArgumentParser(description='Plot amplitude for one or more stations')
parser.add_argument('--idir',     help='input directory', required=True)
parser.add_argument('--file', '-f', help='input file', required=True)
parser.add_argument('--station', '-s', help='radio station', required=True)
parser.add_argument('--begin', '-b', help='start time (h)', type=float, default=0.00)
parser.add_argument('--end', '-e', help='end time', type=float, default = 24.00)
parser.add_argument('--title', '-t', help='Title')
parser.add_argument('--points', '-p', help='plot with points instead of lines', action='store_true')
args = parser.parse_args()

if args.points:
    marker_style='.'

if not os.path.isdir(args.idir):
    print("input directory does not exist, exiting.")
    sys.exit()

wrap = pi
filename = os.path.join(args.idir, args.file)
data = utils.readfile(filename)

plt.style.use('seaborn-ticks')
fig, ax = plt.subplots(1, 1)
plt.suptitle(args.title)

t = data['t']/3600
for stn in args.station.split(' '):
    ax.plot(t, data[utils.stnampl[stn]], marker_style, label = stn)
ax.set(xlabel='time (h) UTC+1', ylabel='amplitude (dBV)')
ax.set_title(args.file)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=5, fancybox=True, shadow=True)
ax.set_xlim(args.begin, args.end)
plt.show()
