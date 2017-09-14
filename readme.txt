
app_logic/ 跟随每一个app而改变的测试逻辑
apps/ 存放apk等
comm/HTMLTestRunner.py html format 支持
data/ 测试数据
testcase/ 测试用例主目录
testcase/login/test*.py 所有以test开头的python文件都会被执行，作为特定testcast
...
testcase/xx/test*.py
report/ 测试报告输出目录

pyappium 参数：
Usage:
	pyappium (-h | --help)
	pyappium [<desc>] [<title>]
	pyappium [<desc>] [<title>] -r <remove_suite>
	pyappium -r <remove_suite>
	
Options:
	-h,--help   显示帮助菜单
	-r,--remove 移除特定目录下用例 login,h5移除login,h5目录的测试

Example:
	pyappium 自动化测试报告 用例执行情况 