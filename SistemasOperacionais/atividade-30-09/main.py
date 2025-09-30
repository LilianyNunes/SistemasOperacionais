from fcfs import fcfs
from round_robin import round_robin
from priority_non_preemptive import priority_non_preemptive

if __name__ == "__main__":
    processes = [
        {"id": "P1", "arrival": 0, "burst": 5, "priority": 2},
        {"id": "P2", "arrival": 2, "burst": 3, "priority": 1},
        {"id": "P3", "arrival": 4, "burst": 8, "priority": 3},
        {"id": "P4", "arrival": 5, "burst": 6, "priority": 2},
        {"id": "P5", "arrival": 11, "burst": 8, "priority": 1},
    ]

    # Limpa o arquivo antes de rodar
    with open("resultados.txt", "w", encoding="utf-8") as f:
        f.write("")

    fcfs(processes)
    round_robin(processes, quantum=2)
    priority_non_preemptive(processes)

    print("Resultados gravados em resultados.txt")
