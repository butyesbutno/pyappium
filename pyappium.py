#!/usr/bin/env python
#coding: utf-8
import gettext

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# email: michael.wangh@gmail.com

import os,sys,unittest,datetime
import argparse
from comm import *
from config import *

__author__ = "Michael Wang"
__version__ = "0.1.0"

# window platform or linux platform
import platform
iswindow = platform.platform().find("Window")>=0
encodestr = "utf-8"
if iswindow:
	encodestr = "gbk"

if __name__ == "__main__":

	# multi-lang / chinese-han
	gettext.install('lang', './locale')
	gettext.translation('lang', './locale', languages=['cn']).install(True)

	# 获取命令行参数 / obtain the commandline parameters
	ap = argparse.ArgumentParser()
	ap.add_argument("-r", "--remove_suite", required = False, help = "Specify removed testsuit")
	ap.add_argument("-d", "--device", required = False, help = "Specify device name(if not, auto detect)")
	ap.add_argument("-a", "--app", required = False, help = "Install app file name")
	ap.add_argument("-p", "--appium_port", required = False, help = "Start new appium with the port")
	args = vars(ap.parse_args())

	title = u'自动化测试报告'
	description = u'用例执行情况'
	deviceName = args['device']
	appName = args['app']
	autoAppium = args['appium_port']
	if autoAppium:
		AppiumServer = 'http://127.0.0.1:%s/wd/hub' % autoAppium
	remove_suite = args['remove_suite']
	remove_suite_list = None
	if remove_suite != None:
		remove_suite_list = remove_suite.split(',')

	# 获取当前正在链接的设备 / the connected mobile phone
	if deviceName == None :
		devlst = pyLib.getConnectAndroidDevices()
		if(len(devlst) >0):
			deviceName = devlst[0]
	if deviceName != None :
		desired_caps['deviceName']=deviceName
		devDesc = pyLib.getAndroidDevProp(deviceName)
		print("Run test on %s. Brand/Model %s" % (deviceName, devDesc))
	else:
		devDesc = ""
		deviceName = ""

	# 上一级基准目录 / the base path
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	
	# 是否指定了app文件以及路径 / Does the apk exist?
	if appName != None:
		desired_caps['app']=BASE_DIR + '/apps/' + appName
		if(os.path.exists(desired_caps['app']) == False):
			print(u'%s %s' % (desired_caps['app']), _('Not Exist'))
			exit(0)

	# 生成测试报告目录 / create the test report directory
	reportpath = BASE_DIR + '/report/' + CurAppName
	# reportpath: utf8 -> gbk(windows system)
	if sys.version_info.major < 3 and iswindow:
		reportpath = reportpath.decode('utf-8').encode(encodestr)
	try:
		os.mkdir(reportpath)
	except:
		pass
	reportpath += '/report.html'

	# 执行../testcase/CurAppName/以及子目录测试用例 / execute testcases under ../testcase/CurAppName/
	basepath = BASE_DIR + "/testcase/" + CurAppName
	# basepath: utf8 -> gbk(windows system)
	if sys.version_info.major < 3 and iswindow:
		basepath = basepath.decode('utf-8').encode(encodestr)
	suit = unittest.TestSuite()

	# 构建所有xml格式的测试用例 / build all testcase write by xml
	xml_testcases = pyLib.walkXmlFiles(basepath + "/xml/", remove_suite_list)
	suit.addTests(makeXmlSuite(xml_testcases))

	# 查找所有python格式的用例 / build all testcase write by python code
	py_testcases = pyLib.walkPyFiles(basepath + "/pycode/", remove_suite_list)
	basepath_len = len(BASE_DIR)+1
	for pyfile in py_testcases:
		pyfile = pyfile[basepath_len:-3]
		pyfile = pyfile.replace('/', '.')
		pyfile = pyfile.replace('\\', '.')
		pyfile = pyfile.replace('\\\\', '.')
		suit.addTests(unittest.defaultTestLoader.loadTestsFromName(pyfile))

	# 查找所有json格式的用例 / build all testcase write by json
	json_testcases = pyLib.walkJsonFiles(basepath + "/json/")
	suit.addTests(makeJsonSuite(json_testcases))

	# has no tests?
	if suit.countTestCases() < 1 :
		print(_('No testcase'));
		exit(0)

	# execute the test case
	fp = open(reportpath, 'wb')	
	runner = HTMLTestRunner(stream=fp, title=title, description=description)
	runner.run(suit, devDesc+deviceName)
	fp.close()

