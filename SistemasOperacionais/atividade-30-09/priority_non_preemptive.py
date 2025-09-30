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
