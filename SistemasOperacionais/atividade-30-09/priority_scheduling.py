# ----------------------------------------------------------------------
# Algoritmo 4 - Prioridade (não-preemptiva)
# ----------------------------------------------------------------------
def priority_scheduling(processes, file_path="resultados.txt"):
    """
    Escalonamento por Prioridade Não-Preemptivo: executa o processo de maior prioridade
    (menor número) entre os que já chegaram.
    """
    n = len(processes)
    procs = [p.copy() for p in processes]
    time = 0
    completed = 0
    order = []
    results = []

    while completed < n:
        available = [p for p in procs if p["arrival"] <= time and "completed" not in p]
        
        if not available:
            time += 1
            continue

        current = min(available, key=lambda x: x["priority"])

        start_time = time
        finish_time = start_time + current["burst"]
        waiting = start_time - current["arrival"]
        turnaround = finish_time - current["arrival"]

        results.append({
            "id": current["id"], "arrival": current["arrival"], "burst": current["burst"],
            "finish": finish_time, "waiting": waiting, "turnaround": turnaround,
            "priority": current["priority"], "start": start_time
        })

        order.append(current["id"])
        time = finish_time
        current["completed"] = True
        completed += 1

    avg_wait = sum(r["waiting"] for r in results) / n
    avg_turn = sum(r["turnaround"] for r in results) / n

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("--- 4. Escalonamento por Prioridade (Não-Preemptivo) ---\n")
        f.write("Ordem de Execução: " + " -> ".join(order) + "\n\n")
        f.write(f"{'ID':<8}{'Chegada':<10}{'Burst':<8}{'Início':<8}{'Fim':<8}{'Espera':<8}{'Retorno':<10}{'Prior.':<8}\n")
        for r in sorted(results, key=lambda x: int(x["id"][1:])):
             f.write(f"{r['id']:<8}{r['arrival']:<10}{r['burst']:<8}{r['start']:<8}{r['finish']:<8}{r['waiting']:<8}{r['turnaround']:<10}{r['priority']:<8}\n")
        f.write(f"\nTempo Médio de Espera: {avg_wait:.2f}\n")
        f.write(f"Tempo Médio de Retorno: {avg_turn:.2f}\n")
        f.write("-" * 75 + "\n\n")