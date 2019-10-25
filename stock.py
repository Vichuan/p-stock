# -*- coding:UTF-8 -*-
import re

import requests
from bs4 import BeautifulSoup

url = 'http://q.10jqka.com.cn/gn/detail/code/301699/'


def get_html(t_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    html = requests.get(t_url, headers=headers).text
    return html


def list_concept(t_url):
    html = get_html(t_url)
    soup = BeautifulSoup(html, 'html.parser')
    cate_items = soup.find_all(href=re.compile("http://q.10jqka.com.cn/gn/detail/code"))
    for cate in cate_items:
        print(cate['href'])
        print(cate.text)

    board_aside = soup.find('div', {'class': 'board-txt board-aside'}).find('p')
    remark = board_aside.text
    print(remark)
    board_hq = soup.find('div', {'class': 'board-hq'})
    name = board_hq.find("h3").text
    print(name[:-6])
    value = board_hq.find('span', {'class': 'board-xj arr-fall'})
    print(value)

    # print(board_hq.find('span', {'class': 'board-xj arr-fall'}).text)
    print(board_hq.find('p').text)

    dl = soup.find('div', {'class': 'board-infos'}).find_all('dl')
    for d in dl:
        print(type(d))
        # print(d['dt'].text+' '+d['dd'].text)
    print(dl)


if __name__ == '__main__':
    # htmlStr = get_html(url)
    # print(htmlStr)
    print(list_concept(url))
