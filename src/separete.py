import sys

def abrir(arquivo):
	try:
		with open(arquivo,'r') as endereco:
			linhas=endereco.readlines()
		contador=67
		for linha in linhas:
			linha=linha.strip()#remove a quebra de linha
			if contador % 5 == 0: # pula os multiplos de 5
			   contador+=1
			with open(f'{contador}'.txt','a') as endereco_arquivo:
				endereco_arquivo.write(f'{linha}')
		print("[+] Todos os arquivos foram salvos!")
		return True
	except ValueError as error:
		return f"{str(error)}")

arquivo="unsolvedpuzzle.txt"
