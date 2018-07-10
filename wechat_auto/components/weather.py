import requests
import json
import os

'''
UNDO, 需要定时获取当天所有天气的预报数据，保存到本地，之后通过调用则返回本地数据
'''

KEY = 'jpc0si7sh9qjudrz'  # API key
UID = "U396147DF7"  # 用户ID
NOW_API = 'https://api.seniverse.com/v3/weather/now.json'  # API URL，可替换为其他 URL
DAILY_API = 'https://api.seniverse.com/v3/weather/daily.json'
LIFE_API = 'https://api.seniverse.com/v3/life/suggestion.json'
UNIT = 'c'  # 单位
LANGUAGE = 'zh-Hans'  # 查询结果的返回语言
PATH=os.path.split(__file__)[0] #当前模块的绝对路径
CITYS = [] #当前API可供查询的城市名称

def init():
    global CITYS
    if len(CITYS)==0:
        with open(PATH+"/../storage/city.json", 'r',encoding="utf8") as load_f:
            city_dict = json.load(load_f)
            CITYS = city_dict["citys"]
    for city in CITYS:
        try:
            print(brief(city))
        except Exception as e:
            print(e)

def _now(location):
    r = requests.session()
    r.keep_alive = False
    result = r.get(NOW_API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=2)
    result = json.loads(result.text)
    if 'results' in result:
        return (True, location+'当前天气'+result['results'][0]['now']['text']+", 气温"+result['results'][0]['now']['temperature']+"摄氏度")
    return (False,result['status'])

def _daily(location):
    r = requests.session()
    r.keep_alive = False
    result = r.get(DAILY_API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=2)
    result = json.loads(result.text)
    return result

def _life(location):
    r = requests.session()
    r.keep_alive = False
    result = r.get(LIFE_API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
    }, timeout=2)
    result = json.loads(result.text)
    return result

def _all(location):
    result = {}
    result['daily'] = _daily(location)
    result['life'] = _life(location)
    return result

#获取目的城市的天气简报
def brief(location):
    content = _all(location)
    result = ""
    #如果查询出结果
    if 'results' in content['life']:
        today = content['daily']['results'][0]['daily'][0]
        suggestion = content['life']['results'][0]['suggestion']
        result = '%s今天(%s)白天%s,夜间%s,最高温度%s摄氏度,最低温度%s摄氏度,%s风。%s洗车，天气偏%s,%s运动，%s旅行' % (location, today['date'], today['text_day'], today['text_night'], today['high'], today['low'], today['wind_direction'],suggestion['car_washing']['brief'],suggestion['dressing']['brief'],suggestion['sport']['brief'],suggestion['travel']['brief'])
        return (True, result)
    else:#如果没有
        return (False, content['life']['status'])




'''Now formate
{
    "results": [
        {
            "location": {
                "id": "WX4FBXXFKE4F",
                "name": "北京",
                "country": "CN",
                "path": "北京,北京,中国",
                "timezone": "Asia/Shanghai",
                "timezone_offset": "+08:00"
            },
            "now": {
                "text": "多云",
                "code": "4",
                "temperature": "25"
            },
            "last_update": "2018-07-09T20:25:00+08:00"
        }
    ]
}

{
    "status": "The location can not be found.",
    "status_code": "AP010010"
}
'''

'''
{
    "results": [
        {
            "location": {
                "id": "WX4FBXXFKE4F",
                "name": "北京",
                "country": "CN",
                "path": "北京,北京,中国",
                "timezone": "Asia/Shanghai",
                "timezone_offset": "+08: 00"
            },
            "daily": [
                {
                    "date": "2018-07-09",
                    "text_day": "雷阵雨",
                    "code_day": "11",
                    "text_night": "阴",
                    "code_night": "9",
                    "high": "29",
                    "low": "22",
                    "precip": "",
                    "wind_direction": "东南",
                    "wind_direction_degree": "135",
                    "wind_speed": "10",
                    "wind_scale": "2"
                },
                {
                    "date": "2018-07-10",
                    "text_day": "多云",
                    "code_day": "4",
                    "text_night": "小雨",
                    "code_night": "13",
                    "high": "30",
                    "low": "22",
                    "precip": "",
                    "wind_direction": "南",
                    "wind_direction_degree": "180",
                    "wind_speed": "10",
                    "wind_scale": "2"
                },
                {
                    "date": "2018-07-11",
                    "text_day": "小雨",
                    "code_day": "13",
                    "text_night": "小雨",
                    "code_night": "13",
                    "high": "25",
                    "low": "22",
                    "precip": "",
                    "wind_direction": "南",
                    "wind_direction_degree": "180",
                    "wind_speed": "10",
                    "wind_scale": "2"
                }
            ],
            "last_update": "2018-07-09T11: 00: 00+08: 00"
        }
    ]
}
'''