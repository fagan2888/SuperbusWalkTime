import time

fpsg=open('indent_out.csv','r')
fdata=open('ident_date.csv','r')

def get_data():
    data_list=[]
    for line in fdata.readlines():
        infos=line.strip().split(',')
        ident=infos[0]
        date=infos[1][5:10].replace('/','')
        arrive_time=infos[3]
        data_list.append([ident,date,arrive_time])
    return data_list

def time_swap(timestamp):
    timeStamp = float(timestamp)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def get_arrive_time(active_date, ident):
    #print active_date,ident
    for infos in data_list:
        if infos[0]==ident and infos[1]==active_date:
            print infos[2]
            return str(infos[2])

data_list=get_data()
for passenger in fpsg.readlines()[1:]:
    idd=passenger.split(',')[0]
    active_timestamp = '%f' % float(passenger.split(',')[1])
    active_date= time_swap(str(active_timestamp)[:10])[5:10].replace('-', '')
    active_time= time_swap(str(active_timestamp)[:10])[11:16]
    ident=passenger.split(',')[3].strip()
    print ident
    flight_arrive_time=str(get_arrive_time(active_date, ident))
    print 'active_date=',active_date,'active_time=',active_time,'flight_arrive_time=',flight_arrive_time

    # atime = time.strptime(flight_arrive_time,"%H:%M")
    # print atime

