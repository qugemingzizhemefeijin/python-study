from agents import Agent, Runner

import local_settings   # 加载本地设置

# async写法和流失传输

agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文进行问答",    # 系统提示词
)

result = Runner.run_sync(agent, "你是谁？")

print(result.final_output)
