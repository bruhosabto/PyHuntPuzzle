Libs necessárias:
--------------------------------
import hashlib
import base58
from ecdsa import SECP256k1, SigningKey
import random
import multiprocessing
import termios
import tty
---------------xxxxxxxxxxxx--------------
HÁ PEQUENOS BUGS NO DESAFIO 1, 4 E 10. Possivelment devido a random ter dificuldade em trabalhar no ranger dado.
-------------------------------------------------------------------------------------
Analise!!!!
------
A random.randint, fica lenta com ranges grandes, estou buscando alternativas para essa lib, caso não encontre, talvez tenha de fazer de outra maneira, manualmente se eu TIVER TEMPO.
No mais, testei aí
-------------------
SpeedTop: 5000 k/s. Atual.
