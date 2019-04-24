from flask import render_template,redirect,jsonify
from flask.views import MethodView
from DbContext.context import *
from models.model import *
from result.result import *
from reqdown.searchbook import *
import asyncio
from pyppeteer import launch

class BookList(MethodView):
	"""docstring for BookList"""
	def get(self):
		b=BookDAL(book)
		b.bookid=1
		result=b.Search()
		if result:
			book.listjson=result
			result=book.convert_listjson(book)
			result=Result(0,result,"OK")
			result=Result.convert_json(result)
			return jsonify(result)
		else:
			return 'OK'
class searchbooks(MethodView):
	"""检索书籍"""
	def get(self):
		d=down_book()
		d.kw='白鹿原'
		res=d.search()
		data=res.get('data',None)
		msg=res.get('msg',None)
		result=Result(0,data,msg)
		result=Result.convert_json(result)
		return jsonify(result)

class spider(MethodView):
	"""下载章节"""
	def get(self):
		d=down_book()
		d.albumId=16874811
		d.pageNum=1
		res=d.searchChapter()
		data=res.get('data',[])
		pageSize=data.get('pageSize',None)
		pageNum=data.get('pageNum',None)
		trackTotalCount=data.get('trackTotalCount',None)
		msg=res.get('msg',None)
		result=ResultData(0,data,msg,pageNum,pageSize,trackTotalCount)
		result=ResultData.convert_json(result)
		return jsonify(result)
class down(MethodView):
	"""docstring for down"""
	res=""
	def get(self):
		try:
			d=down_book()
			res=d.sdownhtml()
		except Exception as e:
			print('异常是{}'.format(e))
		finally:
			return res
		
	
		

