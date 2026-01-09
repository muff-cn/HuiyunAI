import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json
import os  # 新增：用于检查文件路径

# 初始化FastAPI应用
app = fastapi.FastAPI()

# ========== 修复：CORS跨域配置（核心） ==========
# 1. 修正协议为http（WebStorm默认http，而非https）
# 2. allow_origins=['*'] 已覆盖所有源，origins仅作注释参考
origins = [
    "http://localhost:63342",  # 修正：http（不是https）
    "http://127.0.0.1:63342",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # 开发环境允许所有源（生产需指定具体源）
    allow_credentials=True,     # 允许携带Cookie（如需登录态则保留）
    allow_methods=["*"],        # 允许所有HTTP方法
    allow_headers=["*"],        # 允许所有请求头
)

# ========== 接口：根路径 ==========
@app.get("/")
def read_root():
    return {"Hello": "World"}

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

# ========== 业务接口 ==========
@app.get("/test/day_data")
def test_day_data():
    return read_json_file("test_data/test_day_data.json")

@app.get("/test/hourly_data")
def test_hourly_data():
    return read_json_file("test_data/test_hourly_data.json")

@app.get("/test/light_pollution")
def test_light_pollution():
    return read_json_file("test_data/test_light_pollution_data.json")

# ========== 修复：启动参数（适配文件名） ==========
if __name__ == "__main__":
    # 关键："server:app" 中的 "server" 要和你的文件名一致！
    # 比如文件名为 main.py → 改为 "main:app"；文件名为 server.py → 保留 "server:app"
    uvicorn.run(
        "server:app",  # 假设你的文件名为main.py，需根据实际修改！
        host="127.0.0.10",
        port=8000,
        reload=True  # 热重载，开发环境推荐
    )