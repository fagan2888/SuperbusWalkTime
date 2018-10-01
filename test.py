import time
import datetime
a='0901'
a_time= datetime.datetime.strptime(a,'%m%d')
b_time=datetime.timedelta(days=1)
now=  a_time-b_time
print datetime.datetime.strftime(now,'%m%d')