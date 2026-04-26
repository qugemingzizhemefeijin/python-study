import asyncio

import httpx
from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerStdio

import local_settings


@function_tool
def get_weather(latitude, longitude):
    """根据指定的坐标提供当地摄氏度"""
    response = httpx.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return f"{data['current']['temperature_2m']}°C"


@function_tool
def get_coordinates(city_name):
    """根据城市获取经纬度"""
    return [116.39, 39.93]


async def main():
    # 1.启动MCPServer
    # 2.把MCPServer传递给agent （从MCPServer获取支持的工具，把工具传递给agent）
    async with MCPServerStdio(
            name="普通的mcp服务器",
            params={
                "command": "python",
                "args": ["mcp_server.py"]
            }
    ) as mcp_server:
        agent = Agent(
            name="AI助手",
            instructions="你是一个友好的AI助手，使用中文进行问答",  # 系统提示词
            model='qwen3.6-plus',
            tools=[get_weather, get_coordinates],
            mcp_servers=[mcp_server]
        )

        # run为异步调用
        result = await Runner.run(agent, "当前目录有几个文件？")

        print(result.final_output)


# main() 不能直接调用main

if __name__ == '__main__':
    asyncio.run(main())
