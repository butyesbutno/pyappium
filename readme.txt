Mobile App automation test(Appium) / web interface verify based on python requests

app_logic/yourappname/ 跟随每一个app而改变的测试逻辑 / app special lib / functions
apps/ 存放apk等 / stores apk 

comm/HTMLTestRunner.py html format 支持
comm/XmlParser.py xml 格式用例支持 / xml testcase support
comm/JsonParser.py Json格式接口测试 / json interface testcase support
comm/pyLib.py 一些基础方法 / basic lib

config/app.py 当前测试App / configurations for current app

data/ 测试数据 / data
screenshot/youappname/ 测试报告输出目录 / test screenshot
report/youappname/ 测试报告输出目录 / test report

testcase/ 测试用例主目录
testcase/youappname/pycode/test*.py 所有以test开头的python文件都会被执行，作为特定testcast
testcase/youappname/xml/*.xml 加载作为xml用例
testcase/youappname/json/*.json 加载作为json用例

pyappium 参数：
Usage:
	pyappium (-h | --help)
	pyappium -r <remove_suite>
	
Options:
	-h,--help   显示帮助菜单
	-r,--remove 移除特定目录下用例 login,h5移除login,h5目录的测试

