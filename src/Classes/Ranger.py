
class Rangers():
	def __init__(self,index):
		self.__Index = index
	def __RangerStart(self):
		return hex(2**(self.__Index-1))[2:]
	def __RangerEnd(self):
		return hex(2**(self.__Index))[2:]
	def getRangers(self):
		return self.__RangerStart(),self.__RangerEnd()
