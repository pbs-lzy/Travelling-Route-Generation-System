# 贪心算法 先去距离当前城市最近的城市
# 百度地图API跨城市火车信息不准确 所以不用火车信息作为算法参考

# 根据总景点比例安排各城市游玩天数


import math
import sys

from Crawler.CrawlerPlace import get_lng_lat

EARTH_RADIUS = 6378.137  # 地球半径


def generate_inter_city_route(start_city, end_city, city_names, city_play_days):
    curr_city = start_city
    city_flag = [0] * len(city_names)
    city_route = [""] * len(city_names)
    city_route_play_days = [0] * len(city_play_days)
    for i in range(len(city_route)):
        min_distance = sys.maxsize
        next_city = 0
        for j in range(len(city_names)):
            if city_flag[j] == 0:
                distance = inter_city_transit(get_lng_lat(curr_city), get_lng_lat(city_names[j]))
                # print("当前：%s, 去：%s，距离：%f" % (curr_city, city_names[j], distance))
                if min_distance > distance:
                    min_distance = distance
                    next_city = j
        # print(city_names[next_city])
        city_flag[next_city] = 1
        city_route[i] = city_names[next_city]
        city_route_play_days[i] = city_play_days[next_city]
        curr_city = city_names[next_city]
    return city_route, city_route_play_days


def inter_city_transit(origin, destination):
    if origin['status'] == 0 & destination['status'] == 0:
        # print(origin)
        original_lat = round(origin['result']['location']['lat'], 6)
        original_lng = round(origin['result']['location']['lng'], 6)
        destination_lat = round(destination['result']['location']['lat'], 6)
        destination_lng = round(destination['result']['location']['lng'], 6)

        # 经纬度转化为弧度(rad)
        ori_lng_rad = (original_lng * math.pi / 180.0)
        ori_lat_rad = (original_lat * math.pi / 180.0)
        des_lng_rad = (destination_lng * math.pi / 180.0)
        des_lat_rad = (destination_lat * math.pi / 180.0)

        # 计算两点的距离，（单位：m）
        a = ori_lat_rad - des_lat_rad
        b = ori_lng_rad - des_lng_rad
        s = 2 * math.asin(
            math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(ori_lat_rad) * math.cos(des_lat_rad) * math.pow(math.sin(b / 2), 2)))
        s = s * EARTH_RADIUS
        distance = s * 1000
    else:
        print(origin['message'])
    return distance
