from flask import Blueprint


books=Blueprint('books',__name__)

from books.views import *

books.add_url_rule('/',view_func=BookList.as_view('list'))