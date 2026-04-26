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

agent_a = Agent(
    name="AI助手",
    instructions="只使用中文进行回答",
    model='qwen3.6-plus',
)
agent_b = Agent(
    name="AI助手",
    instructions="只使用英文进行回答",
    model='qwen3.6-plus',
)
agent_c = Agent(
    name="AI助手",
    instructions="只使用韩语进行回答",
    model='qwen3.6-plus',
)


async def main():
    query = '太阳围绕地球，还是地球围绕太阳，请言简意赅回答？'
    t1 = time.time()

    # 这个实际还是顺序执行
    # result_1 = await Runner.run(agent_a, query)
    # result_2 = await Runner.run(agent_b, query)
    # result_3 = await Runner.run(agent_c, query)

    result_1, result_2, result_3 = await asyncio.gather(
        Runner.run(agent_a, query),
        Runner.run(agent_b, query),
        Runner.run(agent_c, query)
    )

    t2 = time.time()

    print(result_1.final_output)
    print(result_2.final_output)
    print(result_3.final_output)

    print(f'三个回答所花费的时间{t2 - t1}')


if __name__ == '__main__':
    asyncio.run(main())
