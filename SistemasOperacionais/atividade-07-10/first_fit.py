from memoria import MEM_SIZE

def first_fit(pid, tamanho, memoria_obj):
    memoria = memoria_obj.memoria
    for i in range(MEM_SIZE - tamanho + 1):
        if all(memoria[i + j] == 0 for j in range(tamanho)):
            for j in range(tamanho):
                memoria[i + j] = 1
            memoria_obj.processos_alocados[pid] = (i, tamanho)
            print(f"[First Fit] Processo {pid} alocado no bloco {i}")
            return True
    print(f"[First Fit] ERRO: Processo {pid} não coube.")
    return False
