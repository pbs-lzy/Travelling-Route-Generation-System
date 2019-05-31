# -*- coding: utf-8 -*-
# 从数据库导入城市代码数据
import requests
import json
import csv
from requests import RequestException
from pyquery import PyQuery as pq
from urllib.request import urlopen, quote

from CrawlerSightFeature import get_sight_feature

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'}


# 从文件中读取指定城市代码，用于构造url
def read_csv(city_name):
    csvFile = open("city_list.csv", "r")
    reader = csv.reader(csvFile)

    for item in reader:
        if reader.line_num == 1:
            continue
        if item[0] == city_name:
            csvFile.close()
            return item[1]


def get_pages_from(city_name, num_pages):
    city_code = read_csv(city_name)
    print(city_code)
    urls = ['https://you.ctrip.com/sight/' + city_code + '/s0-p{}.html#sightname'.format(str(i)) for i in range(1, num_pages, 1)]
    return urls


def get_index_url(city_name, num_pages):
    urls = get_pages_from(city_name, num_pages)
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


def parse_html(html):
    doc = pq(html)
    divs = doc('.rdetailbox').items()

    for div in divs:
        title = div('dt a').text()
        address = div('.ellipsis').text()
        sight_url = "https://you.ctrip.com" + div('dt a').attr('href')

        lng = get_lng_lat(title)['result']['location']['lng']  # 获取经度
        lat = get_lng_lat(title)['result']['location']['lat']  # 获取纬度
        location = '{"lat":' + str(lat) + ',"lng":' + str(lng) + '},'
        sight_feature = get_sight_feature(sight_url)

        result = {
                'title': title,
                'address': address,
                'location': location,
                'feature': sight_feature
            }
        print(result)


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


def main():
    city_name = "南宁"
    num_pages = 1
    for index_url in get_index_url(city_name, num_pages + 1):
        html = get_html(index_url)
        if html:
            parse_html(html)


if __name__ == '__main__':
    main()