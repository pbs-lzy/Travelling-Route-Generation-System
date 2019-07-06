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

from Crawler.CrawlerCityDays import get_cities_play_days
from Crawler.CrawlerPlace import get_city_places
from Map.InterCityRoute import generate_inter_city_route
from Map.TwoPlacesRoute import transit

min_total_playtime = 11
max_total_playtime = 13


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
    for i in range(num_days):
        print('Day%d' % (i+1))
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
        print("下一站：%s, 地址：%s，建议游玩时长：%f" % (title[next_place], location[next_place], play_time[next_place]))
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


def main():
    start_city = "广州"
    end_city = "北京"
    city_names = ["南京", "杭州"]
    total_days = 3

    # 返回的参数是一个排序数组，表示城市间的游玩顺序
    cities_play_days = get_cities_play_days(city_names, total_days)
    city_route, city_route_play_days = generate_inter_city_route(start_city, end_city, city_names, cities_play_days)
    # print(city_route)
    # print(city_route_play_days)

    for i in range(len(city_route)):
        # print(city_route[i])
        _, title, location, addresses, play_time = get_city_places(city_route[i])
        num_days = city_route_play_days[i]
        # print(num_days)
        num_place = choose_place(play_time, num_days)
        multi_day_route(title[:num_place], location[:num_place], play_time[:num_place], num_days)


if __name__ == '__main__':
    main()



