from robo_cacador import RoboCacador
from labirinto import Labirinto

def iniciar_simulacao():
    labirinto = Labirinto.carregar_labirinto('labirinto.txt')
    if not labirinto:
        return

    robo = RoboCacador(labirinto)
    robo.desenhar_labirinto()
    robo.mover_robo()

if __name__ == "__main__":
    iniciar_simulacao()
