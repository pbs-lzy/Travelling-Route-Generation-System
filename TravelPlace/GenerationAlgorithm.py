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

加上如果公交时间>3小时或没有公交线路时，打车
"""
import sys

from Crawler.CrawlerPlace import get_lng_lat, get_city_places
from Crawler.CrawlerPlayTime import get_places_playtime
from Map.TwoPlacesRoute import transit

min_total_playtime = 11
max_total_playtime = 13

#   return travel spots of a city and corresponding addresses and play time
def load_data():
    all_titles, all_addresses = get_city_places()
    play_time = get_places_playtime(all_titles)
    return all_titles, all_addresses, play_time

#   
def choose_place(play_time, num_days):
    num_place = 0
    total_time = 0
    while total_time <= (min_total_playtime * num_days):
        total_time = total_time + play_time[num_place]
        num_place = num_place + 1
    return num_place


def multi_day_route(title, address, play_time, num_days):
    place_flag = [0] * len(address)
    for i in range(num_days):
        print('Day%d' % (i+1))
        place_flag = one_day_route(title, address, play_time, place_flag)


def one_day_route(title, address, play_time, place_flag):
    hotel_address = '上海市黄浦区浙江中路379号'
    first_place = True
    real_time = 0
    curr_place = 0
    while real_time <= max_total_playtime:
        if first_place:
            next_place, min_time = get_next_place(place_flag, address, hotel_address)
            first_place = False
        else:
            next_place, min_time = get_next_place(place_flag, address, address[curr_place])

        # Is there enough time for the next attraction?
        _, next_2_hotel_time, _ = transit(get_lng_lat(address[next_place]), get_lng_lat(hotel_address))
        cont_next_time = real_time + min_time / 60 / 60 + play_time[next_place] + next_2_hotel_time / 60 / 60
        if cont_next_time > max_total_playtime:
            break

        real_time = real_time + play_time[next_place] + min_time / 60 / 60
        print("下一站：%s, 地址：%s，建议游玩时长：%d" % (title[next_place], address[next_place], play_time[next_place]))
        curr_place = next_place
        place_flag[curr_place] = 1
    return place_flag


def get_next_place(place_flag, address, curr_place_address):
    curr_time = sys.maxsize
    min_time = sys.maxsize
    next_place = 0
    for i in range(len(address)):
        if place_flag[i] != 1:
            _, curr_time, _ = transit(get_lng_lat(curr_place_address), get_lng_lat(address[i]))
        if curr_time < min_time:
            min_time = curr_time
            next_place = i
    return next_place, min_time

#   
def main():
    title, address, play_time = load_data()
    num_days = 4
    num_place = choose_place(play_time, num_days)
    multi_day_route(title[:num_place], address[:num_place], play_time[:num_place], num_days)


if __name__ == '__main__':
    main()