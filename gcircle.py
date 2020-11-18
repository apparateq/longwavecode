
from math import cos, sin, acos, pi

def d2r(d):
   return 2*pi*d/360

def length(d1, l1, d2, l2):
   d1 =  d2r(d1)
   d2 =  d2r(d2)
   l1 =  d2r(l1)
   l2 =  d2r(l2)
   r = 6370
   a = cos(d1)*cos(d2)*cos(l1 - l2) + sin(d1)*sin(d2)
   return r * acos(a)


print("%.1f" % (length(56.0, 12.0, 56.66, 37.0)))
print("CPH SVO %.1f" % (length(55.66, 12.66, 56.00, 37.5)))
print("latitude 1 degree %.1f" % (length(56.0, 0.0, 57.0, 0.0)))
print("longitude 1 degree %.1f" % (length(0.0, 10.0, 0.0, 11.0)))
print("diag 1 degree %.1f" % (length(0.0, 0.0, 1.0, 1.0)))
