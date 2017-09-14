#!/usr/bin/env python
#coding: utf-8

import unittest,os,time,io,xlrd
from appium import webdriver
from comm import pyconfig, pyLib

class MainH5(unittest.TestCase):
	'''主界面'''

	def setUp(self):
		'''测试准备工作'''
		# appium & 启动app/activity
		self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', pyconfig.desired_caps)
		
	def tearDown(self):
		'''测试结束工作'''
		self.driver.quit()

	def testH5(self):
		'''H5'''

		# 确定进入 近店
		#pyLib.switch_h5(driver, '')
		time.sleep(3)
		print(self.driver.contexts)

		'''
		self.driver.switch_to.context('NATIVE_APP')
		self.driver.switch_to.context('WEBVIEW_com.example.michael.mywebview')
		key = pyLib.tryGetElementByXPath(self.driver, '//*[@id="word"]')
		key.send_keys(u'孔孔')
		key = pyLib.tryGetElementByXPath(self.driver, '/html/body/div/form/input')
		key.click()
		#self.driver.switch_to.context('NATIVE_APP')
		'''
		
if __name__ == "__main__":
	unittest.main()
