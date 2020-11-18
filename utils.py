import numpy as np
import re, sys, math, os

# Must match the names used in genfromtxt()
stnphase = {'MSF':'p1', 'RBU':'p2','DCF77':'p3','TDF':'p4','BBC':'p5'}
stnampl  = {'MSF':'a1', 'RBU':'a2','DCF77':'a3','TDF':'a4','BBC':'a5'}

cf = lambda x: float(x)*0.017453292519943

def readfile(filename):
    try:
        return np.genfromtxt(filename, delimiter=',', comments='#',
                             skip_header=0, skip_footer=0,
            converters = {7: cf, 8: cf, 9: cf, 10: cf, 11: cf},
            names = ['i',  't',
                     'a1',  'a2',  'a3',  'a4',  'a5',
                     'p1',  'p2',  'p3',  'p4',  'p5'])
    except:
        print("Error reading file {}\n".format(filename))
        sys.exit()

# Decimal coordinates classic to degrees mins secs
def dech2hm(dech):
    hour = math.floor(dech)
    minute = (dech - hour)*60
    return "%02d:%02d" % (hour, minute)


###
def date_from_string(filename):
    yymmdd = '([0-9]{2,4})-([0-9]{2})-([0-9]{2})'
    hhmm = '([0-9]{2})([0-9]{2})'
    patt = '.*_' + yymmdd + '_' + hhmm + '.*'
    result = re.match(patt, filename)

    if result:
        year = int(result.group(1))
        month = int(result.group(2))
        day = int(result.group(3))
        hour = int(result.group(4))
        min = int(result.group(5))
        #print("Matched date {:d}-{:02d}-{:02d}_{:02d}:{:02d}".format(year, month, day, hour, min))
        return [year, month, day, hour, min]
    else:
        print("No match!, quitting")
        sys.exit(1)

# Resize data array to include lines where
# amplitude is at least amin
def removebadampl(data, stn, amin):
    t = []
    p = []
    a = []
    for i in range(len(data)):
        if data[stnampl[stn]][i] >= amin:
            nt = data['t'][i]/3600
            na = data[stnampl[stn]][i]
            nf = data[stnphase[stn]][i]
            t.append(nt)
            p.append(nf)
            a.append(na)
    return t, a, p

# Resize data array to include lines where
# amplitude is at least amin
def removebadamplnan(data, stn, amin, tmin, tmax):
    t = []
    p = []
    a = []
    aarr = data[stnampl[stn]]
    parr = data[stnphase[stn]]
    for i in range(len(data)):
        time = data['t'][i]/3600
        if time >= tmin and time <= tmax:
            if aarr[i] >= amin:
                nt = time
                na = aarr[i]
                nf = parr[i]
            else:
                #print('removing bad amplitude')
                nt = time
                na = aarr[i]
                nf = np.nan
            t.append(nt)
            p.append(nf)
            a.append(na)
    return t, a, p

###
class GeoInfo:
    def __init__(self, lat, lon, tz):
        self.lat = lat
        self.lon = lon
        self.tz = tz

CPH   = GeoInfo(55.741389, 12.531111, 1)
MSF   = GeoInfo(54.916667, -3.280000, 0)
RBU   = GeoInfo(56.733333, 37.663333, 3)
DCF77 = GeoInfo(50.016667,  9.000000, 1)
TDF   = GeoInfo(47.169444,  2.204722, 1)
BBC   = GeoInfo(52.296667, -2.105278, 1)

stations = ['MSF', 'RBU', 'DCF77', 'TDF', 'BBC']
positions = {'CPH' : CPH, 'MSF' : MSF, 'RBU' : RBU, 'DCF77' : DCF77, 'TDF' : TDF, 'BBC' : BBC}
#frequencies = {}

def checkdirs(args):
    if not os.path.isdir(args.idir):
        print("input directory does not exist, exiting.")
        sys.exit()

    if os.path.isdir(args.odir):
        print("output directory already exist, exiting.")
        sys.exit()
    else:
        os.mkdir(args.odir)
