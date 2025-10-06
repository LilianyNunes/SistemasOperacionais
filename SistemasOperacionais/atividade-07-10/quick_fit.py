from first_fit import first_fit
from best_fit import best_fit

def quick_fit(pid, tamanho, memoria_obj):
    tamanhos_comuns = [2, 4, 8]
    if tamanho in tamanhos_comuns:
        return best_fit(pid, tamanho, memoria_obj)
    else:
        return first_fit(pid, tamanho, memoria_obj)
