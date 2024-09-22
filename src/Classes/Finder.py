import hashlib
import base58
from ecdsa import SECP256k1, SigningKey
import random
import multiprocessing
from queue import Queue


class FinderMath:
    def __init__(self, start, end, address, linha):
        self.__Start = int(start, 16)
        self.__End = int(end, 16)
        self.__Alvo = address
        self.__Linha = linha
        self.__private_key = None
        #self.__hex_key = None
        #self.__Fila = Queue()
    
    def __generate_private_key(self):
        
        self.__private_key = random.randint(self.__Start, self.__End)
        private_key_hex = format(self.__private_key, '064x')  # Formatar para hexadecimal com 64 caracteres
        return private_key_hex
    
    def __sha256d(self, data):
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()
    
    def __hex_key_to_address(self, hex_key):
        private_key_hex = hex_key

        # Converter a chave privada de hexadecimal para bytes
        private_key_bytes = bytes.fromhex(private_key_hex)

        # Geração da chave pública comprimida usando secp256k1
        private_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
        public_key = private_key.verifying_key

        # Gera a chave pública comprimida (33 bytes, com prefixo 0x02 ou 0x03)
        public_key_compressed = b'\x02' + public_key.to_string()[:32] if public_key.pubkey.point.y() % 2 == 0 else b'\x03' + public_key.to_string()[:32]

        # Aplicar SHA-256 na chave pública comprimida
        sha256_public_key = hashlib.sha256(public_key_compressed).digest()

        # Aplicar RIPEMD-160 no resultado do SHA-256
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_public_key)
        public_key_hash = ripemd160.digest()

        # Adicionar prefixo 0x00 para mainnet
        public_key_hash_mainnet = b'\x00' + public_key_hash

        # Calcular checksum
        checksum_public_key = self.__sha256d(public_key_hash_mainnet)[:4]

        # Concatenar o hash público com o checksum
        bitcoin_address_bytes = public_key_hash_mainnet + checksum_public_key

        # Converter o endereço Bitcoin para base58
        bitcoin_address = base58.b58encode(bitcoin_address_bytes)
        return bitcoin_address.decode()
    def Proccess_key_search_address(self,contador,found):
        
        while not found.is_set():
            hex_key = self.__generate_private_key()
            address = self.__hex_key_to_address(hex_key)
            #print(f"\33[{self.__Linha+4}HAdress:{address} Key: {hex_key}")
            with contador.get_lock():
                contador.value+=1
            if address.startswith(self.__Alvo[:3]):
                print(f"\33[{self.__Linha}HComeçando com:{self.__Alvo[:3]}\nAddress:{address}\nKey: {hex_key}")
            if address.startswith(self.__Alvo[:4]):
                print(f"\33[{self.__Linha+3}HComeçando com:{self.__Alvo[:4]}\nAddress:{address}\nKey: {hex_key}")
            else:
                continue
            if address == self.__Alvo:
                print(f"KEY FOUND!")
                print(f"Encontrado address: {address} key: {hex_key}")
                with open('keyfound.txt', 'a') as abrir:
                    abrir.write(f"key: {hex_key} address: {address}\n")
                found.set()
                break
				
            
