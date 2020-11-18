import utils, sys, os, argparse, sunrise, datetime
from multiprocessing import Pool

def get_sun_up_down(filename, expand):
    y, m, d, h, min = utils.date_from_string(filename)
    last_up, down = sunrise.sunupdown(y, m, d, 'MSF')
    up, first_down = sunrise.sunupdown(y, m, d, 'RBU')
    return [(last_up - expand) * 3600, (first_down + expand) * 3600]

# Returns time range in seconds
def get_time_range(file, args):
    if args.method == 'sun':
        return get_sun_up_down(file, 0.0)
    elif args.method == 'range':
        return args.begin * 3600, args.end * 3600

def is_in_range(line, start, end):
    t = line.split(',')[1]
    if float(t) >= start and float(t) <= end:
        return True
    else:
        return False

# Copies files to odir - only include data in time range [start, end] inclusive
def filter(parms):
    file = parms[0]
    args = parms[1]

    start, end = get_time_range(file, args)
    print('file: {}, time range [{}:{}] UTC+1'.format(file, start, end))
    head, tail = os.path.split(file)
    #y, m, d, h, min = utils.date_from_string(tail)
    ofile = os.path.join(args.odir, tail)

    with open(ofile, 'a') as of:
        of.write('# {}: filtered by time range: from {:9.3f}s to {:9.3f}s\n'.format(
             datetime.datetime.now(), start, end))
        lineswritten = 0
        for line in open(file, 'r'):
            if line[0] == '#': # comment line
                of.write(line)
            elif is_in_range(line, start, end):
                of.write(line)
                lineswritten += 1
        of.close()
        if lineswritten == 0:
            print("Deleting empty ofile {}".format(ofile))
            os.remove(ofile)


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
parser.add_argument('--method', '-m', help='filter: sun, range (use --begin --end)', default='sun')
parser.add_argument('--begin', '-b', help='start time (hours)', type=float, default=0.00)
parser.add_argument('--end', '-e', help='end time (hours)', type=float, default = 24.00)
parser.add_argument('--parallel', '-p', help='number of processes', type=int, default=10)
args = parser.parse_args()

utils.checkdirs(args)

# Collect the two arguments to convert()
fileargs = ((f, args) for f in getfiles(args))

# Ship these off for parallel processing
p = Pool(args.parallel) #
p.map(filter, fileargs)
