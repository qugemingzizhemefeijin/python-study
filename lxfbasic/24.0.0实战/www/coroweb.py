import asyncio, os, inspect, logging, functools

from urllib import parse
from aiohttp import web
from apis import APIError

def get(path):
	'''
	Define decorator @get('/path')
	'''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wrapper.__method__ = 'GET'
		wrapper.__route__ = path
		return wrapper
	return decorator

def post(path):
	'''
	Define decorator @post('/path')
	'''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wrapper.__method__ = 'POST'
		wrapper.__route__ = path
		return wrapper
	return decorator

def get_required_kw_args(fn):
	'''
	此方法是获取函数定义中没有定义默认值的参数名称(对应*或者*args之后的出现的非可变关键字参数)，返回元组类型
	'''
	args = []
	# 获取函数的所有的参数定义集合
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
			args.append(name)
	return tuple(args)

def get_named_kw_args(fn):
	'''
	此方法是获取函数中定义的所有的参数名称集合(对应*或者*args之后的出现的非可变关键字参数)，返回元组类型
	'''
	args = []
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			args.append(name)
	return tuple(args)

def has_named_kw_args(fn):
	'''
	检查函数是否定义了非可变关键字参数
	'''
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			return True

def has_var_kw_arg(fn):
	'''
	检查函数是否定义了可变关键字参数，对应**kwargs
	'''
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.VAR_KEYWORD:
			return True

def has_request_arg(fn):
	'''
	检查函数是否定义了request参数
	'''
	sig = inspect.signature(fn)
	params = sig.parameters
	found = False
	for name, param in params.items():
		if name == 'request':
			found = True
			continue
		# 如果找到了名字叫request的参数，但是又循环了一次后发现后面的参数不是*args 并且 不是*args之后的出现的非可变关键字参数 并且不是**kwargs
		# 则抛出异常，也就是说 request 必须在正常的参数的最后才行
		if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
			raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
	return found

class RequestHandler(object):

	def __init__(self, app, fn):
		self._app = app
		self._func = fn
		self._has_request_arg = has_request_arg(fn)
		self._has_var_kw_arg = has_var_kw_arg(fn)
		self._has_named_kw_args = has_named_kw_args(fn)
		self._named_kw_args = get_named_kw_args(fn)
		self._required_kw_args = get_required_kw_args(fn)

	async def __call__(self, request):
		kw = None
		# 如果函数有**kwargs 或者 有非可变参数 或者有 必填参数
		if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
			if request.method == 'POST':
				# 如果请求没有带content_type，则抛出异常
				if not request.content_type:
					return web.HTTPBadRequest('Missing Content-Type.')
				
				ct = request.content_type.lower()
				if ct.startswith('application/json'):
					params = await request.json()
					if not isinstance(params, dict):
						return web.HTTPBadRequest('JSON body must be object.')
					kw = params
				elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
					params = await request.post()
					kw = dict(**params)
				else:
					return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
			elif request.method == 'GET':
				qs = request.query_string
				if qs:
					kw = dict()
					for k, v in parse.parse_qs(qs, True).items():
						kw[k] = v[0]

		# 如果前面未匹配到提交的参数，则直接将PathVariable赋值给kw
		if kw is None:
			kw = dict(**request.match_info)
		else:
			# 这个分支是说：
			# 如果没有**kw参数 并且 有非可变参数
			# 然后循环方法中定义的非可变参数，如果用户有提交参数过来，则将其放到copy字典中，然后替换到原来的kw参数
			if not self._has_var_kw_arg and self._named_kw_args:
				# remove all unamed kw:
				copy = dict()
				for name in self._named_kw_args:
					if name in kw:
						copy[name] = kw[name]
				kw = copy
			# check named arg:
			for k, v in request.match_info.items():
				# 这里检查到用户又post了参数过来，然后又在PathVariable中有同名参数，则告警
				if k in kw:
					logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
				kw[k] = v
		# 如果形参中有request，则直接赋值
		if self._has_request_arg:
			kw['request'] = request
		# 检查必填参数:
		if self._required_kw_args:
			for name in self._required_kw_args:
				if not name in kw:
					return web.HTTPBadRequest('Missing argument: %s' % name)
		logging.info('call with args:%s' % str(kw))
		try:
			r = await self._func(**kw)
			return r
		except APIError as e:
			return dict(error=e.error, data=e.data, message=e.message)

def add_static(app):
	# 静态文件存储的地址
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
	app.router.add_static('/static/', path)
	logging.info('add static %s ==> %s' % ('/static/', path))

def add_route(app, fn):
	method = getattr(fn, '__method__', None)
	path = getattr(fn, '__route__', None)
	if path is None or method is None:
		raise ValueError('@get or @post not defind in %s.' % str(fn))
	# 如果函数不是协程函数 并且 不是一个装饰器函数，则修改为协程函数
	if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
		fn = asyncio.coroutine(fn)
	logging.info('add route %s %s ==> %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
	app.router.add_route(method, path, RequestHandler(app, fn))

# 自动扫描指定模块的所有符合条件的函数注册了:
def add_routes(app, module_name):
	print('module_name = %s' % module_name)
	n = module_name.rfind('.')
	if n == (-1):
		mod = __import__(module_name, globals(), locals())
	else:
		name = module_name[n+1:]
		mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
	# 动态扫描模块中的函数 dir()返回模块的所有函数名称
	for attr in dir(mod):
		if attr.startswith('_'):
			continue
		fn = getattr(mod, attr)
		print('module_name = %s , attr = %s' % (module_name, attr))
		if callable(fn):
			method = getattr(fn, '__method__', None)
			path = getattr(fn, '__route__', None)
			print('module_name = %s , attr = %s, method = %s, path = %s' % (module_name, attr, method, path))
			if method and path:
				add_route(app, fn)
