# ------------------------------------------------------------
# Algoritmo 3 - Round Robin - (RR)
# ------------------------------------------------------------
def round_robin(processes, quantum=2, file_path="resultados.txt"):
    from collections import deque

    n = len(processes)
    procs = [
        {"id": p["id"], "arrival": p["arrival"], "burst": p["burst"],
         "remaining": p["burst"], "priority": p["priority"], "finish": 0}
        for p in processes
    ]

    time = 0
    queue = deque()
    order = []
    results = []
    completed = 0

    # Adiciona processos que chegam em t=0
    for p in procs:
        if p["arrival"] == 0:
            queue.append(p)

    while completed < n:
        if queue:
            current = queue.popleft()
            # Se o processo ainda não tinha começado, garantir que o tempo respeite chegada
            if time < current["arrival"]:
                time = current["arrival"]

            exec_time = min(quantum, current["remaining"])
            order.extend([current["id"]] * exec_time)  # guarda execução no timeline
            time += exec_time
            current["remaining"] -= exec_time

            # Adiciona novos processos que chegaram durante essa execução
            for p in procs:
                if p["arrival"] <= time and p["remaining"] > 0 and p not in queue and p != current:
                    queue.append(p)

            if current["remaining"] == 0:
                current["finish"] = time
                turnaround = current["finish"] - current["arrival"]
                waiting = turnaround - current["burst"]
                results.append({
                    "id": current["id"],
                    "arrival": current["arrival"],
                    "burst": current["burst"],
                    "finish": current["finish"],
                    "waiting": waiting,
                    "turnaround": turnaround,
                    "priority": current["priority"]
                })
                completed += 1
            else:
                queue.append(current)  # ainda tem tempo, volta pro fim da fila
        else:
            time += 1
            # adiciona processos que chegam nesse tempo
            for p in procs:
                if p["arrival"] <= time and p["remaining"] > 0 and p not in queue:
                    queue.append(p)

    avg_wait = sum(r["waiting"] for r in results) / n
    avg_turn = sum(r["turnaround"] for r in results) / n

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("Round Robin (Quantum = " + str(quantum) + ")\n")
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