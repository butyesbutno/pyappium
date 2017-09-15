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
import pyconfig, pyLib
import xlrd
import unittest

class XmlTest(object):

    def __init__(self, testcaseNode):

        # base dir
        # ../report ../screenshot
        self._basedir = os.path.dirname(os.path.abspath(__file__))

        # save the parameters
        self._checkxmlNode = []

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
            elif step.tag == "checkxml":
                self._checkxmlNode.append(step)

    # check xml
    def __exe_checkxml(self, drvier, checkxml_name):

        for checkNode in self._checkxmlNode:
            if(checkNode.tag != checkxml_name):
                continue
            lst = checkNode.getchildren()
            for n in lst:
                if ( self.__exe_step(driver, n) == False) :
                    return False
        return True

    # execute a step / return True / False
    def __exe_step(self, driver, oneStep, *args, **awd):

        # No exception when access dict
        def NoExceptionDict(d, key):
            try:
                return d[key]
            except:
                return None

        # try execute this step
        h5 = NoExceptionDict(oneStep, "h5")
        if h5 and h5 == "true":
            xpath = NoExceptionDict(oneStep, "xpath")
            pass
        else:
            id = NoExceptionDict(oneStep, "id")
            screensnapshot = NoExceptionDict(oneStep, "screensnapshot")
            swipe = NoExceptionDict(oneStep, "swipe")
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
                checkexist = NoExceptionDict(oneStep, "checkexist")
                checkvalue = NoExceptionDict(oneStep, "checkvalue")
                element = pyLib.tryGetElement(driver, id)
                if checkexist:
                    if checkexist == "true" :
                        return (element != None)
                    else:
                        return (element == None)

                # checkvalue
                if checkvalue:
                    real_text = element.get_attribute('text')
                    return (real_text == checkvalue)

                # set text?
                text = NoExceptionDict(oneStep, "text")
                if text:
                    real_text = text
                    if text.startswith('@') :
                        try:
                            real_text = awd[ text[1:] ]
                        except:
                            pass
                    pyLib.setTextValue(element, real_text)

                # Just click?
                click = NoExceptionDict(oneStep, "click")
                if click:
                    element.click()

                #checkxml
                checkxml = NoExceptionDict(oneStep, "checkxml")
                if checkxml:
                    if( self.__exe_checkxml(drvier, checkxml) == False) :
                        return False

                return True

    @staticmethod
    def getField():
        def func(f):
            ''' f @col:0,sheet:0,test.xls '''
            # if its a fixed parameters
            if(f.startswith('@') == False):
                while(True):
                    yield f

            # its a variable
            eles = f[1:].split(',')
            col = int(eles[0].split(':')[1])
            sheet = int(eles[1].split(':')[1])
            #xlsdata = xlrd.open_workbook(BASE_DIR + '/../../data/'+eles[2])
            xlsdata = xlrd.open_workbook('E:/work/appiumframework/pyappium/data/'+eles[2])
            table = xlsdata.sheets()[sheet]
            for row in range(table.nrows):
                yield table.cell(row, col).value
            xlsdata.close()
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
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', pyconfig.desired_caps)

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
                        fieldgen[k] = XmlTest.getField()(v)

                # the loops defined correctly?
                total_steps = len(oneStep)-1
                if total_steps < 1 :
                    print("Loop "+ loopdesc + " finished")
                    continue

                # execute loops
                seq = 1
                while(True):

                    print("Loop "+ loopdesc + " execute sequence %d" % seq)
                    # yield the parameters
                    fields = {}
                    fieldgen_no_data = False
                    for (k,v) in fieldgen.items():
                        try:
                            fields[k] = pyLib.generatorVersion(v)
                        except BaseException as e:
                            fields[k] = ""
                            fieldgen_no_data = True

                    # execute this loop!
                    for j in range(total_steps):
                        self.__exe_step(driver, oneStep[j+1], fields=fields)

                    # next loop sequence
                    if loop_untile_nodata and fieldgen_no_data:
                        break
                    if loop_untile_nodata == False and seq >= loopcount:
                        break
                    seq = seq + 1
            else:
                self.__exe_step(driver, oneStep)

        driver.quit()

class xmlttt(unittest.TestCase):
    pass

if __name__ == '__main__':
    '''''读xml文件'''
    # 加载XML文件（2种方法,一是加载指定字符串，二是加载指定文件）
    root = ElementTree.parse("e:/test.xml")
    testcases = root.findall("testcase")

    i = 0
    suit = unittest.TestSuite()
    for testcaseNode in testcases:
        a = XmlTest(testcaseNode)
        setattr(xmlttt, "test" + str(i), a.testXml())
        suit.addTests(unittest.makeSuite(xmlttt))
    unittest.TextTestRunner().run(suit)
