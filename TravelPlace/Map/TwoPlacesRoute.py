import urllib.parse
import urllib.request
import json


#from Crawler.CrawlerPlace import get_lng_lat
def get_lng_lat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    ak = 'qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt'
    add = urllib.parse.quote(address)  # 本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url + add + '&output=' + output + "&ak=" + ak
    req = urllib.request.urlopen(url2)
    res = req.read().decode()
    temp = json.loads(res)
    return temp

key = 'qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt'


def transit(origin, destination):
    original_x = round(origin['result']['location']['lat'], 6)
    original_y = round(origin['result']['location']['lng'], 6)
    destination_x = round(destination['result']['location']['lat'], 6)
    destination_y = round(destination['result']['location']['lng'], 6)
    parameters = "origin=" + str(original_x) + "," + str(original_y) + "&destination=" + str(
        destination_x) + "," + str(destination_y) + "&ak=" + key
    response = urllib.request.urlopen('http://api.map.baidu.com/direction/v2/transit?%s' % parameters)
    html = response.read()
    data = html.decode('utf-8')
    result = json.loads(data)
    if result['status'] == 0:
        # There is no transit plan between the two places or transit takes more than 3 hours, change to taxi
        if (result['result']['total'] != 0) and (result['result']['routes'][0]['duration'] / 60 / 60 < 3):
            distance = result['result']['routes'][0]['distance']
            duration = result['result']['routes'][0]['duration']
            price = result['result']['routes'][0]['price']
            return distance, duration, price
        else:
            distance = result['result']['taxi']['distance']
            duration = result['result']['taxi']['duration']
            price = result['result']['taxi']['detail'][0]['total_price']
            return distance, duration, price
    else:
        print('error : %d' % result['status'])


def main():
    l1 = get_lng_lat('南宁市武鸣区两江镇明山路1号')
    l2 = get_lng_lat('南宁市青秀区青山路19号')
    transit(l1, l2)


if __name__ == '__main__':
    main()
