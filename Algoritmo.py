
import numpy as np
from Constants import MATRIZ_MULTIPLICACAO, S_BOX

class Algoritmo:

    @staticmethod
    def add_round_key(matriz_estado, round_key):
        return matriz_estado ^ round_key

    @staticmethod
    def sub_bytes(matriz):
        matriz_saida = matriz.copy()
        num_linhas, num_colunas = matriz.shape
        for i in range(num_linhas):
            for j in range(num_colunas):
                linha, coluna = Algoritmo.obter_posicao_no_s_box(matriz[i, j])
                matriz_saida[i, j] = S_BOX[linha][coluna]
        return matriz_saida

    @staticmethod
    def shift_rows(matriz):
        num_linhas, num_colunas = matriz.shape
        matriz_saida = np.zeros_like(matriz)
        for i in range(num_linhas):
            matriz_saida[i] = np.roll(matriz[i], -i)
        return matriz_saida

    @staticmethod
    def mix_columns(matriz):
        num_linhas, num_colunas = matriz.shape
        matriz_saida = np.zeros_like(matriz)
        for c in range(num_colunas):
            coluna = matriz[:, c]
            nova_coluna = np.zeros(4, dtype=int)
            for i in range(4):
                val = 0
                for j in range(4):
                    val ^= Algoritmo.galois_mult(MATRIZ_MULTIPLICACAO[i][j], coluna[j])
                nova_coluna[i] = val
            matriz_saida[:, c] = nova_coluna
        return matriz_saida

    @staticmethod
    def galois_mult(a, b):
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a = (a << 1) & 0xFF
            if hi_bit_set:
                a ^= 0x1B
            b >>= 1
        return p

    @staticmethod
    def obter_posicao_no_s_box(char):
        linha = char >> 4
        coluna = char & 0x0F
        return linha, coluna

    @staticmethod
    def obter_matriz_estado(dados):
        array_np = np.array(dados, dtype=int)
        matrix = array_np.reshape((4, 4), order='F')
        return matrix

    @staticmethod
    def matriz_para_bytes(matriz):
        lista_plana = matriz.flatten(order='F').tolist()
        return bytes(lista_plana)
