from app import db
class book(db.Model):
	"""书籍信息表"""
	__tablename__='books'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	#书籍ID
	bookid=db.Column(db.String(100))
	#播放ID
	play=db.Column(db.String(60))
	#名称
	title=db.Column(db.String(100))
	#URL路径
	url=db.Column(db.String(300))
	#分类ID
	category_id=db.Column(db.Integer)
	def __init__(self,bookid,play,title,url,category_id):
		self.bookid=bookid
		self.play=play
		self.title=title
		self.url=url
		self.category_id=category_id
		self.listjson=[]
	def convert_json(self):
		return dict(id=self.id,bookid=self.bookid,play=self.play,title=self.title,url=self.url,category_id=self.category_id)
	@property
	def listjson(self):
		return self._listjson
	@listjson.setter
	def listjson(self,value):
		if not isinstance(value,tuple):
			raise ValueError('必须是list')
		self._listjson=value
	def convert_listjson(self):
		return [item.convert_json() for item in self.listjson]
	

class chapters(db.Model):
	"""章节信息表"""
	__tablename__='chapter'
	id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	#音频ID
	trackId=db.Column(db.Integer)
	#这个ID对应bookID,所以不创建主外键关系了
	albumId=db.Column(db.Integer)
	#名称
	title=db.Column(db.String(200))
	#总共播放量
	playCount=db.Column(db.Integer)
	#音频的时长
	duration=db.Column(db.String(50))
	#路径
	url=db.Column(db.String(200))
	#音频存储路径
	path=db.Column(db.String(100))
	#识别结果,音轨为1的时候
	result_one=db.Column(db.Text)
	#识别结果,音轨为2的时候
	result_two=db.Column(db.Text)
	def __init__(self,trackId,title,playCount,duration,url,path,albumId,result_one,result_two):
		self.trackId=trackId
		self.title=title
		self.playCount=playCount
		self.duration=duration
		self.url=url
		self.path=path
		self.albumId=albumId
		self.result_one=result_one
		self.result_two=result_two
		self.listjson=[]
	def convert_json(self):
		return dict(id=self.id,trackId=self.trackId,albumId=self.albumId,title=self.title,playCount=self.playCount,duration=self.duration,url=self.url,path=self.path,result_one=self.result_one,result_two=self.result_two)
	@property
	def listjson(self):
		return self._listjson
	@listjson.setter
	def listjson(self,value):
		if not isinstance(value,tuple):
			raise ValueError('必须是list')
		self._listjson=value
	def convert_listjson(self):
		return [item.convert_json() for item in self.listjson]
	

# db.create_all()