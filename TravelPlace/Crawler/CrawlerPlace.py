# -*- coding: utf-8 -*-
# 从数据库导入城市代码数据
# crawl from ctrip
import requests
import json
import csv
import os
from requests import RequestException
from pyquery import PyQuery as pq
from urllib.request import urlopen, quote

#from Crawler.CrawlerSightFeature import get_sight_feature
def get_index_url_p(sight_url):
    yield sight_url
    return sight_url

def get_sight_feature(sight_url):
    for index_url in get_index_url_p(sight_url):
        html = get_html(index_url)
        if html:
            features = parse_html(html)
            return features

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'}


#   从文件中读取指定城市代码，用于构造url
#   return city_code by city_name
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

#   return urls which contains the travel spots of different cities from ctrip
#   example: https://you.ctrip.com/sight/hangzhou14/s0-p1.html#sightname
def get_pages_from(city_name, num_pages):
    city_code = read_csv(city_name)
    print(city_code)
    urls = ['https://you.ctrip.com/sight/' + city_code +
            '/s0-p{}.html#sightname'.format(str(i)) for i in range(1, num_pages, 1)]
    return urls

#   return urls generators which contains the travel spots of different cities
def get_index_url(city_name, num_pages):
    urls = get_pages_from(city_name, num_pages)
    for url in urls:
        yield url
    return url

#   return html by the given url
def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#   return the titles, addresses of a html from ctrip
#   sight_url:https://you.ctrip.com/sight/shanghaidisneyresort1446916/1412255.html
#   title:上海迪士尼度假区
#   address:上海市浦东新区川沙新镇上海迪士尼度假区
def parse_html(html):
    doc = pq(html)
    divs = doc('.rdetailbox').items()

    page_title = []
    page_address = []

    for div in divs:
        title = div('dt a').text()
        address = div('.ellipsis').text()
        # https://you.ctrip.com/sight/shanghaidisneyresort1446916/1412255.html
        sight_url = "https://you.ctrip.com" + div('dt a').attr('href')
        
        # print("sight_url:" + sight_url)
        # print("title:" + title)
        # print("address:" + address)

        # lat = get_lng_lat(title)['result']['location']['lat']  # 获取纬度
        # lng = get_lng_lat(title)['result']['location']['lng']  # 获取经度
        # location = '{"lat":' + str(lat) + ',"lng":' + str(lng) + '},'
        # sight_feature = get_sight_feature(sight_url)


        result = {
            'title': title,
            'address': address,
            # 'location': location,
            # 'feature': sight_feature
        }

        page_title.append(result['title'])
        page_address.append(result['address'])
    return page_title, page_address


# 构造获取经纬度的函数
def get_lng_lat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    ak = 'qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt'
    add = quote(address)  # 本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url + add + '&output=' + output + "&ak=" + ak
    req = urlopen(url2)
    res = req.read().decode()
    temp = json.loads(res)
    return temp


#   return travel spots and corresponding addresses
def get_city_places():
    city_name = "上海"
    num_pages = 2
    all_titles = []
    all_addresses = []
    for index_url in get_index_url(city_name, num_pages + 1):
        html = get_html(index_url)
        if html:
            page_title, page_address = parse_html(html)
            all_titles.extend(page_title)
            all_addresses.extend(page_address)
    return all_titles, all_addresses

    