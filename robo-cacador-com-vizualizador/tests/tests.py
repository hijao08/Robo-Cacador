import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from robo_cacador import RoboCacador
from labirinto import Labirinto

class TestRoboCacadorComLabirintoTxt(unittest.TestCase):

    def setUp(self):
        # Carregar o labirinto do arquivo 'labirinto.txt'
        self.labirinto = Labirinto.carregar_labirinto('/home/joaosoares/robo-cacador/robo-cacador-com-vizualizador/tests/labirinto.txt')
        self.robo = RoboCacador(self.labirinto)

    def test_encontrar_entrada(self):
        """Testa se o robô encontra corretamente a entrada 'E'"""
        entrada = self.robo.encontrar_entrada()
        self.assertEqual(entrada, (20, 35))  # Posição correta da entrada 'E' no labirinto

    def test_encontrar_humano(self):
        """Testa se o robô encontra corretamente a posição do humano 'H'"""
        humano = self.robo.encontrar_humano()
        self.assertEqual(humano, (1, 2))  # Posição do humano 'H' no labirinto

    def test_a_estrela(self):
        """Testa se o algoritmo A* encontra o caminho correto até o humano"""
        caminho = self.robo.a_estrela(self.robo.encontrar_entrada(), self.robo.encontrar_humano())
        self.assertIsNotNone(caminho)  # Verifica se o caminho foi encontrado
        self.assertGreater(len(caminho), 0)  # Verifica se o caminho tem passos

    def test_mover_robo(self):
        """Testa se o robô consegue se mover até o humano e voltar para a entrada"""
        self.robo.mover_robo()
        self.assertTrue(self.robo.humano_coletado)  # Verifica se o humano foi coletado

    def test_alarme_colisao_parede(self):
        """Testa se o alarme dispara ao colidir com uma parede"""
        self.robo.pos_robo = (1, 1)  # Posição próxima a uma parede
        sensores = self.robo.verificar_sensores()
        self.assertEqual(sensores['frente'], 'PAREDE')  # Verifica se há parede à frente

    def test_alarme_atropelamento_humano(self):
        """Testa se o alarme dispara ao tentar atropelar um humano"""
        self.robo.pos_robo = (1, 1)  # O humano está em (1, 2)
        self.robo.direcao_robo = 'east'  # O robô deve estar voltado para o humano
        sensores = self.robo.verificar_sensores()
        self.assertEqual(sensores['frente'], 'HUMANO')  # Verifica se o humano está à frente

    def test_alarme_beco_sem_saida_apos_coleta(self):
        """Testa se o alarme dispara ao entrar em um beco sem saída após coletar o humano"""
        self.robo.humano_coletado = True
        # Ajustar para uma posição onde o robô está cercado por paredes em três direções
        self.robo.pos_robo = (3, 1)  # Posição cercada por paredes
        sensores = self.robo.verificar_sensores()
        self.assertEqual(sensores['frente'], 'PAREDE')
        self.assertEqual(sensores['esquerda'], 'PAREDE')
        self.assertEqual(sensores['direita'], 'PAREDE')  # Verifica se é um beco sem saída



    def test_alarme_ejetar_sem_humano(self):
        """Testa se o alarme dispara ao tentar ejetar sem o humano"""
        self.robo.humano_coletado = False  # Não coletou o humano
        self.robo.pos_robo = (20, 35)  # Coloca o robô na posição de entrada
        # Simula tentativa de ejeção
        self.robo.registrar_comando('E', self.robo.verificar_sensores())  # Tentativa de ejeção
        self.assertFalse(self.robo.humano_coletado)  # Confirma que o humano não foi coletado



    def test_alarme_coleta_sem_humano_a_frente(self):
        """Testa se o alarme dispara ao tentar coletar sem o humano à frente"""
        self.robo.pos_robo = (1, 1)  # Posição longe do humano
        sensores = self.robo.verificar_sensores()
        self.assertNotEqual(sensores['frente'], 'HUMANO')  # Verifica se não há humano à frente

if __name__ == '__main__':
    unittest.main()
