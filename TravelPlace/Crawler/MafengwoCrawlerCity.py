# -*- coding: utf-8 -*-
# 数据导出到数据库
import re
import os
import requests
import csv
from requests import RequestException
from pyquery import PyQuery as pq

# 1.查询景点名称
# 2.进入搜索到的第一个链接
# 3.得到用时参考
# 4.如果没有结果 则返回2小时

module_path = os.path.dirname(os.path.dirname(__file__))
csv_file_name = module_path + '/data/city_list.csv'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'}


def get_pages_from():
    city_name_list, length = read_city_name()
    for i in range(1, length):
        if i == 1:
            continue
        city_name = city_name_list[i]
        url = 'http://www.mafengwo.cn/search/s.php?q=' + city_name
        html = get_html(url)
        if html:
            parse_html(html, city_name)


def get_index_url():
    url = get_pages_from()
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


def parse_html(html, city_name):
    doc = pq(html)
    # city_name = (doc('.clearfix ser-title').items())('h2 a').text()
    divs = doc('.lst-nub').items()
    for div in divs:
        city_herf = div('a').attr('href')
        city_code = re.match(".*/(\d+).*", city_herf).group(1)
        print(city_name)
        print(city_code)
        write_csv(city_name, city_code)


def ini_csv():
    file_header = ['city_name', 'city_code']
    csv_file = open("mfwcity_list.csv", "w", newline='')
    writer = csv.writer(csv_file)
    writer.writerow(file_header)
    csv_file.close()


def read_city_name():
    csv_file = open(csv_file_name, "r")
    reader = csv.reader(csv_file)
    city_name_list = []
    count = 0
    for item in reader:
        if reader.line_num == 1:
            continue
        else:
            city_name_list.append(item[0])
            count = count + 1
    return city_name_list, count


def write_csv(city_name, city_code):
    csv_file = open("mfwcity_list.csv", "a", newline='')
    writer = csv.writer(csv_file)
    writer.writerow([city_name, city_code])
    csv_file.close()


def main():
    for index_url in get_index_url():
        html = get_html(index_url)
        if html:
            parse_html(html)


if __name__ == '__main__':
    main()
