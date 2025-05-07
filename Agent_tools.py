from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.tools import Tool

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# arxiv 工具后面自动加载即可

# 搜索引擎工具
params = {
    "engine": "bing",
    "gl": "us",
    "hl": "en",
}
search = SerpAPIWrapper(params=params)
search_tool = Tool(
    name="SerpAPI",
    description="Search the web for information. The input can be any sentences, supporting both English and Chinese. ",
    func=search.run,
)

# 天气工具
weather = OpenWeatherMapAPIWrapper()
weather_tool = Tool(
    name="OpenWeatherMapAPI",
    # 工具的描述非常关键！
    description="Get the current weather in a city. You need to input a city name only in English.",
    func=weather.run,
)

# 加载工具
tools = load_tools(
    ["arxiv"],
)
tools.append(search_tool)
tools.append(weather_tool)
