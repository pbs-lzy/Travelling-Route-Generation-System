# -*- coding: utf-8 -*-
import time
import urllib.parse

import requests
from requests import RequestException
from pyquery import PyQuery as pq

csv_file_name = "D:/DevelopTest/ProjectTest/TravelPlace/data/city_list.csv"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def allocate_time(cities_play_days, total_days, count_days):
    allocated_playtime = []
    ave_coe = total_days / count_days
    count = 0
    for i in range(len(cities_play_days)):
        if i != (len(cities_play_days) - 1):
            curr_day = round(cities_play_days[i] * ave_coe)
            allocated_playtime.append(curr_day)
            count += curr_day
        else:
            allocated_playtime.append(total_days - curr_day)
    return allocated_playtime


def get_cities_play_days(city_names_list, total_days):
    cities_play_days = []
    count_days = 0
    for city_name in city_names_list:
        play_day = get_city_play_days(city_name)
        time.sleep(2)
        cities_play_days.append(int(play_day))
        count_days += int(play_day)
    allocated_play_days = allocate_time(cities_play_days, total_days, count_days)
    return allocated_play_days


def get_city_play_days(city_name):
    url_code_city_name = urllib.parse.quote(city_name)
    search_url = 'https://travel.qunar.com/search/all/' + url_code_city_name
    html = get_html(search_url)
    if html:
        city_url = parse_city_html(html)
        city_html = get_html(city_url)
        city_play_days = parse_detail_html(city_html)
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
