from get_jwt import encoded_jwt as jwt
import os

# 通义千问大模型api key
QWEN_key = os.getenv("QWEN_key", "")
# 心知天气api key
XINZHI_key = ""
# 和风天气api key
HEFENG_key = os.getenv("HEFENG_key", "")

# 和风天气jwt token
HEFENG_JWT_token = jwt

if __name__ == '__main__':
    print(jwt)
    with open("test_data/test_loc_data.json", "r", encoding="utf-8") as f:
        d = f.read().replace("'", '"')
    with open("test_data/test_loc_data.json", "w", encoding="utf-8") as f:
        f.write(d)
        print(d)
