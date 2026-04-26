import asyncio

from agents import Agent, Runner

import local_settings


async def main():
    agent = Agent(
        name="AI助手",
        instructions="你是一个友好的AI助手，使用中文进行问答",  # 系统提示词
    )
    # run为异步调用
    result = await Runner.run(agent, "你是谁？")

    print(result.final_output)


# main() 不能直接调用main

if __name__ == '__main__':
    asyncio.run(main())
