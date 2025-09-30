import random
import os
from collections import deque

# ---------------------------------------------
# Algoritmo 1 - FCFS (First-Come, First-Served)
# ---------------------------------------------
def fcfs(processes, file_path="resultados.txt"):
    """
    Escalonamento FCFS: os processos são executados na ordem em que chegam.
    """
    procs = sorted([p.copy() for p in processes], key=lambda p: p["arrival"])
    current_time = 0
    order = []
    results = []

    for p in procs:
        start_time = max(current_time, p["arrival"])
        waiting_time = start_time - p["arrival"]
        finish_time = start_time + p["burst"]
        turnaround = finish_time - p["arrival"]

        results.append({
            "id": p["id"], "arrival": p["arrival"], "burst": p["burst"], "start": start_time,
            "finish": finish_time, "waiting": waiting_time, "turnaround": turnaround, "priority": p["priority"]
        })
        order.append(p["id"])
        current_time = finish_time

    avg_wait = sum(r["waiting"] for r in results) / len(results)
    avg_turn = sum(r["turnaround"] for r in results) / len(results)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("--- 1. FCFS (First-Come, First-Served) ---\n")
        f.write("Ordem de Execução: " + " -> ".join(order) + "\n\n")
        f.write(f"{'ID':<8}{'Chegada':<10}{'Burst':<8}{'Início':<8}{'Fim':<8}{'Espera':<8}{'Retorno':<10}{'Prior.':<8}\n")
        for r in results:
            f.write(f"{r['id']:<8}{r['arrival']:<10}{r['burst']:<8}{r['start']:<8}{r['finish']:<8}{r['waiting']:<8}{r['turnaround']:<10}{r['priority']:<8}\n")
        f.write(f"\nTempo Médio de Espera: {avg_wait:.2f}\n")
        f.write(f"Tempo Médio de Retorno: {avg_turn:.2f}\n")
        f.write("-" * 75 + "\n\n")

