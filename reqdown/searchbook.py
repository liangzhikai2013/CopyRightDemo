import requests
from urllib import parse
import shutil
import os
import asyncio
from pyppeteer import launch
from selenium import webdriver
from bs4 import BeautifulSoup
class down_book(object):
	"""爬虫类"""
	def __init__(self):
		self.kw=""
		self.core="all"
		self.spellchecker="true"
		self.device='iPhone'
		self.urldomain='https://www.ximalaya.com/revision/search'
		self.pageNum=1
		self.albumId=0
		self.chapterurl="https://www.ximalaya.com/revision/album/getTracksList"
		self.audiourl="https://www.ximalaya.com/youshengshu/10579209/"
		self.audiopath="../audiopath"
	@property
	def kw(self):
		return self._kw
	@kw.setter
	def kw(self,value):
		self._kw=value
	
	@property
	def core(self):
		return self._core
	@core.setter
	def core(self,value):
		self._core=value
	@property
	def spellchecker(self):
		return self._spellchecker
	@spellchecker.setter
	def spellchecker(self,value):
		self._spellchecker=value
	@property
	def device(self):
		return self._device
	@device.setter
	def device(self,value):
		self._device=value
	@property
	def urldomain(self):
		return self._urldomain
	@urldomain.setter
	def urldomain(self,value):
		self._urldomain=value
	@property
	def albumId(self):
		return self._albumId
	@albumId.setter
	def albumId(self,value):
		if not isinstance(value,int):
			raise ValueError('albumId为数字')
		self._albumId=value
	@property
	def pageNum(self):
		return self._pageNum
	@pageNum.setter
	def pageNum(self,value):
		if not isinstance(value,int):
			raise ValueError('pageNum为数字')
		self._pageNum=value
	@property
	def chapterurl(self):
		return self._chapterurl
	@chapterurl.setter
	def chapterurl(self,value):
		self._chapterurl=value
	@property
	def audiourl(self):
		return self._audiourl
	@audiourl.setter
	def audiourl(self,value):
		self._audiourl=value
	@property
	def audiopath(self):
		dir=os.path.abspath(self._audiopath)
		self._audiopath=os.path.join(dir,self.filename)
		return self._audiopath
	@audiopath.setter
	def audiopath(self,value):
		self._audiopath=value
	
	@property
	def filename(self):
		return os.path.basename(self.audiourl)

	
	
	##搜索
	def search(self):
		
		refkw=parse.urlencode(dict(res=self.kw))
		refkw=refkw.split("=",1)[1]
		headers={
		         "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
		         "Referer":"https://www.ximalaya.com/search/"+refkw,
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
		        }
		data=dict(core=self.core,kw=refkw,spellchecker=self.spellchecker,device=self.device)
		print(data)
		resp=requests.get(self.urldomain,params=data,headers=headers)
		print(resp.url)
		print(resp.status_code)
		return resp.json()
	#遍历章节信息
	def searchChapter(self):
		data=dict(albumId=self.albumId,pageNum=self.pageNum)
		headers={
		         "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
		         "Referer":"https://www.ximalaya.com/youshengshu/"+str(self.albumId)+"/p"+str(self.pageNum)+"/",
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
		}
		resp=requests.get(self.chapterurl,data,headers=headers)
		print(resp.url)
		print(resp.status_code)
		return resp.json()
	async def downhtml(self):
		browser=await launch({'headless':False})
		page=await browser.newPage()
		#设置窗口大小
		await page.setViewport(viewport={'width':1280,'height':800})
		#是否开启Javascript
		await page.setJavascriptEnabled(enabled=True)
		await page.goto(self.audiopath)
		print(await page.content())
		await browser.close()
		return await page.content()
	#下载文件
	def downaudio(self):
		resp=requests(self.audiourl,stream=True)
		if resp.status_code==200:
			with open(self.audiopath,'wb') as f:
				resp.raw.deconde_content=True
				shutil.copyfileobj(resp.raw,f)
	def sdownhtml(self):
		driver=webdriver.Chrome(executable_path='/Users/qdl/Desktop/webdriver/chromedriver')
		driver.get(self.audiourl)
		source=driver.page_source
		soup=BeautifulSoup(source,'lxml')
		driver.close()
		return soup.prettify()
	



	







		