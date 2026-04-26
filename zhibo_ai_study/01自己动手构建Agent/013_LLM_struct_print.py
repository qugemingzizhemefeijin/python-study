import asyncio

from pydantic import BaseModel
from agents import Agent, Runner


class Data(BaseModel):
    name: str
    age: int
    gender: str
    comment: str


agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文进行回答。",
    output_type=Data  # 指定输出结构
)


async def main():
    result = await Runner.run(agent, "介绍一位值得记住的人。")

    obj: Data = result.final_output
    print(result.final_output)
    print(obj.name)
    print(obj.gender)
    print(obj.comment)

    print('完整的对话记录', result.to_input_list())


if __name__ == "__main__":
    asyncio.run(main())

