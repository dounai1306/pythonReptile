#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('lianjia.db')
c = conn.cursor()
print("Opened database successfully")

cursor = c.execute("SELECT id, xiaoqu, chengjiaoshijian, huxing, suozailouceng, jianzhumianji, huxingjiegou,taoneimianji,jianzhuleixing, fangwuchaoxiang, jianchengniandai,zhuangxiu,jianzhujiegou,gongnuanfangshi,tihubili,dianti,totalprice, unitprice from LIANJIA")
for row in cursor:
    print(row)

print("Operation done successfully")
conn.close()
