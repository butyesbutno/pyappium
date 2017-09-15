#!/usr/bin/env python
#coding: utf-8

desired_caps = {
            'appPackage': 'com.hele.buyer',
            'appActivity': 'com.hele.buyer.MainActivity',
            'platformName': 'Android',
            'platformVersion': '6.0',
            'deviceName': 'TBSDU1553002798',
			'unicodeKeyboard': 'True',
			'resetKeyboard':'True'
        }

CurAppName = "星链生活V3.7.0"

__all__=["desired_caps", "CurAppName"]