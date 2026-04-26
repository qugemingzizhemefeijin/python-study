import asyncio

from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent

import local_settings

agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文进行问答",  # 系统提示词
)


async def main():
    # run为异步调用
    result = Runner.run_streamed(agent, "讲一个故事至少300字？")

    # 用异步的方式源源不断的获取信息
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # raw_response_event 来自LLM的响应
            # run_item_stream_event 来自Runner事件：工具调用、agent之间的交接
            print(event.data.delta)  # 只打印新增的一部分
        print(event.type)
        
        # 有的里面是没有data
        print(event.data)


# main() 不能直接调用main

if __name__ == '__main__':
    asyncio.run(main())
