"""
CrawlJSON:main():
    CrawlJSON:crawl_all_city(startline, endline)
        CrawlJSON:get_index_url(item[1], num_pages + 1)
            CrawlJSON:get_pages_from(city_code, num_pages)
        CrawlJSON:get_html(index_url)
        CrawlJSON:parse_html(html, index)
            CrawlJSON:get_lng_lat(address)
            CrawlerSightFeature:get_sight_feature(sight_url)
                CrawlerSightFeature:get_index_url(sight_url)
                CrawlerSightFeature:get_html(index_url)
                CrawlerSightFeature:parse_html(html)
            CrawlerPlayTime:get_play_time(title)
                CrawlerPlayTime:get_html(search_url)
                CrawlerPlayTime:parse_place_html(html)
                CrawlerPlayTime:get_time(play_time_str)
                    CrawlerPlayTime:str_2_int(play_time_str)
        CrawlerCityDays:get_city_play_days(item[0])
            CrawlerCityDays:get_html(search_url)
            CrawlerCityDays:parse_city_html(html)
            CrawlerCityDays:get_html(city_url)
            CrawlerCityDays:parse_detail_html(city_html)
"""
import copy
import sys
import os
import csv
import time
import threading

from Crawler.CrawlerCityDays import get_cities_play_days
from Crawler.CrawlerPlace import get_city_places
from Map.InterCityRoute import generate_inter_city_route
from Map.TwoPlacesRoute import transit

def get_index_url(city_code, num_pages):
    urls = get_pages_from(city_code, num_pages)
    for url in urls:
        yield url
    return url

def get_pages_from(city_code, num_pages):
    # print(city_code)
    urls = ['https://you.ctrip.com/sight/' + city_code +
            '/s0-p{}.html#sightname'.format(str(i)) for i in range(1, num_pages, 1)]
    return urls

def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

from requests import RequestException
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'}

def parse_html(html, index):
    doc = pq(html)
    divs = doc('.rdetailbox').items()

    all_places = []

    for div in divs:
        title = div('dt a').text()
        address = div('.ellipsis').text()
        sight_url = "https://you.ctrip.com" + div('dt a').attr('href')
        address_detail = get_lng_lat(address)
        if address_detail['status'] == 0:
            # print(addressDetail)
            lat = address_detail['result']['location']['lat']  # 获取纬度
            lng = address_detail['result']['location']['lng']  # 获取经度
        else:
            title_detail = get_lng_lat(title)
            if title_detail['status'] == 0:
                # print(titleDetail)
                lat = title_detail['result']['location']['lat']  # 获取纬度
                lng = title_detail['result']['location']['lng']  # 获取经度
            else:
                continue


        location = {
            "lat": lat,
            "lng": lng
        }
        sight_feature = get_sight_feature(sight_url)
        image_name = ''
        play_time = get_play_time(title)

        result = {
            "title": title, # ctrip
            "address": address, # ctrip
            "image": image_name,
            "rank": index, # ctrip
            "time": play_time, # qunar
            "location": location, # baidu
            "feature": sight_feature # ctrip
        }

        # print(result)

        all_places.append(result)
        index += 1
    return all_places

from pyquery import PyQuery as pq
from Crawler.CrawlerPlayTime import get_play_time


# 构造获取经纬度的函数
def get_lng_lat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    #   zhihui's key
    ak = 'qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt'
    #   ziyi's key
    # ak = 'YBbMVlde0GPAUl6ePBQY2pIfRwkcqFe6'
    add = quote(address)  # 本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url + add + '&output=' + output + "&ak=" + ak
    # print(url2)
    req = urlopen(url2)
    res = req.read().decode()
    temp = json.loads(res)
    return temp

from urllib.request import urlopen, quote
import json

from Crawler.CrawlerSightFeature import get_sight_feature

from Crawler.CrawlerCityDays import get_city_play_days


def crawl_all_city(startline, endline):
    module_path = os.path.dirname(__file__)
    csv_file_name = module_path + '/data/city_list4.csv'
    csv_file = open(csv_file_name, "r", encoding='utf-8')
    reader = csv.reader(csv_file)

    tid = str(threading.get_ident()) + ":"

    interestingrows = [row for idx, row in enumerate(reader) if idx in range(startline, endline)]
    # print(interestingrows)

    # for item in reader:
    for item in interestingrows:
        all_titles = []
        all_location = []
        all_addresses = []
        all_play_time = []

        begin = time.time()

        # 判断文件是否存在
        if os.path.exists(module_path + '/data/' + item[1] + '.json'):
            print("tid:" + tid + "Read from data", flush=True)
            continue
        else:
            print("tid:" + tid + "Crawler", flush=True)
            num_pages = 4
            all_places = []

            # for循环city_route
            index = 1
            for index_url in get_index_url(item[1], num_pages + 1):
                html = get_html(index_url)
                if html:
                    all_places.extend(parse_html(html, index))
                    index += 15

            city_days = get_city_play_days(item[0])
            city_str = {
                'cityName': item[0],
                'days': city_days,
                'cityImage': '',
                'spots': all_places
            }

            for i in range(len(city_str['spots'])):
                all_titles.append(city_str['spots'][i]['title'])
                all_location.append(city_str['spots'][i]['location'])
                all_addresses.append(city_str['spots'][i]['address'])
                all_play_time.append(city_str['spots'][i]['time'])

            f = open(module_path + '/data/' + item[1] + '.json', 'a', newline='', encoding='utf-8')
            f.write(json.dumps(city_str, ensure_ascii=False))
            f.close()

        print("tid:" + tid + "Elapsed time:" + str(time.time() - begin), flush=True)
        
    csv_file.close()


def main():
    num_thread = 10
    lineNumber = int(1843 / num_thread)
    threads = []
    for i in range(num_thread - 1):
        threadi = threading.Thread(target=crawl_all_city, args=(lineNumber * i, lineNumber * (i + 1)))
        threadi.start()
        threads.append(threadi)

    threadi = threading.Thread(target=crawl_all_city, args=(lineNumber * (num_thread - 1), 1844))
    threadi.start()
    threads.append(threadi)


if __name__ == '__main__':
    main()



