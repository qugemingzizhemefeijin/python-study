彻底重建虚拟环境（最可靠）
```
# 1. 退出当前环境（如果有）
deactivate

# 2. 删除旧的虚拟环境
Remove-Item -Recurse -Force .\venv

# 3. 创建新的虚拟环境
python -m venv venv

# 4. 激活新环境
.\venv\Scripts\activate

# 5. 验证
pip -V
```