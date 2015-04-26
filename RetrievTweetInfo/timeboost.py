import time
from time import strftime,gmtime, strptime
import datetime
#Sat Apr 11 05:26:19 +0000 2015
def timeBoost(time1,time2):
    diffEpoch = time.mktime(time.strptime(time1,"%a %b %d %H:%M:%S +0000 %Y"))- time.mktime(time.strptime(time2,"%a %b %d %H:%M:%S +0000 %Y")) 
    if diffEpoch < 3600.0:
        return 50
    elif  diffEpoch < 86400.0:
        return 30
    else: return 20

    
print timeBoost("Sat Apr 11 05:26:19 +0000 2015","Sat Apr 12 5:26:20 +0000 2015")