import utils, sys, os, argparse, datetime, time
from multiprocessing import Pool


phaseindex = {'MSF':7, 'RBU':7,'DCF77':9,'TDF':10,'BBC':11}
amplindex  = {'MSF':2, 'RBU':3,'DCF77':4,'TDF':5, 'BBC':6}


# Copies files to odir - only include data in time range [start, end] inclusive
def filterstation(file, station, fd):
    head, tail = os.path.split(file)
    y, m, d, h, min = utils.date_from_string(tail)

    for line in open(file, 'r'):
        if line[0] == "#":
            print("{}".format(line.strip()))
            continue

        data = line.split(',')

        dt = datetime.datetime(y, m, d, h, min)
        t0 = time.mktime(dt.timetuple())

        t = t0 + float(data[1])
        phase = float(data[phaseindex[station]])
        amp = float(data[amplindex[station]])
        print("{: .2f}, {: .3f}, {: .3f}".format(t, amp, phase))


def getfiles(args):
    filelist = []
    for root, dirs, files in os.walk(args.idir):
        for file in sorted(files):
            if file.endswith(".lvc"):
                filelist.append(os.path.join(root, file))
    return filelist

#
# #
#
parser = argparse.ArgumentParser(description='Remove measurements outside specified range')
parser.add_argument('--idir', help='input directory', required=True)
parser.add_argument('--odir', help='output directory', required=True)
parser.add_argument('--station', '-s', help='output directory', required=True)
args = parser.parse_args()

utils.checkdirs(args)

# Collect the two arguments to convert()
fd = open("{}.pha".format(args.station), 'a')
i = 1
for f in getfiles(args):
    filterstation(f, args.station, fd)
    i = i + 1
    if i == 3:
        break
print("The End\n")
fd.close()
