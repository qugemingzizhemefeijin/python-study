# 多Agent编排
#   顺序
#   并行
#   路由（交接）
#   Agents即工具
#   监督
#   护栏（并行监督）

import asyncio
import time

from agents import Agent, Runner

import local_settings  # 加载本地设置

# 交接的话，注意这里面的Agent的name不要用中文，否则会直接交接给最后一个，因为中文名称无法生成唯一key

agent_a = Agent(
    name="chinese",
    instructions="只使用中文进行回答",
    model='qwen3.6-plus',
    handoff_description="只是用中文进行回答",
)
agent_b = Agent(
    name="english",
    instructions="只使用英文进行回答",
    model='qwen3.6-plus',
    handoff_description="只是用英文进行回答",
)
agent_c = Agent(
    name="korea",
    instructions="只使用韩语进行回答",
    model='qwen3.6-plus',
    handoff_description="只是用韩语进行回答",
)
agent_d = Agent(
    name="前台助手",
    instructions="不回答问题，而是根据语言类型，把问题交接给合适的Agent",
    model='qwen3.6-plus',
    handoffs=[agent_a, agent_b, agent_c]
)


async def main():
    query = '太阳围绕地球，还是地球围绕太阳，请言简意赅回答？'

    result = await Runner.run(agent_d, query)

    print(result.final_output)


if __name__ == '__main__':
    asyncio.run(main())
