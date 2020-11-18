import matplotlib.pyplot as plt
import numpy as np
import utils, argparse, os, sys
from math import pi

# Frequencies needed to convert phase to seconds
freq = {'DCF77': 77500 ,
        'RBU': 66666.66,
        'MSF': 60000,
        'TDF': 162000,
        'BBC': 198000
        }

def readfile(filename):
    try:
        return np.genfromtxt(filename, delimiter=',', comments='#',
                             skip_header=0, skip_footer=0,
            names = ['d',  'pmin', 'pmax', 'pavg', 'pmed'])
    except:
        print("Error reading file {}\n".format(filename))
        sys.exit()

#
#
#
parser = argparse.ArgumentParser(description='Extract phase')
parser.add_argument('--idir',     help='input directory for analysed data', required=True)
parser.add_argument('--station', '-s', help='radio station', required=True)

args = parser.parse_args()

if not os.path.isdir(args.idir):
    print("input directory does not exist, exiting.")
    sys.exit()

statfile = args.station + ".sta"
filename = os.path.join(args.idir, statfile)
ofile = args.station + "_stable32.txt"
ofd = open(ofile, 'a')
data = readfile(filename)

ofd.write("# {}\n".format(filename))

if len(data['pmed']) != 365:
    print("Data missing check input file for gaps")
    sys.exit()

data['pmed'] = data['pmed'] / (2 * pi * freq[args.station])

for i in range(len(data['pmed'])):
    time = 12*3600 + 24*3600 * i
    phase = data['pmed'][i]
    if np.isnan(phase):
         ofd.write("{:7}, 0\n".format(time))
    else:
        ofd.write("{:7}, {:.7}\n".format(time, phase))
