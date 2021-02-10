# -*- coding: UTF-8 -*-
import requests
import time
from bs4 import BeautifulSoup
import datetime
import json
import execjs
import pathlib
import os
import random
import sys
import io

def setup_io():
    sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)
setup_io()

def getIpdp(username, password):
     url = 'https://authserver.nuist.edu.cn/authserver/login?service=http%3A%2F%2Fauthserver.nuist.edu.cn%2Fauthserver%2Findex.do'
     header = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
         'DNT': '1',
         'Host': 'authserver.nuist.edu.cn',
         'Origin': 'https://authserver.nuist.edu.cn',
         'Referer': 'https://authserver.nuist.edu.cn/authserver/login?service=http%3A%2F%2Fauthserver.nuist.edu.cn%2Fauthserver%2Findex.do'
     }
     s = requests.Session()
     r = s.get(url, timeout=5)
     htmlTextOri = r.text
     html = BeautifulSoup(htmlTextOri, 'lxml')
     pwdEncryptSalt = html.find(id='pwdEncryptSalt')['value']
     execution = html.find(id='execution')['value']
     cookies = r.cookies
     # print(cookies.values())
     with open('./encrypt.js', 'r', encoding="utf-8") as f:
         script = f.read()
     encrypt = execjs.compile(script)
     encodedPassword = encrypt.call(
         'encryptPassword', password, pwdEncryptSalt)
     # print(encodedPassword)
     data = {
         'username': username,
         'password': encodedPassword,
         'captcha': '',
         '_eventId': 'submit',
         'cllt': 'userNameLogin',
         'lt': '',
         'execution': execution,
     }
     r2 = s.post(url, data=data, cookies=cookies,
                 headers=header, timeout=5, allow_redirects=False)
     targetCookie = r2.cookies.get_dict()['iPlanetDirectoryPro']
     print(targetCookie)
     return(targetCookie)

# 运行前检查服务器正常吗
print(time.strftime('%Y-%m-%d %H:%M:%S'))
print('检查学校服务器状态...')
try:
    testSvr = requests.get('http://e-office2.nuist.edu.cn/', timeout=3).text
    testSvr = requests.get('http://authserver.nuist.edu.cn', timeout=10).text
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print('服务器正常，正在登陆')
except requests.exceptions.RequestException as e:
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print("学校服务器崩了，请联系辅导员")
    exit(0)
username = '请修改此处为姓名'
password = '请修改此处为密码'
print(time.strftime('%Y-%m-%d %H:%M:%S'))
s = requests.Session()
url = 'http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start'
cookies = dict(iPlanetDirectoryPro=getIpdp(username, password))
print(cookies)
r1 = s.get(url, cookies=cookies, timeout=5)
cookieNew = r1.cookies
htmlTextOri = r1.text
html = BeautifulSoup(htmlTextOri, 'lxml')
tar1 = str(html.find_all('meta')[3])
csrfToken = tar1.split('"')[1]
url2 = 'http://e-office2.nuist.edu.cn/infoplus/interface/start'
data2 = {'idc': 'XNYQSB',
         'release': '',
         'csrfToken': csrfToken,
         'formData': '{"_VAR_URL":"http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start","_VAR_URL_Attr":"{}"}'
         }
header2 = {'Referer': 'http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
           'Origin': 'http://e-office2.nuist.edu.cn',
           }
r2 = s.post(url2, data=data2, cookies=cookieNew,
            headers=header2, timeout=5)
targetUrl = json.loads(r2.text)['entities'][0]
stepId = int(targetUrl.split('/')[-2])
rand = str(random.random() * 1000)
t2 = int(time.time())
PostData = {
                    'stepId': stepId,
                    'instanceId': '',
                    'admin': False,
                    'rand': rand,
                    'width': '1920',
                    'lang': 'zh',
                    'csrfToken': csrfToken
                }
