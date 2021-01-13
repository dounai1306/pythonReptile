#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import requests
import schedule
import datetime
import time
import smtplib
from email.mime.text import MIMEText
import sqlite3

# 开始创建数据库
conn = sqlite3.connect('sqlite.db')
c = conn.cursor()
c.execute('''CREATE TABLE SQLITE
       (ID INT PRIMARY KEY     NOT NULL,
       WTIME           TEXT,
       CONTENT            TEXT,
       IMG         TEXT);''')
conn.commit()
print("数据库创建成功")


def weibo():
    # 将数据库内的数据ID存在变量中
    cursor = c.execute("SELECT id, wtime, content, img  from SQLITE")
    datalist = []
    for row in cursor:
        datalist.append(row[0])
    print('数据库数据', datalist)

    # 去爬微博
    r = requests.get("https://m.weibo.cn/api/container/getIndex?containerid=2304135745966493_-_WEIBO_SECOND_PROFILE_WEIBO")
    j = r.json()
    cards = j['data']['cards']
    length = len(cards)
    html = ""
    for i in range(0, length):
        type = cards[i]['card_type']
        # 他的原创
        if type == 9:
            # 排除非置顶的文章
            if 'isTop' not in cards[i]['mblog']:
                mblog = cards[i]['mblog']
                id = int(mblog['id'])
                created_at = mblog['created_at']
                # 微博正文
                text = '' if 'text' not in mblog else str(mblog['text'])
                # 一般图，非原图非缩略图
                pic = '' if 'bmiddle_pic' not in mblog else str(mblog['bmiddle_pic'])

                # 做数据比对，如果是增量数据开始写入到数据库中
                if id in datalist:
                    print("数据库中已经包含当前数据")
                else:
                    c.execute("insert into SQLITE(ID, WTIME, CONTENT, IMG) values(%s, '%s', '%s', '%s')" % (id, created_at, text, pic))
                    conn.commit()

                    if pic:
                        html = html + ("<div><p><strong>[%s]</strong> %s</p><img src='%s' width='200'></div><hr>" % (created_at, text, pic))
                    else:
                        html = html + ("<div><p><strong>[%s]</strong> %s</p></div><hr>" % (created_at, text))

    if html:
        sendmail(html,  str(datetime.datetime.now()))
    else:
        print("未发现更新")
    print("==========================================本次爬取结束==========================================")


def sendmail(html, bacthtime):
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "用户名"  # 用户名
    mail_pass = "密码"  # 密码
    sender = "用户名@163.com"
    receivers = ["接收邮件@163.com"]  # 接收邮件

    message = MIMEText(html, "html", "utf-8")
    message["From"] = "{}".format(sender)
    message["To"] = ",".join(receivers)
    message["Subject"] = "来自豆奶的邮件" + bacthtime
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("本次邮件发送完成")
    except smtplib.SMTPException as e:
        print("邮件发送异常", e)


# 首次执行
# weibo()

# 定时任务，间隔10分钟
schedule.every(10).minutes.do(weibo)

while 1:
    schedule.run_pending()
    time.sleep(1)

