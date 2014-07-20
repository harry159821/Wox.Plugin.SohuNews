#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json,re
import webbrowser
from bs4 import BeautifulSoup
#import chardet

def query(Allkey):
	Allkey = Allkey.encode("gbk")
	key = Allkey.split(" ")[1]
	results = []
	if key:
		if Allkey.endswith(' '):
			html = requests('http://news.sogou.com/news?query='+key)		
			#print chardet.detect(html)
			html = html.decode('gbk','ignore').encode("utf-8")
			#print chardet.detect(html)
			re_h=re.compile('<!--?\w+[^-->]*>')#HTML标签
			re_comment=re.compile('<!--[^>]*-->')#HTML注释
			html=re_h.sub('',html) #去掉HTML 标签
			html=re_comment.sub('',html)#去掉HTML注释
			bs = BeautifulSoup(html)
			for i in bs.select(".results .rb"):
				res = {}
				link = i.select(".pt a")[0]['href']#新闻链接
				title = i.select("a b")[0].text#新闻标题
				time = i.select("h3 cite")[0].text#新闻时间
				content = i.select(".ft")[0].text#新闻内容
				content = content.replace("\n\r",'')
				content = content.replace("\n",'')
				content = content.replace("\r",'')
				content = content.replace("   ",'')
				#content = content[:60] + '\n' + content[80:]			
				res["Title"] = title
				res["SubTitle"] = content[:-20]
				res["IcoPath"] = "./icon.png"
				res["ActionName"] = "openUrl"
				res["ActionPara"] = link
				results.append(res)
				#print res
			return json.dumps(results)
		else:
			url = 'http://w.sugg.sogou.com/sugg/ajaj_json.jsp?&type=news&pr=news&abtestid=&key=%E9%A9%AC%E8%88%AA'			
			html = requests(url)[16:-4]
			html = html.decode('gbk','ignore').encode("utf-8")			
			#html = json.loads(html)
			exec('html='+html)
			for i in html[0][1]:
				res = {}
				res["Title"] = i
				res["IcoPath"] = "./icon.png"
				#res["ActionName"] = 
				#res["ActionPara"] = 
				results.append(res)
			return json.dumps(results)
	else:
		print 'news'
		for i in get_sohu_news():
			res = {}
			res["Title"] = i[0]
			res["IcoPath"] = "./icon.png"
			res["ActionName"] = "openUrl"
			res["ActionPara"] = i[1]
			results.append(res)
		return json.dumps(results)

def get_sohu_news():
	#下载新闻网页
	url = 'http://news.sohu.com/photo/'
	header = {
			'Host': 'news.sohu.com',
			#'Connection': 'keep-alive',
			#'Cache-Control': 'max-age=0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
			'Referer': 'http://news.sohu.com/',
			#'Accept-Encoding': 'gzip,deflate,sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6',
			}
	req=urllib2.Request(url,data=None, headers=header)
	resp=urllib2.urlopen(req,timeout=10)
	html = resp.read()
	html = html.decode("gbk").encode('utf-8')
	#提取新闻数据,中国观和国际观
	data = re.search(r"DOMESTIC NEWS([\w\W]*)<!--娱乐星闻开始-->",html)
	if data:data = data.group(0)
	#data = data.replace('\r\n\t','')
	#data = data.replace('\r\n','')
	result = []
	data = re.findall(r'''(<li class="list([\w\W]*?)"><a href="([\w\W]*?)" target=_blank><i></i><img src="([\w\W]*?)"  border="0"></a> ([\w\W]*?)<h5><a href="([\w\W]*?)" target=_blank>([\w\W]*?)</a></h5>([\w\W]*?)<span class="picnum_([\w\W]*?)">套图([\w\W]*?)张</span></li>).*?''',data)
	if data:
		for i in data:
			#print i[6],i[2],i[3]
			pass
			result.append([i[6],i[2],i[3]])
	return result

def requests(url,timeouts=5):
	header = {
			#'Host': 'news.sohu.com',
			#'Connection': 'keep-alive',
			#'Cache-Control': 'max-age=0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
			'Referer': 'http://news.sohu.com/',
			#'Accept-Encoding': 'gzip,deflate,sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6',
			}
	request = urllib2.Request(url,headers=header)
	response = urllib2.urlopen(request,timeout=timeouts)
	html = response.read()
	if html:	
		return html
	return False

def openUrl(context,url):	
	webbrowser.open(url)

if __name__ == '__main__':
	#print query(u"sohu ")
	print query(u"sohu 马航")
	#print query(u"sohu 马航 ")
