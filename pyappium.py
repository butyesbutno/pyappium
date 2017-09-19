#!/usr/bin/env python
#coding: utf-8
#python 2.7 / 3.X

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

import os,sys,unittest,subprocess,datetime
import argparse
from comm import *
from config import *
from docopt import docopt
from xml.etree import ElementTree

__author__ = "Michael Wang"
__version__ = "0.1.0"

if __name__ == "__main__":
	
	# 获取命令行参数 / obtain the commandline parameters
	ap = argparse.ArgumentParser()
	ap.add_argument("-r", "--remove_suite", required = False,
	help = "Specify removed testsuit")
	ap.add_argument("-d", "--device", required = False,
	help = "Specify device name(if not, auto detect)")
	ap.add_argument("-a", "--app", required = False,
	help = "Install app file name")
	args = vars(ap.parse_args())

	title = u'自动化测试报告'
	description = u'用例执行情况'
	deviceName = args['device']
	appName = args['app']
	remove_suite = args['remove_suite']
	remove_suite_list = None
	if remove_suite != None:
		remove_suite_list = remove_suite.split(',')

	# 获取当前正在链接的设备 / the connected mobile phone
	if deviceName == None :
		subp = subprocess.Popen('adb devices',shell=True,stdout=subprocess.PIPE)
		l = subp.stdout.readline()
		l = subp.stdout.readline()
		if l and len(l) > 2:
			list = l.split(b'\t')
			deviceName = list[0].decode('utf-8')
		subp.wait()
	if deviceName == None :
		print(u"当前没有设备链接")
		exit(0)
	desired_caps['deviceName']=deviceName
	print("Run test on %s" % deviceName)
	
	# 上一级基准目录 / the base path
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	
	# 是否指定了app文件以及路径 / Does the apk exist?
	if appName != None:
		desired_caps['app']=BASE_DIR + '/apps/' + appName
		if(os.path.exists(desired_caps['app']) == False):
			print(u'%s 不存在' % desired_caps['app'])
			exit(0)

	# 生成测试报告目录 / create the test report directory
	reportpath = BASE_DIR + '/report/'
	try:
		os.mkdir(reportpath)
	except:
		pass
	t = datetime.datetime.now()
	#reportpath += "report-" + '%d-%02d-%02d-%02d-%02d-%02d' % (t.year,t.month,t.day,t.hour, t.minute, t.second) + '.html'
	reportpath += 'report.html'

	# 执行../testcase/CurAppName/以及子目录测试用例 / execute testcases under ../testcase/CurAppName/
	basepath = BASE_DIR + "/testcase/" + CurAppName
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

	# execute the test case
	fp = open(reportpath, 'wb')	
	runner = HTMLTestRunner(stream=fp, title=title, description=description)
	runner.run(suit, deviceName)
	fp.close()

