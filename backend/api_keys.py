import os
from dotenv import load_dotenv
from get_jwt import encoded_jwt as jwt

load_dotenv()
# 通义千问大模型api key
QWEN_key = os.getenv("QWEN_KEY")
# 心知天气api key
XINZHI_key = ""
# 和风天气api key
HEFENG_key = os.getenv("HEFENG_KEY")

# 和风天气jwt token
HEFENG_JWT_token = jwt

if __name__ == '__main__':
    print(QWEN_key)
    print(HEFENG_key)
