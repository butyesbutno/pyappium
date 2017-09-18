#!/usr/bin/env python
#coding: utf-8

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# email: michael.wangh@gmail.com

__author__ = 'michael'
__version__ = "0.1.0"

from appium import webdriver
from xml.etree import ElementTree
from . import pyLib
from config import *
import xlrd, unittest, os, time, importlib

class _XmlTest(unittest.TestCase):

	def __init__(self, testcaseNode):

		# base dir
		# ../report ../screenshot
		self._basedir = os.path.dirname(os.path.abspath(__file__))

		# save the parameters
		self._xmlmethodNode = []

		# testcase's step
		self._step = []

		# testcase attributes
		for k in testcaseNode.attrib.keys():
			setattr(self, k, testcaseNode.attrib[k])

		# step / theloop / subnode
		step_lst = testcaseNode.getchildren()
		for step in step_lst:
			if step.tag == 'step':
				self._step.append(step.attrib)
			elif step.tag == 'theloop':
				theloop = [step.attrib]
				theloop_lst = step.getchildren()
				for childStep in theloop_lst:
					# 不嵌套loop
					if childStep.tag == 'step':
						theloop.append(childStep.attrib)
				self._step.append(theloop)
			elif step.tag == "xmlmethod":
				self._xmlmethodNode.append(step)

	# check xml
	def __exe_xmlMethod(self, driver, element, method_name):

		# xml:domethod / pycode:shoptest
		method_array = method_name.split(':')
		if len(method_array) < 2 :
			print("Xml format error - %s" % method_name)
			return False

		if method_array[0] == "xml":
			for xmlmethod in self._xmlmethodNode:
				if(xmlmethod.attrib["name"] != method_name):
					continue
				lst = xmlmethod.getchildren()
				for n in lst:
					if ( self.__exe_step(driver, n.attrib) == False) :
						return False
		elif method_array[0] == "pycode":
			libpath = 'app_logic.' + CurAppName ;
			libs = method_array[1].split('.')
			for i in range(len(libs) - 1):
				libpath += '.' + libs[i]
			lib = importlib.import_module(libpath)
			evalStr = "lib."+ libs[len(libs)-1] + "(driver, " + "element)"
			eval(evalStr)
		return True

	# execute a step / return True / False
	def __exe_step(self, driver, oneStep, *args, **awd):

		# No exception when access dict
		def SafeAccessStepDict(key, field_translate=True):
			try:
				val = oneStep[key]
				if field_translate and awd :
					fields = awd["fields"]
					for (k,v) in fields.items():
						if v == None :
							continue
						if type(v) == str:
							val = val.replace("@" + k, v)
						else:
							if '@'+k == val :
								return v
				return val
			except:
				return None

		# step desc
		desc = SafeAccessStepDict("desc")
		if desc != None:
			print(desc)

		# try execute this step
		h5 = SafeAccessStepDict("h5")
		if h5 and h5 == "true":
			xpath = SafeAccessStepDict("xpath")
			pass
		else:
			id = SafeAccessStepDict("id")
			screensnapshot = SafeAccessStepDict("screensnapshot")
			swipe = SafeAccessStepDict("swipe")
			if screensnapshot:
				filepath = self._basedir + 'screenshot/' +  "Error_%d.png" % int(time.strftime("%Y%m%d%H%M"))
				driver.get_screenshot_as_file(filepath)
				return True
			if swipe:
				# swipe="2/3,1/3,1/3,1/3,1000"
				lst = swipe.split(',')
				try:
					pyLib.swipeRelative(driver, float(lst[0]), float(lst[1]), float(lst[2]), float(lst[3]), int(lst[4]))
				except:
					return False
				return True
			if id:
				# check the element exist
				checkexist = SafeAccessStepDict("checkexist")
				checkvalue = SafeAccessStepDict("checkvalue")
				method = SafeAccessStepDict("method")
				if type(id) == str :
					element = pyLib.tryGetElement(driver, id)
				else:
					element = id
				if checkexist:
					if checkexist == "true" :
						self.assertIsNotNone(element)
					else:
						self.assertIsNone(element)
					print("checkexist passed")

				#ifexist
				ifexist = SafeAccessStepDict("ifexist", False)
				if ifexist and ifexist.startswith('@'):
					if( self.__exe_xmlMethod(driver, element, ifexist[1:]) == False) :
						return False
				#ifnotexist
				ifnotexist = SafeAccessStepDict("ifnotexist", False)
				if ifnotexist and ifnotexist.startswith('@'):
					if( self.__exe_xmlMethod(driver, element, ifnotexist[1:]) == False) :
						return False

				# checkvalue
				if checkvalue:
					real_text = element.get_attribute('text')
					self.assertEqual(real_text, checkvalue)

				# set text?
				text = SafeAccessStepDict("text")
				if text:
					pyLib.setTextValue(element, text)

				# Just click?
				click = SafeAccessStepDict("click")
				if click:
					element.click()

				# Just click?
				sleep = SafeAccessStepDict("sleep")
				if sleep:
					time.sleep(int(sleep))

				# Just execute a method
				if method and method.startswith('@'):
					if( self.__exe_xmlMethod(driver, element, method[1:]) == False) :
						return False
				return True
			else:
				return True

	@staticmethod
	def getField():
		def func(basedir, driver, f):
			''' f @xls,col:0,sheet:0,test.xls '''
			# if its a fixed parameters
			if(f.startswith('@') == False):
				while(True):
					yield f

			# its a variable
			eles = f[1:].split(',')
			if eles[0] == "xls":
				col = int(eles[1].split(':')[1])
				sheet = int(eles[2].split(':')[1])
				xlsdata = xlrd.open_workbook(basedir + '/../data/'+eles[3])
				table = xlsdata.sheets()[sheet]
				for row in range(table.nrows):
					yield table.cell(row, col).value
				xlsdata.close()
			elif eles[0] == "idlst":
				elements = pyLib.getElements(driver, eles[1])
				for element in elements:
					yield element
				raise ValueError('No data')
		return func

	def testXml(self):
		'''Execute the test case'''

		# testcase informations
		desc = getattr(self, "desc", "")
		platform = getattr(self, "platform", "")
		author = getattr(self, "author", "")
		version = getattr(self, "version", "")
		loopcount = getattr(self, "loopcount", "")
		print(desc + ', write by ' + author + ', for ' + platform + ', version ' + version)

		# webdriver
		driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

		# execute the testcase
		for oneStep in self._step:
			if(type(oneStep) == list) :
			   # onStep is a list, each element is a dict
				loopdesc = ""
				loop_untile_nodata = True
				loopcount = 1
				fieldgen = {}
				for (k,v) in oneStep[0].items():
					if k == 'desc' :
						loopdesc = oneStep[0][k]
					elif k == 'loopcount':
						loopcount = int(oneStep[0][k])
						if(loopcount<1) :
							loopcount = 1
						loop_untile_nodata = False
					elif k.startswith('field'):
						fieldgen[k] = _XmlTest.getField()(self._basedir, driver, v)

				# the loops defined correctly?
				total_steps = len(oneStep)-1
				if total_steps < 1 :
					print("Loop "+ loopdesc + " finished")
					continue

				# execute loops
				seq = 1
				while(True):

					# yield the parameters
					fields = {}
					fieldgen_no_data = False
					for (k,v) in fieldgen.items():
						try:
							fields[k] = pyLib.generatorGetNext(v)
						except BaseException as e:
							fields[k] = None
							fieldgen_no_data = True

					# Check all fields are None
					if fieldgen_no_data:
						all_fields_none = True
						for (k,v) in fields.items():
							if v != None:
								all_fields_none = False
						if all_fields_none:
							break

					print("Loop "+ loopdesc + " execute sequence %d" % seq)
					# execute this loop!
					for j in range(total_steps):
						if(self.__exe_step(driver, oneStep[j+1], fields=fields) == False):
							driver.quit()
							return False

					# Has no data?
					if loop_untile_nodata and fieldgen_no_data:
						break

					if loop_untile_nodata == False and seq >= loopcount:
						break
					seq = seq + 1
			else:
				if (self.__exe_step(driver, oneStep) == False) :
					driver.quit()
					return False
		driver.quit()

