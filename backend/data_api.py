import json
import datetime
import requests
import api_keys as keys


class DataAPI:
    def __init__(self, city: str = '深圳', lat=22.54, lon=114.05):
        self.city = city
        self.lat = f'{lat:.2f}'
        self.lon = f'{lon:.2f}'
        self.date = datetime.datetime.now().strftime("%Y%m%d")
        # 设置请求头
        self.hefeng_headers = {
            "Authorization": f"Bearer {keys.HEFENG_JWT_token}",
            "Accept-Encoding": "gzip, deflate, br"  # 支持压缩响应
        }
        self.hefeng_api_host = 'nr5ctv7egx.re.qweatherapi.com'
        self.city_change= False
        self.day_data = {}
        self.hourly_data = {}

        # self.light_pollution = {}

    # TODO: 通过心知天气api获取天气数据  (不使用)
    def xinzhi_get_weather(self, req_type) -> dict:
        present_weather_url = "https://api.seniverse.com/v3/weather/now.json"
        future_weather_url = "https://api.seniverse.com/v3/weather/daily.json"
        test_present_weather_params = {
            "key": keys.XINZHI_key,
            "location": self.city,

        }
        test_future_weather_params = {
            "key": keys.XINZHI_key,
            "location": self.city,
            "days": "15",

        }
        info_dict = {
            "present": present_weather_url,
            "future": future_weather_url
        }
        response = requests.get(info_dict[req_type], params=test_future_weather_params)
        return response.json()

    # TODO: 使用和风天气api获取天气预测数据
    def hefeng_get_weather(self, days='15d') -> dict:
        # 通过api获取城市id
        loc_id = self.city_to_location()["location"][0]["id"]
        url = f'https://{self.hefeng_api_host}/v7/weather/{days}?location={loc_id}'
        params = {
            # "key": keys.HEFENG_key,
            "location": self.city
        }
        if not self.day_data or self.date != datetime.datetime.now().strftime("%Y%m%d") or self.city_change:
            response = requests.get(url, params=params, headers=self.hefeng_headers)
            self.date = datetime.datetime.now().strftime("%Y%m%d")
            self.day_data = response.json()
            self.city_change = False
            return response.json()
        else:
            return self.day_data

    # TODO: 使用和风天气提供的接口获取城市的id
    def city_to_location(self) -> dict:
        url = f'https://{self.hefeng_api_host}/geo/v2/city/lookup'
        params = {
            # "key": keys.HEFENG_key,
            "location": self.city
        }
        response = requests.get(url, params=params, headers=self.hefeng_headers)
        city_data = response.json()
        # print(city_data)
        try:
            self.lat = city_data['location'][0]['lat']
            self.lon = city_data['location'][0]['lon']
            return city_data
        except (KeyError, IndexError):
            return {"error": f"城市不存在或数据格式错误：{self.city}"}

    # TODO: 通过和风天气API获得分时天气预报
    def hefeng_get_hours_weather(self, hours='72h') -> dict:
        loc_id = self.city_to_location()["location"][0]["id"]

        url = f'https://{self.hefeng_api_host}/v7/weather/{hours}?location={loc_id}'
        params = {
            "location": self.city
        }
        if not self.hourly_data or self.date != datetime.datetime.now().strftime("%Y%m%d") or self.city_change:
            response = requests.get(url, params=params, headers=self.hefeng_headers)
            self.date = datetime.datetime.now().strftime("%Y%m%d")
            self.hourly_data = response.json()
            self.city_change = False
            return response.json()
        else:
            return self.hourly_data

    # TODO: 通过天文通api获取光污染数据
    def laysky_light_pollution(self, key='darkmap_key_twt') -> dict | None:
        if not self.lat or not self.lon:
            self.city_to_location()
        # API请求地址
        url = "https://nodeapi.knockdream.com/api/lightpollution/latest"

        # 请求参数
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "key": key
        }

        # 请求头（完全模拟浏览器请求）
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "dnt": "1",
            "origin": "https://www.darkmap.cn",
            "priority": "u=1, i",
            "referer": "https://www.darkmap.cn/",
            "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
        }
        response = None
        try:
            # 发送GET请求
            response = requests.get(
                url=url,
                params=params,
                headers=headers,
                timeout=10  # 设置10秒超时
            )

            # 检查响应状态码
            response.raise_for_status()

            # 解析JSON响应
            light_pol_data = response.json()
            # print("请求成功！返回数据：")
            # print(json.dumps(light_pol_data, ensure_ascii=False, indent=2))
            return light_pol_data

        except requests.exceptions.Timeout:
            print("错误：请求超时")
            return None
        except requests.exceptions.ConnectionError:
            print("错误：网络连接失败")
            return None
        except requests.exceptions.HTTPError:
            print(f"错误：HTTP请求失败，状态码 {response.status_code}")
            print(f"响应内容：{response.text}")
            return None
        except json.JSONDecodeError:
            print("错误：返回数据不是有效的JSON格式")
            print(f"响应内容：{response.text}")
            return None
        except Exception as e:
            print(f"未知错误：{str(e)}")
            return None

    # TODO: 通过和风天气API获取月相 (不使用, 日数据中已有月相信息)
    def hefeng_get_moon_phase(self):
        loc_id = self.city_to_location()["location"][0]["id"]
        url = f'https://{self.hefeng_api_host}/v7/astronomy/moon'
        params = {
            "location": loc_id,
            'date': self.date
        }
        response = requests.get(url, params=params, headers=self.hefeng_headers)
        return response.json()


if __name__ == '__main__':
    api = DataAPI('Shenzhen')
    # data = api.hefeng_get_moon_phase()
    # print(data)
    data = api.city_to_location()
    # print(api.date)
    print(data)