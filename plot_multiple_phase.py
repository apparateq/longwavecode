import matplotlib.pyplot as plt
import numpy as np
import utils, argparse, os, sys
from math import pi
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

marker_style='-'  # default plot type is lines

files = ['lw_raw_dk_normal_time_2019-01-17_0000.lvc',
         'lw_raw_dk_normal_time_2019-01-18_0000.lvc',
         'lw_raw_dk_normal_time_2019-01-19_0000.lvc',
         'lw_raw_dk_normal_time_2019-01-20_0000.lvc',
         'lw_raw_dk_normal_time_2019-01-21_0000.lvc',
         'lw_raw_dk_normal_time_2019-01-22_0000.lvc',
         'lw_raw_dk_normal_time_2019-01-23_0000.lvc'
         ]

#
#
#
parser = argparse.ArgumentParser(description='Multiplot of phase for one or more stations')
parser.add_argument('--idir', help='input directory', required=True)
parser.add_argument('--station', '-s', help='Callsign(s)', default='MSF')
parser.add_argument('--begin', '-b', help='start time (h)', type=float, default=0.00)
parser.add_argument('--end', '-e', help='end time', type=float, default = 24.00)
parser.add_argument('--unwrap', '-u', help='unwrap phase', action='store_true')
parser.add_argument('--points', '-p', help='plot with points instead of lines', action='store_true')
args = parser.parse_args()

if args.points:
    marker_style='.'

if not os.path.isdir(args.idir):
    print("input directory does not exist, exiting.")
    sys.exit()

plt.style.use('seaborn-white')
fig, ax = plt.subplots(len(files), 1, sharex='col', sharey='row')
wrap = pi
for idx, file in enumerate(files):
    data = utils.readfile(os.path.join(args.idir, file))

    t = data['t']/3600.0
    for stn in args.station.split(' '):
        print(idx, file, stn)
        lbl='file {}: {}'.format(idx, stn)
        if args.unwrap:
            ax[idx].plot(t, np.unwrap(data[utils.stnphase[stn]], wrap), marker_style, label=lbl)
        else:
            ax[idx].plot(t, data[utils.stnphase[stn]], marker_style, label=lbl)

        ax[idx].axhline(y=0, linewidth=0.5, color='k')
        ax[idx].axvline(x=6, linewidth=0.5, color='k', linestyle='--')
        ax[idx].axvline(x=12, linewidth=0.5, color='k')
        ax[idx].axvline(x=18, linewidth=0.5, color='k', linestyle='--')

    #ax[idx].set_title(file)
    ax[idx].grid(True, which='both')

# Make a plot with major ticks that are multiples of 20 and minor ticks that
# are multiples of 5.  Label major ticks with '%d' formatting but don't label
# minor ticks.
    ax[idx].yaxis.set_major_locator(MultipleLocator(pi))
    ax[idx].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

# For the minor ticks, use no labels; default NullFormatter.
    ax[idx].yaxis.set_minor_locator(MultipleLocator(pi/2))
    ax[idx].legend(prop={'size': 6}, bbox_to_anchor=(0.9, 1.00))
    if not args.unwrap:
        ax[idx].set_ylim(-pi, pi)
    else:
        ax[idx].set_ylim(-2*pi, 2*pi)
    #abbfilenames = {x.replace('lw_raw_dk_normal_time_','') for x in files}
    #fig.suptitle(abbfilenames)
    ax[idx].set_xlim(args.begin, args.end)
plt.show()
