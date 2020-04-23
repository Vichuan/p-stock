# -*- coding:UTF-8 -*-
import re
import time
import random
import redis as redis
import requests
from bs4 import BeautifulSoup

url = 'http://q.10jqka.com.cn/gn/detail/code/301699/'
concept_url = 'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{}/ajax/1/code/{}'

pool = redis.ConnectionPool(host='49.232.82.238', port=26379, password='Abc1234%', decode_responses=True)
r = redis.Redis(connection_pool=pool)

# 个股概念，redis set，stock->set
STOCK_CONCEPT_DETAIL = "Stock:Concept:Detail:{}"
# 个股详情，redis hash，stock->hash
STOCK_BASIC_SYMBOL = "Stock:Basic:Symble"


def get_html(t_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        'Cookie': '__utma=156575163.1459235509.1583745090.1583745090.1583745090.1; __utmz=156575163.1583745090.1.1.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; spversion=20130314; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1587447698,1587619508,1587619567; historystock=600191%7C*%7C600527; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1587619702; v=Asum7EVbETMft03ncEcG3gBcWmS2YNaTWXKjrD3NpOpjYuUSxTBvMmlEM4FO',
        'Referer': 'http://q.10jqka.com.cn/gn/detail/code/301558/',
        'hexin-v': 'Asum7EVbETMft03ncEcG3gBcWmS2YNaTWXKjrD3NpOpjYuUSxTBvMmlEM4FO',
        'Host': 'q.10jqka.com.cn'
    }
    html = requests.get(t_url, headers=headers).text
    return html


def list_concept(t_url):
    concept_dict = {}
    html = get_html(t_url)
    soup = BeautifulSoup(html, 'html.parser')
    cate_items = soup.find_all(href=re.compile("http://q.10jqka.com.cn/gn/detail/code"))
    for cate in cate_items:
        code = cate['href'].split('/')[6]
        concept_dict[code] = cate.text
    # board_aside = soup.find('div', {'class': 'board-txt board-aside'}).find('p')
    # remark = board_aside.text
    # print(remark)
    # print(type(board_aside))
    # board_hq = soup.find('div', {'class': 'board-hq'})
    # print(board_hq.find("h3").text)
    # print(board_hq.find('span', {'class': 'board-xj arr-fall'}).text)
    # print(board_hq.find('p').text)
    return concept_dict


def concept_(ccpt_url):
    html = get_html(ccpt_url)
    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.find('tbody').find_all('tr')
    for idx, tr in enumerate(tbody):
        tds = tr.find_all('td')
        symbol = tds[1].text
        r.sadd(STOCK_CONCEPT_DETAIL.format(r.hget(STOCK_BASIC_SYMBOL, symbol)), tds[2].text)


if __name__ == '__main__':
    dict_concept = list_concept(url)
    for k, v in dict_concept.items():
        c_url = concept_url.format(1, k)
        soup = BeautifulSoup(get_html(c_url), 'html.parser')
        board_aside = soup.find('span', {'class': 'page_info'})
        pages = board_aside.text.split('/')[1]
        i = 1
        while i <= int(pages):
            second = random.randint(0, 10) + 10
            time.sleep(second)
            print("Concept:", v, "，Page:", i, "，Sleep:", second)
            concept_(concept_url.format(i, k))
            i = i + 1
