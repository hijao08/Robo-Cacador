import tkinter as tk
from robo_cacador import RoboCacador
from labirinto import Labirinto

def iniciar_simulacao():
    labirinto = Labirinto.carregar_labirinto('labirinto.txt')
    if not labirinto:
        return

    root = tk.Tk()
    root.title("Simulação do Robô de Resgate")
    size = 40

    linhas, colunas = len(labirinto), len(labirinto[0])
    canvas = tk.Canvas(root, width=colunas * size, height=linhas * size)
    canvas.pack()

    robo = RoboCacador(labirinto)
    robo.canvas = canvas
    robo.desenhar_labirinto(canvas)

    btn_iniciar = tk.Button(root, text="Iniciar Caçada", command=robo.mover_robo)
    btn_iniciar.pack()

    root.mainloop()

if __name__ == "__main__":
    iniciar_simulacao()