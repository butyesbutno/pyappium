#!/usr/bin/env python
#coding: utf-8

from comm import pyLib
import time

def shoptest(driver, shop):

	# 此处查看店铺页面是否正常，暂空
	print(u'进入店铺：' + shop.text )
	shop.click()
	time.sleep(5)
	# 原生应用内的Webview须进行相应的调试声明配置
	# 暂时无法app 内webview定位,五秒内有返回就算打开网页了
	#driver.switch_to.context(webview)
	find_shop_name = False
	try:
		if len(driver.page_source) > 0 :
			find_shop_name = True
	except:
		pass
	driver.back()
	time.sleep(1)
	return find_shop_name
	
def goodtest(driver, good):
	
	# 进入商品详情
	good.click()
	
	# 获取商品名称、店铺名称
	shop_name_tv = pyLib.tryGetElement(driver, 'com.hele.buyer:id/shop_name_tv')
	goods_name_tv = pyLib.tryGetElement(driver, 'com.hele.buyer:id/goods_name_tv')
	if shop_name_tv == None:
		print(u'该商品所属店铺没有名称')
		return False
	if goods_name_tv == None:
		print(u'该商品没有名称')
		return False
	print(u'商品页：' + goods_name_tv.text + '(' + shop_name_tv.text + ")")
	
	# 去结算
	settle_tv = pyLib.tryGetElement(driver, 'com.hele.buyer:id/settle_tv')
	if settle_tv == None:
		print(u'没有结算功能')
		return False
	#settle_tv.get_attribute("enabled")
	
	# 加入购物车
	add_to_cart_tv = pyLib.tryGetElement(driver, 'com.hele.buyer:id/add_to_cart_tv')
	if add_to_cart_tv == None:
		print(u'没有购物车')
		return False
	if add_to_cart_tv.get_attribute("enabled") != u'true' :
		print(u'不能添加到购物车')
		return False
	
	# 返回
	driver.back()
	time.sleep(1)
	
	return True