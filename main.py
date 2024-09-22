import tkinter as tk
from simulador import carregar_labirinto, simular_movimento

# Função principal para iniciar a simulação
def iniciar_simulacao():
    nome_arquivo = 'labirinto.txt'  # Altere para o arquivo que você estiver usando
    labirinto = carregar_labirinto(nome_arquivo)
    if not labirinto:
        return

    root = tk.Tk()
    root.title("Simulação do Robô no Labirinto")

    size = 40
    linhas, colunas = len(labirinto), len(labirinto[0])
    canvas = tk.Canvas(root, width=colunas * size, height=linhas * size)
    canvas.pack()

    simular_movimento(labirinto, canvas, root, nome_arquivo)

    root.mainloop()

# Executa o simulador
if __name__ == '__main__':
    iniciar_simulacao()
