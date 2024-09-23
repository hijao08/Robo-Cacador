import heapq
import csv
import os

class RoboCacador:
    def __init__(self, labirinto, arquivo_log='logs/operacao.csv'):
        self.labirinto = labirinto
        self.pos_robo = self.encontrar_entrada()
        self.pos_humano = self.encontrar_humano()
        self.direcao_robo = 'north'
        self.canvas = None
        self.humano_coletado = False
        self.arquivo_log = arquivo_log
        self.comandos = []
        self.iniciar_log()

    def iniciar_log(self):
        os.makedirs('logs', exist_ok=True)
        with open(self.arquivo_log, 'w', newline='') as csvfile:
            logwriter = csv.writer(csvfile)
            logwriter.writerow(['Comando', 'Sensor Esquerdo', 'Sensor Direito', 'Sensor Frente', 'Carga'])

    def registrar_comando(self, comando, sensores):
        estado_carga = 'COM HUMANO' if self.humano_coletado else 'SEM CARGA'
        self.comandos.append([comando, sensores['esquerda'], sensores['direita'], sensores['frente'], estado_carga])

    def encontrar_entrada(self):
        for i, linha in enumerate(self.labirinto):
            if 'E' in linha:
                return (i, linha.index('E'))
        return None

    def encontrar_humano(self):
        for i, linha in enumerate(self.labirinto):
            if 'H' in linha:
                return (i, linha.index('H'))
        return None

    def desenhar_labirinto(self, canvas, size=40):
        canvas.delete("all")
        for i, linha in enumerate(self.labirinto):
            for j, char in enumerate(linha):
                x1, y1 = j * size, i * size
                x2, y2 = x1 + size, y1 + size
                color = 'white'
                if char == '*':
                    color = 'black'
                elif (i, j) == self.pos_robo:
                    color = 'red'
                elif (i, j) == self.pos_humano and not self.humano_coletado:
                    color = 'blue'
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def distancia_manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_estrela(self, inicio, fim):
        fila = [(0, inicio)]
        caminho = {}
        custo_ate_agora = {inicio: 0}

        while fila:
            _, atual = heapq.heappop(fila)

            if atual == fim:
                caminho_reconstruido = []
                while atual != inicio:
                    caminho_reconstruido.append(atual)
                    atual = caminho[atual]
                caminho_reconstruido.reverse()
                return caminho_reconstruido

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                novo = (atual[0] + dx, atual[1] + dy)
                if 0 <= novo[0] < len(self.labirinto) and 0 <= novo[1] < len(self.labirinto[0]) and self.labirinto[novo[0]][novo[1]] != '*':
                    novo_custo = custo_ate_agora[atual] + 1
                    if novo not in custo_ate_agora or novo_custo < custo_ate_agora[novo]:
                        custo_ate_agora[novo] = novo_custo
                        prioridade = novo_custo + self.distancia_manhattan(novo, fim)
                        heapq.heappush(fila, (prioridade, novo))
                        caminho[novo] = atual
        return None

    def verificar_sensores(self):
        movimentos = {
            'north': (-1, 0),
            'south': (1, 0),
            'west': (0, -1),
            'east': (0, 1)
        }
        sensores = {'frente': 'VAZIO', 'esquerda': 'VAZIO', 'direita': 'VAZIO'}

        # Verifica a frente
        pos_frente = (self.pos_robo[0] + movimentos[self.direcao_robo][0], 
                    self.pos_robo[1] + movimentos[self.direcao_robo][1])
        if 0 <= pos_frente[0] < len(self.labirinto) and 0 <= pos_frente[1] < len(self.labirinto[0]):
            if self.labirinto[pos_frente[0]][pos_frente[1]] == '*':
                sensores['frente'] = 'PAREDE'
            elif self.labirinto[pos_frente[0]][pos_frente[1]] == 'H':
                sensores['frente'] = 'HUMANO'
            else:
                sensores['frente'] = 'VAZIO'

        # Verifica esquerda e direita com base na direção atual
        if self.direcao_robo == 'north':
            # Esquerda é oeste, direita é leste
            pos_esquerda = (self.pos_robo[0], self.pos_robo[1] - 1)
            pos_direita = (self.pos_robo[0], self.pos_robo[1] + 1)
        elif self.direcao_robo == 'south':
            # Esquerda é leste, direita é oeste
            pos_esquerda = (self.pos_robo[0], self.pos_robo[1] + 1)
            pos_direita = (self.pos_robo[0], self.pos_robo[1] - 1)
        elif self.direcao_robo == 'west':
            # Esquerda é sul, direita é norte
            pos_esquerda = (self.pos_robo[0] + 1, self.pos_robo[1])
            pos_direita = (self.pos_robo[0] - 1, self.pos_robo[1])
        elif self.direcao_robo == 'east':
            # Esquerda é norte, direita é sul
            pos_esquerda = (self.pos_robo[0] - 1, self.pos_robo[1])
            pos_direita = (self.pos_robo[0] + 1, self.pos_robo[1])

        for direcao, posicao in zip(['esquerda', 'direita'], [pos_esquerda, pos_direita]):
            if 0 <= posicao[0] < len(self.labirinto) and 0 <= posicao[1] < len(self.labirinto[0]):
                if self.labirinto[posicao[0]][posicao[1]] == '*':
                    sensores[direcao] = 'PAREDE'
                elif self.labirinto[posicao[0]][posicao[1]] == 'H':
                    sensores[direcao] = 'HUMANO'
                else:
                    sensores[direcao] = 'VAZIO'
            else:
                sensores[direcao] = 'PAREDE'

        return sensores

    def ajustar_direcao(self, destino):
        if self.pos_robo == destino:
            return  # Não precisa se mover se já está na posição de destino

        dx = destino[0] - self.pos_robo[0]
        dy = destino[1] - self.pos_robo[1]

        # Inicializa nova_direcao como None
        nova_direcao = None

        if dx == -1:
            nova_direcao = 'north'
        elif dx == 1:
            nova_direcao = 'south'
        elif dy == -1:
            nova_direcao = 'west'
        elif dy == 1:
            nova_direcao = 'east'

        # Verifica se nova_direcao foi definida
        if nova_direcao is None:
            print("Erro: Não foi possível determinar a nova direção.")
            return
        
        while self.direcao_robo != nova_direcao:
            self.girar_robo()

    def girar_robo(self):
        direcoes = ['north', 'east', 'south', 'west']
        idx_atual = direcoes.index(self.direcao_robo)
        self.direcao_robo = direcoes[(idx_atual + 1) % 4]
        sensores = self.verificar_sensores()
        self.registrar_comando('G', sensores)

        if self.canvas is not None:
            self.canvas.update()
            self.desenhar_labirinto(self.canvas)
            self.canvas.after(100)

    def mover_robo(self):
        sensores = self.verificar_sensores()
        self.registrar_comando('LIGAR', sensores)

        # Caminho até o humano
        caminho_ate_humano = self.a_estrela(self.pos_robo, self.pos_humano)
        if caminho_ate_humano:
            # Mova até a posição anterior ao humano
            posicao_antes_humano = caminho_ate_humano[-2]

            for posicao in caminho_ate_humano[:-1]:
                self.ajustar_direcao(posicao)
                self.pos_robo = posicao
                sensores = self.verificar_sensores()

                if self.pos_robo == 'PAREDE':
                    print("Atenção, voce bateu em uma parede!!")
                    
                if sensores['frente'] == 'HUMANO':
                    print("Cuidado, vá com calma, tem um humano a frente!") 
                    
                if self.pos_robo == 'HUMANO':
                    print("Atenção, voce bateu em um humano!")

                self.registrar_comando('A', sensores)
                if self.canvas is not None:  # Verifica se o canvas existe antes de atualizar
                    self.canvas.update()
                    self.desenhar_labirinto(self.canvas)
                    self.canvas.after(100)

            # Mover para a posição anterior ao humano
            self.ajustar_direcao(posicao_antes_humano)
            self.pos_robo = posicao_antes_humano
            sensores = self.verificar_sensores()
            if self.canvas is not None:
                self.canvas.update()
                self.desenhar_labirinto(self.canvas)
                self.canvas.after(100)

            # Alinhar-se com o humano
            while not self.verificar_se_frente_do_humano():
                self.girar_robo()
                sensores = self.verificar_sensores()
                if self.canvas is not None:
                    self.canvas.update()
                    self.desenhar_labirinto(self.canvas)
                    self.canvas.after(100)

            if not self.humano_coletado:
                self.humano_coletado = True
                self.registrar_comando('P', sensores)  # Registrar coleta do humano
                if not self.verificar_se_frente_do_humano():
                    print("Erro: O humano não está na frente do robô!")
                    self.registrar_comando('P, Erro: O humano não está na frente do robô!', sensores)
                    return
                print("Humano coletado!")
                print("Voltando para a Entrada!")

        # Voltar para a entrada
        caminho_de_volta = self.a_estrela(self.pos_robo, self.encontrar_entrada())
        if caminho_de_volta:
            for posicao in caminho_de_volta:
                self.ajustar_direcao(posicao)
                self.pos_robo = posicao
                sensores = self.verificar_sensores()
                if sensores['frente'] == 'PAREDE' and sensores['esquerda'] == 'PAREDE' and sensores['direita'] == 'PAREDE':
                    print("Erro: Robô entrou em um beco sem saída com o humano!")
                    return

                self.registrar_comando('A', sensores)
                if self.canvas is not None:
                    self.canvas.update()
                    self.desenhar_labirinto(self.canvas)
                    self.canvas.after(100)

            if not self.humano_coletado:
                print("Erro: Tentativa de ejetar sem o humano!")
                self.registrar_comando('TENTATIVA FALHA DE EJETAR SEM HUMANO', sensores)
            else:
                self.registrar_comando('E', sensores)
                print("Humano resgatado!")
                print("O Robo saiu com o Humano do labirinto!")
        else:
            print("Caminho não encontrado.")
            print("Não existe caminho até o humano")
            self.registrar_comando("CAMINHO NÃO ENCONTRADO", sensores)
            self.registrar_comando("NÃO EXISTE CAMINHO ATÉ O HUMANO", sensores)

        self.salvar_log()

    def salvar_log(self):
        os.makedirs('logs', exist_ok=True)
        with open(self.arquivo_log, 'w', newline='') as csvfile:
            logwriter = csv.writer(csvfile)
            logwriter.writerow(['Comando', 'Sensor Esquerdo', 'Sensor Direito', 'Sensor Frente', 'Carga'])
            for comando in self.comandos:
                logwriter.writerow(comando)

    def verificar_se_frente_do_humano(self):
        direcoes = {
            'north': (-1, 0),
            'south': (1, 0),
            'west': (0, -1),
            'east': (0, 1)
        }
        # Verifica a direção em que o robô está apontando e se há um humano na frente
        movimento = direcoes[self.direcao_robo]
        nova_pos = (self.pos_robo[0] + movimento[0], self.pos_robo[1] + movimento[1])
        return nova_pos == self.pos_humano

    def verificar_se_adjacente(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1