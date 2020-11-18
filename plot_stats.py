import matplotlib.pyplot as plt
import numpy as np
import utils, argparse, os, sys, time
from math import pi

marker_style='-'  # default plot type is lines

ylbl = {'pmin':'phase (radians)',
        'pmax':'phase (radians)',
        'pavg':'phase (radians)',
        'pmed':'phase (radians)',
        'amin':'amplitude (dBV)',
        'amax':'amplitude (dBV)',
        'aavg':'amplitude (dBV)',
        'amed':'amplitude (dBV)'}

titl = {'pmin':'Minimum Phase',
        'pmax':'Maximum Phase',
        'pavg':'Average Phase',
        'pmed':'Median Phase',
        'amin':'Minimum Amplitude',
        'amax':'Maximum Amplitude',
        'aavg':'Average Amplitude',
        'amed':'Median Amplitude'}

#
#
#
parser = argparse.ArgumentParser(description='Plot statistics for a single station.')
parser.add_argument('--idir',     help='input directory', required=True)
parser.add_argument('--station', '-s', help='radio station', required=True)
parser.add_argument('--title', '-t', help='Title', default='')
parser.add_argument('--stat', '-a', help='Statistics field to plot', default='aavg')
parser.add_argument('--points', '-p', help='plot with points instead of lines', action='store_true')
args = parser.parse_args()

if args.points:
    marker_style='.'

if not os.path.isdir(args.idir):
    print("input directory does not exist, exiting.")
    sys.exit()

plt.style.use('seaborn-ticks')
fig, ax = plt.subplots(1, 1)
plt.suptitle(args.title)

for stn in args.station.split(' '):
    filename = os.path.join(args.idir, stn + '.sta')
    data = np.genfromtxt(filename, delimiter=',', comments='#',
                         skip_header=0, skip_footer=0,
        names = ['d',  'pmin', 'pmax', 'pavg', 'pmed', 'amin', 'amax', 'aavg', 'amed'])

    year = int(data['d'][0]/10000)  # extract year from date
    year10k = year*10000

    t = []
    time_tuple = time.strptime(str(year)+'-01-01 12:00:00', '%Y-%m-%d %H:%M:%S')
    t0 = time.mktime(time_tuple)
    for date in data['d']:
        y = int(date/10000)
        m = int((date - year10k)/100)
        d = int((date - year10k - m*100))
        time_tuple = time.strptime('{}-{}-{} 12:00:00'.format(y, m, d), '%Y-%m-%d %H:%M:%S')
        time_epoch = time.mktime(time_tuple)
        t.append((time_epoch - t0)/(24*3600))

    ax.plot(t, data[args.stat], marker_style, label=stn)
    #ax.set_ylim(-80.0, -55.0)

ax.set(xlabel='time (days)', ylabel=ylbl[args.stat])
ax.set_title(titl[args.stat] + " - " + args.station)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00),
          ncol=5, fancybox=True, shadow=True)
plt.show()