class _XmlTestProtoType(unittest.TestCase):
	'''XML 测试用例'''
	pass

# 为xml形式的testcase构建unittest形式的用例
def makeXmlSuite(xml_testcases):

	funNumber = 0
	for filename in xml_testcases:
		try:
			root = ElementTree.parse(filename)
			testcases = root.findall("testcase")

			for testcaseNode in testcases:
				setattr(_XmlTestProtoType, "test" + str(funNumber), _XmlTest(testcaseNode).testXml)
				try:
					setattr(_XmlTestProtoType, "test" + str(funNumber)+'xmldoc', testcaseNode.attrib["desc"])
				except:
					pass
				funNumber = funNumber + 1
		except:
			print("Xml file %s has error" % filename)
	return unittest.makeSuite(_XmlTestProtoType)

def getXmlTestcaseDesc(name):
	return getattr(_XmlTestProtoType, name+'xmldoc')

# properties of all
__all__=["makeXmlSuite", "getXmlTestcaseDesc"]

if __name__ == '__main__':
	'''''读xml文件'''
	# 加载XML文件（2种方法,一是加载指定字符串，二是加载指定文件）
	root = ElementTree.parse("D:/kongkong/appiumframework/pyappium/testcase/星链生活V370/xml/test.xml")
	testcases = root.findall("testcase")

	i = 0
	suit = unittest.TestSuite()
	for testcaseNode in testcases:
		a = _XmlTest(testcaseNode)
		setattr(_XmlTestProtoType, "test" + str(i), a.testXml())
		suit.addTests(unittest.makeSuite(_XmlTestProtoType))
	unittest.TextTestRunner().run(suit)
