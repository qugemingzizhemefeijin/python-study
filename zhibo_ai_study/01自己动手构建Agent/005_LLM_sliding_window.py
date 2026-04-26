from deepseek_tokenizer import ds_token


message_history = []
system_prompt = """
你运行在一个和思考、行动、观察和回答的循环，在循环结束时，你输出最终的答案。
用“思考”来描述你对被问问题的想法。
用“操作”运行您可用的操作之一。
“观察”将是运行这些操作的结果。
“答案”将是分析观察结果的结果。
"""
message_history.append({"role": "system", "content": system_prompt})

query = "比赛场上，篮球队的球员人数乘以排球队的球员人数，结果是多少"
message_history.append({"role": "user", "content": query})
message_history.append({"role": "user", "content": query})
message_history.append({"role": "user", "content": "1+1=?"})
message_history.append({"role": "user", "content": "再加1呢？"})


def context_sliding_window(message_list: list, k=2):
    new_message_list: list = message_list[-1*k:]

    # 如果丢失了系统提示，则手动补上
    if new_message_list[0]['role'] != 'system': # 检查之前有没有系统提示
        if message_list[0]['role'] == 'system': # 检查现在有没有系统提示
            new_message_list.insert(0, message_list[0])

    return new_message_list


print(context_sliding_window(message_history))
