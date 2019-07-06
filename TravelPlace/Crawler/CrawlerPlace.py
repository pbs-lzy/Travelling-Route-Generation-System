# -*- coding: utf-8 -*-
# 从数据库导入城市代码数据
import io
import sys

import requests
import json
import csv
import os
from pyquery import PyQuery as pq
from urllib.request import urlopen, quote

from requests import RequestException

from Crawler.CrawlerCityDays import get_city_play_days
from Crawler.CrawlerPlayTime import get_play_time
from Crawler.CrawlerSightFeature import get_sight_feature

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'}

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# 从文件中读取指定城市代码，用于构造url
def read_csv(city_name):
    module_path = os.path.dirname(os.path.dirname(__file__))
    csv_file_name = module_path + '/data/city_list.csv'
    csv_file = open(csv_file_name, "r")
    reader = csv.reader(csv_file)

    for item in reader:
        if reader.line_num == 1:
            continue
        if item[0] == city_name:
            csv_file.close()
            return item[1]


def get_pages_from(city_code, num_pages):
    # print(city_code)
    urls = ['https://you.ctrip.com/sight/' + city_code +
            '/s0-p{}.html#sightname'.format(str(i)) for i in range(1, num_pages, 1)]
    return urls


def get_index_url(city_code, num_pages):
    urls = get_pages_from(city_code, num_pages)
    for url in urls:
        yield url
    return url


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_html(html, index):
    doc = pq(html)
    divs = doc('.rdetailbox').items()

    all_places = []

    for div in divs:
        title = div('dt a').text()
        address = div('.ellipsis').text()
        sight_url = "https://you.ctrip.com" + div('dt a').attr('href')
        addressDetail = get_lng_lat(address)
        if addressDetail['status'] == 0:
            # print(addressDetail)
            lat = addressDetail['result']['location']['lat']  # 获取纬度
            lng = addressDetail['result']['location']['lng']  # 获取经度
        else:
            titleDetail = get_lng_lat(title)
            # print(titleDetail)
            lat = titleDetail['result']['location']['lat']  # 获取纬度
            lng = titleDetail['result']['location']['lng']  # 获取经度

        location = {
            "lat": lat,
            "lng": lng
        }
        sight_feature = get_sight_feature(sight_url)
        image_name = ''
        play_time = get_play_time(title)

        result = {
            "title": title,
            "address": address,
            "image": image_name,
            "rank": index,
            "time": play_time,
            "location": location,
            "feature": sight_feature
        }

        # print(result)

        all_places.append(result)
        index += 1
    return all_places


# 构造获取经纬度的函数
def get_lng_lat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    ak = 'qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt'
    # ak = 'YBbMVlde0GPAUl6ePBQY2pIfRwkcqFe6'
    add = quote(address)  # 本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url + add + '&output=' + output + "&ak=" + ak
    # print(url2)
    req = urlopen(url2)
    res = req.read().decode()
    temp = json.loads(res)
    return temp


def get_city_places(city_name):
    # 取json数据例子
    # str = '{"country" : "china", "person":[{"name": 2.5, "gender": "male"}, {"name": 3, "gender": "male"}]}'
    # json_str = json.loads(str)
    # print(type(json_str))
    # person = json_str['person']
    # print(type(person))
    # print(person[1]['name'])

    all_titles = []
    all_location = []
    all_addresses = []
    all_play_time = []

    # 判断文件是否存在
    city_code = read_csv(city_name)
    module_path = os.path.dirname(os.path.dirname(__file__))
    if os.path.exists(module_path + '/data/' + city_code + '.json'):
        print("Read from data")
        fp = open(module_path + '/data/' + city_code + '.json', 'r', encoding='utf-8')
        # print(fp)
        city_str = json.load(fp)

        city_days = city_str['days']
        # for i in range(city_str['spots'][-1]['rank']):
        for i in range(len(city_str['spots'])):
            all_titles.append(city_str['spots'][i]['title'])
            all_location.append(city_str['spots'][i]['location'])
            all_addresses.append(city_str['spots'][i]['address'])
            all_play_time.append(city_str['spots'][i]['time'])

        # print(city_days)
        # print(all_titles)
        # print(all_location)
        # print(all_addresses)
        # print(all_play_time)
        return city_days, all_titles, all_location, all_addresses, all_play_time
    else:
        print("Crawler")

        num_pages = 4
        all_places = []

        # for循环city_route
        index = 1
        for index_url in get_index_url(city_code, num_pages + 1):
            html = get_html(index_url)
            if html:
                all_places.extend(parse_html(html, index))
                index += 15

        city_days = get_city_play_days(city_name)
        city_str = {
            'cityName': city_name,
            'days': city_days,
            'cityImage': '',
            'spots': all_places
        }

        # print("type:")
        # print(type(city_str))
        # print("city_str:")
        # print(city_str)

        # print("type:")
        # print(type(city_str['spots'][-1]['rank']))
        # print("city_str['spots'][-1]['rank']:")
        # print(city_str['spots'][-1]['rank'])

        for i in range(len(city_str['spots'])):
            all_titles.append(city_str['spots'][i]['title'])
            all_location.append(city_str['spots'][i]['location'])
            all_addresses.append(city_str['spots'][i]['address'])
            all_play_time.append(city_str['spots'][i]['time'])

        f = open(module_path + '/data/' + city_code + '.json', 'a', newline='', encoding='utf-8')
        f.write(json.dumps(city_str, ensure_ascii=False))
        f.close()

        # print(city_days)
        # print(all_titles)
        # print(all_location)
        # print(all_addresses)
        # print(all_play_time)

        return city_days, all_titles, all_location, all_addresses, all_play_time
