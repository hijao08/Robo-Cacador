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
- **Algoritmo de Backtracking** para retornar do beco sem saída.

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3 instalado. Se não tiver, você pode instalá-lo seguindo as instruções no [site oficial do Python](https://www.python.org/downloads/).
- Clonar o repositório localmente:

```bash
git clone https://github.com/hijao08/robo-cacador.git
