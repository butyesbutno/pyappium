#!/usr/bin/env python
#coding: utf-8

import pymysql
from config import *

def exec_sql(sql):
    """
    :param sql: sql language for query / update / add /delete for the test.
    :param db: database
    :return:  data for query , null for update/delete and id or other key for add.
    """
    try:
        # if db:
            # conn = pymysql.connect(host=mysql_config.host, user=user,  passwd=psw, port=mysql_config.port, db=db_name)
        # else:
        #     conn = pymysql.connect(host=mysql_config.host, user=user, passwd=psw, port=mysql_config.port)
        conn = pymysql.connect(host=mysql_config["host"], user=mysql_config["user"], passwd=mysql_config["passwd"], port=mysql_config["port"],
                               db=mysql_config["db"], charset="utf-8")
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        r = cur.fetchall()
        cur.close()
        conn.close()
        return r
    except Exception as e:
        print('Mysql Error %d: %s' % (e.args[0], e.args[1]))
		
# properties of all
__all__=["exec_sql"]