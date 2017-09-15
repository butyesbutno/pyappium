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

"""python app test framework

Usage:
	pyappium (-h | --help)
	pyappium [<desc>] [<title>]
	pyappium [<desc>] [<title>] -r <remove_suite> -d <deviceName> -a <appName>
	pyappium -r <remove_suite>
	pyappium -d <deviceName>
	pyappium -a <appName>
	
Options:
	-h,--help   显示帮助菜单
	-r,--remove 移除特定目录下用例 login,h5移除login,h5目录的测试
	-d,--device 设置所链接的真机，不设置将自动检测
	-a,--app    app文件名，位于apps/

Example:
	pyappium 
	pyappium 自动化测试报告 用例执行情况 
	pyappium -r login,h5
"""
import os,sys,unittest,subprocess,datetime
from comm import HTMLTestRunner, pyconfig
from docopt import docopt
from xml.etree import ElementTree

__author__ = "Michael Wang"
__version__ = "0.1.0"

if __name__ == "__main__":
	
	# 获取命令行参数
	if sys.version_info.major > 2:
		arguments = docopt(__doc__)
	else:
		arguments = docopt(__doc__.decode('utf8'))
	title = arguments.get('<title>')
	description = arguments.get('<desc>')
	deviceName = arguments.get('<deviceName>')
	appName = arguments.get('<appName>')
	remove_suite = arguments.get('<remove_suite>')
	remove_suite_list = None
	if title == None:
		title = u'自动化测试报告'
	if description == None:
		description = u'用例执行情况'
	if remove_suite != None:
		remove_suite_list = remove_suite.split(',')

	# 获取当前正在链接的设备
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
	pyconfig.desired_caps['deviceName']=deviceName
	print("Run test on %s" % deviceName)
	
	# 上一级基准目录
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	
	# 是否指定了app文件以及路径
	if appName != None:
		pyconfig.desired_caps['app']=BASE_DIR + '/apps/' + appName
		if(os.path.exists(pyconfig.desired_caps['app']) == False):
			print(u'%s 不存在' % pyconfig.desired_caps['app'])
			exit(0)

	# 生成测试报告目录
	reportpath = BASE_DIR + '/report/'
	try:
		os.mkdir(reportpath)
	except:
		pass
	t = datetime.datetime.now()
	#reportpath += "report-" + '%d-%02d-%02d-%02d-%02d-%02d' % (t.year,t.month,t.day,t.hour, t.minute, t.second) + '.html'
	reportpath += 'report.html'

	# 执行../testcase/以及子目录测试用例
	basepath = BASE_DIR + "/testcase/"
	tests = unittest.suite.TestSuite()
	for filename in os.listdir(basepath):
	
		# 每一个子目录测试用例都要执行，生成相应的测试报告html形式
		childpath = os.path.join(basepath, filename)
		if os.path.isdir(childpath):

			# 此目录暂时不参加测试?
			try:
				if remove_suite_list != None and remove_suite_list.index(filename) >= 0:
					continue;
			except:
				pass

			# find the test case under childpath
			newtestsuit = unittest.TestLoader()
			tests.addTests( newtestsuit.discover(start_dir=childpath, pattern='test*.py', top_level_dir=None) )
			
		else:
			continue

	# execute the test case
	fp = open(reportpath, 'wb')	
	runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=title, description=description)
	runner.run(tests, deviceName)
	fp.close()

	# execute xml format testcase
    root = ElementTree.parse("e:/test.xml")
    testcases = root.findall("testcase")

    i = 0
    suit = unittest.TestSuite()
    for testcaseNode in testcases:
        a = XmlTest(testcaseNode)
        setattr(xmlttt, "test" + str(i), a.testXml())
        suit.addTests(unittest.makeSuite(xmlttt))
    unittest.TextTestRunner().run(suit)