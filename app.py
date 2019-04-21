from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#打开调试
app.debug=True
#配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Zgmqdl11@cdb-oe787i4t.gz.tencentcdb.com:10018/XMLY'
#打开
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#打印SQL
app.config['SQLALCHEMY_ECHO']=True

#数据库db对象关联app
db=SQLAlchemy(app)
from spider import spider as bluespider
from books import books as bluebook


app.register_blueprint(bluespider,url_prefix='/spider')
app.register_blueprint(bluebook,url_prefix="/books")

@app.route("/")
def index():
	return 'Index'
#启动APP
if __name__ == '__main__':
    app.run()