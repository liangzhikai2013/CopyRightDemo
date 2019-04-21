from flask import render_template, redirect
from flask.views import MethodView
from models.model import *


class Spider(MethodView):
	def get(self):
		return '爬虫相关的API'

