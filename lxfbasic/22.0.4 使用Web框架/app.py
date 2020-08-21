from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	return '<H1>Hello Python!</H1>'

@app.route('/signin', methods=['GET'])
def signin_form():
	return '''<form action="/signin" method="post">
			<p><input name="username"></p>
			<p><input name="password" type="password"></p>
			<p><button type="submit">Sign In</button></p>
			</form>'''

@app.route('/signin', methods=['POST'])
def signin():
	# 需要从request对象读取表单内容：
	if request.form['username'] == 'admin' and request.form['password'] == 'password':
		return '<h3>Hello, admin!</h3>'
	return '<3>Bad username or password.</h3>'

if __name__ == '__main__':
	app.run()

"""
运行python app.py，Flask自带的Server在端口5000上监听：

python app.py 
Running on http://127.0.0.1:5000/

打开浏览器，输入首页地址http://localhost:5000/：
"""

"""
实际的Web App应该拿到用户名和口令后，去数据库查询再比对，来判断用户是否能登录成功。

除了Flask，常见的Python Web框架还有：

Django：全能型Web框架；

web.py：一个小巧的Web框架；

Bottle：和Flask类似的Web框架；

Tornado：Facebook的开源异步Web框架。

当然了，因为开发Python的Web框架也不是什么难事，我们后面也会讲到开发Web框架的内容。
"""