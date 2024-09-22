from Classes.Addresses import Addresses_get
class PuzzleNumber(Addresses_get):
	def __init__(self):
		
		
		Addresses_get.__init__(self)
	def Exists(self,i):
		return self.getIndex(i)
		
	def getPuzzleNumbers(self,index_a):
		return self.getIndex(index_a)
