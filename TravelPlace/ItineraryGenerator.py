"""
挑选出可能可以游玩到的景点
从头开始累加各景点游玩时间，求到>13为止

贪婪算法
    1.给定酒店位置
    while（总游玩时间不超过13小时）
        if（已经用掉的时间+此时位置回酒店的时间>11） 回酒店
        else
            2.遍历所有点，储存用时，比较出最短用时的下一地点
            3.进入下一地点，到达过的地点不再遍历

从当前景点A决定去不去下一个景点B的话 应该是判断
（去B的时间+B的建议游玩时间+B到酒店的时间）<剩下可以玩的时间 否则的话找下一个可能的B'再判断

加上如果公交时间>3小时或没有公交线路时，打车
"""
import copy
import sys
import os
import csv
import json
import math
import requests
import numpy
from urllib.request import urlopen, quote

from Crawler.CrawlerCityDays import get_cities_play_days
from Crawler.CrawlerPlace import get_city_places
from Map.InterCityRoute import generate_inter_city_route
from Map.TwoPlacesRoute import transit

max_total_playtime = 13
EARTH_RADIUS = 6378.137  # 地球半径


# def load_data(city_name):
#     city_days, all_titles, all_location, all_addresses, all_play_time = get_city_places(city_name)
#     return all_titles, all_location, all_addresses, all_play_time


def choose_place(play_time, num_days):
    num_place = 0
    total_time = 0
    while total_time <= (max_total_playtime * num_days):
        total_time = total_time + play_time[num_place]
        num_place = num_place + 1
    return num_place

def multi_day_route(hotelName, hotelLocation, title, location, play_time, num_days):
    place_flag = [0] * len(title)
    hotel_time_matrix = numpy.zeros(len(location))
    for i in range(len(location)):
        _, hotel_time_matrix[i], _ = transit(hotelLocation, location[i])

    hotel_return_time_matrix = numpy.zeros(len(location))
    for i in range(len(location)):
        _, hotel_return_time_matrix[i], _ = transit(location[i], hotelLocation)

    time_matrix = numpy.zeros((len(location), len(location)))
    for i in range(len(location)):
        for j in range(len(location)):
            _, time_matrix[i][j], _ = transit(location[i], location[j])

    for i in range(num_days):
        # print('Day%d' % (i+1), flush=True)
        place_flag = one_day_route(hotelName, hotelLocation, title, location, play_time, place_flag, hotel_time_matrix, hotel_return_time_matrix, time_matrix)

def one_day_route(hotelName, hotelLocation, title, location, play_time, place_flag, hotel_time_matrix, hotel_return_time_matrix, time_matrix):
    daily_place_flag = copy.deepcopy(place_flag)
    first_place = True
    real_time = 0
    curr_place = 0

    phptitle = hotelName + '|'
    phplongitude = str(hotelLocation["lng"]) + '|'
    phplatitude = str(hotelLocation["lat"]) + '|'
    phpplaytime = "0" + '|'
    while 0 in daily_place_flag:
        curr_time = sys.maxsize
        min_time = sys.maxsize
        if first_place:
            for i in range(len(hotel_time_matrix)):
                if daily_place_flag[i] != 1:
                    curr_time = hotel_time_matrix[i]
                if curr_time < min_time:
                    min_time = curr_time
                    next_place = i
            first_place = False
        else:
            for i in range(len(time_matrix)):
                if daily_place_flag[i] != 1:
                    curr_time = time_matrix[curr_place][i]
                if curr_time < min_time:
                    min_time = curr_time
                    next_place = i

        # Is there enough time for the next attraction?
        # 从当前景点A决定去不去下一个景点B的话 应该是判断
        # （去B的时间 + B的建议游玩时间 + B到酒店的时间） < 剩下可以玩的时间 否则标记B为今日不去的景点
        # 并找下一个可能的B '再判断
        next_2_hotel_time = hotel_return_time_matrix[next_place]
        cont_next_time = real_time + min_time / 60 / 60 + play_time[next_place] + next_2_hotel_time / 60 / 60
        if cont_next_time > max_total_playtime:
            daily_place_flag[next_place] = 1
            continue
        real_time = real_time + play_time[next_place] + min_time / 60 / 60
        # print("下一站：%s, 地址：%s，建议游玩时长：%f" % (title[next_place], location[next_place], play_time[next_place]), flush=True)
        curr_place = next_place
        daily_place_flag[curr_place] = 1
        place_flag[curr_place] = 1

        phptitle = phptitle + title[next_place] + '|'
        phpplaytime = phpplaytime + str(play_time[next_place]) + '|'
        phplongitude = phplongitude + str(location[next_place]["lng"]) + '|'
        phplatitude = phplatitude + str(location[next_place]["lat"]) + '|'
    phpoutput = phptitle[:-1] + '&' + phpplaytime[:-1] + '&' + phplongitude[:-1] + '&' + phplatitude[:-1]

    print(phpoutput, flush=True)
    return place_flag


