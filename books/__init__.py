from flask import Blueprint


books=Blueprint('books',__name__)

from books.views import *

books.add_url_rule('/',view_func=BookList.as_view('list'))
books.add_url_rule("/searchbooks",view_func=searchbooks.as_view("searchbooks"))
books.add_url_rule("/spider",view_func=spider.as_view("spider"))
books.add_url_rule("/down",view_func=down.as_view("down"))