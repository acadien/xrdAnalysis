#!/usr/bin/python
import sys
import pylab as pl
from scipy import signal
#from scipy.signal import iirdesign
from math import fabs

#What does this script do?
#Testing out a high-pass FIR for removing the underlying noise

#Arguement handline
def usage():
    print "%s <input chifile> <Start(2theta)> <End(2theta)> <0:disable plot>"%sys.argv[0].split("/")[-1]

if not(len(sys.argv) in [4,5]):
    usage()
    exit(0)

ifilename=sys.argv[1]
ofilename="filtered_"+ifilename
strt=float(sys.argv[2])
end=float(sys.argv[3])
enableplot=True
if len(sys.argv)==5:
    if sys.argv[4]==0:
        enableplot=False

#####################
#Read in the achi file
f=open(ifilename,'r').readlines()
xxa=list()
yya=list()
for line in f[4:]:
    [a,b]=[float(i) for i in line.split()]
    xxa.append(a)
    yya.append(b)

b,a = signal.iirdesign(wp = 0.06, ws= 1e-10, gstop= 12, gpass=0.01, ftype='cheby1')
filtyya=signal.lfilter(b,a,yya)
#b,a = signal.iirdesign(wp = 0.01, ws= 1e-10, gstop= 10, gpass=0.001, ftype='cheby1')
#filtyya=signal.lfilter(b,a,filtyya)
"""filtyya=list()
for i in signal.lfilter(b,a,yya):
    if i<0:
        filtyya.append(0)
    else:
        filtyya.append(i)
"""

si= sum([1 for i in xxa if i<strt]) #index of the starting location for 2theta
ei= sum([1 for i in xxa if i<end]) #index of the ending location for 2theta
if enableplot:
    pl.figure()
    pl.plot(xxa,yya)
    pl.plot(xxa[si:ei],filtyya[si:ei])
    pl.plot(xxa,[0]*len(xxa))
    pl.xlabel("2Theta")
    pl.ylabel("Intensity")
    pl.legend(["Raw-chi","Filtered"])
    pl.show()

import datetime
data="This chifile generated by %s. %s\n"%(sys.argv[0],datetime.date.today())
data+="2-Theta Angle (Degrees)\n"
data+="Intensity\n"
data+="\t%d\n"%len(filtyya)
for i in range(si,ei+1):
    data+="%e  %e\n"%(xxa[i],filtyya[i])
    
open(ofilename,"w").write(data)
