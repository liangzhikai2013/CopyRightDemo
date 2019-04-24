from models.model import *
class BaseDAL:
	"""基础数据操作类"""
	
	def __init__(self,entity):
		self.entity=entity
	
	def Search(self):
		result=db.session.query(self.entity).all()
		if result:
			return result
		else:
			return None
	def Insert(self):
		db.session.add(self.entity)
		result=db.session.commit()
		if result:
			return True
		else:
			return False


class BookDAL(BaseDAL):
	"""书籍数据操作类"""
	@property
	def id(self):
		return self._id
	@id.setter
	def id(self,value):
		if not isinstance(value,int):
			raise ValueError('id为数字')
		self._id=value
	@property
	def bookid(self):
		return self._bookid
	@bookid.setter
	def bookid(self,value):
		if not isinstance(value,int):
			raise ValueError("bookid为数字")
		self._bookid=value
	@property
	def BookTitle(self):
		return self._BookTitle
	@BookTitle.setter
	def BookTitle(self,value):
		if value:
			self._BookTitle=value
		else:
			self._BookTitle=None
	def __init__(self,entity):
		BaseDAL.__init__(self,entity)

	def SearchBookById(self):
		result=db.session.query(self.entity).filter(self.entity.bookid==self.bookid).first()
		return result

class AudioDAL(BaseDAL):
	"""docstring for Audio"""
	@property
	def id(self):
		return self._id
	@id.setter
	def id(self,value):
		if not isinstance(value,int):
			raise ValueError('id为数字')
		self._id=value
	@property
	def albumId(self):
		return self._albumId
	@albumId.setter
	def albumId(self,value):
		if not isinstance(value,int):
			raise ValueError('albumId为数字')
		self.albumId=value
	@property
	def path(self):
		return self._path
	@path.setter
	def path(self,value):
		if value:
			self._path=value
		else:
			self._path=None
	def __init__(self, arg):
		super(Audio, self).__init__()
		self.arg = arg
	@property
	def AudioTitle(self):
		return self._AudioTitle
	@AudioTitle.setter
	def AudioTitle(self,value):
		if value:
			self._AudioTitle=value
		else:
			self._AudioTitle=None
		


	

		





		