def get_next_place(place_flag, location, curr_place_location):
    curr_time = sys.maxsize
    min_time = sys.maxsize
    next_place = 0
    for i in range(len(location)):
        if place_flag[i] != 1:
            _, curr_time, _ = transit(curr_place_location, location[i])
        if curr_time < min_time:
            min_time = curr_time
            next_place = i
    return next_place, min_time


def main(argv):
    # python3 /Users/lauzingai/Desktop/Travelling-Route-Generation-System/TravelPlace/ItineraryGenerator.py 广州 北京 7 Luxury Loose 长沙 天津
    # start_city = "广州"
    start_city = sys.argv[1]
    # end_city = "北京"
    end_city = sys.argv[2]
    # total_days = 3
    total_days = int(argv[3])
    # city_names = ["南京", "杭州"]
    hotel_luxury = argv[4]
    schedule_type = argv[5]
    city_names = []
    for i in range(6, len(argv)):
        city_names.append(sys.argv[i])

    if schedule_type == "Loose":
        max_total_playtime = 11
    elif schedule_type == "Moderate":
        max_total_playtime = 12
    else:
        max_total_playtime = 13


    # 返回的参数是一个排序数组，表示城市间的游玩顺序
    # cities_play_days = get_cities_play_days(city_names, total_days)

    city_codes = []
    for i in range(len(city_names)):
        module_path = os.path.dirname(__file__)
        csv_file_name = module_path + '/data/city_list.csv'
        csv_file = open(csv_file_name, "r", encoding='utf-8')
        reader = csv.reader(csv_file)

        #   可用二分查找加速
        for item in reader:
            if reader.line_num == 1:
                continue
            if item[0] == city_names[i]:
                city_codes.append(item[1])
                break;
    csv_file.close()

    cities_play_days = []
    count_days = 0
    for city_code in city_codes:
        # play_day = get_city_play_days(city_name)

        f = open(module_path + '/data/' + city_code + '.json', 'r', encoding='utf-8')
        city_str = json.load(f)
        play_day = city_str['days']

        f.close()

        cities_play_days.append(int(play_day))
        count_days += int(play_day)
    # allocated_play_days = allocate_time(cities_play_days, total_days, count_days)

    allocated_playtimes = []
    ave_coe = total_days / count_days
    count = 0
    curr_day = 0
    for i in range(len(cities_play_days)):
        if i != (len(cities_play_days) - 1):
            curr_day = round(cities_play_days[i] * ave_coe)
            allocated_playtimes.append(curr_day)
            count += curr_day
        else:
            allocated_playtimes.append(total_days - count)
    cities_play_days = allocated_playtimes
    
    city_route, city_route_play_days = generate_inter_city_route(start_city, end_city, city_names, cities_play_days)

    print(start_city + '|' + end_city)

    phpoutput = ""
    for item in city_route:
        phpoutput += item + '|'
    print(phpoutput[:-1], flush=True)

    phpoutput = ""
    for item in city_route_play_days:
        phpoutput += str(item) + '|'
    print(phpoutput[:-1], flush=True)

    # The above are good.

    # The following are waited to be changed:

    for i in range(len(city_route)):
        _, title, location, _, play_time = get_city_places(city_route[i])
        num_days = city_route_play_days[i]
        num_place = choose_place(play_time, num_days)

        hotelapi = ""
        if hotel_luxury == "Economic":
            hotelapi = "http://api.map.baidu.com/place/v2/search?query=酒店&region=" + city_route[i] + "&scope=2&industry_type=hotel&filter=sort_name:level|sort_rule:1&output=json&ak=qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt"
        elif hotel_luxury == "Luxury":
            hotelapi = "http://api.map.baidu.com/place/v2/search?query=酒店&region=" + city_route[i] + "&scope=2&industry_type=hotel&filter=sort_name:level|sort_rule:0&output=json&ak=qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt"
        else:
            hotelapi = "http://api.map.baidu.com/place/v2/search?query=酒店&region=" + city_route[i] + "&scope=2&industry_type=hotel&filter=sort_name:total_score|sort_rule:0&output=json&ak=qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt"
        r = requests.get(hotelapi)
        json_object = r.json()
        hotelName = json_object["results"][0]["name"]
        hotelLocation = json_object["results"][0]["location"]

        multi_day_route(hotelName, hotelLocation, title[:num_place], location[:num_place], play_time[:num_place], num_days)

if __name__ == '__main__':
    main(sys.argv[0:])











