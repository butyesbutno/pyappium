#!/usr/bin/env python
#coding: utf-8

#Apache License
#Version 2.0, January 2004
#http://www.apache.org/licenses/

from appium.webdriver.mobilecommand import MobileCommand
import time

__author__ = "Michael Wang"
__version__ = "0.1.0"

# https://github.com/appium/sample-code/blob/master/sample-code/examples/python/android_webview.py

# chrome://inspect/#devices
# print driver.contexts
# http://blog.csdn.net/wyb199026/article/details/50958662
'''
['NATIVE_APP', 'WEBVIEW_com.hele.buyer:remote', 'WEBVIEW_com.hele.buyer:pushservice', 'WEBVIEW_com.hele.buyer', 'WEBVIEW_com.hele.seller2', 'WEBVIEW_com.hele.seller2:pushservice']
[u'NATIVE_APP', u'WEBVIEW_com.hele.buyer', u'WEBVIEW_com.android.browser']
'''
# maybe
def switch_h5(driver, webview_content):
	driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": webview_content})
def switch_app(driver):
	driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "NATIVE_APP"})

# 内部函数，防止find_element_by_id异常
def getElement(driver, inname):
	try:
		ele = driver.find_element_by_id(inname)
		return ele
	except:
		return None

# 内部函数，防止find_elements_by_id异常, return a list
def getElements(driver, inname):
	try:
		ele = driver.find_elements_by_id(inname)
		return ele
	except:
		return None

# 尝试获取元素
def tryGetElement(driver, inname):
	for i in range(8):
		ele = getElement(driver, inname)
		if ele:
			return ele
		else:
			time.sleep(1)
	return None
		
# 尝试获取元素列表
def tryGetElements(driver, inname):
	for i in range(8):
		ele_list = getElements(driver, inname)
		if ele_list != None and len(ele_list) > 0:
			return ele_list
		else:
			time.sleep(1)
	return None

def getElementByXPath(driver, inxpath):
	try:
		ele = driver.find_element_by_xpath(inxpath)
		return ele
	except:
		return None

# 尝试获取元素列表
def tryGetElementByXPath(driver, inxpath):
	for i in range(8):
		ele = getElementByXPath(driver, inxpath)
		if ele != None:
			return ele
		else:
			time.sleep(1)
	return None

# 清除EditText文本框里的内容，@param:text 要清除的内容
def edittextclear(driver, text):
	driver.keyevent(123)       
	for i in range(0,len(text)):
		driver.keyevent(67)

#获得机器屏幕大小x,y
def getScreenSize(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)
 
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
	
# Copy from appium.io
def test_webview(self):
	if (PLATFORM_VERSION == '4.4'):
		button = self.driver.find_element_by_accessibility_id('buttonStartWebviewCD')
	else:
		button = self.driver.find_element_by_name('buttonStartWebviewCD')
	button.click()

	self.driver.switch_to.context('WEBVIEW_0')

	input_field = self.driver.find_element_by_id('name_input')
	sleep(1)
	input_field.clear()
	input_field.send_keys('Appium User')
	input_field.submit()

	# test that everything is a-ok
	source = self.driver.page_source
	self.assertNotEqual(-1, source.find('This is my way of saying hello'))
	self.assertNotEqual(-1, source.find('"Appium User"'))	