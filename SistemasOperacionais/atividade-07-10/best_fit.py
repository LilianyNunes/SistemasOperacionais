from memoria import MEM_SIZE

def best_fit(pid, tamanho, memoria_obj):
    memoria = memoria_obj.memoria
    melhor_pos = None
    melhor_tam = MEM_SIZE + 1
    i = 0
    while i < MEM_SIZE:
        if memoria[i] == 0:
            j = i
            while j < MEM_SIZE and memoria[j] == 0:
                j += 1
            livre = j - i
            if tamanho <= livre < melhor_tam:
                melhor_tam = livre
                melhor_pos = i
            i = j
        else:
            i += 1
    if melhor_pos is not None:
        for j in range(tamanho):
            memoria[melhor_pos + j] = 1
        memoria_obj.processos_alocados[pid] = (melhor_pos, tamanho)
        print(f"[Best Fit] Processo {pid} alocado no bloco {melhor_pos}")
        return True
    print(f"[Best Fit] ERRO: Processo {pid} não coube.")
    return False
