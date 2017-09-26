#!/usr/bin/env python
#coding: utf-8

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

from appium.webdriver.mobilecommand import MobileCommand
from xml.etree import ElementTree
import time,sys,os,unittest,subprocess

__author__ = "Michael Wang"
__version__ = "0.1.0"

# chrome://inspect/#devices
# print driver.contexts
# maybe
def switch_h5(driver, webview_content):
	driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": webview_content})
def switch_app(driver):
	driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "NATIVE_APP"})
def switch_context(driver):
	driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": webview_content})

# 获取相连的安卓机器名称
def getConnectAndroidDevices():
	devlst = []
	subp = subprocess.Popen('adb devices',shell=True,stdout=subprocess.PIPE)
	l = subp.stdout.readline()
	while True:
		l = subp.stdout.readline().decode('utf-8')
		if l == None or len(l) == 0:
			break
		if len(l) > 2 and l.startswith('*') == False:
			list = l.split('\t')
			devlst.append( list[0] )
	subp.wait()
	return devlst

# 获取相连的安卓机器品牌/型号
def getAndroidDevProp(deviceName):
	brandAndModelStr = ""
	subp = subprocess.Popen( 'adb -s ' + deviceName + ' shell getprop | findstr product',shell=True,stdout=subprocess.PIPE)
	l = subp.stdout.readline()
	while True:
		l = subp.stdout.readline().decode('utf-8')
		if l == None or len(l) == 0:
			break

		if l.startswith('[ro.product.brand]') :
			brandAndModelStr += l.split(':')[1]
		if l.startswith('[ro.product.model]') :
			brandAndModelStr += l.split(':')[1]
	subp.wait()
	brandAndModelStr = brandAndModelStr.replace('\r', '')
	brandAndModelStr = brandAndModelStr.replace('\n', '')
	return brandAndModelStr

# find_element_by_id may throw exception
def getElement(driver, resId):
	try:
		return driver.find_element_by_id(resId)
	except:
		return None

# try find element, waitting for
def tryGetElement(driver, resId, waittingsecond=10):
	if (waittingsecond<1):
		waittingsecond = 1
	for i in range(waittingsecond):
		ele = getElement(driver, resId)
		if ele:
			return ele
		else:
			time.sleep(1)
	return None

# find_elements_by_id may throw exception, return a list
def getElements(driver, resId):
	try:
		return driver.find_elements_by_id(resId)
	except:
		return None

# find_element_by_xpath
def getElementByXPath(driver, inxpath):
	try:
		return driver.find_element_by_xpath(inxpath)
	except:
		return None

# try find element xpath, waitting for
def tryGetElementByXPath(driver, inxpath, waittingsecond=10):
	if (waittingsecond<1):
		waittingsecond = 1
	for i in range(waittingsecond):
		ele = getElementByXPath(driver, inxpath)
		if ele:
			return ele
		else:
			time.sleep(1)
	return None

# find_element_by_name
def getElementByName(driver, inname):
	try:
		return driver.find_element_by_name(inname)
	except:
		return None

# try find element name, waitting for
def tryGetElementByName(driver, inname, waittingsecond=10):
	if (waittingsecond<1):
		waittingsecond = 1
	for i in range(waittingsecond):
		ele = getElementByName(driver, inname)
		if ele:
			return ele
		else:
			time.sleep(1)
	return None

# 清除EditText文本框里的内容，@param:text 要清除的内容
def edittextclear(driver, text):
	driver.keyevent(123)
	for i in range(0,len(text)):
		driver.keyevent(67)

# driver.set_value(passwdview, passwd)
def setTextValue(element, val):
	try:
		# appium 1.4
		element.send_keys(val)
		return
	except:
		pass
	try:
		# appium 1.6
		element.set_value(val)
	except:
		pass

#获得机器屏幕大小x,y / the screen size
def getScreenSize(driver):
	x = driver.get_window_size()['width']
	y = driver.get_window_size()['height']
	return (x, y)

# 相对滑动
def swipeRelative(driver, ratioX1, ratioY1, ratioX2, ratioY2, t):
	l = getScreenSize(driver)
	x1 = int(l[0] * ratioX1)	#x坐标
	y1 = int(l[1] * ratioY1)	#起始y坐标
	x2 = int(l[1] * ratioX2)	#终点x坐标
	y2 = int(l[1] * ratioY2)	#终点y坐标
	driver.swipe(x1, y1, x2, y2,t)

#屏幕向上滑动
def swipeUp(driver, t):
	l = getScreenSize(driver)
	x1 = int(l[0] * 0.5)  	#x坐标
	y1 = int(l[1] * 0.75)   #起始y坐标
	y2 = int(l[1] * 0.25)   #终点y坐标
	driver.swipe(x1, y1, x1, y2,t)
	
#屏幕向下滑动
def swipeDown(driver, t):
	l = getScreenSize(driver)
	x1 = int(l[0] * 0.5)  #x坐标
	y1 = int(l[1] * 0.25)   #起始y坐标
	y2 = int(l[1] * 0.75)   #终点y坐标
	driver.swipe(x1, y1, x1, y2,t)

#屏幕向左滑动
def swipLeft(driver, t):
	l = getScreenSize(driver)
	x1 = int(l[0]*0.75)
	y1 = int(l[1]*0.5)
	x2 = int(l[0]*0.05)
	driver.swipe(x1,y1,x2,y1,t)

#屏幕向右滑动
def swipRight(driver, t):
	l = getScreenSize(driver)
	x1 = int(l[0]*0.05)
	y1 = int(l[1]*0.5)
	x2 = int(l[0]*0.75)
	driver.swipe(x1,y1,x2,y1,t)

# python 2.7 / 3.x generator has difference
def generatorGetNext(v):
	if (sys.version_info.major < 3) :
		return v.next()
	return next(v)

# 遍历目录下所有xml类型文件
# rootDir=d:/testcast/
def walkXmlFiles(rootDir, exclude_relative_path_list):
	xmllst = []
	for root,dirs,files in os.walk(rootDir):
		for file in files:

			if(file.lower().endswith('.xml') == False):
				continue

			if exclude_relative_path_list!=None :
				suite_not_include = False
				for exclude_path in exclude_relative_path_list:
					if file == exclude_path :
						suite_not_include = True
						break
				if suite_not_include :
					continue

			xmllst.append(os.path.join(root,file))
		for dir in dirs:
			lst = walkXmlFiles(dir, exclude_relative_path_list)
			if lst is not None:
				xmllst += lst
	return xmllst

# 遍历目录下所有test*.py类型文件
# rootDir=d:/testcast/ ext='.py'
def walkPyFiles(rootDir, exclude_relative_path_list):
	pylst = []
	for root,dirs,files in os.walk(rootDir):
		for file in files:
			if file.startswith('test') == False:
				continue
			if(file.lower().endswith('.py') == False):
				continue

			if exclude_relative_path_list!=None :
				suite_not_include = False
				for exclude_path in exclude_relative_path_list:
					if file == exclude_path :
						suite_not_include = True
						break
				if suite_not_include :
					continue

			pylst.append(os.path.join(root,file))
		for dir in dirs:
			lst = walkPyFiles(dir, exclude_relative_path_list)
			if lst is not None:
				pylst += lst
	return pylst


# 遍历目录下所有json类型目录
def walkJsonFiles(rootDir):
	jsonlst = []
	for root,dirs,files in os.walk(rootDir):
		for file in files:

			if(file.lower().endswith('.json') == False):
				continue

			jsonlst.append(root)
			break
		for dir in dirs:
			lst = walkJsonFiles(dir)
			if lst is not None:
				jsonlst += lst
	return jsonlst