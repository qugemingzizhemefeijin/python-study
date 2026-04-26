# 多模态
import asyncio
import base64

from agents import Agent, Runner

import local_settings

agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文进行问答",  # 系统提示词
)


def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        bin_content = image_file.read()
        return base64.b64encode(bin_content).decode('utf-8')


async def main():
    base64_image = encode_image('hello.png')
    print(base64_image)

    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'input_image',
                    'image_url': f"data:image/jpeg;base64,{base64_image}",
                }
            ],
        },  # 图片内容
        {
            'role': 'user',
            'content': '图片中是什么内容？是什么颜色？',
        },  # 提示词内容
    ]
    # run为异步调用
    result = await Runner.run(agent, messages)

    print(result.final_output)


# main() 不能直接调用main

if __name__ == '__main__':
    asyncio.run(main())
