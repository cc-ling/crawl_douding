import requests
import re
import json
import os
from PIL import Image

req = requests.Session()
req.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})

def save_pic(title, index ,content): #存图片
	my_file = './' + str(title)
	if not os.path.exists(my_file):
		os.mkdir(my_file) #如果本文档目录不存在，就创建

	with open(my_file + './' + str(index) + '.png' ,'wb' ) as f:
		f.write( content )

def get_pic(start_url):
	#start_url = 'https://max.book118.com/html/2017/0905/132056933.shtm'

	view_token_text = req.get(start_url).text
	view_token = re.findall("view_token.*?'(.*?)'",str(view_token_text))[0]
	page = re.findall('id="pagenumber">(.*?)</span>',str(view_token_text))[0].strip()[:-1]
	page = int(page)
	title = re.findall('<title>(.*?)</title>',str(view_token_text))[0].split('.')[0]
	url = 'https://max.book118.com/index.php?g=Home&m=Ajax&a=getPreviewData' #所有文档都是这个url
	print('共'+ str(page) + '页')
	for i in range(0,page//6 +1 ):
		data= {
			'aid' :  start_url.split('/')[-1].split('.')[0] ,
			'page_number' : i*6+1,
			'view_token' : view_token,
			}
		pic_url_dict = json.loads( req.post(url, data=data).text ) ['data'] #所欲图片序号和url的字典

		for pic_url_key in pic_url_dict.keys():
			pic_url = 'http:' + pic_url_dict[pic_url_key ] 
			pic_content = req.get(pic_url).content 
			save_pic(title, pic_url_key,pic_content) 
		print('已完成'+ str( i*6/page*100)[:4] + '%' )
	return title

def save_pdf(path):
	img_open = []
	#字符串11和2排序问题，在这把png文件以数量形式展示出来
	#因为图片名全为数字
	file_name = 0
	for i in os.listdir(path):
		if str(i)[-4:] == '.png':
			file_name +=1
	file_name = list(range(1,file_name+1)) 
	file_name.sort()
	file_name = [ str( _ )+'.png' for _ in file_name ]
	for i in file_name[1:]: #第一个不要了，在下面合并文件时候调用
		img = Image.open(  path + '\\'+i)
		if img.mode == 'RGBA' :
			img_open.append(img.convert('RGB'))
		else:
			img_open.append(img)
	f = Image.open(path + '\\'+ file_name[0])
	f.save(  path + '\\'+ '.pdf','PDF',resolution = 100.0,save_all=True,append_images= img_open)

word_url = input('请输入豆丁网文档网址：\n>')
path = os.getcwd()
title = get_pic(word_url)

#此处不建议调用自动存pdf，存出来的pdf文件过大
#save_pdf(path + '\\' + title) 
