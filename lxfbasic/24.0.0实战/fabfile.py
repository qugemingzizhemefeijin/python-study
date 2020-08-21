# -*- coding: utf8 -*-

"""
Fabric就是一个自动化部署工具。

要用Fabric部署，需要在本机（是开发机器，不是Linux服务器）安装Fabric

# pip uninstall Fabric
pip install Fabric3

https://github.com/mathiasertl/fabric/

fab build
fab deploy
"""

import os , re
from datetime import datetime

# 导入Fabric API
from fabric.api import *

# 服务器登录用户名
env.user = 'root'
# 服务器地址，可以有多个，依次部署
env.hosts = ['1.24.40.18:22']
env.passwords = {
    'root@1.24.40.18:22':'112%',
}

# 服务器MySQL用户名和口令
db_user = 'test'
db_password = 'test'

_TAR_FILE = 'dist-awesome.tar.gz'

# 上传文件的临时目录
_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
# 项目
_REMOTE_BASE_DIR = '/opt/backend/python'

def _current_path():
	return os.path.abspath('.')

def _now():
	return datetime.now().strftime('%y-%m-%d_%H.%M.%S')

def build():
	'''
	构建部署包
	'''
	includes = ['static', 'templates', 'transwarp', 'favicon.ico', '*.py']
	excludes = ['test', '.*', '*.pyc', '*.pyo']
	local('rm -f dist/%s' % _TAR_FILE)
	with lcd(os.path.join(_current_path(), 'www')):
		cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
		cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
		cmd.extend(includes)
		local(' '.join(cmd))

# 注意run()函数执行的命令是在服务器上运行，with cd(path)和with lcd(path)类似，把当前目录在服务器端设置为cd()指定的目录。
# 如果一个命令需要sudo权限，就不能用run()，而是用sudo()来执行。
def deploy():
	newdir = 'www-%s' % _now()
	# 删除已有的tar文件:
	run('rm -f %s' % _REMOTE_TMP_TAR)
	# 上传新的tar文件:
	put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
	# 创建新目录:
	with cd(_REMOTE_BASE_DIR):
		run('mkdir %s' % newdir)
	# 解压到/tep/**.tar.gz 到新目录:
	with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
		run('tar -zxvf %s' % _REMOTE_TMP_TAR)
	# 重置软链接:
	with cd(_REMOTE_BASE_DIR):
		run('rm -f www')
		run('ln -s %s www' % newdir)
		#run('chown root:root www')
		#run('chown -R root:root %s' % newdir)
	# 重启Python服务和nginx服务器:
	with settings(warn_only=True):
		#run('supervisorctl stop awesome')
		#run('supervisorctl start awesome')
		#run('/etc/init.d/nginx reload')
		print('====')

def backup():
	'''
	将数据库数据备份到备份目录中
	'''
	dt = _now()
	f = 'backup-awesome-%s.sql' % dt
	with cd('/tmp'):
		run('mysqldump --user=%s --password=%s --skip-opt --add-drop-table --default-character-set=utf8 --quick awesome > %s' % (db_user, db_password, f))
		run('tar -czvf %s.tar.gz %s' % (f, f))
		get('%s.tar.gz' % f, '%s/backup/' % _current_path())
		run('rm -f %s' % f)
		run('rm -f %s.tar.gz' % f)

RE_FILES = re.compile('\r?\n')

def rollback():
	'''
	回滚到上一个版本
	'''
	with cd(_REMOTE_BASE_DIR):
		r = run('ls -p -1')
		# 去掉目录的名字中最后的'/'字符
		files = [s[:-1] for s in RE_FILES.split(r) if s.startswith('www-') and s.endswith('/')]
		# 按照名称倒排
		files.sort(key=cmp_to_key(lambda s1, s2 : 1 if s1 < s2 else -1))
		r = run('ls -l www')
		if len(ss) != 2:
			print("ERROR: 'www' is not a symbol link.")
			return
		# 从当前的索引中找出现在部署文件所在目录的位置索引
		current = ss[1]
		print('Found current symbol link points to: %s\n' % current)
		try:
			index = files.index(current)
		except ValueError as e:
			print('ERROR: symbol link is invalid.')
			return

		if len(files) == index + 1:
			print('ERROR: already the oldest version.')
		old = files[index + 1]
		print('='*20)

		for f in files:
			if f == current:
				print('      Current ---> %s' % current)
			elif f == old:
				print('  Rollback to ---> %s' % old)
			else:
				print('                   %s' % f)
		print('='*20)
		print('')

		yn = raw_input('continue? y/N ')
		if yn != 'y' and yn != 'Y':
			print('Rollback cancelled.')
			return

		print('Start rollback...')
		run('rm -f www')
		run('ln -s %s www' % old)
		run('chown www-data:www-data www')
		with settings(warn_only=True):
			run('supervisorctl stop awesome')
			run('supervisorctl start awesome')
			#run('/etc/init.d/nginx reload')
		print('ROLLBACKED OK.')

def restore2local():
	'''
	将备份的数据库文件导入到mysql中
	'''
	backup_dir = ps.path.join(_current_path(), 'backup')
	fs = os.listdir(backup_dir)
	files = [f for f in fs if f.startswith('backup-') and f.endswith('.sql.tar.gz')]
	# 按照目录中文件名称倒序排列
	files.sort(key=cmp_to_key(lambda s1, s2 : 1 if s1 < s2 else -1))
	if len(files) == 0:
		print('No backup files found.')
		return
	print('Found %s backup files:' % len(files))
	print('='*20)
	# 打印出目录中所有的备份数据库名称
	n = 0
	for f in files:
		print('%s: %s' % (n, f))
		n = n + 1
	print('='*20)
	print('')

	# 选择需要下载的数据库文件索引
	try:
		num = int(raw_input('Restore file: '))
	except ValueError:
		print('Invalid file number.')
		return

	restore_file = files[num]
	yn = raw_input('Restore file %s: %s? y/N ' % (num, resotre_file))
	if yn != 'y' and yn != 'Y':
		print('Restore cancelled.')
		return

	print('Start restore to local database...')
	# 终端输入本地的用户名和密码并创建数据
	p = raw_input('Input mysql root password: ')
	sqls = [
		'drop database if exists awesome;',
		'create database awesome;',
		'grant select, insert, update, delete on awesome.* to \'%s\'@\'localhost\' identifed by \'%s\';' % (db_user, db_password)
	]
	# 生成数据库和用户
	for sql in sqls:
		local(r'mysql -uroot -p%s -e "%s"' % (p, sql))
	# 解压指定的数据库压缩文件
	with lcd(backup_dir):
		local('tar -zxvf %s' % restore_file)
	# 将解压后的数据库数据导入到mysql中
	local(r'mysql -uroot -p%s awesome < backup/%s' % (p, restore_file[:-7]))
	with lcd(backup_dir):
		local('rm -f %s' % restore_file[:-7])
