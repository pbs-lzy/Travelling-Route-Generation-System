# -*- coding: utf-8 -*-
import requests
from requests import RequestException
from pyquery import PyQuery as pq

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'}


def get_index_url(sight_url):
    yield sight_url
    return sight_url


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
    ul = doc('.introduce-feature')
    p = doc('.introduce-content')
    sight_features = ul('span').text()
    sight_content = p.text()
    result = {
        'sight_features': sight_features,
        'sight_content': sight_content
    }
    return result


def get_sight_feature(sight_url):
    for index_url in get_index_url(sight_url):
        html = get_html(index_url)
        if html:
            features = parse_html(html)
            return features
