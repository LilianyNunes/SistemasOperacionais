from memoria import MEM_SIZE

def worst_fit(pid, tamanho, memoria_obj):
    memoria = memoria_obj.memoria
    pior_pos = None
    pior_tam = -1
    i = 0
    while i < MEM_SIZE:
        if memoria[i] == 0:
            j = i
            while j < MEM_SIZE and memoria[j] == 0:
                j += 1
            livre = j - i
            if tamanho <= livre > pior_tam:
                pior_tam = livre
                pior_pos = i
            i = j
        else:
            i += 1
    if pior_pos is not None:
        for j in range(tamanho):
            memoria[pior_pos + j] = 1
        memoria_obj.processos_alocados[pid] = (pior_pos, tamanho)
        print(f"[Worst Fit] Processo {pid} alocado no bloco {pior_pos}")
        return True
    print(f"[Worst Fit] ERRO: Processo {pid} não coube.")
    return False
