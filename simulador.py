import csv
import os
import tkinter as tk

# Função para carregar o labirinto
def carregar_labirinto(arquivo):
    try:
        with open(arquivo, 'r') as f:
            labirinto = [list(linha.strip()) for linha in f.readlines()]
        return labirinto
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado!")
        return None

# Função para encontrar a posição do robô ou do humano
def encontrar_posicao(labirinto, caractere):
    for i, linha in enumerate(labirinto):
        if caractere in linha:
            return (i, linha.index(caractere))
    return None

# Função para verificar se a posição é válida
def posicao_valida(labirinto, pos):
    linhas, colunas = len(labirinto), len(labirinto[0])
    i, j = pos
    return 0 <= i < linhas and 0 <= j < colunas and labirinto[i][j] == ' '

# Função para desenhar a direção do robô
def desenhar_direcao_robo(canvas, pos_robo, direcao_robo, size=40):
    x1, y1 = pos_robo[1] * size, pos_robo[0] * size
    x2, y2 = x1 + size, y1 + size
    # Desenha o corpo do robô
    canvas.create_rectangle(x1, y1, x2, y2, fill="red")
    
    # Desenha a seta que indica a frente do robô
    if direcao_robo == 'north':
        # Desenhar seta apontando para cima
        points = [x1 + size/2, y1 + size/4, x1 + size/4, y2 - size/4, x2 - size/4, y2 - size/4]
    elif direcao_robo == 'south':
        # Desenhar seta apontando para baixo
        points = [x1 + size/4, y1 + size/4, x2 - size/4, y1 + size/4, x1 + size/2, y2 - size/4]
    elif direcao_robo == 'west':
        # Desenhar seta apontando para a esquerda
        points = [x1 + size/4, y1 + size/2, x2 - size/4, y1 + size/4, x2 - size/4, y2 - size/4]
    elif direcao_robo == 'east':
        # Desenhar seta apontando para a direita
        points = [x2 - size/4, y1 + size/2, x1 + size/4, y1 + size/4, x1 + size/4, y2 - size/4]
    
    canvas.create_polygon(points, fill="yellow")

# Função para desenhar o labirinto no Canvas do Tkinter
def desenhar_labirinto(canvas, labirinto, pos_robo, pos_humano, caminho_percorrido, direcao_robo, size=40):
    canvas.delete("all")  # Limpa o canvas
    for i, linha in enumerate(labirinto):
        for j, caractere in enumerate(linha):
            x1, y1 = j * size, i * size
            x2, y2 = x1 + size, y1 + size
            if caractere == '*':
                canvas.create_rectangle(x1, y1, x2, y2, fill="black")
            elif (i, j) == pos_humano:
                canvas.create_rectangle(x1, y1, x2, y2, fill="blue")  # Humano
            elif (i, j) in caminho_percorrido:
                canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")  # Caminho percorrido
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white")

    # Desenhar o robô com a direção
    desenhar_direcao_robo(canvas, pos_robo, direcao_robo, size)

# Função para verificar os sensores
def verificar_sensores(labirinto, pos, direcao):
    movimentos = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }
    sensores = {}
    frente = (pos[0] + movimentos[direcao][0], pos[1] + movimentos[direcao][1])
    esquerda = (pos[0] + movimentos[girar_direita(girar_direita(girar_direita(direcao)))][0], pos[1] + movimentos[girar_direita(girar_direita(girar_direita(direcao)))][1])
    direita = (pos[0] + movimentos[girar_direita(direcao)][0], pos[1] + movimentos[girar_direita(direcao)][1])

    sensores['frente'] = 'PAREDE' if not posicao_valida(labirinto, frente) else 'VAZIO'
    sensores['esquerda'] = 'PAREDE' if not posicao_valida(labirinto, esquerda) else 'VAZIO'
    sensores['direita'] = 'PAREDE' if not posicao_valida(labirinto, direita) else 'VAZIO'

    return sensores

# Função para girar o robô à direita
def girar_direita(direcao_atual):
    direcoes = ['north', 'east', 'south', 'west']
    idx_atual = direcoes.index(direcao_atual)
    nova_direcao = direcoes[(idx_atual + 1) % 4]
    return nova_direcao

