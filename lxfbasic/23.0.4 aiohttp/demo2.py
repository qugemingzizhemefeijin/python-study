#采用flask风格路由修饰器，实现flask提交表单那个例子

import asyncio
from aiohttp import web

#采用flask风格路由修饰器

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
	return web.Response(body=b"<h1>Hello, world!</h1>", headers={'content-type':'text/html'})

@routes.get('/signin')
async def signin_form(request):
	return web.Response(body=b'''<form action="/signin" method="post"
								<p><input name="username" /></p>
								<p><input name="password" type="password" /></p>
								<p><button type="submit">Sign In</button><p>
								</form>''',
								headers = {'content-type':'text/html'})

@routes.post('/signin')
async def signin(request):
	# 读取表单内容
	data = await request.post()
	if data['username'] == 'admin' and data['password'] == 'mypassword':
		return web.Response(body=b'<h3>Hello, admin!</h3>', headers={'content-type':'text/html'})
	return web.Response(body=b'<h3>Bad username or password</h3>', headers={'content-type':'text/html'})

app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0',port=8000)
