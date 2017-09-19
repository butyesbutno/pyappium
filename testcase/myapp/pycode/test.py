#!/usr/bin/env python
#coding: utf-8

import unittest,os,time,io,xlrd
from appium import webdriver
from comm import pyLib

class ExampleTestCase(unittest.TestCase):
	'''测试范例'''

	def setUp(self):
		'''测试准备工作'''
		# appium & 启动app/activity
		self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
		
	def tearDown(self):
		'''测试结束工作'''
		self.driver.quit()

	def testMe(self):
		'''显示'''
		pass
		
if __name__ == "__main__":
	unittest.main()
