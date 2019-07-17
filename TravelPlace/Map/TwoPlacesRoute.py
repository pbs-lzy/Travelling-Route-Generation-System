import urllib.parse
import urllib.request
import json

key = 'qe6LKhNsAcSPGixXUz0NZGRsZCFYhzwt'
# key = 'YBbMVlde0GPAUl6ePBQY2pIfRwkcqFe6'


def transit(origin, destination):
    # print(origin['lat'])
    # print(destination)
    original_x = round(origin['lat'], 6)
    original_y = round(origin['lng'], 6)
    destination_x = round(destination['lat'], 6)
    destination_y = round(destination['lng'], 6)
    parameters = "origin=" + str(original_x) + "," + str(original_y) + "&destination=" + str(
        destination_x) + "," + str(destination_y) + "&ak=" + key
    # print(parameters)
    response = urllib.request.urlopen('http://api.map.baidu.com/direction/v2/transit?%s' % parameters)
    html = response.read()
    data = html.decode('utf-8')
    result = json.loads(data)
    if result['status'] == 0:
        # There is no transit plan between the two places or transit takes more than 3 hours, change to taxi
        if result['result']['total'] != 0:
            distance = result['result']['routes'][0]['distance']
            duration = result['result']['routes'][0]['duration']
            price = result['result']['routes'][0]['price']
            return distance, duration, price
        else:
            # print(result)
            distance = result['result']['taxi']['distance']
            duration = result['result']['taxi']['duration']
            price = result['result']['taxi']['detail'][0]['total_price']
            return distance, duration, price
    else:
        print('error : %d' % result['status'])
