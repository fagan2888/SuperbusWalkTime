#coding:utf-8
import datetime
fdata=open('ident_date_new.csv','r')


flight_time_list=[]
def get_data():
    data_list = []
    for line in fdata.readlines():
        infos = line.strip().split(',')
        ident = infos[0]
        date = infos[1][5:10].replace('/', '')
        time_delta = datetime.timedelta(days=1)
        print infos[2],infos[3]
        if infos[3]!='' and infos[2]!='':#去掉有缺失数据的
            try:
                arrive_time = datetime.datetime.strptime(infos[3],'%H:%M') # 到达时间转换为时间格式
            except:
                #  如果无法转换，说明时间大于24个小时，减去24个小时
                arrive_time = datetime.datetime.strptime(str(int(infos[3][:2])-24)+infos[3][2:],'%H:%M')
            deptime=datetime.datetime.strptime(infos[2],'%H:%M')

            time0=datetime.datetime.strptime('2018,00:00','%Y,%M:%S')
            flighttime=datetime.datetime.strftime(time0+(arrive_time-deptime),'%H%M')
            flighttime= int(flighttime[:2])*60+int(flighttime[2:])
            if flighttime>1000:
                print ident,date
                print deptime,arrive_time
                raw_input()
            flight_time_list.append(flighttime)
            #data_list.append([ident, date, arrive_time])
get_data()

print flight_time_list