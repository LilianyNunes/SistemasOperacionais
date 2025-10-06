MEM_SIZE = 32

class Memoria:
    def __init__(self):
        self.memoria = [0] * MEM_SIZE
        self.processos_alocados = {}

    def mostrar(self):
        print("Memória:", "".join(str(x) for x in self.memoria))

    def desalocar(self, pid):
        if pid in self.processos_alocados:
            inicio, tam = self.processos_alocados[pid]
            for i in range(inicio, inicio + tam):
                self.memoria[i] = 0
            print(f"Processo {pid} desalocado.")
            del self.processos_alocados[pid]
        else:
            print(f"Processo {pid} não está na memória.")

    def calcular_fragmentacao(self, tamanho_minimo):
        """
        Conta os blocos livres que pertencem a 'buracos' menores que o tamanho mínimo.
        """
        memoria = self.memoria
        fragmentacao = 0
        i = 0
        while i < MEM_SIZE:
            if memoria[i] == 0:
                j = i
                while j < MEM_SIZE and memoria[j] == 0:
                    j += 1
                tamanho_buraco = j - i
                if tamanho_buraco < tamanho_minimo:
                    fragmentacao += tamanho_buraco
                i = j
            else:
                i += 1
        return fragmentacao