# ------------------------------------------------------------
# Algoritmo 2 - SJF (Shortest Job First - não-preemptivo)
# ------------------------------------------------------------
def sjf(processes, file_path="resultados.txt"):
    """
    Escalonamento SJF Não-Preemptivo: executa o processo mais curto entre os que já chegaram.
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
            
        current = min(available, key=lambda x: x["burst"])
        
        start_time = time
        finish_time = start_time + current["burst"]
        waiting_time = start_time - current["arrival"]
        turnaround = finish_time - current["arrival"]

        results.append({
            "id": current["id"], "arrival": current["arrival"], "burst": current["burst"], "start": start_time,
            "finish": finish_time, "waiting": waiting_time, "turnaround": turnaround, "priority": current["priority"]
        })
        
        order.append(current["id"])
        time = finish_time
        current["completed"] = True
        completed += 1
        
    avg_wait = sum(r["waiting"] for r in results) / n
    avg_turn = sum(r["turnaround"] for r in results) / n

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("--- 2. SJF (Shortest Job First - Não-Preemptivo) ---\n")
        f.write("Ordem de Execução: " + " -> ".join(order) + "\n\n")
        f.write(f"{'ID':<8}{'Chegada':<10}{'Burst':<8}{'Início':<8}{'Fim':<8}{'Espera':<8}{'Retorno':<10}{'Prior.':<8}\n")
        for r in sorted(results, key=lambda x: int(x["id"][1:])):
            f.write(f"{r['id']:<8}{r['arrival']:<10}{r['burst']:<8}{r['start']:<8}{r['finish']:<8}{r['waiting']:<8}{r['turnaround']:<10}{r['priority']:<8}\n")
        f.write(f"\nTempo Médio de Espera: {avg_wait:.2f}\n")
        f.write(f"Tempo Médio de Retorno: {avg_turn:.2f}\n")
        f.write("-" * 75 + "\n\n")

# ---------------------------------------------
# Algoritmo 3 - Round Robin (RR)
# ---------------------------------------------
def round_robin(processes, quantum, file_path="resultados.txt"):
    """
    Escalonamento Round Robin: cada processo recebe uma fatia de tempo (quantum).
    """
    n = len(processes)
    procs = [p.copy() for p in processes]
    for p in procs:
        p["remaining"] = p["burst"]
    
    time = 0
    completed = 0
    ready_queue = deque()
    timeline = []
    results = {}
    
    procs_to_arrive = sorted(procs, key=lambda p: p["arrival"])

    while completed < n:
        # Adiciona processos que chegaram na fila de prontos
        while procs_to_arrive and procs_to_arrive[0]["arrival"] <= time:
            ready_queue.append(procs_to_arrive.pop(0))

        if not ready_queue:
            time += 1
            continue

        current = ready_queue.popleft()
        
        if not timeline or timeline[-1] != current["id"]:
            timeline.append(current["id"])

        exec_time = min(quantum, current["remaining"])
        time += exec_time
        current["remaining"] -= exec_time

        # Adiciona processos que chegaram DURANTE a execução do quantum
        while procs_to_arrive and procs_to_arrive[0]["arrival"] <= time:
            ready_queue.append(procs_to_arrive.pop(0))
        
        if current["remaining"] > 0:
            ready_queue.append(current)
        else:
            completed += 1
            finish_time = time
            turnaround = finish_time - current["arrival"]
            waiting = turnaround - current["burst"]
            results[current["id"]] = {
                "id": current["id"], "arrival": current["arrival"], "burst": current["burst"],
                "finish": finish_time, "waiting": waiting, "turnaround": turnaround,
                "priority": current["priority"]
            }

    results_list = [results[key] for key in sorted(results.keys(), key=lambda x: int(x[1:]))]
    avg_wait = sum(r["waiting"] for r in results_list) / n
    avg_turn = sum(r["turnaround"] for r in results_list) / n
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"--- 3. Round Robin (RR) [Quantum={quantum}] ---\n")
        f.write("Linha do Tempo de Execução: " + " -> ".join(timeline) + "\n\n")
        f.write(f"{'ID':<8}{'Chegada':<10}{'Burst':<8}{'Fim':<8}{'Espera':<8}{'Retorno':<10}{'Prior.':<8}\n")
        for r in results_list:
            f.write(f"{r['id']:<8}{r['arrival']:<10}{r['burst']:<8}{r['finish']:<8}{r['waiting']:<8}{r['turnaround']:<10}{r['priority']:<8}\n")
        f.write(f"\nTempo Médio de Espera: {avg_wait:.2f}\n")
        f.write(f"Tempo Médio de Retorno: {avg_turn:.2f}\n")
        f.write("-" * 75 + "\n\n")


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

# ----------------------------------------------------------------------
# Algoritmo 5 - Prioridade com Múltiplas Filas (Preemptivo)
# ----------------------------------------------------------------------
def priority_multiple_queues(processes, quantum, file_path="resultados.txt"):
    """
    Múltiplas Filas de Prioridade: Filas separadas por prioridade. As de maior prioridade
    executam primeiro. Dentro de cada fila, usa-se Round Robin.
    """
    n = len(processes)
    procs = [p.copy() for p in processes]
    for p in procs:
        p["remaining"] = p["burst"]
    
    unique_priorities = sorted(list(set(p["priority"] for p in procs)))
    queues = {priority: deque() for priority in unique_priorities}
    
    time = 0
    completed = 0
    timeline = []
    results = {}
    procs_to_arrive = sorted(procs, key=lambda p: p["arrival"])

    while completed < n:
        # Adiciona processos que chegaram na fila de prioridade correta
        while procs_to_arrive and procs_to_arrive[0]["arrival"] <= time:
            proc = procs_to_arrive.pop(0)
            queues[proc["priority"]].append(proc)
            
        found_process = False
        for priority in unique_priorities:
            if queues[priority]:
                current = queues[priority].popleft()
                found_process = True
                break # Sai do loop de prioridades, pois encontrou o mais prioritário
        
        if not found_process:
            time += 1
            continue

        if not timeline or timeline[-1] != current["id"]:
            timeline.append(current["id"])
        
        exec_time = min(quantum, current["remaining"])
        time += exec_time
        current["remaining"] -= exec_time

        # Adiciona processos que chegaram DURANTE a execução
        while procs_to_arrive and procs_to_arrive[0]["arrival"] <= time:
            proc = procs_to_arrive.pop(0)
            queues[proc["priority"]].append(proc)
        
        if current["remaining"] > 0:
            queues[current["priority"]].append(current) # Devolve para sua própria fila
        else:
            completed += 1
            finish_time = time
            turnaround = finish_time - current["arrival"]
            waiting = turnaround - current["burst"]
            results[current["id"]] = {
                "id": current["id"], "arrival": current["arrival"], "burst": current["burst"],
                "finish": finish_time, "waiting": waiting, "turnaround": turnaround,
                "priority": current["priority"]
            }
            
    results_list = [results[key] for key in sorted(results.keys(), key=lambda x: int(x[1:]))]
    avg_wait = sum(r["waiting"] for r in results_list) / n
    avg_turn = sum(r["turnaround"] for r in results_list) / n
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"--- 5. Prioridade com Múltiplas Filas [Quantum={quantum}] ---\n")
        f.write("Linha do Tempo de Execução: " + " -> ".join(timeline) + "\n\n")
        f.write(f"{'ID':<8}{'Chegada':<10}{'Burst':<8}{'Fim':<8}{'Espera':<8}{'Retorno':<10}{'Prior.':<8}\n")
        for r in results_list:
            f.write(f"{r['id']:<8}{r['arrival']:<10}{r['burst']:<8}{r['finish']:<8}{r['waiting']:<8}{r['turnaround']:<10}{r['priority']:<8}\n")
        f.write(f"\nTempo Médio de Espera: {avg_wait:.2f}\n")
        f.write(f"Tempo Médio de Retorno: {avg_turn:.2f}\n")
        f.write("-" * 75 + "\n\n")

# ----------------------------------------------------------------------
# Algoritmo 6 - Loteria (não-preemptivo)
# ----------------------------------------------------------------------
def lottery_scheduling(processes, file_path="resultados.txt"):
    """
    Escalonamento por Loteria: um processo é sorteado para execução com base
    no número de 'bilhetes' que possui.
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

        total_tickets = sum(p["tickets"] for p in available)
        
        if total_tickets == 0:
            current = random.choice(available)
        else:
            ticket_draw = random.randint(1, total_tickets)
            counter = 0
            for p in available:
                counter += p["tickets"]
                if ticket_draw <= counter:
                    current = p
                    break
        
        start_time = time
        finish_time = start_time + current["burst"]
        waiting = start_time - current["arrival"]
        turnaround = finish_time - current["arrival"]

        results.append({
            "id": current["id"], "arrival": current["arrival"], "burst": current["burst"],
            "finish": finish_time, "waiting": waiting, "turnaround": turnaround,
            "priority": current["priority"], "start": start_time, "tickets": current["tickets"]
        })

        order.append(current["id"])
        time = finish_time
        current["completed"] = True
        completed += 1

    avg_wait = sum(r["waiting"] for r in results) / n
    avg_turn = sum(r["turnaround"] for r in results) / n

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("--- 6. Escalonamento por Loteria (Não-Preemptivo) ---\n")
        f.write("Ordem de Execução: " + " -> ".join(order) + "\n\n")
        f.write(f"{'ID':<8}{'Chegada':<10}{'Burst':<8}{'Início':<8}{'Fim':<8}{'Espera':<8}{'Retorno':<10}{'Tickets':<8}\n")
        for r in sorted(results, key=lambda x: int(x["id"][1:])):
            f.write(f"{r['id']:<8}{r['arrival']:<10}{r['burst']:<8}{r['start']:<8}{r['finish']:<8}{r['waiting']:<8}{r['turnaround']:<10}{r['tickets']:<8}\n")
        f.write(f"\nTempo Médio de Espera: {avg_wait:.2f}\n")
        f.write(f"Tempo Médio de Retorno: {avg_turn:.2f}\n")
        f.write("-" * 75 + "\n\n")


