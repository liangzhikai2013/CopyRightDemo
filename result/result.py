class Result(object):
	"""返回类基类"""
	def __init__(self,code,data,msg):
		self.code=code
		self.data=data
		self.msg=msg
		self.token=None
	@property
	def token(self):
		if self._token:
			return self._token
		else:
			return None
	@token.setter
	def token(self,value):
		if value:
			self._token=value
		else:
			self._token=None
	def convert_json(self):
		return dict(code=self.code,data=self.data,msg=self.msg,token=self.token)
class ResultData(Result):
	"""分页结果类"""
	def __init__(self,code,data,msg,PageIndex,PageSize,TotoalCount):
		Result.__init__(self,code,data,msg)
		self.PageIndex=PageIndex
		self.PageSize=PageSize
		self.TotoalCount=TotoalCount
	@property
	def token(self):
		if self._token:
			return self._token
		else:
			return None
	@token.setter
	def token(self,value):
		if value:
			self._token=value
		else:
			self._token=None
	def convert_json(self):
		return dict(code=self.code,data=self.data,msg=self.msg,PageIndex=self.PageIndex,PageSize=self.PageSize,TotoalCount=self.TotoalCount,token=self.token)

		