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

import argparse, os
import multiprocessing, subprocess
from comm import *

__author__ = "Michael Wang"
__version__ = "0.1.0"

# window platform or linux platform
import platform
iswindow = platform.platform().find("Window")>=0
encodestr = "utf-8"
if iswindow:
	encodestr = "gbk"
	
# 在每一个设备上面运行测试用例 / run testcase on each device
# python pyappium -d emulator-5554
def StartTestRunner(*args):
	subp = subprocess.Popen(args[0],shell=True,stdout=subprocess.PIPE)
	while True:
		l = subp.stdout.readline().decode(encodestr)
		l = l.rstrip('\n')
		l = l.rstrip('\r')
		if l == None or len(l) == 0:
			break
		print(l)
	subp.wait()
	
if __name__ == "__main__":
	
	# 获取命令行参数 / obtain the commandline parameters
	ap = argparse.ArgumentParser()
	ap.add_argument("-r", "--remove_suite", required = False, help = "Specify removed testsuit")
	ap.add_argument("-a", "--app", required = False, help = "Install app file name")

	args = vars(ap.parse_args())
	appName = args['app']
	remove_suite = args['remove_suite']

	# 获取当前正在链接的设备 / the connected mobile phone
	devlst = pyLib.getConnectAndroidDevices()
	if len(devlst) == 0:
		print(u"当前没有设备链接")
		exit(0)

	# kill all previously appium
	os.system('taskkill /IM Appium.exe /F')

	# 开启测试
	jobs = []
	appiumPort = 4723
	for dev in devlst:
		argstr = "python pyappium.py -p %d -d %s" % (appiumPort, dev)
		if appName:
			argstr += " -a %s"%appName
		if remove_suite:
			argstr += " -r %s"%remove_suite
		service = multiprocessing.Process(name=dev, target=StartTestRunner, args=(argstr,))
		jobs.append(service)
		service.start()

		# 启动 Appium server
		appiumstr = 'appium -p %d -bp %d -U %s' % (appiumPort, appiumPort+1, dev)
		subp = subprocess.Popen(appiumstr,shell=True,stdout=subprocess.PIPE)
		appiumPort += 2
		
	# waitting
	for job in jobs:
		job.join()

