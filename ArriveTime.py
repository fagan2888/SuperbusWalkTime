# coding:utf-8
import re
import time
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException



def login():
    driver.get(login_url)
    usrname = driver.find_element_by_name('flightaware_username').send_keys('zikepeng')
    pswd = driver.find_element_by_name('flightaware_password').send_keys('3014159f')
    driver.find_element_by_class_name('actionButton').click()

def output(string):
    f=open(outfile,'a')
    f.write(string)
    f.close()

def trans_time(deptime):
    hour=int(deptime[:2])
    hour+=12
    deptime=str(hour)+deptime[2:]
    return deptime

def timeplus1(arrtime):
    hour=int(arrtime[:2])
    if hour==12:
        hour+=12
    else:
        hour+=24
    arrtime=str(hour)+arrtime[2:]
    return arrtime
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option("prefs",prefs)

# edit the file name to avoid rewrite the origin file
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
outfile='ident_date_new.csv'
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if raw_input('sure to truncate the file>>  '+outfile+'  <<?(y/n)')=='y':
    pass
else:
    print 'exit!'
    sys.exit()

open(outfile,'w').close()
t0=time.time()
login_url = 'https://zh.flightaware.com/account/session'
driver = webdriver.Chrome(chrome_options=chrome_options)
login()


for ident in open('ident_list.txt','r').readlines()[1:]:
    ident=ident.strip()
    print ident,round(time.time()-t0,2)
    url='https://flightaware.com/live/flight/'+ident+'/history/160'
    try:
        driver.get(url)
    except TimeoutException,e:
        print type(e)
    soup=BeautifulSoup(driver.page_source,'lxml')
    for one_day in soup.select('.rowClickTarget'):
        infos=one_day.text.split('\n')
        date=re.findall('2018.*?\d+.*?\d+',infos[1])[0].replace(u'年 ','/').replace(u'月 ','/')
        try:

            deptime=re.findall('\d\d:\d\d',infos[2])[0]
            time_flag=infos[2].find(u'下')
            if time_flag!=-1:
                deptime=trans_time(deptime)
        except:
            deptime=''
        try:
            arrtime=re.findall('\d\d:\d\d',infos[3])[0]
            time_flag=infos[3].find(u'下')
            if arrtime[0:2]=='12':
                arrtime='00'+arrtime[2:]
            if time_flag!=-1:
                arrtime=trans_time(arrtime)
            plus_flag=infos[3].find('+1') #是否到达时间+1天
            if plus_flag!=-1:
                arrtime=timeplus1(arrtime)

        except:
            arrtime=''
        #print date,deptime,arrtime
        outstring=','.join([ident,date,deptime,arrtime])+'\n'
        output(outstring.encode('utf-8'))
driver.quit()


