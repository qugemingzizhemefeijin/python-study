import os
import openai

key = os.getenv('DEEP_SEEK_KEY')
os.environ["OPENAI_API_KEY"] = key
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"

client = openai.OpenAI()

# 利用大模型来讲之前的对话进行总结。
# 适合短期记忆

# 如果要长期记忆
# 知识图谱记忆：将对话中的实体和关系提取出来存入知识图谱，Agent可以查询图谱获取相关信息，适用于需要结构化知识的场景。
# 向量数据库记忆：将对话（或外部文档）分块、向量化后存入向量数据库。当需要相关信息时，将用户查询向量化，在数据库中进行相似度搜索，召回最相关的片段作为上下文。这是实现RAG的核心。


def context_summary(message_list):
    response = client.chat.completions.create(
        model="deepseek-v3",
        messages=[{
            "role": "user",
            "content": f"请对以下对话内容进行总结：{message_list}"
        }]
    )

    new_message_list = {"role": "system", "content": f"此前对话内容的总结：{response.completion.choices[0].message.content}"}
    return new_message_list


message_list = []
system_prompt = """
你运行在一个和思考、行动、观察和回答的循环，在循环结束时，你输出最终的答案。
用“思考”来描述你对被问问题的想法。
用“操作”运行您可用的操作之一。
“观察”将是运行这些操作的结果。
“答案”将是分析观察结果的结果。
"""
message_list.append({"role": "system", "content": system_prompt})

query = "比赛场上，篮球队的球员人数乘以排球队的球员人数，结果是多少"
message_list.append({"role": "user", "content": query})
message_list.append({"role": "user", "content": query})
message_list.append({"role": "user", "content": "1+1=?"})
message_list.append({"role": "user", "content": "再加1呢？"})

print(context_summary(message_list))
