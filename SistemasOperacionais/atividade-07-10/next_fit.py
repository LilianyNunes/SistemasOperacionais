from memoria import MEM_SIZE

def next_fit(pid, tamanho, memoria_obj, start_index=[0]):
    memoria = memoria_obj.memoria
    n = MEM_SIZE
    i = start_index[0]
    count = 0
    while count < n:
        if i + tamanho <= n and all(memoria[i + j] == 0 for j in range(tamanho)):
            for j in range(tamanho):
                memoria[i + j] = 1
            memoria_obj.processos_alocados[pid] = (i, tamanho)
            start_index[0] = i + tamanho
            print(f"[Next Fit] Processo {pid} alocado no bloco {i}")
            return True
        i = (i + 1) % n
        count += 1
    print(f"[Next Fit] ERRO: Processo {pid} não coube.")
    return False
