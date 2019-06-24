# -*- coding: utf-8 -*-
import time
import urllib.parse
import re

import requests
from requests import RequestException
from pyquery import PyQuery as pq

csv_file_name = "D:/DevelopTest/ProjectTest/TravelPlace/data/city_list.csv"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def get_places_playtime(titles):
    places_play_time = []
    for title in titles:
        # print(title)
        play_time = get_play_time(title)
        time.sleep(2)
        places_play_time.append(play_time)
    return places_play_time


def get_time(play_time_str):
    play_time_int = str_2_int(play_time_str)
    return play_time_int


def get_play_time(title):
    url_code_title = urllib.parse.quote(title)
    search_url = 'https://travel.qunar.com/search/all/' + url_code_title
    html = get_html(search_url)
    if html:
        play_time_str = parse_place_html(html)
        play_time = get_time(play_time_str)
        return play_time


def get_html(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_place_html(html):
    doc = pq(html)
    divs = doc('.d_days').items()
    if doc('.d_days'):
        for div in divs:
            # print(div.text())
            return div.text()
    else:
        divs = doc('.sc_info').items()
        for div in divs:
            p = div('.days')
            # print(p.text())
            return div('.days').text()


def str_2_int(string):
    # 模板： 建议游玩时间：？？小时（ - ？？小时）
    # 1.取出所有数字求平均（double型）
    # 2.没有的默认设为2小时
    if string:
        str_list = re.findall(r"\d+\.?\d*", string)
        count = 0
        for str in str_list:
            count += float(str)
        # print(count / len(str_list))
        return count / len(str_list)
    else:
        return 2



