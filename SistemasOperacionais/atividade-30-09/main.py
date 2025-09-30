from fcfs import fcfs
from sjf import sjf
from round_robin import round_robin
from priority_non_preemptive import priority_non_preemptive
from priority_scheduling import priority_scheduling
from lotterry_schedueling import lottery_scheduling

if __name__ == "__main__":
    processes = [
    {"id": "P1", "arrival": 0, "burst": 5, "priority": 2, "tickets": 10},
    {"id": "P2", "arrival": 2, "burst": 3, "priority": 1, "tickets": 20},
    {"id": "P3", "arrival": 4, "burst": 8, "priority": 3, "tickets": 5},
    {"id": "P4", "arrival": 5, "burst": 6, "priority": 2, "tickets": 15},
    {"id": "P5", "arrival": 11, "burst": 8, "priority": 1, "tickets": 25},
]

    # Limpa o arquivo antes de rodar
    with open("resultados.txt", "w", encoding="utf-8") as f:
        f.write("")

    # Executa todos os algoritmos
    fcfs(processes)
    sjf(processes)
    round_robin(processes, quantum=2)
    priority_scheduling(processes)
    priority_non_preemptive(processes)
    lottery_scheduling(processes)

    print("Resultados gravados em resultados.txt")
