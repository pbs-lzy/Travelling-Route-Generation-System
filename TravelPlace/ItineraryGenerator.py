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
from urllib.request import urlopen, quote

from Crawler.CrawlerCityDays import get_cities_play_days
from Crawler.CrawlerPlace import get_city_places
from Map.InterCityRoute import generate_inter_city_route
from Map.TwoPlacesRoute import transit

min_total_playtime = 11
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


def multi_day_route(title, location, play_time, num_days):
    place_flag = [0] * len(title)
    print(place_flag)
    for i in range(num_days):
        print('Day%d' % (i+1), flush=True)
        place_flag = one_day_route(title, location, play_time, place_flag)


def one_day_route(title, location, play_time, place_flag):
    daily_place_flag = copy.deepcopy(place_flag)
    hotel_location = location[1]
    first_place = True
    real_time = 0
    curr_place = 0
    while 0 in daily_place_flag:
        if first_place:
            next_place, min_time = get_next_place(daily_place_flag, location, hotel_location)
            first_place = False
        else:
            next_place, min_time = get_next_place(daily_place_flag, location, location[curr_place])

        # Is there enough time for the next attraction?
        # 从当前景点A决定去不去下一个景点B的话 应该是判断
        # （去B的时间 + B的建议游玩时间 + B到酒店的时间） < 剩下可以玩的时间 否则标记B为今日不去的景点
        # 并找下一个可能的B '再判断
        _, next_2_hotel_time, _ = transit(location[next_place], hotel_location)
        cont_next_time = real_time + min_time / 60 / 60 + play_time[next_place] + next_2_hotel_time / 60 / 60
        if cont_next_time > max_total_playtime:
            daily_place_flag[next_place] = 1
            continue
        real_time = real_time + play_time[next_place] + min_time / 60 / 60
        print("下一站：%s, 地址：%s，建议游玩时长：%f" % (title[next_place], location[next_place], play_time[next_place]), flush=True)
        # print(title[next_place])
        # print(play_time[next_place])
        # print(location[next_place])
        curr_place = next_place
        daily_place_flag[curr_place] = 1
        place_flag[curr_place] = 1
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
    # start_city = "广州"
    start_city = sys.argv[1]
    # end_city = "北京"
    end_city = sys.argv[2]
    # total_days = 3
    total_days = int(argv[3])
    # city_names = ["南京", "杭州"]
    city_names = []
    for i in range(4, len(argv)):
        city_names.append(sys.argv[i])


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
            allocated_playtimes.append(total_days - curr_day)
    cities_play_days = allocated_playtimes
    print(cities_play_days)
    
    # The above are good.

    
    city_route, city_route_play_days = generate_inter_city_route(start_city, end_city, city_names, cities_play_days)
    print(city_route, flush=True)
    print(city_route_play_days, flush=True)

    # curr_city = start_city
    # city_flag = [0] * len(city_names)
    # city_route = [""] * len(city_names)
    # city_route_play_days = [0] * len(cities_play_days)
    # for i in range(len(city_route)):
    #     min_distance = sys.maxsize
    #     next_city = 0
    #     for j in range(len(city_names)):
    #         if city_flag[j] == 0:
    #             # distance = inter_city_transit(get_lng_lat(curr_city), get_lng_lat(city_names[j]))
    #             url = 'http://api.map.baidu.com/geocoder/v2/?address='
    #             output = 'json'
    #             ak = 'qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt'
    #             # ak = 'YBbMVlde0GPAUl6ePBQY2pIfRwkcqFe6'
    #             add1 = quote(curr_city)  # 本文城市变量为中文，为防止乱码，先用quote进行编码
    #             url1 = url + add1 + '&output=' + output + "&ak=" + ak
    #             req = urlopen(url1)
    #             res = req.read().decode()
    #             origin = json.loads(res)
    #             add2 = quote(curr_city)  # 本文城市变量为中文，为防止乱码，先用quote进行编码
    #             url2 = url + add2 + '&output=' + output + "&ak=" + ak
    #             req = urlopen(url2)
    #             res = req.read().decode()
    #             destination = json.loads(res)

    #             if origin['status'] == 0 & destination['status'] == 0:
    #                 # print(origin)
    #                 original_lat = round(origin['result']['location']['lat'], 6)
    #                 original_lng = round(origin['result']['location']['lng'], 6)
    #                 destination_lat = round(destination['result']['location']['lat'], 6)
    #                 destination_lng = round(destination['result']['location']['lng'], 6)

    #                 # 经纬度转化为弧度(rad)
    #                 ori_lng_rad = (original_lng * math.pi / 180.0)
    #                 ori_lat_rad = (original_lat * math.pi / 180.0)
    #                 des_lng_rad = (destination_lng * math.pi / 180.0)
    #                 des_lat_rad = (destination_lat * math.pi / 180.0)

    #                 # 计算两点的距离，（单位：m）
    #                 a = ori_lat_rad - des_lat_rad
    #                 b = ori_lng_rad - des_lng_rad
    #                 s = 2 * math.asin(
    #                     math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(ori_lat_rad) * math.cos(des_lat_rad) * math.pow(math.sin(b / 2), 2)))
    #                 s = s * EARTH_RADIUS
    #                 distance = s * 1000
    #             else:
    #                 print(origin['message'])
                

    #             # print("当前：%s, 去：%s，距离：%f" % (curr_city, city_names[j], distance))
    #             if min_distance > distance:
    #                 min_distance = distance
    #                 next_city = j
    #     # print(city_names[next_city])
    #     city_flag[next_city] = 1
    #     city_route[i] = city_names[next_city]
    #     city_route_play_days[i] = cities_play_days[next_city]
    #     curr_city = city_names[next_city]

    # print(city_route)
    # print(city_route_play_days)


    # The following are waited to be changed:

    # print(city_route_play_days)

    for i in range(len(city_route)):
        # print(city_route[i])
        _, title, location, addresses, play_time = get_city_places(city_route[i])
        print(play_time, flush=True)
        num_days = city_route_play_days[i]
        # print(num_days)
        num_place = choose_place(play_time, num_days)
        print(num_place, flush=True)
        multi_day_route(title[:num_place], location[:num_place], play_time[:num_place], num_days)


    # return 
    # day = [
    #   city, title[], time[], logitude[], latitude[]
    # ]

if __name__ == '__main__':
    main(sys.argv[0:])


