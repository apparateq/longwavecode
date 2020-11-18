import matplotlib.pyplot as plt
import numpy as np
import utils, argparse, os, sys
from math import pi

marker_style='-'  # default plot type is lines

# Adds vertical lines to the figure, for example
# start, peak, end of solar flares, etc.
def addvlines(ax, vlines):
    if vlines == '':
        return
    for mark in vlines.split(' '):
        ax.axvline(x=float(mark), linewidth=0.75, linestyle='--', color='k')

#
#
#
parser = argparse.ArgumentParser(description='Plot phase and amplitude for one or more stations')
parser.add_argument('--title', '-t', help='Title')
parser.add_argument('--idir', help='input directory', required=True)
parser.add_argument('--file', '-f', help='input file', required=True)
parser.add_argument('--station', '-s', help='radio station', required=True)
parser.add_argument('--begin', '-b', help='start time (hours)', type=float, default=0.00)
parser.add_argument('--end', '-e', help='end time (hours)', type=float, default = 24.00)
parser.add_argument('--amin', '-a', help='minimum accepted amplitude', type=float, default = -1000.0)
parser.add_argument('--unwrap', '-u', help='unwrap phase', action='store_true')
parser.add_argument('--vlines', '-v', help='vertical markers', default='')
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
fig, ax = plt.subplots(2, 1)
plt.suptitle(args.title, weight='bold')
for stn in args.station.split(' '):
    t, a, p = utils.removebadamplnan(data, stn, args.amin, args.begin, args.end)
    if args.unwrap:
        ax[0].plot(t, np.unwrap(p, wrap), marker_style, label=stn)
    else:
        ax[0].plot(t, p, marker_style, label=stn)
    ax[1].plot(t, a, marker_style)

# PHASE
ax[0].set(xlabel='time (h) UTC+1', ylabel='phase (radians)')
ax[0].set_title(args.file)
ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=5, fancybox=True, shadow=True)
ax[0].set_xlim(args.begin, args.end)
addvlines(ax[0], args.vlines)

# AMPLITUDE
ax[1].set(xlabel='time (h) UTC+1', ylabel='amplitude (dBV)')
addvlines(ax[1], args.vlines)
ax[1].set_xlim(args.begin, args.end)

if args.amin != -1000.0:
    ax[1].axhline(y=args.amin, linestyle='--', linewidth=0.75, color='k')
plt.show()
