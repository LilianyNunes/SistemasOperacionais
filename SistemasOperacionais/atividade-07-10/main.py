import random
from datetime import datetime
from memoria import Memoria
from first_fit import first_fit
from next_fit import next_fit
from best_fit import best_fit
from worst_fit import worst_fit
from quick_fit import quick_fit

# ------------------------------
# Dicionário de processos
# ------------------------------
processos = {
    "P1": 5, "P2": 4, "P3": 2, "P4": 5, "P5": 8,
    "P6": 3, "P7": 5, "P8": 8, "P9": 2, "P10": 6
}

# ------------------------------
# Função de simulação
# ------------------------------
def simular(algoritmo, nome):
    memoria = Memoria()
    log = []

    log.append(f"\n{'='*30}")
    log.append(f"SIMULAÇÃO: {nome}")
    log.append(f"{'='*30}\n")

    for passo in range(30):  # 30 operações
        pid = random.choice(list(processos.keys()))
        if pid in memoria.processos_alocados:
            memoria.desalocar(pid)
            log.append(f"PASSO {passo+1}: Processo {pid} desalocado.")
        else:
            algoritmo(pid, processos[pid], memoria)
            log.append(f"PASSO {passo+1}: Processo {pid} tentou alocar {processos[pid]} blocos.")

        estado = "".join(str(x) for x in memoria.memoria)
        log.append(f"Estado da memória: {estado}")

    # Fragmentação externa
    menor_processo = min(processos.values())
    frag = memoria.calcular_fragmentacao(menor_processo)
    log.append(f"\nFragmentação externa (blocos inutilizáveis): {frag}")
    log.append(f"{'='*30}\n")

    return "\n".join(log)

# ------------------------------
# Execução principal
# ------------------------------
if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"relatorio_geral_{timestamp}.txt"

    resultados = []
    resultados.append(simular(first_fit, "FIRST FIT"))
    resultados.append(simular(next_fit, "NEXT FIT"))
    resultados.append(simular(best_fit, "BEST FIT"))
    resultados.append(simular(worst_fit, "WORST FIT"))
    resultados.append(simular(quick_fit, "QUICK FIT"))

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n\n".join(resultados))

    print(f"Relatório geral salvo como '{filename}'")
    print("Contém todas as simulações com fragmentação externa e mapa de memória.\n")
