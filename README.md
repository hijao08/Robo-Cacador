# Robô Caçador 🤖💡

O **Robô Caçador** é uma simulação de um robô autônomo que navega por um labirinto, encontra um humano e retorna à posição inicial com ele. O objetivo do projeto é implementar uma solução de movimentação para o robô com verificação de sensores, tratamento de becos sem saída e um sistema de logging para monitorar as operações.

## 📝 Funcionalidades

- Movimentação automática do robô por um labirinto.
- Verificação de obstáculos utilizando sensores simulados (frente, esquerda, direita).
- Detecção e tratamento de becos sem saída (backtracking).
- Registra log de todas as operações do robô em um arquivo CSV.
- Visualização do labirinto e do robô utilizando Tkinter.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Tkinter** para visualização gráfica do labirinto.
- **CSV** para salvar o log das operações do robô.
- **Algoritmo 'A*'** para encontrar o caminho mais curto.
- **Terminal** para visualização do labirinto (sem uso de Tkinter).

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3 instalado. Se não tiver, você pode instalá-lo seguindo as instruções no [site oficial do Python](https://www.python.org/downloads/).
- Clonar o repositório localmente:

```bash
git clone https://github.com/hijao08/robo-cacador.git
cd robo-cacador
```
#### pode escolher se quer
- com vizualizador
```bash
cd robo-cacador-cem-vizualizador
```
- sem vizualizador
```bash
cd robo-cacador-sem-vizualizador
```

## Executando o Projeto
- Configurar o labirinto:
- Crie um arquivo chamado labirinto.txt no diretório principal. Este arquivo conterá o layout do labirinto. Exemplo de um labirinto:

```markdown
*E*********
*     *   *
* *** * * *
* * * * * *
* * * *** *
* *      H*
***********
```

- O labirinto usa:
- '*' para representar paredes.
- 'E' para a entrada (onde o robô começa).
- 'H' para a posição do humano.

## Rodar o Projeto:

- Execute o comando abaixo para iniciar a simulação:
```bash
python3 main.py
```

## Estrutura de Arquivos
```bash
.
├── labirinto.py             # Módulo para carregar o labirinto a partir de um arquivo de texto.
├── robo_cacador.py          # Lógica principal do robô, incluindo movimentação e algoritmo A*.
├── main.py                  # Arquivo principal que inicializa a simulação.
├── labirinto.txt            # Arquivo contendo a representação do labirinto.
└── logs/
    └── operacao.csv         # Contem os logs
```

## 📄 Logs de Operação 

Todos os movimentos e verificações de sensores do robô são registrados em um arquivo CSV (logs/operacao.csv). O arquivo contém as seguintes colunas:

- Comando: O comando executado (LIGAR, ANDAR, GIRAR, etc.).
- Sensor Esquerdo: Estado do sensor esquerdo (PAREDE, VAZIO, HUMANO).
- Sensor Direito: Estado do sensor direito.
- Sensor Frente: Estado do sensor frontal.
- Carga: Se o humano foi coletado ou não (COM HUMANO ou SEM CARGA).

## 🎮 Exemplo de Execução

### Com Vizualizador
Durante a execução, e você verá a movimentação do robô como um quadrado vermelho e a posição do humano como um quadrado azul.

![Print Com Vizualizador](./print_vizualizador.png)

Conforme o robô se move, o labirinto será atualizado até o humano ser resgatado e o robô retornar à entrada.

### Sem Vizualizador
Durante a execução, o labirinto será impresso no terminal, e você verá a movimentação do robô (R) e a posição do humano (H).

```markdown
*E*********
*     *   *
* *** * * *
* * * * * *
* * * *** *
* *      H*
***********
```

Conforme o robô se move, o labirinto será atualizado até o humano ser resgatado e o robô retornar à entrada.
