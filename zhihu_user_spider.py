#！/usr/bin/env python
#-*-coding:utf-8-*-
# chenkehao

import requests
from selenium import webdriver
import time
import re
import queue

USER_url = []
xinxi = {'name': '', '性别': '', '居住地': '', '行业': '', '教育经历': ''}
D_url = queue.Queue('https://www.zhihu.com/people/zhaoyan-vivian/activities')
D_xinxi = queue.Queue()
headres = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0 '}

#用selenium进行半自动登陆知乎
def denglu():
    wd = webdriver.Firefox (executable_path='C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe') #构建浏览器
    wd.get('https://www.zhihu.com/')
    time.sleep(40)
    req = requests.Session() #构建Session
    cookies = wd.get_cookies() #导出cookie
    for cookie in cookies:
        req.cookies.set(cookie['name'], cookie['value'])
    req.headers.clear()
    return req

def cunchu():
    x = D_xinxi.get()
    
#爬取关注userID
def main():
    req = denglu()
    '''从队列中取user链接'''
    url = D_url.get()
    g_z_shudata = req.get(url[1])

    '''采集信息加入队列'''
    xinxi['name'] = re.compile('>(.*?)</span><span class="RichText ProfileHeader-headline"').findall(g_z_shudata)
    xinxi['性别'] = re.compile('class="Icon Icon--(.*?)"').findall(g_z_shudata)
    xinxi['居住地'] = re.compile('&quot;,&quo;type&quot;:&quot;topic&quot;,&quot;excerpt&quot;:&quot;(.*?)'
                              '&quot;,&quot;id&quot;:&quot;').findall(g_z_shudata)
    xinxi['行业'] = re.compile('</g></svg></div><!-- react-text: .*? -->(.*?)<!-- /react-text -->'
                             '<div class="ProfileHeader').findall(g_z_shudata)
    xinxi['教育经历'] = re.compile('586L11 0z"/></g></svg></div><!-- react-text: 119 -->(.*?)<!--').findall(g_z_shudata)
    D_xinxi.put(xinxi)

    '''判断关注者住并请求关注着列表拼接成新的user链接'''
    g_z_shu = re.compile('关注者</div><strong class="NumberBoard-itemValue" title="(.*?)"').findall(g_z_shudata)
    if int(g_z_shu[0]) >= 20:
        ye = int(g_z_shu[0]) // 20
        jishu = 0
        for i in range(ye):
            data = req.get('https://www.zhihu.com/api/v4/members/'+url[0]+'/followers?&offset='+str(jishu)+'&limit='
                           +str(jishu), headers=headres)
            data1 = data.text
            name = re.compile('"url_token": "(.*?)"').findall(data1)
            for i1 in range(len(name)):
                user_url = 'https://www.zhihu.com/people/'+name[i1]+'/activities'
                if USER_url.count(user_url) == 0:
                    USER_url.append(user_url)
                    D_url.put([name, user_url])
    data = req.get('https://www.zhihu.com/api/v4/members/'+url[0]+'/followers?&offset=0&limit=0', headers=headres)
    data1 = data.text
    name = re.compile('"url_token": "(.*?)"').findall(data1)
    for i1 in range(len(name)):
                user_url = 'https://www.zhihu.com/people/'+name[i1]+'/activities'
                if USER_url.count(user_url) == 0:
                    USER_url.append(user_url)
                    D_url.put(user_url)
