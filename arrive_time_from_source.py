# coding:utf-8
import re
import time
from bs4 import BeautifulSoup
import sys


def output(string):
    f = open(outfile, 'a')
    f.write(string)
    f.close()


def trans_time(deptime):
    hour = int(deptime[:2])
    hour += 12
    deptime = str(hour) + deptime[2:]
    return deptime


def timeplus1(arrtime):
    hour = int(arrtime[:2])
    if hour == 12:
        hour += 12
    else:
        hour += 24
    arrtime = str(hour) + arrtime[2:]
    return arrtime


def process_time(atime):
    arrtime = re.findall('\d\d:\d\d', atime)[0]
    if arrtime[0:2] == '12':
        arrtime = '00' + arrtime[2:]

    time_flag = atime.find(u'下')  # 是否是下午
    if time_flag != -1:
        arrtime = trans_time(arrtime)

    plus_flag = atime.find('+1')  # 是否到达时间+1天
    if plus_flag != -1:
        arrtime = timeplus1(arrtime)

    if atime.find('?') != -1:
        arrtime = ''

    return arrtime


# edit the file name to avoid rewrite the origin file
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
outfile = 'ident_date_new.csv'
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if raw_input('sure to truncate the file>>  ' + outfile + '  <<?(y/n)') == 'y':
    pass
else:
    print 'exit!'
    sys.exit()

open(outfile, 'w').close()
t0 = time.time()

for ident in open('ident_list.txt', 'r').readlines()[1:]:
    ident = ident.strip()
    print ident, round(time.time() - t0, 2)

    page_source = open('./web_source/' + ident + '.html', 'r').read()
    soup = BeautifulSoup(page_source, 'lxml')
    for one_day in soup.select('.rowClickTarget'):
        infos = one_day.text.split('\n')
        if infos[1].encode('utf-8').find('目的地Chengdu')!=-1:
            date = re.findall('2018.*?\d+.*?\d+', infos[1])[0].replace(u'年 ', '/').replace(u'月 ', '/')
            try:
                deptime = process_time(infos[2])
            except:
                deptime = ''
            try:
                arrtime = process_time(infos[3])
            except:
                arrtime = ''
            # print date,deptime,arrtime
            outstring = ','.join([ident, date, deptime, arrtime]) + '\n'
            output(outstring.encode('utf-8'))