# -----------------------------
# Programa Principal
# -----------------------------
if __name__ == "__main__":
    # Processos de exemplo
    process_list = [
        {"id": "P1", "arrival": 0, "burst": 8, "priority": 3, "tickets": 20},
        {"id": "P2", "arrival": 1, "burst": 4, "priority": 1, "tickets": 80}, # Maior prioridade
        {"id": "P3", "arrival": 2, "burst": 9, "priority": 4, "tickets": 10}, # Menor prioridade
        {"id": "P4", "arrival": 3, "burst": 5, "priority": 2, "tickets": 40},
    ]
    
    # Quantum para os algoritmos preemptivos
    QUANTUM = 3
    
    output_file = "resultados.txt"

    # Limpa o arquivo de resultados antes de executar
    if os.path.exists(output_file):
        os.remove(output_file)
    
    print(f"Executando simulação de escalonamento...")
    print(f"Os resultados serão salvos em '{output_file}'")

    # Chamada dos 6 algoritmos
    fcfs(process_list, output_file)
    sjf(process_list, output_file)
    round_robin(process_list, QUANTUM, output_file)
    priority_scheduling(process_list, output_file)
    priority_multiple_queues(process_list, QUANTUM, output_file)
    lottery_scheduling(process_list, output_file)

    print("Simulação concluída com sucesso! ✅")