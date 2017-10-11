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

import unittest, json, os, re, requests, codecs, sys, platform
from config import *
from . import mysqldb

class _JsonTestProtoType(unittest.TestCase):
	'''JSON 接口测试'''

	# testcase prepare
	def setUp(self):
		print( "\nJson:\t%s" % _JsonTestProtoType.__doc__)

	# testcase ending
	def tearDown(self):
		pass

	# init
	def __init__(self, methodName='runTest'):

		super(_JsonTestProtoType, self).__init__(methodName)
		
		# base dir
		# ../report ../screenshot
		self._basedir = os.path.dirname(os.path.abspath(__file__))

		# testcase's step
		self._Jsons = []

	# Load testcase format json
	def _loadTestcase(self, testcaseFolder):

		# testcase's step
		self._Jsons = []

		# testcase attributes
		index = 1
		while True:
			try: 
				with codecs.open(testcaseFolder+'/%03d.json'%index, 'r', 'utf-8') as f:
					self._Jsons.append( json.load(f) )
				index = index + 1
			except BaseException as e:
				break

	# check http response / valid
	def _check_resp(self, rules, httpresp):
	
		# retrive section from httpresp likes data.list.0.integralNumber
		def get_resp_section(rule_k, sections):
			if type(rule_k) == str:
				rule_k_array = rule_k.split('.')
			elif type(rule_k) == list:
				rule_k_array = rule_k
			else :
				return None
			# rule_k_array is list type
			length = len(rule_k_array)
			if( length < 1 ) :
				return None
			# current checking rule
			cur_rule = rule_k_array[0]
			# sections dict ? list ? 
			if type(sections) == dict:
				cur_section = sections[ cur_rule ]
			elif type(sections) == list:
				cur_section = sections[ int(cur_rule) ]
			if( length == 1 ) :
				return cur_section
			return get_resp_section(rule_k_array[1:], cur_section)
			
		# must json format response?
		if type(httpresp) != dict or type(rules) != dict :
			print(_("Got none json format response"))
			return 

		# dump 
		print(_("Interface response"))
		print(json.dumps(httpresp, sort_keys=True, indent=2))
		
		# check begin / "state": {"eq":0} rule_k == state, rule_v = {"eq":0}
		for (rule_k, rule_v) in rules.items():
			
			# rule_k / data.list.0.integralNumber
			resp_v = get_resp_section(rule_k, httpresp)
			# assert the section exist unicode -> utf-8
			txt = "%s: %s" % ( _("Has no section"), rule_k)
			self.assertIsNotNone(resp_v,  txt.encode('utf-8'))

			# failed str
			rule_k_failed = "%s %s %s" % (rule_k, _("does not match"), rule_v)
			rule_k_failed = rule_k_failed.encode('utf-8')

			# apply the rules 
			for (k, pattern) in rule_v.items():

				if k == 'eq':
					self.assertEqual(pattern, resp_v, rule_k_failed)
				elif k == 'type':
					self.assertEqual(type(resp_v).__name__, pattern, rule_k_failed)
				elif k == 're':
					# v == "[a-z0-9]+" 
					self.assertIsNotNone(re.match(pattern, resp_v), rule_k_failed)
			
	# execute a json / python requests
	def _exe_Jsons(self, oneJson, *args, **awd):

		# No exception when access dict
		def getKeyParameter(vdict):
			for (k,v) in vdict.items():
				# find all parameters likes {{key.para}}
				if type(v) == dict:
					getKeyParameter(v)
				elif type(v) == str:
					paralist = re.findall(r'{+key.\w+}+', v)
					for para in paralist:
						para = para.replace('{', '')
						para = para.replace('}', '')
						try:
							vdict[k] = re.sub(r'{+key.%s}+'%para, str(awd['key'][para]), v)
						except BaseException as e:
							pass

		if 'sql' in oneJson:
			k = 'sql'
			v = oneJson[k]
			# execute sql, persist the value/parameter
			for (sql_k, sql_v) in v.items():
				if sql_k in mysql_config:
					mysql_config[sql_k] = sql_v

			if "command" in v:
				print('%s: %s' % (_("Execute SQL"), v['command']))
				print('%s: %s' % (_("Database"), json.dumps(mysql_config, sort_keys=True, indent=2)) )
				
				result = mysqldb.exec_sql(v['command'])
				if 'key' in oneJson:
					for i, item in enumerate(oneJson["key"]):
						awd['key'][item] = result[0][i];
		if 'input' in oneJson:
			k = 'input'
			v = oneJson[k]
			# json format request / replace parameter with values
			getKeyParameter(v)
			
			# url / headers
			url = ''
			if 'url' in v:
				url = v['url']
			if 'rest' in v:
				url += v['rest']
			
			#  method:get / method:post 
			method = 'get'
			if 'method' in v:
				method = v['method']
				
			# headers
			headers = {'content-type': 'application/json'}
			if 'headers' in v:
				headers = v['headers']

			# print before the request
			print('%s URL: %s' % (_("Test"), url))
			print('%s header: %s' % ( _("Test"), json.dumps(headers)))
			print('%s: %s' % ( _("Test parameters"), json.dumps(v['param'])) )
			
			# we store http response 
			if method == 'get':
				if 'param' in v:
					r = requests.get(url, params=v['param'], headers=headers)
				else:
					r = requests.get(url, headers=headers)
			else:
				r = requests.post(url, data=json.dumps(v['param']), headers=headers)
			awd['httpresp'] = json.loads(r.text)
		if 'output' in oneJson:
			# check response
			self._check_resp(oneJson['output'], awd['httpresp'])

	# execute the testcase
	def _exe_testcase(self):
		'''Execute the test case'''
		# execute the testcase
		key = {}
		httpresp = {}
		for oneJson in self._Jsons:
			self._exe_Jsons(oneJson, key=key, httpresp=httpresp)

	# testcase prototype
	@staticmethod
	def newTestCase(testcaseFolder):
		def func(self):
			self._loadTestcase(testcaseFolder)
			self._exe_testcase()
		return func
		
# build the testcase for json format file/folder
def makeJsonSuite(json_testcases):

	funNumber = 0
	for folder in json_testcases:
		try:
			# create testcase 
			setattr(_JsonTestProtoType, "test" + str(funNumber), _JsonTestProtoType.newTestCase(folder))
			# set testcase's desc
			try:

				desc = None
				eles = folder.replace('\\', '/').split('/')
				for j in range(len(eles)-1, 0, -1):
					if len(eles[j]) > 0 :
						desc = eles[j]
						break
				if desc :
					if sys.version_info.major < 3 and platform.platform().find("Window") >= 0:
						desc = desc.decode('gbk').encode('utf-8')
					setattr(_JsonTestProtoType, "test" + str(funNumber)+'jsondoc', desc)
			except:
				pass
			
			# Next testcase
			funNumber = funNumber + 1
		except BaseException as e:
			print(e)
	return unittest.makeSuite(_JsonTestProtoType)

# build testcase's desc
def getJsonTestcaseDesc(tids):
	try:
		if tids.index("_JsonTestProtoType") < 0:
			return None
		name = tids.split('.')[-1]
		return getattr(_JsonTestProtoType, name+'jsondoc')
	except:
		return None
		
# properties of all
__all__=["makeJsonSuite", "getJsonTestcaseDesc"]

if __name__ == "__main__":
	pass


