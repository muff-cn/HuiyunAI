import fastapi
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
from data_api import DataAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# 初始化FastAPI应用
app = fastapi.FastAPI()
app.mount("/static", fastapi.staticfiles.StaticFiles(directory="../frontend/static/"), name="static")

templates = Jinja2Templates(directory="../frontend/")

origins = [
    "http://localhost:63342",
    "http://127.0.0.1:63342",
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
    data = api.city_to_location()
    return data


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="127.0.0.10",
        port=80,
        reload=True  # 热重载，开发环境推荐
    )
