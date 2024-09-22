from Classes.Puzzle import PuzzleNumber
from Classes.Ranger import Rangers
from Classes.Addresses import Addresses_get
from Classes.Help import Helps
import sys
class Menus(PuzzleNumber,Addresses_get):
	def __init__(self):
		self.__option = None#privada
		self.Start = None
		self.End = None
		self.Address = None
		self.__puzzle = None#privada
		PuzzleNumber.__init__(self)
		Addresses_get.__init__(self)
	def __Input(self):# método privado
		try:
			self.__option = int(input("Informe o número do desafio:"))
			
			if self.__option == 0:
				help = Helps()
				help.ShowAddress()
				return "Informe o núnmero do desafio deseja buscar a chave. O desafio '20' já foi encontrado!"
			
			if self.Exists(self.__option) is not None:
				r = Rangers(self.__option)
				self.Start, self.End= r.getRangers()
				self.Address = self.getAddress(self.__option)
			else:
					return f"[!] Puzzle já solucionado ou inexistente!"
					
		except ValueError as error:
			return str(error)
		return self.Start,	self.End,	self.Address
	def getResponse(self):
		return self.__Input()
				
				
				
			
