import sys
import os
import fileinput
import json
import requests

dirPath="F:\\python\\program\\bnn"
setting_file_path=dirPath+"\\setting.txt"
bnnfile=dirPath+"\\bnn.txt"

def writeLastIdx(idx):
	with open(setting_file_path,'w') as fw:
		fw.write(str(idx))

		
#添加请求头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
	'Accept':'*/*'
}

def downloadVideo(url):
	url = url.strip()
	filePath = os.path.basename(url)
	print("download url %s " %(url))
	im = requests.get(url, headers=headers)  # 请求url
	print("download url %s status code %s"%(url,im.status_code))
	if im.status_code == 200:
		open(dirPath+"\\"+filePath, 'wb').write(im.content)  # 写入文件


#从上次位置继续执行
idx=0
if os.path.exists(setting_file_path):
	with open(setting_file_path,'r') as fr:
		idx = int(fr.read())

print("start line %s " %(idx))
i=0
counter=0
for url in fileinput.input(dirPath+"\\bnn.txt"):
	if i >= idx:
		downloadVideo(url)
		idx += 1
		writeLastIdx(idx)
		counter += 1
		if counter >= 10:	#下载10个则结束
			break
	i += 1
    
print('download finish')
