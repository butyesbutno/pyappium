#!/usr/bin/env python
#coding: utf-8

import unittest,os,time,io,xlrd
from appium import webdriver
from comm import pyLib
from app_logic import shopLogic

class NearbyShop(unittest.TestCase):
	'''近店'''

	def setUp(self):
		'''测试准备工作'''
		# appium & 启动app/activity
		self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
		
	def tearDown(self):
		'''测试结束工作'''
		self.driver.quit()

	def testShopLoaded(self):
		'''店铺显示'''
		print(u'进入近店页面')
		# 确定进入 近店
		#driver.implicitly_wait(10)
		shop_page = pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/tab_near')
		self.assertIsNotNone(shop_page)
		shop_page.click()

		# wait for refresh
		for times in range(20):
			waitting = pyLib.getElement(self.driver, "com.hele.buyer:id/pull_to_refresh_text")
			if waitting == None:
				break
			time.sleep(1)
		
		#不能一直等待 
		waitting = pyLib.getElement(self.driver, "com.hele.buyer:id/pull_to_refresh_text")
		self.assertEqual(waitting, None)
			
		# 商品列表
		for i in range(10):
			
			#测试店铺
			shops = pyLib.getElements(self.driver, 'com.hele.buyer:id/shop_name')
			if shops != None:
				for shop in shops:
					shopLogic.shoptest(self.driver, shop)

			# 测试商品
			good1 = pyLib.getElements(self.driver, 'com.hele.buyer:id/iv_goods_1')
			good2 = pyLib.getElements(self.driver, 'com.hele.buyer:id/iv_goods_2')
			good3 = pyLib.getElements(self.driver, 'com.hele.buyer:id/iv_goods_3')
			goods = good1 + good2 + good3
			for good in goods:
				if good == None :
					continue
				shopLogic.goodtest(self.driver, good)
			
			# 滚动屏幕
			lastStr = self.driver.page_source
			pyLib.swipeUp(self.driver, 1000)
			if lastStr == self.driver.page_source :
				print(u"滑动%d次到达底部" % (i+1))
				break
		
if __name__ == "__main__":
	unittest.main()
