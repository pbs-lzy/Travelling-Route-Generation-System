# -*- coding: utf-8 -*-
# 数据导出到数据库
import requests
import csv
from requests import RequestException
from pyquery import PyQuery as pq

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'}


def get_pages_from():
    # 共185页
    urls = ['https://you.ctrip.com/countrysightlist/china110000/p{}.html'.format(str(i)) for i in range(1, 186, 1)]
    return urls


def get_index_url():
    urls = get_pages_from()
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
    divs = doc('.list_mod1').items()
    for div in divs:
        city_name = div('dt a').text()
        city_herf = div('dt a').attr('href')
        city_code = city_herf[7:-5]
        write_csv(city_name, city_code)


def ini_csv():
    file_header = ['city_name', 'city_code']
    csv_file = open("city_list.csv", "w", newline='')
    writer = csv.writer(csv_file)
    writer.writerow(file_header)
    csv_file.close()


def write_csv(city_name, city_code):
    csv_file = open("city_list.csv", "a", newline='')
    writer = csv.writer(csv_file)
    writer.writerow([city_name, city_code])
    csv_file.close()


def main():
    ini_csv()
    for index_url in get_index_url():
        html = get_html(index_url)
        if html:
            parse_html(html)


if __name__ == '__main__':
    main()
