# coding:utf-8
import time
import numpy
import datetime
import sys
global tot_none
global wait_time_list

fpsg = open('indent_out.csv', 'r')
fdata = open('ident_date_new.csv', 'r')
ferror = open('error_ident_list.txt', 'w')
fpsgout =open('passenger_wait_time.csv','w')
fpsgout2=open('passenger_wait_time2.csv','w')
# edit the file name to avoid rewrite the origin file
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if raw_input('sure to truncate the file>>  '+'passenger_wait_time.csv'+'  <<?(y/n)')=='y':
    pass
else:
    print 'exit!'
    sys.exit()

def dateminusone(a):
    a_time = datetime.datetime.strptime(a, '%m%d')
    b_time = datetime.timedelta(days=1)
    now = a_time - b_time
    return str(datetime.datetime.strftime(now, '%m%d'))


def get_data():
    data_list = []
    for line in fdata.readlines():
        infos = line.strip().split(',')
        ident = infos[0]
        date = infos[1][5:10].replace('/', '')
        arrive_time = infos[3]
        data_list.append([ident, date, arrive_time])
    return data_list


def time_swap(timestamp):
    timeStamp = float(timestamp)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def get_arrive_time(active_date, ident):
    # print active_date,ident
    ident_flag=0
    for infos in data_list:
        if infos[0] == ident:
            ident_flag=1
            if infos[1] == active_date:
                return str(infos[2])
    if ident_flag==1:
        return 'error'
    else:
        return None


def get_wait_time(active_time, flight_arrive_time, ifpre=0):
    if ifpre != 0:
        flight_arrive_time = str(int(flight_arrive_time[0:2]) - 24).zfill(2) + flight_arrive_time[2:5]
    else:
        pass
    wait_min = (int(active_time[0:2]) - int(flight_arrive_time[0:2])) * 60 + int(active_time[3:]) - int(
        flight_arrive_time[3:])
    print 'waiting_time===========', wait_min
    return wait_min


def previous_day(active_date, active_time, ident):
    global tot_none,wait_time_list
    flight_arrive_time = str(get_arrive_time(dateminusone(active_date).zfill(4), ident))  # 前一天的数据
    # print '到达日期', dateminusone(active_date).zfill(4), '验票日期', active_date
    try:
        wait_time=get_wait_time(active_time, flight_arrive_time,ifpre=1)
        wait_time_list.append(wait_time)
        outstring=wait_time
    except Exception, e:
        # print e, 'cannot get the previous arrive time'
        print '  id=', idd, '\n  ident=', ident, '\n  active_date=', active_date, '\n  active_time=', active_time, '\n  flight_arrive_time=', flight_arrive_time
        print 'can not get the previous arrive time'
        ferror.write(ident + '\n')
        tot_none += 1
        outstring=''
    return outstring


def process_result(wait_time_list):
    print 'tot_num=',len(wait_time_list)
    print 'wait_time_list', wait_time_list
    print 'no ident num=', no_ident_num
    print 'tot_none=', tot_none
    narray = numpy.array(wait_time_list)
    print 'average=', narray.sum() / len(wait_time_list)
    print 'max=', narray.max()

    tot_impossible_num = 0
    new_list = []
    for t in wait_time_list:
        if t < 0 or t > 90:
            tot_impossible_num += 1
        else:
            new_list.append(t)
    print 'error info num=', tot_impossible_num
    print new_list
    l = numpy.array(new_list)
    print 'new_max_waiting_time', l.max()
    print 'new_list_average', l.sum() / len(new_list)


data_list = get_data()
tot_none = 0
wait_time_list = []
no_ident_num = 0
for index,passenger in  enumerate(fpsg.readlines()[1:]):

    idd = passenger.split(',')[0]
    active_timestamp = '%f' % float(passenger.split(',')[1])
    active_date = time_swap(str(active_timestamp)[:10])[5:10].replace('-', '')
    active_time = time_swap(str(active_timestamp)[:10])[11:16]
    ident = passenger.split(',')[3].strip()
    if ident == '':
        no_ident_num += 1
        print 'this passenger do not have ident'
        outstring=''
    else:
        flight_arrive_time = str(get_arrive_time(active_date, ident))  # 飞机到达时间
        if flight_arrive_time == 'None' or flight_arrive_time == '':  # 如果为空,获取前一天
            print 'No airplane ident'
            tot_none += 1
            outstring=''
        elif flight_arrive_time == 'error' or int(active_time[0:2]) - int(flight_arrive_time[0:2]) <= -12:  # 由于0点的原因日期有误
            outstring = previous_day(active_date, active_time, ident)
            if outstring<0 or outstring>90:
                outstring=''

        else:
            wait_time=get_wait_time(active_time, flight_arrive_time, ifpre=0)
            wait_time_list.append(wait_time)
            outstring = wait_time
            if outstring<0 or outstring>90:
                outstring=''
    if outstring!='':
        fpsgout2.write(','.join([idd, active_date, active_time.replace(':',','), str(outstring)]) + '\n')
    fpsgout.write(','.join([idd,active_date,active_time.replace(':',','),str(outstring)])+'\n')

ferror.close()
fpsgout.close()
fpsgout2.close()
process_result(wait_time_list)

