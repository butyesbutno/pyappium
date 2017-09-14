#!/usr/bin/env python
#coding: utf-8

import unittest,os,time,io,xlrd
from appium import webdriver
from comm import pyconfig, pyLib
from app_logic import shopLogic

class FenLei(unittest.TestCase):
	'''分类'''

	def setUp(self):
		'''测试准备工作'''
		# appium & 启动app/activity
		self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', pyconfig.desired_caps)

	def tearDown(self):
		'''测试结束工作'''
		self.driver.quit()

	def testFenLeiLoaded(self):
		'''分类'''
		print(u'进入分类页面')
		# 确定进入 近店
		#driver.implicitly_wait(10)
		fenlei_page = pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/tab_goods')
		self.assertIsNotNone(fenlei_page)
		fenlei_page.click()

		# 分类列表
		leibies = pyLib.tryGetElements(self.driver, 'com.hele.buyer:id/name')
		if leibies != None:
			for leibie in leibies:
				leibie.click()
				print(u'遍历类别'+leibie.text)
				# 遍历分类的子项目
				items = pyLib.tryGetElements(self.driver, 'com.hele.buyer:id/name')
				for item in items:
					print(u'子分类'+item.text)

if __name__ == "__main__":
	unittest.main()
