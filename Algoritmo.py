
import numpy as np
from Constants import INV_S_BOX, MATRIZ_MULTIPLICACAO, S_BOX, TABLE_E, TABLE_L

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
        matriz_saida = np.zeros_like(matriz)
        for c in range(4):
            r1, r2, r3, r4 = matriz[:, c]
            b1 = (Algoritmo.galois_mult(r1, 2) ^
                  Algoritmo.galois_mult(r2, 3) ^
                  Algoritmo.galois_mult(r3, 1) ^
                  Algoritmo.galois_mult(r4, 1))
            b2 = (Algoritmo.galois_mult(r1, 1) ^
                  Algoritmo.galois_mult(r2, 2) ^
                  Algoritmo.galois_mult(r3, 3) ^
                  Algoritmo.galois_mult(r4, 1))
            b3 = (Algoritmo.galois_mult(r1, 1) ^
                  Algoritmo.galois_mult(r2, 1) ^
                  Algoritmo.galois_mult(r3, 2) ^
                  Algoritmo.galois_mult(r4, 3))
            b4 = (Algoritmo.galois_mult(r1, 3) ^
                  Algoritmo.galois_mult(r2, 1) ^
                  Algoritmo.galois_mult(r3, 1) ^
                  Algoritmo.galois_mult(r4, 2))
            matriz_saida[:, c] = [b1, b2, b3, b4]
        return matriz_saida

    @staticmethod
    def galois_mult(a, b):
        if a == 0 or b == 0:
            return 0
        if b == 1:
            return a

        linha_a, coluna_a = a >> 4, a & 0x0F
        linha_b, coluna_b = b >> 4, b & 0x0F
        la = TABLE_L[linha_a][coluna_a]
        lb = TABLE_L[linha_b][coluna_b]

        soma = la + lb
        if soma > 0xFF:
            soma -= 0xFF

        linha_e, coluna_e = soma >> 4, soma & 0x0F
        resultado = TABLE_E[linha_e][coluna_e]
        return resultado
    
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


    @staticmethod
    def inv_shift_rows(matriz):
        matriz_saida = np.zeros_like(matriz)
        for i in range(4):
            matriz_saida[i] = np.roll(matriz[i], i)
        return matriz_saida
    
    
    @staticmethod
    def inv_sub_bytes(matriz):
        matriz_saida = matriz.copy()
        for i in range(4):
            for j in range(4):
                linha = matriz[i, j] >> 4
                coluna = matriz[i, j] & 0x0F
                matriz_saida[i, j] = INV_S_BOX[linha][coluna]
        return matriz_saida
    
    @staticmethod
    def inv_mix_columns(matriz):
        matriz_saida = np.zeros_like(matriz)
        for c in range(4):
            r1, r2, r3, r4 = matriz[:, c]
            b1 = (Algoritmo.galois_mult(r1, 0x0e) ^
                  Algoritmo.galois_mult(r2, 0x0b) ^
                  Algoritmo.galois_mult(r3, 0x0d) ^
                  Algoritmo.galois_mult(r4, 0x09))
            b2 = (Algoritmo.galois_mult(r1, 0x09) ^
                  Algoritmo.galois_mult(r2, 0x0e) ^
                  Algoritmo.galois_mult(r3, 0x0b) ^
                  Algoritmo.galois_mult(r4, 0x0d))
            b3 = (Algoritmo.galois_mult(r1, 0x0d) ^
                  Algoritmo.galois_mult(r2, 0x09) ^
                  Algoritmo.galois_mult(r3, 0x0e) ^
                  Algoritmo.galois_mult(r4, 0x0b))
            b4 = (Algoritmo.galois_mult(r1, 0x0b) ^
                  Algoritmo.galois_mult(r2, 0x0d) ^
                  Algoritmo.galois_mult(r3, 0x09) ^
                  Algoritmo.galois_mult(r4, 0x0e))
            matriz_saida[:, c] = [b1, b2, b3, b4]
        return matriz_saida