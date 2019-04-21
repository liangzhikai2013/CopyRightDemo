from flask import render_template,redirect
from flask.views import MethodView
from models.model import *
class BookList(MethodView):
	"""docstring for BookList"""
	def get(self):
		result=db.session.query(book.id).first()
		if result:
			return result
		else:
			return 'OK'
	
