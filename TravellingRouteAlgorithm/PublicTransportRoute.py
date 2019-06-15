import urllib.parse
import urllib.request
import json

def 计算所有路线(origin, destionation):
    '''
    tactics_incity 市内公交换乘策略
            可选，默认为0
            可选值：
            0 推荐
            1 少换乘
            2 少步行
            3 不坐地铁
            4 时间短
            5 地铁优先
    '''
    tactics_incity = 0
    data = urllib.parse.urlencode(
        {'origin': '%s,%s' % (origin.y, origin.x), 'destination': '%s,%s' % (destionation.y, destionation.x),
         'tactics_incity': tactics_incity, 'ak': key})
    response = urllib.request.urlopen('http://api.map.baidu.com/direction/v2/transit?%s' % data)
    html = response.read()
    data = html.decode('utf-8')
    result = json.loads(data)
    # print(data)
    路线总数 = result['result']['total']
    if (result['status'] == 0):
        for x in range(路线总数):
            if (result['status'] == 0):
                distance = result['result']['routes'][x]['distance']
                duration = result['result']['routes'][x]['duration']
                print('路线：%s,距离%s米，花费%s分钟' % (x, distance, duration / 60))
    else:
        print('error : %d' % result['status'])
        '''
        status 备注
                0：成功
                1：服务器内部错误
                2：参数无效
                1001：没有公交方案
                1002：没有匹配的POI
        '''


def main():
    l1 = locationXY(113.464838, 23.111949)  # 大沙东地铁站的坐标
    l2 = getLocation('御富科贸园b2座205-20')
    # print("%s\n%s"%(l1.x,l1.y))
    计算所有路线(l1, l2)
    # l2 =


if __name__ == '__main__':
    main()