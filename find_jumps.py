import utils, sys, os, argparse, datetime
from multiprocessing import Pool

# Reduce raw data by extracting relevant fields only
def findjumps(file):
    data = utils.readfile(file)
    print("lines {}".format(len(data)))
    for i in range(len(data) - 1):
        t =  data['t'][i]
        p1 = data[utils.stnphase['TDF']][i]
        p2 = data[utils.stnphase['TDF']][i+1]
        if ( abs(p1 - p2) > 6 ):
            print("large phase jump at {}: {} {}".format(t, p1, p2))

#
#
#
parser = argparse.ArgumentParser(description='Find phase jumps')
parser.add_argument('--idir',           help='input directory', required=True)
parser.add_argument('--file', '-f',     help='filename', default='')
parser.add_argument('--match', '-m',    help='match string', default='')
parser.add_argument('--odir',           help='output directory', required=True)
parser.add_argument('--number', '-n',   help='number of files to process', type=int, default=1000000000)
parser.add_argument('--parallel', '-p', help='number of processes', type=int, default=10)
args = parser.parse_args()

utils.checkdirs(args)

findjumps(args.file)
