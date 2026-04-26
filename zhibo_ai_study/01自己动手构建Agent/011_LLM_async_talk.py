# 连续对话和多模态

import asyncio

from agents import Agent, Runner

import local_settings

agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文进行问答",  # 系统提示词
)


async def main():
    # run为异步调用
    # result = await Runner.run(agent, "1+1=？")
    # result = await Runner.run(agent, "再加1=？")
    # 这里只会输出 再加1等于2。没有做到连续对话

    result = await Runner.run(agent, '1+1=？')
    history = result.to_input_list()    # 转成列表
    print('对话历史')

    history.append({'role': 'user', 'content': '再+1=？'})    # 对会话进行管理

    result = await Runner.run(agent, history)

    print(result.final_output)

    print('最新的完整对话过程', result.to_input_list())


if __name__ == '__main__':
    asyncio.run(main())
