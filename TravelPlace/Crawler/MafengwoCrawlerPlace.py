'''
    每个城市
    '_ts': 1559799547314,
    '_sn': '6935c0f07f'
    参数都不一样 没法爬...
'''
import json
import re
import urllib
from urllib import request

from bs4 import BeautifulSoup

headers = {
        'Referer': 'http://www.mafengwo.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }


def get_places():
    city_code = 10035
    page = 1
    num_pages = get_num_pages(city_code, page)
    for page in range(num_pages):
        places = get_route(city_code, page)
        print(places)


def enter_web(city_code, page):
    post_data = {
        'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
        'iMddid': city_code,
        'iTagId': 0,
        'iPage': page,
        '_ts': 1559799547314,
        '_sn': '6935c0f07f'
    }
    url = 'http://www.mafengwo.cn/ajax/router.php'
    data = urllib.parse.urlencode(post_data).encode()
    req = request.Request(url, data=data, headers=headers)
    res = request.urlopen(req)
    res = res.read()
    print(res)
    json_dict = json.loads(res)
    return json_dict


def get_num_pages(city_code, page):
    json_dict = enter_web(city_code, page)
    page_data = json_dict['data']['page']

    soup_page = BeautifulSoup(page_data, "html.parser")
    page = int(soup_page.find('span', class_='count').find('span').text)
    return page


def get_route(city_code, page):
    json_dict = enter_web(city_code, page)
    list_data = json_dict['data']['list']

    soup = BeautifulSoup(list_data, "html.parser")
    route_list = soup.find_all('a')
    place_list = []
    for route in route_list:
        link = route['href']
        route_id = re.findall(r'/poi/(.*?).html', link)
        name = route['title']
        image = route.find('img')['src'].split('?')[0]
        place_list.append({
            'poi_id': int(route_id[0]),
            'name': name,
            'image': image,
            'link': 'http://www.mafengwo.cn'+link,
        })
    return place_list


def main():
    get_places()


if __name__ == '__main__':
    main()

