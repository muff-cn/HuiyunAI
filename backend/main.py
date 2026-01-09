import requests
import json

def get_light_pollution_data(lat, lon, key):
    """
    获取光污染指数数据
    :param lat: 纬度
    :param lon: 经度
    :param key: 访问密钥
    :return: 光污染数据字典，失败时返回None
    """
    # API请求地址
    url = "https://nodeapi.knockdream.com/api/lightpollution/latest"

    # 请求参数
    params = {
        "lat": lat,
        "lon": lon,
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
        data = response.json()
        print("请求成功！返回数据：")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return data

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

# 主程序
if __name__ == "__main__":
    # 替换为你要查询的经纬度和key
    LATITUDE = 22.71991
    LONGITUDE = 114.24779
    API_KEY = "darkmap_key_twt"

    # 调用函数获取数据
    light_pollution_data = get_light_pollution_data(LATITUDE, LONGITUDE, API_KEY)