#!/usr/bin/env python
#coding: utf-8

from comm import pyLib
import time,unittest

def shoptest(driver, shop):
	pass
	
def waitRefresh(driver, element):
	# wait for refresh
	for times in range(20):
		waitting = pyLib.getElement(driver, "com.XXX:id/refresh_text")
		if waitting == None:
			return True
		time.sleep(1)

	#不能一直等待
	waitting = pyLib.getElement(driver, "com.XXX:id/refresh_text")
	unittest.TestCase().assertEqual(waitting, None)
	return True