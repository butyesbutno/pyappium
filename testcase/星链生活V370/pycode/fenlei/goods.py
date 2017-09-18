#!/usr/bin/env python
#coding: utf-8

from appium import webdriver
import unittest,os,time
import xlrd
from comm import pyconfig

# 内部函数，强制退出登录

class fenlei(unittest.TestCase):
	'''分类'''
	# 测试准备工作
	def setUp(self):
		self.driver=webdriver.Remote('http://127.0.0.1:4723/wd/hub', pyconfig.desired_caps)
		pass
		
	# 测试结束工作
	def tearDown(self):
		self.driver.quit()
		
	# 内部函数，防止find_element_by_id异常
	def getElement(self, inname):
		try:
			ele = self.driver.find_element_by_id(inname)
			return ele
		except:
			return None
			
	# 测试用例
	def test_tab_goods(self):
		'''分类'''
		time.sleep(8)
		setting = self.getElement('com.hele.buyer:id/tab_goods')
		if setting == None :
			return 
		setting.click()
		time.sleep(1)
		pass

	def test_jindain(self):
		'''近店'''
		print('jindian')
		time.sleep(8)
		self.driver.find_element_by_id('com.hele.buyer:id/tab_near').click()
		dianpufenlei_name=self.driver.find_element_by_id('com.hele.buyer:id/tv_on_category').text
		print(dianpufenlei_name)
		self.assertEqual(dianpufenlei_name,'店铺分类')


		self.driver.find_element_by_id('com.hele.buyer:id/tab_near').click()
		xiaoliang_name=self.driver.find_element_by_id('com.hele.buyer:id/tv_on_sale').text
		print(xiaoliang_name)
		self.assertEqual(xiaoliang_name,'销量')

if __name__ == "__main__":
	unittest.main()
