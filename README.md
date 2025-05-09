## 代码结构及部署说明



#### 项目结构

```
├── .env                   # 环境变量
├── requirements.txt       # Python 包依赖列表
├── Agent_tools.py         # 智能体可用工具集
├── Chat_history.py        # 聊天历史处理
├── Chat_summary.py        # 聊天摘要生成
├── DeepSeek_v3.py         # DeepSeek v3 基础聊天
├── DeepSeek_v3_agent.py   # DeepSeek v3 为基座的智能体
└── main.py                # Server 封装与主程序入口
```



#### 部署方式

1. 运行以下代码安装依赖：

   ```shell
   pip install -r requirements.txt
   ```

​	推荐使用 conda 创建虚拟环境。

2. 项目根目录中新建一个 .env 文件，配置以下环境变量：

   ```
   OPENWEATHERMAP_API_KEY = <YOUR_API_KEY>
   SERPAPI_API_KEY = <YOUR_API_KEY>
   DEEPSEEK_API_KEY = <YOUR_API_KEY>
   LANGSMITH_TRACING = true
   LANGSMITH_ENDPOINT = "https://api.smith.langchain.com"
   LANGSMITH_API_KEY = <YOUR_API_KEY>
   LANGSMITH_PROJECT = <YOUR_PROJECT>
   REDIS_URL = redis://localhost:6379/0
   ```

   OpenWeatherMap: https://openweathermap.org  注册登录后获取 API_KEY

   SERPAPI: https://serpapi.com  注册登录后获取 API_KEY

   DeepSeek 开放平台: https://platform.deepseek.com  注册登录后获取 API_KEY

   LangSmith: https://www.langchain.com/langsmith  注册登录后获取 API_KEY 以及创建跟踪的 PROJECT

3. 下载并启动 Redis

   可从 https://github.com/microsoftarchive/redis 获取 Windows 版本

   使用以下命令在 Linux 上安装 Redis：

   ```shell
   sudo apt update
   sudo apt install redis-server -y
   ```

   修改 `redis.windows.conf`（Linux 上为 `redis.conf`），将 # bind 127.0.0.1 改为 bind 127.0.0.1 （也就是取消前面 # 的注释），保证安全性。

   使用以下命令启动 Redis Server：

   ```shell
   redis-server.exe redis.windows.conf
   ```

   可以通过以下命令启动 Redis Client 查看并操作 Redis：

   ```shell
   redis-cli
   ```

4. 运行 `main.py` 启动后端服务。



如文档有疏漏或操作遇到问题，可直接联系作者。