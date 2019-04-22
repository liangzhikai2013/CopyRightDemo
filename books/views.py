from flask import render_template,redirect,jsonify
from flask.views import MethodView
from DbContext.context import *
from models.model import *
from result.result import *
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
	

