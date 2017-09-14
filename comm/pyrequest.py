#!usr/bin/env python
#coding: utf-8

# 32位小写md5(明文)
import hashlib
pwd = 'kong1121K'
md5_pwd = hashlib.md5(pwd.encode('utf-8')).hexdigest()

# 流水号ID（生成规则：调用方ID+年月日时分秒毫秒+3位随机数）例如：1012015091611120101001
import datetime,random
t = datetime.datetime.now()
t_id = '101%d%02d%02d%02d%02d%02d%02d%03d' % (t.year,t.month,t.day,t.hour, t.minute, t.second, t.microsecond/10000, random.randint(0,1000))

# 尝试登陆
url = 'http://xinglianconnect-test.380star.com/uic/user/userLogin.do'
para = {
'phone' : '18938884424', #用户ID
'source' : '1',
'macType' : '2',
'clientNum' : '5.1',
'pwd' : md5_pwd,
't_id' : t_id
}
import requests
import json
headers = {'content-type': 'application/json'}
print(para)
r = requests.post(url, data=json.dumps(para), headers=headers)
print(r.text)

