# -*- coding:UTF-8 -*-
import os
import re
import urllib
from io import open

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
        # for ah in cate:
        #     # cate.find_all('div', {'class': 'cate_items'})
        #     print(ah.find_all(attrs={'name': 'href'}))
    board_wrap = soup.find_all('div', {'class': 'board-wrap'})
    board_wrap.


if __name__ == '__main__':
    # htmlStr = get_html(url)
    # print(htmlStr)
    print(list_concept(url))

# soup = BeautifulSoup(html, 'html.parser')
# img_ul = soup.find_all('div', {'class': 'li_img'})
#
# os.makedirs('./传播智客/', exist_ok=True)
#
# for ul in img_ul:
#     imgs = ul.find_all('img')
#     # print(imgs)
#     for img in imgs:
#         url = img['data-original']
#         img_name = url.split('/')[-1]
#         req = requests.get(main_url + url, stream=True)
#         with open('./传播智客/%s' % img_name, 'wb') as f:
#             for chunk in req.iter_content(chunk_size=128):
#                 f.write(chunk)
#         print('Saved %s' % img_name)
