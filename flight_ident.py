# coding:utf-8

import requests
import json
import time
import xlrd

code_url='https://e1.flightcdn.com/ajax/ignoreall/omnisearch/flight.rvt?v=47&locale=zh_CN&searchterm='
outfile='indent_out2.csv'
f=open(outfile,'w')
t0=time.time()

def get_flight_code(flight_no):
    res=requests.get(code_url+flight_no)
    json_obj=json.loads(res.text)
    try:
        ident=json_obj[u'data'][0][u'ident']
    except:
        print 'cannot get flight'
        ident=''
    return ident
def time_swap(timestamp):
    timeStamp = float(timestamp[:-3])
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print otherStyleTime

data = xlrd.open_workbook('2018data.xlsx')
table = data.sheets()[0]
nrows = table.nrows
ids = table.col_values(0)
activeTime = table.col_values(16)
flight_no = table.col_values(24)
all_flight = map(lambda x, y, z: [x, y, z], ids, activeTime, flight_no)
all_flight[0].append('flight_code')
ncols = table.ncols
print '总行数=', nrows


f.write(','.join([str(all_flight[0][i]).replace('.0','') for i in range(4)])+'\n')
for idd,one in enumerate(all_flight[1:]):
    flight_code=get_flight_code(one[2])
    print idd,flight_code,'time:',round(time.time()-t0,1)
    # all_flight[idd+1].append(flight_code)
    one.append(flight_code)
    f.write(','.join([str(one[i]).replace('.0','') for i in range(4)])+'\n')
f.close()