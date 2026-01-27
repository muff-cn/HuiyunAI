# 彗云AI  HuiyunAI

### 🌟开发背景 Development Background

当前，AI技术正逐渐成为我们生活中不可或缺的一部分。
开发者希望利用AI赋能传统天气与天文领域, 为用户提供更准确、更高效的服务。
彗云AI 是一个基于FastAPI和阿里通义千问的AI应用, 旨在为用户提供天气和天文相关的咨询服务。

Nowadays, AI technology is becoming increasingly important in our lives.
Developers hope to use AI to empower traditional weather and astronomy, providing users with more accurate and efficient
services.
HuiyunAI is an AI application based on FastAPI and Alibaba's Qwen model, designed to provide users with weather and
astronomy-related consultation services.

### 🚀项目目标 Project Goals

HuiyunAI的目标是为用户提供准确、高效的天气和天文咨询服务。
通过与阿里通义千问等AI平台的集成, 提供用户个性化的天气和天文建议。

HuiyunAI aims to provide accurate and efficient weather and astronomy consultation services to users.
By integrating with Alibaba's Qwen model and other AI platforms, providing users with personalized weather and astronomy
suggestions.

### 🛠️技术栈/开发环境 The technology stack/development environment

- FastAPI: 用于构建后端API服务
- 阿里通义千问: 用于提供AI服务
- HTML/CSS/JavaScript: 用于构建原生前端界面
- Docker: 用于容器化部署
- Git: 用于版本控制
- GitHub: 用于托管代码仓库


- FastAPI: Used to build the API service
- Alibaba's Qwen model: Used to provide AI services
- HTML/CSS/JavaScript: Used to build the original frontend interface
- Docker: Used for containerization deployment
- Git: Used for version control
- GitHub: Used for hosting the code repository

### 📝功能列表  Function list

- 天气查询: 用户可以查询当前天气情况
- 天文预测: 用户可以获取天文相关的预测信息
- 个性化建议: 基于用户输入, 提供个性化的天气和天文建议


- Weather query: Users can query the current weather conditions
- Astronomy prediction: Users can get predictions of astronomical information
- Personalized suggestions: Based on user input, provide personalized weather and astronomical suggestions

### 📦安装与运行 Installation and Running

1. 克隆代码仓库到本地:
   ```bash
   git clone https://github.com/muff-cn/HuiyunAI.git
   cd HuiyunAI
    ```
2. 安装依赖:

   ```bash
       pip install -r requirements.txt
   ```
3. 配置环境变量:
   - 在`/backend`目录下创建一个`.env`文件, 并在其中添加以下内容:
   ```bash
   QWEN_API_KEY=your_qwen_api_key
   HEFENG_API_KEY=your_hefeng_api_key
   ```
   - 替换`your_qwen_api_key`为你自己的阿里通义千问API密钥。
   - 替换`your_hefeng_api_key`为你自己的和风天气API密钥。
4. 运行应用:
   ```bash
    run.bat
   ```
5. 访问应用:
   - 打开浏览器, 访问`http://localhost`
      