recvUrl = "http://e-office2.nuist.edu.cn/infoplus/interface/render"
temp = s.post(recvUrl, data=PostData, headers=header2, timeout=15)
selfData = temp.json()
recvData = selfData['entities'][0]['data']
recvData["_VAR_ENTRY_NAME"] = "学生健康状况申报"
recvData["_VAR_ENTRY_TAGS"] = "学工部"
recvData["_VAR_URL"] = targetUrl
recvData["fieldCNS"] = True
recvData["fieldCXXXfxxq"] = "1"
recvData["fieldCXXXfxxq_Name"] = "南京校区"
recvData["fieldSTQKfrtw"] = str(random.randint(355, 365) / 10).ljust(3, '0')[:4]
listNextUrl = 'http://e-office2.nuist.edu.cn/infoplus/interface/listNextStepsUsers'
postData2 = {
    'stepId': stepId,
    'actionId': 1,
    'formData': str(recvData),
    'timestamp': t2,
    'rand': 185.43415117494698,
    'boundFields': 'fieldCXXXjtgjbc,fieldMQJCRxh,fieldCXXXsftjhb,fieldSTQKqt,fieldSTQKglsjrq,fieldYQJLjrsfczbldqzt,fieldCXXXjtfsqtms,fieldCXXXjtfsfj,fieldJBXXjjlxrdh,fieldJBXXxm,fieldJBXXjgsjtdz,fieldCXXXsftjhbss,fieldSTQKfrtw,fieldMQJCRxm,fieldCXXXsftjhbq,fieldSTQKqtms,fieldCXXXjtfslc,fieldJBXXlxfs,fieldJBXXxb,fieldCXXXjtfspc,fieldYQJLsfjcqtbl,fieldCXXXssh,fieldJBXXgh,fieldCNS,fieldYC,fieldSTQKfl,fieldCXXXsftjwh,fieldCXXXfxxq,fieldSTQKdqstzk,fieldSTQKhxkn,fieldSTQKqtqksm,fieldFLid,fieldYQJLjrsfczbl,fieldJBXXjjlxr,fieldCXXXfxcfsj,fieldMQJCRcjdd,fieldSQSJ,fieldSTQKfrsjrq,fieldSTQKks,fieldJBXXcsny,fieldSTQKgm,fieldJBXXnj,fieldCXXXjtzzq,fieldJBXXJG,fieldCXXXdqszd,fieldCXXXjtzzs,fieldSTQKfx,fieldSTQKfs,fieldCXXXjtfsdb,fieldCXXXcxzt,fieldCXXXjtfshc,fieldCXXXjtjtzz,fieldCXXXsftjhbs,fieldJBXXsfzh,fieldSTQKsfstbs,fieldCXXXcqwdq,fieldJBXXfdygh,fieldJBXXjgshi,fieldJBXXfdyxm,fieldWXTS,fieldCXXXjtzz,fieldJBXXjgq,fieldCXXXjtfsqt,fieldJBXXjgs,fieldSTQKfrsjsf,fieldSTQKglsjsf,fieldJBXXdw,fieldCXXXsftjhbjtdz,fieldMQJCRlxfs',
    'csrfToken': csrfToken,
    'lang': 'zh',
}
r22 = s.post(listNextUrl, data=postData2, timeout=15)
url3 = 'http://e-office2.nuist.edu.cn/infoplus/interface/doAction'
secondData = {
                    'actionId': '1',
                    'formData': str(recvData),
                    'remark': '',
                    'rand': 185.43415117494698,
                    'nextUsers': "{}",
                    'stepId': stepId,
                    'timestamp': t2,
                    'boundFields': 'fieldCXXXjtgjbc,fieldMQJCRxh,fieldCXXXsftjhb,fieldSTQKqt,fieldSTQKglsjrq,fieldYQJLjrsfczbldqzt,fieldCXXXjtfsqtms,fieldCXXXjtfsfj,fieldJBXXjjlxrdh,fieldJBXXxm,fieldJBXXjgsjtdz,fieldSTQKfrtw,fieldMQJCRxm,fieldCXXXsftjhbq,fieldSTQKqtms,fieldCXXXjtfslc,fieldJBXXlxfs,fieldJBXXxb,fieldCXXXjtfspc,fieldYQJLsfjcqtbl,fieldCXXXssh,fieldJBXXgh,fieldCNS,fieldYC,fieldSTQKfl,fieldCXXXsftjwh,fieldCXXXfxxq,fieldSTQKdqstzk,fieldSTQKhxkn,fieldSTQKqtqksm,fieldFLid,fieldYQJLjrsfczbl,fieldJBXXjjlxr,fieldCXXXfxcfsj,fieldMQJCRcjdd,fieldSQSJ,fieldSTQKfrsjrq,fieldSTQKks,fieldJBXXcsny,fieldSTQKgm,fieldJBXXnj,fieldCXXXjtzzq,fieldJBXXJG,fieldCXXXdqszd,fieldCXXXjtzzs,fieldSTQKfx,fieldSTQKfs,fieldCXXXjtfsdb,fieldCXXXcxzt,fieldCXXXjtfshc,fieldCXXXjtjtzz,fieldCXXXsftjhbs,fieldJBXXsfzh,fieldSTQKsfstbs,fieldCXXXcqwdq,fieldJBXXfdygh,fieldJBXXjgshi,fieldJBXXfdyxm,fieldWXTS,fieldCXXXjtzz,fieldJBXXjgq,fieldCXXXjtfsqt,fieldJBXXjgs,fieldSTQKfrsjsf,fieldSTQKglsjsf,fieldJBXXdw,fieldCXXXsftjhbjtdz,fieldMQJCRlxfs',
                    'csrfToken': csrfToken,
                    'lang': 'zh'
                }
r3 = s.post(url3, data=secondData, timeout=15)
print(time.strftime('%Y-%m-%d %H:%M:%S'))
print('成功！')