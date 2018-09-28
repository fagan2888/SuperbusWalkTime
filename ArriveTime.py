# coding:utf-8
import re
import time
import xlrd
import sys


def time_swap(timestamp):
    timeStamp = float(timestamp[:-3])
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print otherStyleTime

data = xlrd.open_workbook('2018data.xlsx')
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
print '总行数=', nrows
# for i in range(ncols):
#     print i,table.cell(0,i).value
# 'id	order_time订单时间	book_depart_time订单出发时间	depart_time 最迟出发时间（验票+30min）	service_begin_time	active_time验票时间	onspot_timestamp	offspot_timestamp'

ids = table.col_values(0)
activeTime = table.col_values(16)
flight_num = table.col_values(24)
print map(lambda x, y, z: [x, y, z], ids, activeTime, flight_num)

# timestamp='1530376500000'
# timeStamp = float(timestamp[:-3])
# timeArray = time.localtime(timeStamp)
# otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
# print otherStyleTime
