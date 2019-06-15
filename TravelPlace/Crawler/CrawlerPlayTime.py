# -*- coding: utf-8 -*-
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup
from requests import RequestException
from pyquery import PyQuery as pq

csv_file_name = "D:/DevelopTest/ProjectTest/TravelPlace/data/city_list.csv"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def get_places_playtime(titles):
    places_play_time = []
    for title in titles:
        print(title)
        play_time = get_playtime(title)
        time.sleep(3)
        places_play_time.append(play_time)
    print(places_play_time)
    return places_play_time


def get_time(place_url):
    place_html = get_html(place_url)
    play_time_str = parse_time_html(place_html)
    play_time_int = str_2_int(play_time_str)
    return play_time_int


def get_playtime(title):
    url_code_title = urllib.parse.quote(title)
    search_url = 'http://www.mafengwo.cn/search/s.php?q=' + url_code_title + '&t=pois&seid=&mxid=&mid=&mname=&kt=1'
    html = get_html(search_url)
    if html:
        poi_url = parse_poi_html(html)
        poi_html = get_html(poi_url)
        place_url = parse_place_html(poi_html)
        playtime_from_html = get_time(place_url)
        return playtime_from_html


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_poi_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for poi in soup.find_all('a', attrs={'data-search-category' : 'poi'}):
        poi_url = poi.get('href')
        return poi_url


def parse_place_html(html):
    doc = pq(html)
    divs = doc('.ct-text').items()
    for div in divs:
        place_herf = div('a').attr('href')
        print(place_herf)
        return place_herf


def parse_time_html(html):
    if html:
        doc = pq(html)
        li = doc('.item-time')
        time = li('.content').text()
        if time == '':
            return '2小时'
        return time
    else:
        return '2小时'


def str_2_int(str):
    if str == '1小时以下':
        return 1
    elif str == '1-3小时':
        return 2
    elif str == '3小时以上':
        return 4
    elif str == '1天':
        return 6
    else:
        return 2



