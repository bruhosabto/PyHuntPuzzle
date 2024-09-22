#--bruno santos
#--20 de set 2024

from Classes.Menu import Menus
from Classes.Terminal import CursorTerminal
from Classes.Finder import FinderMath
import multiprocessing
import sys
import time
import signal


L = CursorTerminal()
l=L.getLinha()#apenas fiquei com preguiça
# Função que será executada em paralelo para mostrar senhas por segundo
def monitor_progress(counter):
    start_time = time.time()
    while True:
        time.sleep(5)  # A cada 5 segundos
        elapsed_time = time.time() - start_time
        passwords_per_second = round(counter.value / elapsed_time)
        print(f"\33[{l+15}HSenhas testadas: {counter.value} | Senhas por segundo: {passwords_per_second:.2f}")

# Função que será executada em cada processo de busca
def handle_interrupt(signal_num, frame):
    sys.exit(0)
def process_search(find, counter,found):
    find.Proccess_key_search_address(counter,found)
    
    with counter.get_lock():  # Usa lock para evitar condições de corrida
        counter.value += 1  # Incrementa o contador a cada senha testada

if __name__ == "__main__":
    terminal = CursorTerminal()
    print("Digite '0' para visualizar os valores e endereços!")
    menu = Menus()
    try:
        response = menu.getResponse()
        
        if isinstance(response, tuple) and len(response) == 3:
            start, end, address = response
        else:
            print(response)
            sys.exit()
    except ValueError as error:
        print(error)
        sys.exit()
    print("----------------------------------------------------------------------------")
    print(f"start:{start} end:{end}\naddress:{address}")
    print("----------------------------------------------------------------------------")
    find = FinderMath(start, end, address, terminal.getLinha())
    signal.signal(signal.SIGINT,handle_interrupt)
    # Inicializa um contador compartilhado entre os processos
    counter = multiprocessing.Value('i', 0)  # 'i' indica que é um inteiro
    found = multiprocessing.Event()
    num_processes = multiprocessing.cpu_count()
    processes = []

    # Inicia o processo que monitora o progresso
    monitor_process = multiprocessing.Process(target=monitor_progress, args=(counter,))
    monitor_process.start()
    #process_search(find,counter)
    # Inicia os processos de busca
    
    for _ in range(num_processes):
        p = multiprocessing.Process(target=process_search, args=(find, counter,found))
        processes.append(p)
        p.start()
    
    # Espera todos os processos de busca finalizarem
    for p in processes:
        p.join()

    # Termina o processo de monitoramento
    monitor_process.terminate()

