import os
import httpx
import json
from openai import OpenAI

key = os.getenv('QWEN_API_KEY')
os.environ["OPENAI_API_KEY"] = key
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def get_weather(latitude, longitude):
    response = httpx.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return f"{data['current']['temperature_2m']}°C"


client = OpenAI()

# 使用JSON格式描述函数的名字、功能、参数
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "根据指定的坐标提供当地摄氏温度",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

# 使用变量保存历史记录
message_history = []

# 发送消息给大模型，并自动保存记录


def get_completion(message):
    message_history.append(message) # 用户提问加入记录
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=message_history,
        tools=tools,
    )

    response_dict = dict(response.choices[0].message)
    message_history.append(response_dict)   # 大模型回答加入记录
    return response_dict


mess = get_completion({"role": "user", "content": "今天北京天气如何？"})
print(mess)  # LLM返回工具调用信息

func_call_id = mess['tool_calls'][0].id
func_kwargs = json.loads(mess['tool_calls'][0].function.arguments)
func_result = get_weather(**func_kwargs)    # 调用函数

print("")
mess = get_completion({"role": "tool", "tool_call_id": func_call_id, "content": str(func_result)})
print(mess)  # LLM返回工具调用信息

# {'content': '', 'refusal': None, 'role': 'assistant', 'annotations': None, 'audio': None, 'function_call': None, 'tool_calls': [ChatCompletionMessageFunctionToolCall(id='call_702d19ce855b4cc9894aa7', function=Function(arguments='{"latitude": 39.9042, "longitude": 116.4074}', name='get_weather'), type='function', index=0)]}
# {'content': '今天北京的天气温度为26.0°C。', 'refusal': None, 'role': 'assistant', 'annotations': None, 'audio': None, 'function_call': None, 'tool_calls': None}

