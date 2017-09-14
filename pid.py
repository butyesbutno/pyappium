#!/usr/bin/env python
#coding: utf-8
	
import jpype,time,os

#开启JVM，且指定jar包位置
jarpath = os.path.join(os.path.abspath('.'), '/work/appiumframework/apps/')
print(jarpath, jpype.getDefaultJVMPath())
jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.ext.dirs=%s" % jarpath)
print("toe he")
#引入java程序中的类.路径应该是项目中的package包路径
javaClass = jpype.JClass('ChromedriverHandler.chromeDriverHandlerThread')
#这一步就是具体执行类中的函数了
print("before started")
javaInstance = javaClass.start()
javaInstance = javaClass.stop()
print("started")
time.sleep(6)
jpype.shutdownJVM()
print("end")
