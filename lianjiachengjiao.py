#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3


# 开始创建数据库
conn = sqlite3.connect('lianjia.db')
c = conn.cursor()
c.execute('''CREATE TABLE LIANJIA
       (ID INT PRIMARY KEY     NOT NULL,
       CHENGJIAOSHIJIAN           TEXT,
       XIAOQU            TEXT,
       HUXING            TEXT,
       SUOZAILOUCENG            TEXT,
       JIANZHUMIANJI            TEXT,
       HUXINGJIEGOU            TEXT,
       TAONEIMIANJI            TEXT,
       JIANZHULEIXING            TEXT,
       FANGWUCHAOXIANG            TEXT,
       JIANCHENGNIANDAI            TEXT,
       ZHUANGXIU            TEXT,
       JIANZHUJIEGOU            TEXT,
       GONGNUANFANGSHI            TEXT,
       TIHUBILI            TEXT,
       DIANTI            TEXT,
       TOTALPRICE            TEXT,
       UNITPRICE         TEXT);''')
print("数据库创建成功")
conn.commit()


from requests_html import HTMLSession
session = HTMLSession()

r = session.get('https://sh.lianjia.com/chengjiao/')
houseList = r.html.find('.listContent > li')

data_map = {
    '房屋户型': 'HUXING',
    '所在楼层': 'SUOZAILOUCENG',
    '建筑面积': 'JIANZHUMIANJI',
    '户型结构': 'HUXINGJIEGOU',
    '套内面积': 'TAONEIMIANJI',
    '建筑类型': 'JIANZHULEIXING',
    '房屋朝向': 'FANGWUCHAOXIANG',
    '建成年代': 'JIANCHENGNIANDAI',
    '装修情况': 'ZHUANGXIU',
    '建筑结构': 'JIANZHUJIEGOU',
    '供暖方式': 'GONGNUANFANGSHI',
    '梯户比例': 'TIHUBILI',
    '配备电梯': 'DIANTI'
}


def return_text(src, tag):
    obj = src.find(tag, first=True)
    return obj.text


def async_get_detail(link):
    res = session.get(link)
    intro_list = res.html.find('#introduction > .introContent > .base > .content > ul > li')
    info = dict()

    house_href = res.html.find('.house-title', first=True)
    house_id = house_href.attrs['data-lj_action_resblock_id']

    info['HOUSEID'] = house_id

    for intro in intro_list:
        full_text = intro.text
        label_text = return_text(intro, 'span')
        val_text = full_text.strip(label_text)
        info[data_map[label_text]] = val_text
    return info


def insert_db(xiaoqu, total_price, unit_price, deal_date, asyncInfo):
    HOUSEID = asyncInfo['HOUSEID']
    HUXING = asyncInfo['HUXING']
    SUOZAILOUCENG = asyncInfo['SUOZAILOUCENG']
    JIANZHUMIANJI = asyncInfo['JIANZHUMIANJI']
    HUXINGJIEGOU = asyncInfo['HUXINGJIEGOU']
    TAONEIMIANJI = asyncInfo['TAONEIMIANJI']
    JIANZHULEIXING = asyncInfo['JIANZHULEIXING']
    FANGWUCHAOXIANG = asyncInfo['FANGWUCHAOXIANG']
    JIANCHENGNIANDAI = asyncInfo['JIANCHENGNIANDAI']
    ZHUANGXIU = asyncInfo['ZHUANGXIU']
    JIANZHUJIEGOU = asyncInfo['JIANZHUJIEGOU']
    GONGNUANFANGSHI = asyncInfo['GONGNUANFANGSHI']
    TIHUBILI = asyncInfo['TIHUBILI']
    DIANTI = asyncInfo['DIANTI']

    c.execute(
        '''insert into LIANJIA values(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',  '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
        HOUSEID, deal_date, xiaoqu, HUXING, SUOZAILOUCENG, JIANZHUMIANJI, HUXINGJIEGOU, TAONEIMIANJI, JIANZHULEIXING,
        FANGWUCHAOXIANG, JIANCHENGNIANDAI, ZHUANGXIU, JIANZHUJIEGOU, GONGNUANFANGSHI, TIHUBILI, DIANTI, total_price,
        unit_price))
    conn.commit()
    print("写入成功")


for house in houseList:
    title = return_text(house, '.title > a')
    totalPrice = return_text(house, '.totalPrice > .number')
    unitPrice = return_text(house, '.unitPrice > .number')
    dealDate = return_text(house, '.dealDate')

    # 拿到详情链接去爬详情
    detail_href = house.find('.title > a', first=True)
    href = detail_href.attrs['href']
    asyncInfo = async_get_detail(href)

    # 写库
    name = (title.split(' '))[0]
    insert_db(name, totalPrice, unitPrice, dealDate, asyncInfo)
