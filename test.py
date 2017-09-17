#!/usr/bin/env python
#coding: utf-8

import unittest

suit = unittest.TestSuite()
a=unittest.TestLoader()
suit.addTests(a.loadTestsFromName("testcase.xml.testMain"))
suit.addTests(a.loadTestsFromName("testcase.pycode.testMain"))
print(suit)
unittest.TextTestRunner().run(suit)