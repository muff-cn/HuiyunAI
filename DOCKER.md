# Docker 使用说明

项目包含后端（FastAPI）和前端静态文件（位于 `frontend/`），后端会直接从镜像中的 `frontend/` 提供静态资源。

快速开始（开发）

1. 在项目根目录创建一个 `.env` 或在终端里导出需要的环境变量（可选）：

```powershell
set HEFENG_key=your_hefeng_key
set XINZHI_key=your_xinzhi_key
set QWEN_key=your_qwen_key
```

2. 使用 docker-compose 启动（会把当前目录挂载到容器，适合开发）：

```powershell
docker compose up --build
```

访问： http://localhost:8000

生产构建（不挂载、使用构建产物）：

```powershell
docker build -t huiyunai:latest .
docker run -p 8000:8000 --env HEFENG_key=xxx --env XINZHI_key=xxx --env QWEN_key=xxx huiyunai:latest
```

安全建议

- 请通过环境变量或 secret 管理 API Key，避免将密钥写死在仓库中。
- 若用于生产，可选择移除 `--reload` 并使用 uvicorn+gunicorn 等更健壮的进程管理方案。
