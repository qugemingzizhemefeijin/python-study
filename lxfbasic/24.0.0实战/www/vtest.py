import inspect

def aaa(id, request, *, content):
	print('123')

params = inspect.signature(aaa).parameters
for k, param in params.items():
	print('k==%s' % k)
	print('param.kind == %s' % param.kind)
	print('param.default == %s' % param.default)

