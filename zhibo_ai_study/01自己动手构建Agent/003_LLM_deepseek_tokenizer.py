from deepseek_tokenizer import ds_token

# 统计分词数

text = "你是谁？"
result = ds_token.encode(text)

print(result)
print(f"Token数：{len(result)}")
