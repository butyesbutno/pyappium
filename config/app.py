#!/usr/bin/env python
#coding: utf-8

'''
app.py 作为当前测试配置 / app.py as the valid configuration
app2.py 可以理解为另一个app的测试配置，需要的时候修改为app.py即可 
app2.py is test configuration of another app, change to app.py if you want to run it
'''

desired_caps = {
		'appPackage': 'com.xxx',
		'appActivity': 'com.xxx.MainActivity',
		'platformName': 'Android',
		'platformVersion': '5.1',
		'deviceName': 'TBSDU1551002798',#实时通过adb获取 / obtain over adb realtime
		'unicodeKeyboard': 'True',
		'resetKeyboard':'True'
	}

mysql_config = {
    "host": "172.30.2.28",
    "user": "test_user",
    "passwd": "SjFuyBpuHBJnHiFT",
    "port": 18806,
    "db": "uic"
    }
	
# 请确保此名称可以创建目录，将仅仅运行testcase/星链生活V370/目录下面的测试用例
# Please make sure of CurAppName can mkdir, we will only run testcase under testcase/"CurAppName"/ 
CurAppName = "yourapp"

# 默认appium server
AppiumServer = 'http://127.0.0.1:4723/wd/hub'

__all__=["desired_caps", "CurAppName", "AppiumServer", "mysql_config"]