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
import xlrd, unittest, os, time, importlib, platform

class _XmlTestProtoType(unittest.TestCase):
	'''XML 测试用例'''

	def setUp(self):
		try:
			# appium & start app/activity
			self.driver = webdriver.Remote(AppiumServer, desired_caps)
		except:
			print(_('No webdriver connection'))
		self.assertIsNotNone(self.driver)

	def tearDown(self):
		self.driver.quit()

	def __init__(self, methodName='runTest'):

		super(_XmlTestProtoType, self).__init__(methodName)
		
		# base dir
		# ../report ../screenshot
		self._basedir = os.path.dirname(os.path.abspath(__file__))

		# save the parameters
		self._xmlmethodNode = []

		# testcase's step
		self._step = []

	# Load testcase format xml
	def _loadTestcase(self, testcaseNode):
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
	def _exe_xmlMethod(self, element, method_name):

		# xml:domethod / pycode:shoptest
		method_array = method_name.split(':')
		if len(method_array) < 2 :
			print("%s - %s" % (_("Xml function error"), method_name))
			return False

		if method_array[0] == "xml":
			for xmlmethod in self._xmlmethodNode:
				# find match xml process
				if(xmlmethod.attrib["name"] != method_name):
					continue
				# execute desc
				print('%s: %s' % (_('Execute xml process'), method_name))
				# execute
				lst = xmlmethod.getchildren() 
				for n in lst:
					if ( self.__exe_step(n.attrib, subproc=1) == False) :
						return False
		elif method_array[0] == "pycode":
		
			# build python code import path
			libpath = 'app_logic.' + CurAppName ;
			libs = method_array[1].split('.')
			for i in range(len(libs) - 1):
				libpath += '.' + libs[i]
			# support chinese path
			if platform.platform().find("Window") >= 0:
				libpath = libpath.decode('utf-8').encode('gbk')
			# Load / import
			lib = importlib.import_module(libpath)
			evalStr = "lib."+ libs[len(libs)-1] + "(self.driver, " + "element)"
			# execute desc
			print('%s: %s' % (_('Execute python process'), evalStr))
			# execute
			eval(evalStr)
		return True

	# execute a step / return True / False
	def _exe_step(self, oneStep, *args, **awd):

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

		# the step's desc str
		step_desc_str = "<step "
		if 'subproc' in awd:
			step_desc_str = "\t<step "
		
		# try execute this step
		# first find the element
		element = None
		for (k,v) in oneStep.items():
			# v = oneStep[k] / translated_v = translated(v) if v startswith '@'
			translated_v = SafeAccessStepDict(k)
			# build / recovery step desc
			step_desc_str += ('%s="%s" ' % (k, translated_v))			
			if k == "desc":
				print(translated_v)
			if k == "h5" and len(translated_v) > 0:
				pyLib.switch_context(translated_v)
			if k == "id":
				if type(translated_v) == str :
					element = pyLib.tryGetElement(self.driver, v)
				else:
					element = translated_v
			elif k == "xpath":
				if type(translated_v) == str :
					element = pyLib.tryGetElementByXPath(self.driver, v)
				else:
					element = translated_v
			elif k == "name":
				if type(translated_v) == str :
					element = pyLib.tryGetElementByName(self.driver, v)
				else:
					element = translated_v
		
		# executing the step
		step_desc_str += ' />'
		print(step_desc_str)
		
		# step's attributes
		for (k,v) in oneStep.items():
			translated_v = SafeAccessStepDict(k)
			if k == "screenshot":
				filepath = self._basedir + '/../screenshot/' +  CurAppName + "/"
				try:
					os.mkdir(filepath)
				except:
					pass
				filepath += v + "_%d.png" % int(time.strftime("%Y%m%d%H%M"))
				self.driver.get_screenshot_as_file(filepath)
			elif k == "swipe":
				# swipe="2/3,1/3,1/3,1/3,1000"
				lst = v.split(',')
				try:
					pyLib.swipeRelative(self.driver, float(lst[0]), float(lst[1]), float(lst[2]), float(lst[3]), int(lst[4]))
				except:
					pass
			elif k == "checkexist":
				# check the element exist
				if translated_v == "true" :
					self.assertIsNotNone(element)
				else:
					self.assertIsNone(element)
			elif k == "checkvalue":
				real_text = element.get_attribute('text')
				if(translated_v[0] == '='):
					self.assertEqual(real_text, translated_v[1:])
				if(translated_v[0] == '!' and translated_v[1] == '='):
					self.assertNotEqual(real_text, translated_v[2:])
				if v.startswith('@'):
					self._exe_xmlMethod(element, v[1:])

			elif k == "ifexist":
				#ifexist
				if element != None and v.startswith('@'):
					self._exe_xmlMethod(element, v[1:])

			elif k == "ifnotexist":
				#ifnotexist
				if element == None and v.startswith('@'):
					self._exe_xmlMethod(element, v[1:])

			elif k == "text":
				# set text?
				pyLib.setTextValue(element, translated_v)

			elif k == "click":
				# Just click?
				element.click()

			elif k == "sleep":
				# Just click?
				time.sleep(int(translated_v))

			elif k == "method":
				# Just execute a method
				if v.startswith('@'):
					self._exe_xmlMethod(element, v[1:])

	# Execute the test case
	def _exe_testcase(self):
		'''Execute the test case'''

		# testcase informations
		desc = getattr(self, "desc", "")
		platform = getattr(self, "platform", "")
		author = getattr(self, "author", "")
		version = getattr(self, "version", "")
		loopcount = getattr(self, "loopcount", "")
		print('%s: %s %s: %s %s: %s %s: %s' % (_('Execute testcase'), desc, _('author'), author, _('platform'), platform, _('version'), version))

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
						fieldgen[k] = _XmlTestProtoType.getField()(self._basedir, self.driver, v)

				# the loops defined correctly?
				total_steps = len(oneStep)-1
				if total_steps < 1 :
					print('%s: %s %s' % (_('Execute loop'), loopdesc, _('End')) )
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

					# execute loop times
					print('%s: %s %d' % (_('Execute loop'), loopdesc, seq) )

					# execute this loop!
					for j in range(total_steps):
						self._exe_step(oneStep[j+1], subproc=1, fields=fields)

					# Has no data?
					if loop_untile_nodata and fieldgen_no_data:
						break

					if loop_untile_nodata == False and seq >= loopcount:
						break
					seq = seq + 1
			else:
				self._exe_step(oneStep)

		# Testcase End
		print(_("Testcase End"))

	# generator of any parameter start with @
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
			elif eles[0] == "xpathlst":
				elements = driver.find_elements_by_xpath(eles[1])
				for element in elements:
					yield element
				raise ValueError('No data')
		return func

	# testcase prototype
	@staticmethod
	def newTestCase(testcaseNode):
		def func(self):
			self._loadTestcase(testcaseNode)
			self._exe_testcase()
		return func

# build the testcase for xml format file/folder
def makeXmlSuite(xml_testcases):

	funNumber = 0
	for filename in xml_testcases:
		try:
			root = ElementTree.parse(filename)
			testcases = root.findall("testcase")

			for testcaseNode in testcases:
				setattr(_XmlTestProtoType, "test" + str(funNumber), _XmlTestProtoType.newTestCase(testcaseNode))
				try:
					setattr(_XmlTestProtoType, "test" + str(funNumber)+'xmldoc', testcaseNode.attrib["desc"])
				except:
					pass
				funNumber = funNumber + 1
		except BaseException as e:
			print(e)
			print("Xml file %s has error" % filename)
	return unittest.makeSuite(_XmlTestProtoType)

# build testcase's desc
def getXmlTestcaseDesc(tids):
	try:
		if tids.index("_XmlTestProtoType") < 0:
			return None
		name = tids.split('.')[-1]
		return getattr(_XmlTestProtoType, name+'xmldoc')
	except:
		return None

# properties of all
__all__=["makeXmlSuite", "getXmlTestcaseDesc"]


