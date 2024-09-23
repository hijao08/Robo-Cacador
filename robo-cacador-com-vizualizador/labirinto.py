class Labirinto:
    @staticmethod
    def carregar_labirinto(arquivo):
        try:
            with open(arquivo, 'r') as f:
                labirinto = [list(linha.strip()) for linha in f.readlines()]
            return labirinto
        except FileNotFoundError:
            print(f"Erro: Arquivo {arquivo} não encontrado.")
            return None