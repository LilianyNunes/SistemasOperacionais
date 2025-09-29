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
        f.write("FCFS (First-Come, First-Served)\n")
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


# ------------------------------------------------------------
# Algoritmo 3 - SRTF (Shortest Remaining Time First - preemptivo)
# ------------------------------------------------------------
def srtf(processes, file_path="resultados.txt"):
    n = len(processes)
    # Faz uma cópia da lista com "remaining" (tempo restante)
    procs = [
        {"id": p["id"], "arrival": p["arrival"], "burst": p["burst"],
         "remaining": p["burst"], "priority": p["priority"]}
        for p in processes
    ]

    time = 0
    completed = 0
    order = []    # ordem de execução segundo a linha do tempo
    results = []

    while completed < n:
        # Seleciona todos os processos já chegados
        available = [p for p in procs if p["arrival"] <= time and p["remaining"] > 0]
        if available:
            # Escolhe o que tem menor tempo restante
            current = min(available, key=lambda x: x["remaining"])
            order.append(current["id"])   # adiciona à ordem de execução
            current["remaining"] -= 1     # executa 1 unidade de tempo
            time += 1

            # Se terminou, calcula tempos
            if current["remaining"] == 0:
                completed += 1
                finish_time = time
                turnaround = finish_time - current["arrival"]
                waiting = turnaround - current["burst"]
                results.append({
                    "id": current["id"],
                    "arrival": current["arrival"],
                    "burst": current["burst"],
                    "finish": finish_time,
                    "waiting": waiting,
                    "turnaround": turnaround,
                    "priority": current["priority"]
                })
        else:
            time += 1  # CPU ociosa, avança tempo

    # Calcula as médias
    avg_wait = sum(r["waiting"] for r in results) / n
    avg_turn = sum(r["turnaround"] for r in results) / n

    # Escreve no arquivo de saída
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("SRTF (Shortest Remaining Time First)\n")
        f.write("Ordem de Execução (linha do tempo): " + " -> ".join(order) + "\n\n")
        f.write(f"{'Processo':<10}{'Chegada':<10}{'Burst':<8}{'Fim':<8}"
                f"{'Espera':<8}{'Retorno':<10}{'Prior.':<8}\n")
        for r in sorted(results, key=lambda x: x["id"]):
            f.write(f"{r['id']:<10}{r['arrival']:<10}{r['burst']:<8}{r['finish']:<8}"
                    f"{r['waiting']:<8}{r['turnaround']:<10}{r['priority']:<8}\n")
        f.write(f"\nTempo Médio de Espera: {avg_wait:.2f}\n")
        f.write(f"Tempo Médio de Retorno: {avg_turn:.2f}\n")
        f.write("-------\n\n")

    return results, avg_wait, avg_turn


# ----------------------------------------------------------------------
# Algoritmo 5 - Prioridade (não-preemptiva) - também chamado Multiple Queues
# ----------------------------------------------------------------------
def priority_non_preemptive(processes, file_path="resultados.txt"):
    n = len(processes)
    procs = [
        {"id": p["id"], "arrival": p["arrival"], "burst": p["burst"],
         "priority": p["priority"]}
        for p in processes
    ]

    time = 0
    completed = 0
    order = []
    results = []
    ready_queue = []

    while completed < n:
        # Adiciona processos que chegaram à fila de prontos
        for p in procs:
            if p["arrival"] <= time and "added" not in p:
                ready_queue.append(p)
                p["added"] = True

        if ready_queue:
            # Escolhe o processo com maior prioridade (menor número)
            current = min(ready_queue, key=lambda x: x["priority"])
            ready_queue.remove(current)

            # Calcula início, fim, espera e retorno
            start_time = max(time, current["arrival"])
            finish_time = start_time + current["burst"]
            waiting = start_time - current["arrival"]
            turnaround = finish_time - current["arrival"]

            results.append({
                "id": current["id"],
                "arrival": current["arrival"],
                "burst": current["burst"],
                "finish": finish_time,
                "waiting": waiting,
                "turnaround": turnaround,
                "priority": current["priority"]
            })

            order.append(current["id"])
            time = finish_time
            completed += 1
        else:
            time += 1  # CPU ociosa

    avg_wait = sum(r["waiting"] for r in results) / n
    avg_turn = sum(r["turnaround"] for r in results) / n

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("Prioridade (Não-Preemptiva)\n")
        f.write("Ordem de Execução: " + " -> ".join(order) + "\n\n")
        f.write(f"{'Processo':<10}{'Chegada':<10}{'Burst':<8}{'Fim':<8}"
                f"{'Espera':<8}{'Retorno':<10}{'Prior.':<8}\n")
        for r in sorted(results, key=lambda x: x["id"]):
            f.write(f"{r['id']:<10}{r['arrival']:<10}{r['burst']:<8}{r['finish']:<8}"
                    f"{r['waiting']:<8}{r['turnaround']:<10}{r['priority']:<8}\n")
        f.write(f"\nTempo Médio de Espera: {avg_wait:.2f}\n")
        f.write(f"Tempo Médio de Retorno: {avg_turn:.2f}\n")
        f.write("-------\n\n")

    return results, avg_wait, avg_turn


# -----------------------------
# Programa principal de teste
# -----------------------------
if __name__ == "__main__":
    # Processos de exemplo
    process_list = [
        {"id": "P1", "arrival": 0,  "burst": 5, "priority": 2},
        {"id": "P2", "arrival": 2,  "burst": 3, "priority": 1},
        {"id": "P3", "arrival": 4,  "burst": 8, "priority": 3},
        {"id": "P4", "arrival": 5,  "burst": 6, "priority": 2},
        {"id": "P5", "arrival": 11, "burst": 8, "priority": 1},
    ]

    # Cada função escreve no mesmo arquivo resultados.txt
    fcfs(process_list)
    srtf(process_list)
    priority_non_preemptive(process_list)

    print("Resultados dos algoritmos 1, 3 e 5 gravados em resultados.txt")
