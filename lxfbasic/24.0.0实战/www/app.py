import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web, web_runner
from jinja2 import Environment, FileSystemLoader

import orm
from coroweb import add_routes, add_static

from handlers import cookie2user, COOKIE_NAME

def init_jinja2(app, **kw):
	logging.info('init jinja2...')
	options = dict(
		autoescape = kw.get('autoescape', True),# 如果设置为True，在渲染模板时，会自动将模板转义实体字符，此时使用safe过滤器可以使不需转义的渲染变量不转义，如{{ user.username|safe }}
		block_start_string = kw.get('block_start_string', '{%'),# 模块开始标记符，默认值{%
		block_end_string = kw.get('block_end_string', '%}'),# 模块结束标记符，默认值%}
		variable_start_string = kw.get('variable_start_string', '{{'),# 变量开始标记符，默认值{{
		variable_end_string = kw.get('variable_end_string', '}}'),# 变量结束标记符，默认值}}
		auto_reload = kw.get('auto_reload', True)# 如果设定为True，则当模板发生改动时会自动重载
	)
	path = kw.get('path', None)
	# 默认为当前文件的所属目录下的templates文件夹为模版文件目录
	if path is None:
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
	logging.info('set jinja2 template path: %s' % path)
	# 模板加载器，形式是loader=FileSystemLoader(path)，其中的path表示的是模板的文件路径
	env = Environment(loader=FileSystemLoader(path), **options)
	# 过滤器，多数用于渲染变量标记符的时候，在渲染模板时其语法形式是{{args|function}}（结合day8中的时间过滤器）。
	# 过滤器不是创建Environment实例的参数，它是以方法的形式绑定在Environment实例上，如Env.filters[FunctionName]=function
	filters = kw.get('filters', None)
	if filters is not None:
		for name, f in filters.items():
			env.filters[name] = f
	app['__templating__'] = env

async def logger_factory(app, handler):
	async def logger(request):
		logging.info('Request: %s %s' % (request.method, request.path))
		return (await handler(request))
	return logger

async def auth_factory(app, handler):
	'''
	把当前用户绑定到request上，并对URL/manage/进行拦截，检查当前用户是否是管理员身份
	'''
	async def auth(request):
		logging.info('check user: %s %s' % (request.method, request.path))
		request.__user__ = None
		cookie_str = request.cookies.get(COOKIE_NAME)
		if cookie_str:
			user = await cookie2user(cookie_str)
			if user:
				logging.info('set current user: %s' % user.email)
				request.__user__ = user
		# 如果访问地址是/manage/，则用户必须登录，否则自动跳转到登录页面
		if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
			return web.HTTPFound('/signin')
		return (await handler(request))
	return auth

async def response_factory(app, handler):
	async def response(request):
		logging.info('Response handler...')
		r = await handler(request)
		if isinstance(r, web.StreamResponse):
			return r
		elif isinstance(r, bytes):
			resp = web.Response(body=r)
			resp.content_type = 'application/octet-stream'
			return resp
		elif isinstance(r, str):
			if r.startswith('redirect:'):
				return web.HTTPFound(r[9:])
			resp = web.Response(body=r.encode('utf-8'))
			resp.content_type = 'text/html;charset=utf-8'
			return resp
		elif isinstance(r, dict):	# 返回的对象是字典，则判断是否包含template字段，包含的话则代码需要解析模版引擎，否则返回json
			template = r.get('__template__')
			if template is None:
				# 将返回的字典类型的对象转换成json对象输出
				resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
				resp.content_type = 'application/json;charset=utf-8'
				return resp
			else:
				r['__user__'] = request.__user__
				resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
				resp.content_type = 'text/html;charset=utf-8'
				return resp
		elif isinstance(r, int) and t>=100 and t<600:
			return web.Response(t)
		elif isinstance(r, tuple) and len(r) == 2:
			t, m = r
			if isinstance(t, int) and t >= 100 and t < 600:
				return web.Response(t, str(m))
		else:
			resp = web.Response(body=str(r).encode('utf-8'))
			resp.content_type = 'text/plain;charset=utf-8'
			return resp
	return response

def datetime_filter(t):
	'''
	用于模版页面的日期显示
	'''
	delta = int(time.time() - t)
	if delta < 60:
		return u'1分钟前'
	elif delta < 3600:
		return u'%s分钟前' %(delta // 60)
	elif delta < 86400:
		return u'%s小时前' % (delta // 3600)
	elif delta < 604800:
		return u'%s天前' % (delta // 86400)
	dt = datetime.fromtimestamp(t)
	return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

def init():
	# 初始化服务
	app = web.Application(middlewares=[
		logger_factory, auth_factory, response_factory
	])
	# 初始化数据库连接池
	app.on_startup.append(orm.create_pool)

	# 初始化模版引擎
	init_jinja2(app, filters=dict(datetime=datetime_filter))
	# 扫描所有的Path
	add_routes(app, 'handlers')
	# 加载静态资源目录
	add_static(app)
	# 启动服务
	web.run_app(app,host='0.0.0.0',port=9527)

if __name__ == '__main__':
	init()

'''
app = web.Application(middlewares=[middleware])

routes = web.RouteTableDef()
def init():
	app = web.Application()
	app.add_routes(routes)
	logging.info('server started at http://127.0.0.1:9257...')
	web.run_app(app, host='0.0.0.0',port=9527)

if __name__ == '__main__':
	init()
'''


'''
def start_rest_api(host, port, connection, timeout, registry):
    """Builds the web app, adds route handlers, and finally starts the app.
    """
    loop = asyncio.get_event_loop()
    connection.open()
    app = web.Application(loop=loop)
    app.on_cleanup.append(lambda app: connection.close())

    # Add routes to the web app
    LOGGER.info('Creating handlers for validator at %s', connection.url)

    handler = RouteHandler(loop, connection, timeout, registry)

    app.router.add_post('/batches', handler.submit_batches)
    app.router.add_get('/batch_statuses', handler.list_statuses)
    app.router.add_post('/batch_statuses', handler.list_statuses)

    app.router.add_get('/state', handler.list_state)
    app.router.add_get('/state/{address}', handler.fetch_state)

    app.router.add_get('/blocks', handler.list_blocks)
    app.router.add_get('/blocks/{block_id}', handler.fetch_block)

    app.router.add_get('/batches', handler.list_batches)
    app.router.add_get('/batches/{batch_id}', handler.fetch_batch)

    app.router.add_get('/transactions', handler.list_transactions)
    app.router.add_get(
        '/transactions/{transaction_id}',
        handler.fetch_transaction)

    app.router.add_get('/receipts', handler.list_receipts)
    app.router.add_post('/receipts', handler.list_receipts)

    app.router.add_get('/peers', handler.fetch_peers)

    subscriber_handler = StateDeltaSubscriberHandler(connection)
    app.router.add_get('/subscriptions', subscriber_handler.subscriptions)
    app.on_shutdown.append(lambda app: subscriber_handler.on_shutdown())

    # Start app
    LOGGER.info('Starting REST API on %s:%s', host, port)

    web.run_app(
        app,
        host=host,
        port=port,
        access_log=LOGGER,
        access_log_format='%r: %s status, %b size, in %Tf s')
'''