# Simulação de movimento com melhorias de beco sem saída e backtracking explícito
def simular_movimento(labirinto, canvas, root, nome_arquivo):
    inicio = encontrar_posicao(labirinto, 'E')  # Posição inicial do robô (entrada)
    humano = encontrar_posicao(labirinto, 'H')  # Posição do humano

    if inicio is None or humano is None:
        print("Erro: não foi possível encontrar a entrada ou o humano.")
        return

    pos_robo = inicio
    direcao_robo = 'north'
    caminho_percorrido = [inicio]  # Usando uma lista para guardar o caminho
    comandos = []
    humano_encontrado = False
    estado_carga = 'SEM CARGA'
    visitados = set()
    marcados = set()  # Para marcar becos sem saída
    modo_backtracking = False  # Indica se o robô está em backtracking
    giro_continuo = 0  # Contador para evitar giros contínuos

    movimentos = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }

    # Log inicial - LIGAR
    sensores = verificar_sensores(labirinto, pos_robo, direcao_robo)
    comandos.append(['LIGAR', sensores['esquerda'], sensores['direita'], sensores['frente'], estado_carga])

    while True:
        # Desenhar o labirinto e atualizar a tela
        desenhar_labirinto(canvas, labirinto, pos_robo, humano, set(caminho_percorrido), direcao_robo)
        root.update()

        # Verifica os sensores
        sensores = verificar_sensores(labirinto, pos_robo, direcao_robo)

        # Se o robô encontrar o humano ao lado, pega o humano
        if abs(pos_robo[0] - humano[0]) + abs(pos_robo[1] - humano[1]) == 1 and not humano_encontrado:
            print("Humano encontrado!")
            comandos.append(['P', sensores['esquerda'], sensores['direita'], sensores['frente'], 'COM HUMANO'])
            humano_encontrado = True
            estado_carga = 'COM HUMANO'
            modo_backtracking = True  # Ativa backtracking para retornar à entrada
            continue  # Continua para iniciar o processo de retorno

        # Se o humano foi encontrado, o robô começa a retornar
        if humano_encontrado:
            if pos_robo == inicio:
                print("Robô voltou para a entrada com o humano!")
                comandos.append(['E', sensores['esquerda'], sensores['direita'], sensores['frente'], 'SEM CARGA'])
                break  # Termina a simulação

            # Voltar pelo caminho percorrido de forma eficiente
            if caminho_percorrido:
                pos_robo = caminho_percorrido.pop()  # Volta para a posição anterior
                comandos.append(['A', sensores['esquerda'], sensores['direita'], sensores['frente'], estado_carga])
            continue

        # Tentar avançar se não houver parede à frente e não tiver sido marcado como beco
        nova_pos = (pos_robo[0] + movimentos[direcao_robo][0], pos_robo[1] + movimentos[direcao_robo][1])

        if sensores['frente'] == 'VAZIO' and nova_pos not in visitados and nova_pos not in marcados:
            if posicao_valida(labirinto, nova_pos):
                pos_robo = nova_pos
                caminho_percorrido.append(pos_robo)
                visitados.add(pos_robo)
                comandos.append(['A', sensores['esquerda'], sensores['direita'], sensores['frente'], estado_carga])
                modo_backtracking = False  # Desativa o modo de backtracking, estamos avançando
                giro_continuo = 0  # Reseta o contador de giros
        else:
            # Se não puder avançar, tentar girar ou ativar backtracking
            direcao_robo = girar_direita(direcao_robo)
            sensores = verificar_sensores(labirinto, pos_robo, direcao_robo)  # Recalcular os sensores após o giro
            comandos.append(['G', sensores['esquerda'], sensores['direita'], sensores['frente'], estado_carga])
            giro_continuo += 1

            # Se girar 4 vezes e não encontrar saída, ativar backtracking
            if giro_continuo >= 4:
                print("Beco sem saída detectado! Iniciando backtracking...")
                marcados.add(pos_robo)  # Marcar o beco sem saída
                modo_backtracking = True  # Ativa o modo de backtracking
                giro_continuo = 0  # Reseta o contador de giros

                # Voltar para o caminho anterior
                if caminho_percorrido:
                    pos_robo = caminho_percorrido.pop()
                    comandos.append(['A', sensores['esquerda'], sensores['direita'], sensores['frente'], estado_carga])
                else:
                    print("Erro: Não há mais caminho para retornar. Fim da linha.")
                    break

        # Pausa para visualização
        root.after(200)

    # Salvar log de operações (comandos) após a simulação
    salvar_log(comandos, nome_arquivo)

# Função para salvar o log de operações
def salvar_log(comandos, nome_arquivo):
    # Define o caminho correto para o arquivo de log
    arquivo_log = os.path.join('logs', 'operacao.csv')

    # Verifica se o diretório de logs existe, se não, cria-o
    os.makedirs(os.path.dirname(arquivo_log), exist_ok=True)

    with open(arquivo_log, 'w', newline='') as csvfile:
        logwriter = csv.writer(csvfile)
        logwriter.writerow(['Comando', 'Sensor Esquerdo', 'Sensor Direito', 'Sensor Frente', 'Carga'])
        for comando in comandos:
            logwriter.writerow(comando)

    print(f"Log salvo em: {arquivo_log}")