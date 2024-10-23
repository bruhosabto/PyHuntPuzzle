import hashlib
import base58
from ecdsa import SECP256k1, SigningKey
import random
import multiprocessing
from queue import Queue

import os

class FinderMath:
    def __init__(self, start, end, address, linha):
        self.__Start = int(start, 16)
        self.__End = int(end, 16)
        self.__Alvo = address
        self.__Linha = linha
        self.__private_key = None
        self.__private_key_hex_show = None
    def base58_encode(self,b):
        """Codifica bytes em Base58."""
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        num = int.from_bytes(b, 'big')
        encode = ''
        
        while num > 0:
            num, remainder = divmod(num, 58)
            encode = alphabet[remainder] + encode

        # Adiciona zeros à esquerda
        n_zeros = len([byte for byte in b if byte == 0])
        encode = alphabet[0] * n_zeros + encode

        return encode
    def private_key_to_wif(self,hex_private_key):
        """Converte uma chave privada hexadecimal para WIF comprimido."""
        # Passo 1: Converte a chave privada hexadecimal em bytes
        private_key_bytes = bytes.fromhex(hex_private_key)

        # Passo 2: Adiciona prefixo (0x80)
        prefixed_key = b'\x80' + private_key_bytes

        # Passo 3: Adiciona sufixo para a versão comprimida (0x01)
        compressed_key = prefixed_key + b'\x01'

        # Passo 4: Calcula o checksum usando SHA-256 duas vezes
        sha_hash = self.__sha256d(compressed_key)
        checksum = self.__sha256d(sha_hash)[:4]

        # Passo 5: Concatena a chave com o checksum
        wif_bytes = compressed_key + checksum

        # Passo 6: Codifica em Base58
        wif = self.base58_encode(wif_bytes)

        return wif[len("111111111111111111111111111111"):]
    def __generate_private_key(self):
        # Calcular a quantidade de bits necessária para cobrir o intervalo
        num_bits = self.__End.bit_length()
        
        # Gera um número aleatório de bits e aplica uma máscara para garantir que esteja no intervalo
        self.__private_key = random.getrandbits(num_bits) % (self.__End - self.__Start + 1) + self.__Start
        
        # Mostrar a chave privada em hexadecimal
        self.__private_key_hex_show = hex(self.__private_key)
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
            if address.startswith(self.__Alvo[:4]):
                print(f"\33[{self.__Linha}HComeçando com:{self.__Alvo[:4]}\nAddress: {address}\nBase Key: {hex_key}")
            if address.startswith(self.__Alvo[:5]):
                print(f"\33[{self.__Linha+3}HComeçando com:{self.__Alvo[:5]}\nAddress:{address}\nBase Key: {self.__private_key_hex_show}")
            else:
                continue
            if address == self.__Alvo:
                print(f"KEY FOUND!")
                wif=self.private_key_to_wif(hex_key)
                print(f"Encontrado address: {address}\nkey: {hex_key}\nwif:{wif}")
                with open('keyfound.txt', 'a') as abrir:
                    abrir.write(f"key: {hex_key} address: {address}\nwif:{wif}\n")
                found.set()
                break
				
            
