import os

from openai import OpenAI

key = os.getenv('DEEP_SEEK_KEY')
os.environ["OPENAI_API_KEY"] = key
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"

client = OpenAI()

# 与LLM的对话是通过消息（Message）进行的，每个消息都是一个字典，包含以下关键信息：
# role（角色）：消息的发送者角色
#     user: 代表用户的消息，即我们向LLM提出的问题或指令。
#     assistant: 代表AI助手的消息，即LLM给出的回复。
#     system: 代表对给LLM的设定，如角色、性格或其他要求。
# content(内容)：消息的具体文本内容，即对话内容。

# temperature：温度可以控制LLM生成文本的创造性和随机性，范围0-2，默认为1
# 越接近0：生成的文本更保守，重复性高，更倾向于选择最可能的Token。适合需要更准确性和一致性的任务，例如事实、代码、数学相关等。
# 越接近2：生成的文本更更新、发散。重复性低，更倾向于选择不太常见但仍然合理的Token。适合需要创造性和灵感的任务，例如故事创作、头脑风暴等。

t = 0.9
completion = client.chat.completions.create(
    model="deepseek-v3", # 不支持工具调用
    messages=[
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    temperature=t,
    stream=True
)

# print(completion.choices[0].message.content)

# 逐步、增量输出生成内容
for chunk in completion:
    print(chunk.choices[0].delta.content, end="")
