#!/usr/bin/env python
#coding: utf-8

from appium import webdriver
import unittest,os,time,io
import xlrd
from comm import pyLib

class Login(unittest.TestCase):
	'''我的'''

	def setUp(self):
		'''测试准备工作'''

		# appium & 启动app/activity
		self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
		
		# xls 初始化
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		self.xlsdata = xlrd.open_workbook(BASE_DIR + '/../../data/test.xls')
		
	def tearDown(self):
		'''测试结束工作'''
		self.driver.quit()

	def forceLogout(self):
		'''内部函数，强制退出登录'''

		# 确定 进入到的页面
		my_page = pyLib.getElement(self.driver, 'com.hele.buyer:id/tab_person')
		if my_page:
			my_page.click()
			time.sleep(1)

		# 我的设置按钮
		setting = pyLib.getElement(self.driver, 'com.hele.buyer:id/setting')
		if setting == None :
			return 
		setting.click()
		
		# click logout
		logout = pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/login_out')
		logout.click()
		
		# 确认退出
		logout = pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/right')
		logout.click()

	def testLoginOk(self):
		'''正确登录'''
		# 找到主界面，我的按钮
		print('-'*10 + Login.testLoginOk.__doc__ + '-'*10)
		pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/tab_index')
		
		# 获取xls 用户名 密码 是否可以登录
		table = self.xlsdata.sheet_by_name(u'login')
		
		# 逐一尝试登录
		for row in range(0, table.nrows):
			
			user = table.cell(row,0).value
			passwd = table.cell(row,1).value
			can_login = table.cell(row,2).value
			if can_login != 'ok':
				continue
			
			# 强制退出之前账号
			self.forceLogout()
			
			# 确定进入到的页面
			my_page = pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/tab_person')
			if my_page:
				my_page.click()
				time.sleep(1)
			
			# 找到密码输入框
			print(u'准备输入用户名%s，密码%s' % (user, passwd) )
			passwdview=pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/pwdCET')
			pyLib.setTextValue(passwdview, passwd)
			#passwdview.send_keys(passwd)
			userview=pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/phoneCET')
			userview.click()
			context2=userview.get_attribute('text')#获取文本框里的内容
			pyLib.edittextclear(self.driver, context2)#删除文本框中是内容
			pyLib.setTextValue(userview, user)
			
			# 登录
			print(u'尝试登录')
			login=pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/loginBT')
			login.click()
			
			# 登录应该成功
			self.assertIsNotNone(pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/setting'))
			
	def testLoginFailed(self):
		'''错误登录'''
		# 找到主界面，我的按钮
		print('-'*10 + Login.testLoginFailed.__doc__ + '-'*10)
		pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/tab_index')
		
		# 获取xls 用户名 密码 是否可以登录
		table = self.xlsdata.sheet_by_name(u'login')
		
		# 逐一尝试登录
		for row in range(0, table.nrows):
			
			user = table.cell(row,0).value
			passwd = table.cell(row,1).value
			can_login = table.cell(row,2).value
			if can_login == 'ok':
				continue
				
			# 强制退出之前账号
			self.forceLogout()
			
			# 确定进入到的页面
			my_page = pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/tab_person')
			if my_page:
				my_page.click()
				time.sleep(1)
			
			# 找到密码输入框
			print(u'准备输入用户名%s，密码%s' % (user, passwd) )
			passwdview=pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/pwdCET')
			pyLib.setTextValue(passwdview, passwd)
			userview=pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/phoneCET')
			userview.click()
			context2=userview.get_attribute('text')#获取文本框里的内容
			pyLib.edittextclear(self.driver, context2)#删除文本框中是内容
			pyLib.setTextValue(userview, user)
			
			# 登录
			print(u'尝试登录')
			login=pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/loginBT')
			login.click()
			
			# 登录应该失败
			self.assertIsNone(pyLib.tryGetElement(self.driver, 'com.hele.buyer:id/setting'))
			
if __name__ == "__main__":
	unittest.main()
