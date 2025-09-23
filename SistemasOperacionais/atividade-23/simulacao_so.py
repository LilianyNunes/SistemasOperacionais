# "A transição de processos entre os estados Pronto, Executando e Bloqueado."
# "A Troca de Contexto, que ocorre quando um processo cede a CPU para outro."
# "O tratamento de operações de Entrada e Saída (E/S), que fazem um processo ficar bloqueado."
# "O conceito de Quantum, que é o tempo máximo que um processo pode executar antes de ser interrompido."
# "E a importância da Tabela de Processos, que salva o estado de cada processo a cada mudança."


import random
import time
from collections import deque

# --- Constantes de Configuração da Simulação ---
QUANTUM = 1000
CHANCE_IO = 0.01  # 1% de chance de E/S por ciclo
CHANCE_SAIR_BLOQUEADO = 0.30  # 30% de chance de sair do bloqueio
TOTAL_PROCESSOS = 10

# Tabela de tempo de execução total para cada processo
TEMPOS_EXECUCAO = {
    0: 10000, 1: 5000, 2: 7000, 3: 3000, 4: 3000,
    5: 8000, 6: 2000, 7: 5000, 8: 4000, 9: 10000
}

class Processo:
    """
    Representa um Processo (Process Control Block - PCB).
    Armazena todos os dados vitais de um processo.
    """
    def __init__(self, pid, tempo_total):
        self.pid = pid  # IDENTIFICADOR DE PROCESSO (PID)
        self.tempo_total_execucao = tempo_total
        self.tp = 0  # TEMPO DE PROCESSAMENTO (total de ciclos já executados)
        self.cp = 0  # CONTADOR DE PROGRAMA (CP = TP + 1)
        self.ep = 'PRONTO'  # ESTADO DO PROCESSO (EP)
        self.nes = 0  # NÚMERO DE VEZES QUE REALIZOU E/S
        self.n_cpu = 0  # NÚMERO DE VEZES QUE USOU A CPU

    def exibir(self):
        """Formata e imprime os dados do processo."""
        print(f"  PID: {self.pid}, Estado: {self.ep}, TP: {self.tp}, CP: {self.cp}, "
              f"N_CPU: {self.n_cpu}, NES: {self.nes}")

    def to_file_format(self):
        """Formata os dados para salvar no arquivo de texto."""
        return (f"PID: {self.pid:<3} | Estado: {self.ep:<12} | TP: {self.tp:<6} | "
                f"CP: {self.cp:<6} | N_CPU: {self.n_cpu:<4} | NES: {self.nes:<4}\n")

def salvar_tabela_processos(processos, nome_arquivo="Tabela_de_Processos.txt"):
    """
    Salva o estado atual de todos os processos em um arquivo de texto,
    sobrescrevendo o conteúdo anterior.
    """
    with open(nome_arquivo, 'w') as f:
        f.write("--- Tabela de Processos do Sistema Operacional ---\n")
        for processo in sorted(processos, key=lambda p: p.pid):
            f.write(processo.to_file_format())

def main():
    """
    Função principal que executa a simulação do escalonador.
    """
    print("Iniciando a simulação do Escalonador de Processos...")

    # --- Inicialização ---
    todos_processos = [Processo(pid, tempo) for pid, tempo in TEMPOS_EXECUCAO.items()]
    
    # Usamos 'deque' por ser mais eficiente para operações de fila (adicionar no fim, remover do início)
    fila_prontos = deque(todos_processos)
    fila_bloqueados = deque()
    processos_finalizados = []

    # Salva o estado inicial de todos os processos no arquivo
    salvar_tabela_processos(todos_processos)

    # --- Loop Principal da Simulação ---
    # O loop continua enquanto houver processos prontos, bloqueados ou em execução.
    while len(processos_finalizados) < TOTAL_PROCESSOS:
        
        # 1. Tentar desbloquear processos da fila de bloqueados
        # Itera sobre uma cópia da fila para poder modificá-la durante o loop
        for _ in range(len(fila_bloqueados)):
            processo_b = fila_bloqueados.popleft()
            if random.random() < CHANCE_SAIR_BLOQUEADO:
                processo_b.ep = 'PRONTO'
                fila_prontos.append(processo_b)
                print(f"\nPROCESSO {processo_b.pid} DESBLOQUEADO: BLOQUEADO -> PRONTO")
            else:
                # Se não desbloqueou, volta para o final da fila de bloqueados
                fila_bloqueados.append(processo_b)

        # 2. Se não há processos prontos, a CPU fica ociosa neste ciclo
        if not fila_prontos:
            print("\nCPU Ociosa... aguardando processos prontos ou desbloqueio.")
            time.sleep(0.5) # Pausa para facilitar a visualização
            continue

        # 3. Pega o próximo processo da fila de prontos para executar
        processo_atual = fila_prontos.popleft()
        processo_atual.ep = 'EXECUTANDO'
        processo_atual.n_cpu += 1
        
        print(f"\n--- Processo {processo_atual.pid} entrando na CPU (Nº de uso: {processo_atual.n_cpu}) ---")
        processo_atual.exibir()
        
        ocorreu_io = False
        quantum_restante = QUANTUM

        # 4. Simula a execução do processo ciclo a ciclo dentro do seu quantum
        for ciclo in range(QUANTUM):
            # Verifica se o processo terminou sua execução
            if processo_atual.tp >= processo_atual.tempo_total_execucao:
                break 

            processo_atual.tp += 1
            processo_atual.cp = processo_atual.tp + 1
            
            # Verifica a chance de ocorrer uma operação de E/S
            if random.random() < CHANCE_IO:
                processo_atual.nes += 1
                ocorreu_io = True
                quantum_restante = QUANTUM - (ciclo + 1)
                break
        
        # 5. Avalia o que aconteceu ao final do ciclo de execução
        # Caso A: Processo terminou sua execução total
        if processo_atual.tp >= processo_atual.tempo_total_execucao:
            processo_atual.ep = 'FINALIZADO'
            processos_finalizados.append(processo_atual)
            print(f"\n***** PROCESSO {processo_atual.pid} FINALIZADO *****")
            processo_atual.exibir()

        # Caso B: Ocorreu uma operação de E/S
        elif ocorreu_io:
            processo_atual.ep = 'BLOQUEADO'
            fila_bloqueados.append(processo_atual)
            print(f"\n(PID {processo_atual.pid}) TROCA DE CONTEXTO: EXECUTANDO -> BLOQUEADO (E/S)")
            print(f"  (Quantum restante: {quantum_restante} ciclos)")
            processo_atual.exibir()
        
        # Caso C: O quantum terminou sem E/S e sem o processo finalizar
        else:
            processo_atual.ep = 'PRONTO'
            fila_prontos.append(processo_atual)
            print(f"\n(PID {processo_atual.pid}) TROCA DE CONTEXTO: EXECUTANDO -> PRONTO (Quantum Expirado)")
            processo_atual.exibir()

        # Atualiza o arquivo de texto com o estado mais recente de todos os processos
        salvar_tabela_processos(todos_processos)
        time.sleep(0.2) # Pausa para facilitar a visualização da simulação

    print("\n--- SIMULAÇÃO FINALIZADA ---")
    print("Todos os processos foram executados.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()