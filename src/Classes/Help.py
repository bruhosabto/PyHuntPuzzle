from Classes.Puzzle import PuzzleNumber
from Classes.Addresses import Addresses_get
class Helps(PuzzleNumber):
    def __init__(self):
        PuzzleNumber.__init__(self)
        Addresses_get.__init__(self)
    def ShowAddress(self):
        listaNumeros = self.getListaDesafio()
        for i in listaNumeros:
            print(f"Desafio:{i} Endereço:{self.getAddress(i)}")
