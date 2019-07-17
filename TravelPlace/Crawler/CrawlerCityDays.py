# -*- coding: utf-8 -*-
import time
import urllib.parse

import requests
import os
import csv
import json


from requests import RequestException
from pyquery import PyQuery as pq

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

# 从文件中读取指定城市代码，用于构造url
#   get the city_code by the city_name
def read_csv(city_name):
    module_path = os.path.dirname(os.path.dirname(__file__))
    csv_file_name = module_path + '/data/city_list.csv'
    csv_file = open(csv_file_name, "r", encoding='utf-8')
    reader = csv.reader(csv_file)

    #   可用二分查找加速
    for item in reader:
        if reader.line_num == 1:
            continue
        if item[0] == city_name:
            csv_file.close()
            return item[1]

    csv_file.close()

#   generate the play times of different cities by scaling up or down
def allocate_time(cities_play_days, total_days, count_days):
    allocated_playtime = []
    ave_coe = total_days / count_days
    count = 0
    curr_day = 0
    for i in range(len(cities_play_days)):
        if i != (len(cities_play_days) - 1):
            curr_day = round(cities_play_days[i] * ave_coe)
            allocated_playtime.append(curr_day)
            count += curr_day
        else:
            allocated_playtime.append(total_days - count)
    return allocated_playtime


def get_cities_play_days(city_names_list, total_days):
    cities_play_days = []
    count_days = 0
    for city_name in city_names_list:
        play_day = get_city_play_days(city_name)
        # time.sleep(2)
        cities_play_days.append(int(play_day))
        count_days += int(play_day)
    allocated_play_days = allocate_time(cities_play_days, total_days, count_days)
    return allocated_play_days

#   get the city recommended playtime in json file
def get_city_play_days(city_name):
    method = "byJSON"
    if method == "byJSON":
        city_code = read_csv(city_name)
        module_path = os.path.dirname(os.path.dirname(__file__))
        f = open(module_path + '/data/' + city_code + '.json', 'r', encoding='utf-8')
        city_str = json.load(f)
        city_days = city_str['days']
        f.close()
        # can return log latitude
        return city_days
    else:
        url_code_city_name = urllib.parse.quote(city_name)
        search_url = 'https://travel.qunar.com/search/all/' + url_code_city_name
        html = get_html(search_url)
        if html:
            city_url = parse_city_html(html)
            city_html = get_html(city_url)
            if city_html:
                city_play_days = parse_detail_html(city_html)
            else:
                city_play_days = 2
            return city_play_days


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_city_html(html):
    doc = pq(html)
    div = doc('.sc_info')
    city_url = div('h2 a').attr('href')
    return city_url


def parse_detail_html(html):
    doc = pq(html)
    div = doc('.countbox')
    span = div('.c_item span')
    city_playtime = span.text()
    return city_playtime



