# ---------------------------------------------
# Algoritmo 1 - FCFS (First Come, First Served)
# ---------------------------------------------
def fcfs(processes, file_path="resultados.txt"):
    # Ordena os processos pelo tempo de chegada
    procs = sorted(processes, key=lambda p: p["arrival"])
    current_time = 0
    order = []    # ordem de execução dos processos
    results = []  # guarda os cálculos de cada processo

    for p in procs:
        # O processo começa quando o processador está livre
        start_time = max(current_time, p["arrival"])
        # Tempo de espera = início - chegada
        waiting_time = start_time - p["arrival"]
        # Fim = início + burst
        finish_time = start_time + p["burst"]
        # Tempo de retorno = fim - chegada
        turnaround = finish_time - p["arrival"]

        # Guarda os resultados desse processo
        results.append({
            "id": p["id"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "start": start_time,
            "finish": finish_time,
            "waiting": waiting_time,
            "turnaround": turnaround,
            "priority": p["priority"]
        })
        order.append(p["id"])
        current_time = finish_time  # CPU vai estar ocupada até o fim

    # Calcula as médias
    avg_wait = sum(r["waiting"] for r in results) / len(results)
    avg_turn = sum(r["turnaround"] for r in results) / len(results)

    # Escreve no arquivo de saída
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("--- 1 .FCFS (First-Come, First-Served) ---\n")
        f.write("Ordem de Execução: " + " -> ".join(order) + "\n\n")
        f.write(f"{'Processo':<10}{'Chegada':<10}{'Burst':<8}{'Início':<8}{'Fim':<8}"
                f"{'Espera':<8}{'Retorno':<10}{'Prior.':<8}\n")
        for r in results:
            f.write(f"{r['id']:<10}{r['arrival']:<10}{r['burst']:<8}{r['start']:<8}"
                    f"{r['finish']:<8}{r['waiting']:<8}{r['turnaround']:<10}{r['priority']:<8}\n")
        f.write(f"\nTempo Médio de Espera: {avg_wait:.2f}\n")
        f.write(f"Tempo Médio de Retorno: {avg_turn:.2f}\n")
        f.write("-------\n\n")

    return results, avg_wait, avg_turn