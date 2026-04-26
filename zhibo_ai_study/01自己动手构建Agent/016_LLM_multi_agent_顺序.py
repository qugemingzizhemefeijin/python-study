# 多Agent编排
#   顺序
#   并行
#   路由（交接）
#   Agents即工具
#   监督
#   护栏（并行监督）

import asyncio

from agents import Agent, Runner

import local_settings  # 加载本地设置

agent_a = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文进行问答",
    model='qwen3.6-plus',
)
agent_b = Agent(
    name="AI助手",
    instructions="对前一个Agent回答进行扩展和补充",
    model='qwen3.6-plus',
)


async def main():
    result = await Runner.run(agent_a, "太阳围绕地球，还是地球围绕太阳？")
    print(result.final_output)

    result = await Runner.run(agent_b, result.final_output)
    print(result.final_output)


if __name__ == '__main__':
    asyncio.run(main())
