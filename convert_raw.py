import utils, sys, os, argparse, datetime
from multiprocessing import Pool

# Keep ignoring lines until 'X_Value' is found
def skip_header(file):
    header = True
    while header:
        line = file.readline()
        line = line.replace(')',' ')
        line = line.replace(',','.').split()
        if len(line) != 0 and line[0] == 'X_Value':
            header = False

# Read block of four lines, replace , with .
def read_data_block(file):
    b1 = file.readline().replace(',', '.')
    b2 = file.readline().replace(',', '.')
    b3 = file.readline().replace(',', '.')
    b4 = file.readline().replace(',', '.')
    if b1 == '' or b2 == '' or b3 == '' or b4 == '':
        return ''
    if len(b1) <= 150:
        print('first line in block has wrong length, unrecoverable, exiting...')
        print(b1)
        sys.exit()
    else:
        b2 = b2.split()
        b3 = b3.split()

        try:
            if float(b3[1]) > 180.0 or float(b3[1]) < -180.0:
                print('b3 data out of range')
                print(b3)
            if float(b2[1]) > 0.0 or float(b2[1]) < -200.0:
                print('b2 data out of range')
                print(b2)

            res = "{: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}"\
                .format( float(b2[1]), float(b2[3]), float(b2[5]), float(b2[7]), float(b2[9]),
                         float(b3[1]), float(b3[3]), float(b3[5]), float(b3[7]), float(b3[9]))
        except:
            print("Data error in b2 or b3")
            err = -1001.0
            res = "{: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}, {: 9.3f}"\
                .format( err, err, err, err, err, err, err, err, err, err)
        return res

# Reduce raw data by extracting relevant fields only
def convert(parms):
    ifile = parms[0]
    odir = parms[1]
    head, tail = os.path.split(ifile)
    y, m, d, h, min = utils.date_from_string(tail)
    y += 2000
    offset = h * 3600 + min * 60

    ofilename = "lw_raw_dk_normal_time_{:4d}-{:02d}-{:02d}_{:02d}{:02d}.lvc".format(y,m,d,h,min)
    print("Filename: %s -> %s" % (tail, ofilename))
    ofile = os.path.join(odir, ofilename)

    with open(ofile, 'a') as of:
        of.write("# {}: converted from {}\n".format(datetime.datetime.now(), ifile))
        of.write("#                        ------------------ amplitudes (dB) ----------------  ----------------- phases (deg.) --------------------\n")
        of.write("# sampno     time        {:11}{:11}{:11}{:11}{:11}{:11}{:11}{:11}{:11}{:11}\n".format(
              'a60k', 'a200/3k', 'a77.5k', 'a162k', 'a198k',
              'p60k', 'p200/3k', 'p77.5k', 'p162k', 'p198k'))

        #with open(ifile, 'r') as ipf:
        with open(ifile, 'r', encoding="latin-1") as ipf:
            skip_header(ipf)
            samples = 0
            while True:
                res = read_data_block(ipf)
                if res == "":
                    #print("end of file with {} lines".format(samples))
                    break
                else:
                    of.write("{:9d}, {:9.3f}, {:s}\n".format(samples, offset + samples * 1.44, res))
                    samples += 1
            ipf.close()
    of.close()


# Return list of files to be converted
def getfiles(args):
    filelist = []
    if args.file != '':
          filelist.append(os.path.join(args.idir, args.file))
    else:
        for root, dirs, files in os.walk(args.idir):
            for idx, file in enumerate(sorted(files)):
                if file.endswith(".lvm") and idx <= args.number:
                    if (file.find(args.match) != -1):
                      filelist.append(os.path.join(root, file))
    return filelist



#
#
#
parser = argparse.ArgumentParser(description='Convert raw data to single line per measurement')
parser.add_argument('--idir',           help='input directory', required=True)
parser.add_argument('--file', '-f',     help='filename', default='')
parser.add_argument('--match', '-m',    help='match string', default='')
parser.add_argument('--odir',           help='output directory', required=True)
parser.add_argument('--number', '-n',   help='number of files to process', type=int, default=1000000000)
parser.add_argument('--parallel', '-p', help='number of processes', type=int, default=10)
args = parser.parse_args()

utils.checkdirs(args)

# Collect the two arguments to convert()
fileargs = ((f, args.odir) for f in getfiles(args))
# Ship these off for parallel processing
p = Pool(args.parallel) # 1:22 min for p = 10), 5:18 for p = 1
p.map(convert, fileargs)
