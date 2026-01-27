import time
import fastapi
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import os
import socket
import logging
from data_api import DataAPI

# 检测是否是uvicorn导入模式
is_uvicorn_import = os.environ.get("RUNNING_UVICORN") == "1" or "uvicorn" in os.path.basename(os.getenv("_", ""))

# ========== 核心修改：计算绝对路径（解决Railway路径问题） ==========
# 1. 获取当前文件（server.py）的绝对路径（/app/backend/server.py）
current_file_path = os.path.abspath(__file__)
# 2. 获取backend目录的绝对路径（/app/backend/）
backend_dir = os.path.dirname(current_file_path)
# 3. 获取项目根目录的绝对路径（/app/）
root_dir = os.path.dirname(backend_dir)
# 4. 拼接前端相关目录的绝对路径（替代相对路径../frontend/）
frontend_dir = os.path.join(root_dir, "frontend")
static_dir = os.path.join(frontend_dir, "static")
node_modules_dir = os.path.join(frontend_dir, "node_modules")

logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(root_dir, 'backend.log'),
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

# 初始化FastAPI应用
app = fastapi.FastAPI()

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

# ========== 挂载静态文件（添加容错，避免目录不存在导致启动失败） ==========
try:
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    if not is_uvicorn_import:  # 只有当不是uvicorn导入模式时才打印
        # print(f"✅ 成功挂载静态文件目录: {static_dir}")
        pass
except RuntimeError as e:
    if not is_uvicorn_import:
        print(f"⚠️  静态文件目录不存在，跳过挂载: {e}")
    # 可选：自动创建空目录，避免后续访问报错
    os.makedirs(static_dir, exist_ok=True)

# 挂载/node_modules目录
try:
    app.mount("/node_modules", StaticFiles(directory=node_modules_dir), name="node_modules")
    if not is_uvicorn_import:
        # print(f"✅ 成功挂载node_modules目录: {node_modules_dir}")
        pass
except RuntimeError as e:
    if not is_uvicorn_import:
        print(f"⚠️  node_modules目录不存在，跳过挂载: {e}")
    os.makedirs(node_modules_dir, exist_ok=True)

# ========== 初始化模板引擎（替换相对路径为绝对路径） ==========
try:
    templates = Jinja2Templates(directory=frontend_dir)
    if not is_uvicorn_import:
        # print(f"✅ 成功加载模板目录: {frontend_dir}")
        pass
except Exception as e:
    if not is_uvicorn_import:
        print(f"⚠️  模板目录加载失败: {e}")
    # 兜底：使用当前目录作为模板目录，避免应用崩溃
    templates = Jinja2Templates(directory=backend_dir)


# ========== 接口：根路径 ==========
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


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
    except Exception as err:
        return {"error": f"读取文件失败：{str(err)}"}, 500


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
        except Exception or NameError:
            logging.exception("AI调用失败")
            yield ''

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
    PORT = int(os.getenv("PORT", 80))
    print(f"✅ 服务器运行中！局域网下其他设备请访问：http://{get_ip()}:{PORT}")
    time.sleep(1)
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=PORT,
        # reload=True,  # 可以重新开启热重载
    )
