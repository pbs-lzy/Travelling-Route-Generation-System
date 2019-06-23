# -*- coding: utf-8 -*-
# crawl from mafengwo
import time
import urllib.parse
import os
import requests
from bs4 import BeautifulSoup
from requests import RequestException
from pyquery import PyQuery as pq

#csv_file_name = "D:/DevelopTest/ProjectTest/TravelPlace/data/city_list.csv"
module_path = os.path.dirname(os.path.dirname(__file__))
csv_file_name = module_path + '/data/city_list.csv'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

#   get the array of playtime
def get_places_playtime(titles):
    places_play_time = []
    for title in titles:
        play_time = get_playtime(title)
        #   time.sleep(3)
        places_play_time.append(play_time)
    return places_play_time

#   search travel spots
#   search_url: http://www.mafengwo.cn/search/s.php?q=%E4%B8%8A%E6%B5%B7%E8%BF%AA%E5%A3%AB%E5%B0%BC%E5%BA%A6%E5%81%87%E5%8C%BA&t=pois&seid=&mxid=&mid=&mname=&kt=1
#   search_url: http://www.mafengwo.cn/search/s.php?q=上海迪士尼度假区&t=pois&seid=&mxid=&mid=&mname=&kt=1
#   choose the "景点" on the mafengwo webpage
#   poi_url: http://www.mafengwo.cn/search/q.php?q=%E4%B8%8A%E6%B5%B7%E8%BF%AA%E5%A3%AB%E5%B0%BC%E5%BA%A6%E5%81%87%E5%8C%BA&t=pois&seid=&mxid=0&mid=0&mname=&kt=1
#   poi_url: http://www.mafengwo.cn/search/q.php?q=上海迪士尼度假区&t=pois&seid=&mxid=0&mid=0&mname=&kt=1
#   click the first link
#   place_url: http://www.mafengwo.cn/poi/6102028.html
#   get the "用时参考"
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

#   choose the "景点" on the mafengwo webpage
#   return that url
def parse_poi_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for poi in soup.find_all('a', attrs={'data-search-category' : 'poi'}):
        poi_url = poi.get('href')
        return poi_url

#   return html by the given url
def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#   get the first url of the html page
def parse_place_html(html):
    doc = pq(html)
    divs = doc('.ct-text').items()
    for div in divs:
        place_herf = div('a').attr('href')
        return place_herf

#   get the "参考用时"
def get_time(place_url):
    place_html = get_html(place_url)
    play_time_str = parse_time_html(place_html)
    play_time_int = str_2_int(play_time_str)
    return play_time_int
    
#   get time under the "用时参考"
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

#   return time in int type from string type
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



