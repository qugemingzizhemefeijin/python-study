import openai
import json
import os

key = os.getenv('QWEN_API_KEY')
os.environ["OPENAI_API_KEY"] = key
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"

client = openai.OpenAI()


# 充当数据库
def get_info_on_ball_game(game_name: str):
    data = [
        {
            "name": "篮球（Basketball）",
            "description": "两支球队通过投篮得分，比赛分为四节，每节时间因联赛而异。",
            "team_members": 12,
            "players_on_field": 5,
        },
        {
            "name": "排球（Volleyball）",
            "description": "两队隔网对抗，通过击球过网并使其落在对方场地得分",
            "team_members": 12,
            "players_on_field": 6,
        },
        {
            "name": "足球（Soccer）",
            "description": "两支球队通过踢球进入对方球门得分，比赛分为上下半场。",
            "team_members": 11,
            "players_on_field": 11,
        },
        {
            "name": "沙滩排球（Beach Volleyball）",
            "description": "排球的变种，在沙地上进行，每队人数较少",
            "team_members": 2,
            "players_on_field": 2,
        },
        {
            "name": "网球（Tennis）",
            "description": "单打或双打比赛，球员用球拍击球过网，使对手无法回击。",
            "team_members": 1,
            "players_on_field": 1,
        },
        {
            "name": "棒球（Baseball）",
            "description": "进攻方击球后跑垒得分，防守方投球并试图使击球手出局。",
            "team_members": 9,
            "players_on_field": 9,
        },
        {
            "name": "冰球（Ice Hockey）",
            "description": "在冰面上进行，球员用球棍击打冰球进入对方球门。",
            "team_members": 20,
            "players_on_field": 6,
        },
        {
            "name": "橄榄球（Rugby）",
            "description": "球员持球奔跑或传球，通过达阵或射门得分。",
            "team_members": 15,
            "players_on_field": 15,
        },
        {
            "name": "乒乓球（Table Tennis）",
            "description": "两名或四名球员在球桌上用球拍击打小球。",
            "team_members": 1,
            "players_on_field": 1,
        },
        {
            "name": "羽毛球（Badminton）",
            "description": "球员用球拍击打羽毛球过网，使对手无法回击。",
            "team_members": 1,
            "players_on_field": 1,
        }
    ]
    ret = []
    for d in data:
        if game_name.lower() in d['name'].lower():
            ret.append(d)
    return ret


# 大模型的可调用工具
tools = [{
    "type": "function",
    "function": {
        "name": "get_info_on_ball_game",
        "description": "获取球类比赛的基本信息和人员规模",
        "parameters": {
            "type": "object",
            "properties": {
                "game_name": {"type": "string"}
            },
            "required": ["game_name"],
            "additionalProperties": False   # 不允许 AI 传入 schema 中未定义的额外属性（AI 只允许传入 properties 中定义的字段，多传任何一个额外字段都会报错）
        },
        "strict": True
        # 当 strict: True 时，模型强制要求：
        # 1、additionalProperties 必须为 False
        # 2、所有字段的类型必须是 JSON Schema 的子集（string、number、integer、boolean、array、object 等）
        # 3、不能使用 anyOf、allOf 等复杂约束
    }
}]

system_prompt = """
你运行在一个和思考、行动、观察和回答的循环，在循环结束时，你输出最终的答案。
用“思考”来描述你对被问问题的想法。
用“操作”运行您可用的操作之一。
“观察”将是运行这些操作的结果。
“答案”将是分析观察结果的结果。
"""
message_history = []
message_history.append({"role": "system", "content": system_prompt})


# 登录模型，提交问题，并将回答记录到历史对话中
def get_completion(message):
    message_history.append(message)     # 用户提问加入记录
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=message_history,
        tools=tools,
    )

    response_dict = dict(response.choices[0].message)
    message_history.append(response_dict)   # 大模型回答加入记录
    return response_dict


def agent(query):
    max_turns = 5
    current_turns = 1
    next_message = {"role": "user", "content": query}
    while current_turns <= max_turns:
        message = get_completion(next_message)
        print(message['content'])
        if message['tool_calls']:
            func_call_id = message['tool_calls'][0].id
            func_kwargs = json.loads(message['tool_calls'][0].function.arguments)
            func_result = get_info_on_ball_game(**func_kwargs)  # 调用函数

            print(f"观察：{func_result}")
            next_message = {"role": "tool", "tool_call_id": func_call_id, "content": str(func_result)}
        else:
            break


if __name__ == '__main__':
    query = "比赛场上，篮球队的球员人数乘以排球队的球员人数，结果是多少？"
    agent(query)
