from Sun import Sun

import utils, sys

def sunupdown(y, m, d, stn):
    coords = {'longitude' : utils.positions[stn].lon, 'latitude' : utils.positions[stn].lat }
    sun = Sun(d,m,y)

    # Sunrise time UTC (decimal, 24 hour format)
    sunrise = sun.getSunriseTime( coords )['decimal']

    # Sunset time UTC (decimal, 24 hour format)
    sunset = sun.getSunsetTime( coords )['decimal']

    return [sunrise, sunset]


def main():
    if len(sys.argv) == 4:
        d = int(sys.argv[1])
        m = int(sys.argv[2])
        y = int(sys.argv[3])
    else:
        d = 1
        m = 1
        y = 1970

    for stn in utils.stations:
        up, down = sunupdown(y, m, d, stn)
        print("%-5s, Date: %d-%d-%d, sunrise %s (%f), sunset: %s (%f)"  %
              (stn, y, m, d, utils.dech2hm(up), up, utils.dech2hm(down), down))

if __name__ == "__main__":
    main()
