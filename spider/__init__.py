from flask import Blueprint

spider=Blueprint('spider',__name__)

from spider.views import *

spider.add_url_rule('/',view_func=Spider.as_view("list"))