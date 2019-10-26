# -*- coding:UTF-8 -*-
import re

import requests
from bs4 import BeautifulSoup
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url = 'http://q.10jqka.com.cn/gn/detail/code/301699/'


def get_html(t_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    html = requests.get(t_url, headers=headers).text
    return html


def list_concept(t_url):
    html = get_html(t_url)
    soup = BeautifulSoup(html, 'html.parser')
    # cate_items = soup.find_all(href=re.compile("http://q.10jqka.com.cn/gn/detail/code"))
    # for cate in cate_items:
    #     print(cate['href'])
    #     print(cate.text)

    # 概念定义
    board_aside = soup.find('div', {'class': 'board-txt board-aside'}).find('p')
    remark = board_aside.text
    print('remark:', remark)

    # 概念名称
    concept_name = ''
    # 概念code
    concept_code = ''
    # 当前价格
    current = 0
    # 涨跌额
    extent = 0
    # 涨跌幅
    percent = 0
    open1 = 0
    yesterday_close = 0
    low = 0
    high = 0
    amount = 0
    volume = 0
    inflow = 0
    rise_count = 0
    fall_count = 0

    board_hq = soup.find('div', {'class': 'board-hq'})
    all_contents = board_hq.contents
    for i, child in enumerate(all_contents):
        if child.name == 'h3':
            for j, sub in enumerate(child):
                if j == 0:
                    concept_name = sub
                if sub.name == 'span':
                    concept_code = sub.text
        if child.name == 'span':
            current = child.text
        if child.name == 'p':
            str_list = child.text.split()
            extent = str_list[0]
            percent = float(str_list[1][:-1]) / 100

    dl = soup.find('div', {'class': 'board-infos'}).find_all('dl')
    for d in dl:
        if d.dt.text == '今开':
            open1 = d.dd.text
        if d.dt.text == '昨收':
            yesterday_close = d.dd.text
        if d.dt.text == '最低':
            low = d.dd.text
        if d.dt.text == '最高':
            high = d.dd.text
        if d.dt.text == '成交量(万手)':
            amount = d.dd.text
        if d.dt.text == '成交额(亿)':
            volume = d.dd.text
        if d.dt.text == '资金净流入(亿)':
            inflow = d.dd.text
        if d.dt.text == '涨跌家数':
            for i, dc in enumerate(d.dd.contents):
                if i == 1:
                    rise_count = dc.text
                if i == 3:
                    fall_count = dc.text

    print('concept_name:', concept_name)
    print('concept_code:', concept_code)
    print('current:', current)
    print('extent:', extent)
    print('percent:', percent)
    print('open:', open1)
    print('yesterday_close:', yesterday_close)
    print('low:', low)
    print('high:', high)
    print('amount:', amount)
    print('volume:', volume)
    print('inflow:', inflow)
    print('rise_count:', rise_count)
    print('fall_count:', fall_count)


if __name__ == '__main__':
    # htmlStr = get_html(url)
    # print(htmlStr)
    print(list_concept(url))
