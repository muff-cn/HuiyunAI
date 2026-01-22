import time

import fastapi
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
# import asyncio
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import os
import socket


from data_api import DataAPI

# 初始化FastAPI应用
app = fastapi.FastAPI()
app.mount("/static", fastapi.staticfiles.StaticFiles(directory="../frontend/static/"), name="static")
app.mount("/node_modules", fastapi.staticfiles.StaticFiles(directory="../frontend/node_modules/"), name="node_modules")

templates = Jinja2Templates(directory="../frontend/")

origins = [
    "http://localhost:63342",
    "http://127.0.0.10:8000",
    "http://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 开发环境允许所有源（生产需指定具体源）
    allow_credentials=True,  # 允许携带Cookie（如需登录态则保留）
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)


# ========== 接口：根路径 ==========
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ========== 修复：添加文件读取异常处理 ==========
def read_json_file(file_path):
    """封装JSON文件读取函数，添加异常处理"""
    # 拼接绝对路径（避免相对路径问题）
    abs_file_path = os.path.join(os.path.dirname(__file__), file_path)
    try:
        with open(abs_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {"error": f"文件不存在：{abs_file_path}"}, 404
    except json.JSONDecodeError:
        return {"error": f"JSON文件格式错误：{abs_file_path}"}, 400
    except Exception as e:
        return {"error": f"读取文件失败：{str(e)}"}, 500


# ========== 测试业务接口 ==========
@app.get("/test/day_data")
def test_day_data(city: str = Query("深圳")):
    if city: pass
    return read_json_file("test_data/test_day_data.json")


@app.get("/test/hourly_data")
def test_hourly_data(city: str = Query("深圳")):
    if city: pass
    return read_json_file("test_data/test_hourly_data.json")


@app.get("/test/light_pollution")
def test_light_pollution(city: str = Query("深圳")):
    if city: pass
    return read_json_file("test_data/test_light_pollution_data.json")


@app.get("/test/loc_data")
def test_loc_data(city: str = Query("深圳")):
    if city: pass
    return read_json_file("test_data/test_loc_data.json")


api = DataAPI()


# ========== 实际业务接口 ==========
@app.get("/api/day_data")
def api_day_data(city: str = Query("深圳")):
    global api
    if city != api.city:
        api.city = city
        api.city_change = True

    data = api.hefeng_get_weather()
    return data


@app.get("/api/hourly_data")
def api_hourly_data(city: str = Query("深圳")):
    global api
    if city != api.city:
        api.city = city
        api.city_change = True

    data = api.hefeng_get_hours_weather()
    return data


@app.get("/api/light_pollution")
def api_light_pollution(city: str = Query("深圳")):
    global api
    if city != api.city:
        api.city = city
        api.city_change = True
    data = api.laysky_light_pollution()
    return data


@app.get("/api/loc_data")
def api_loc_data(city: str = Query("深圳")):
    global api
    if city != api.city:
        api.city = city
        api.city_change = True
        # print(city)
    data = api.city_to_location()
    # print(city)
    return data

@app.get("/api/chat")
def api_ai_data(
        city: str = Query("深圳"),
        prompt: str = Query("分析这几天的天气/观星条件怎么样？")  # 默认提问
):
    global api
    # 切换城市（复用原有逻辑）
    if city != api.city:
        api.city = city
        api.city_change = True

    # 调用AI方法（生成器），包装为异步生成器适配StreamingResponse
    async def ai_stream_generator():
        try:
            # 遍历AI返回的流式数据
            for chunk in api.ai_data(prompt):
                if chunk:
                    yield chunk  # 逐段返回AI输出
                    # await asyncio.sleep(0.01)  # 避免输出过快（可选）
        except Exception as e:
            yield ''
            print(f"AI调用失败：{str(e)}")

    # 返回流式响应，指定媒体类型为文本
    return StreamingResponse(
        ai_stream_generator(),
        media_type="text/plain; charset=utf-8"
    )



def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


if __name__ == "__main__":
    import os
    os.system("pip install -r requirements.txt")
    print(f"✅ 服务器运行中！其他设备请访问：http://{get_ip()}:8000")
    time.sleep(1)
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 热重载，开发环境推荐
        # ssl_keyfile="local.key",  # 私钥文件路径
        # ssl_certfile="local.crt"  # 证书文件路径
    )
