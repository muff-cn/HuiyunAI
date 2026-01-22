from get_jwt import encoded_jwt as jwt

# 通义千问大模型api key
QWEN_key = "sk-bca5cf8906a947dba1d7bacd3d692e19"
# 心知天气api key
XINZHI_key = "Si5MJI6hIRPa4fTyO"
# 和风天气api key
HEFENG_key = "8580b32d090e48208888981b4587d9a7"

# 和风天气jwt token
HEFENG_JWT_token = jwt

if __name__ == '__main__':
    print(jwt)
    with open("test_data/test_loc_data.json", "r", encoding="utf-8") as f:
        d = f.read().replace("'", '"')
    with open("test_data/test_loc_data.json", "w", encoding="utf-8") as f:
        f.write(d)
        print(d)
