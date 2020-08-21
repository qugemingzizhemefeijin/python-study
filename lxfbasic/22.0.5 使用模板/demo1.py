from flask import Flask, request, render_template

app = Flask(__name__)

# Flask通过render_template()函数来实现模板的渲染。和Web框架类似，Python的模板也有很多种。Flask默认支持的模板是jinja2，所以我们先直接安装jinja2：
# pip install jinja2
# 一定要把模板放到正确的templates目录下，templates和app.py在同级目录下：

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
	return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
	username = request.form['username']
	password = request.form['password']
	if username == 'admin' and password == 'password':
		return render_template('signin-ok.html', username=username)
	return render_template('form.html', message = 'Bad username or password', username=username)

if __name__ == '__main__':
	app.run()
