import numpy as np

from Bloco import *
from Chave import *

def cifrar(msg, chave: bytes):
    key_schedule = expandir_chave(chave)

    msg = aplicar_padding_pkcs7(msg)
    blocos = dividir_em_blocos(msg)

    msg_cifrada = b''

    for bloco in blocos:
        bloco_cifrado = cifrar_bloco(bloco, key_schedule)
        msg_cifrada += matriz_para_bytes(bloco_cifrado)
    
    return msg_cifrada

def cifrar_bloco(bloco, key_schedule):
    matriz_estado = obter_matriz_estado(bloco)
    # imprimir_matriz_em_hex(matriz_estado)
    # imprimir_matriz_em_hex(key_schedule[0])  

    etapa1 = add_round_key(matriz_estado, key_schedule[0])
    # imprimir_matriz_em_hex(etapa1)

    for i in range(1, 10):
        matriz_estado = sub_bytes(matriz_estado)
        matriz_estado = shift_rows(matriz_estado)
        matriz_estado = mix_columns(matriz_estado)
        matriz_estado = add_round_key(matriz_estado, key_schedule[i])
        # imprimir_matriz_em_hex(matriz_estado)
        
    matriz_estado = sub_bytes(matriz_estado)
    matriz_estado = shift_rows(matriz_estado)
    matriz_estado = add_round_key(matriz_estado, key_schedule[10])
    # imprimir_matriz_em_hex(matriz_estado)

    return matriz_estado    

def add_round_key(matriz_estado, round_key):
    return matriz_estado ^ round_key

def sub_bytes(matriz):
    matriz_saida = matriz.copy()
    num_linhas, num_colunas = matriz.shape
    for i in range(num_linhas):
        for j in range(num_colunas):
            linha, coluna = obter_posicao_no_s_box(matriz[i, j])
            matriz_saida[i, j] = S_BOX[linha][coluna]
    return matriz_saida

def shift_rows(matriz):
    num_linhas, num_colunas = matriz.shape
    matriz_saida = np.zeros_like(matriz)
    for i in range(num_linhas):
        matriz_saida[i] = np.roll(matriz[i], -i)
    return matriz_saida

def mix_columns(matriz):
    num_linhas, num_colunas = matriz.shape
    matriz_saida = np.zeros_like(matriz)
    for c in range(num_colunas):
        coluna = matriz[:, c]
        nova_coluna = np.zeros(4, dtype=int)
        for i in range(4):
            val = 0
            for j in range(4):
                val ^= galois_mult(MATRIZ_MULTIPLICACAO[i][j], coluna[j])
            nova_coluna[i] = val
        matriz_saida[:, c] = nova_coluna
    return matriz_saida
            
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

def obter_posicao_no_s_box(char):
    linha = char >> 4
    coluna = char & 0x0F
    return linha, coluna

def obter_matriz_estado(dados):
    array_np = np.array(dados)
    matrix = array_np.reshape((4, 4), order='F')
    return matrix

def matriz_para_bytes(matriz):
    lista_plana = matriz.flatten(order='F').tolist()
    return bytes(lista_plana)


def imprimir_matriz_em_hex(matriz):
    print("-------------------------------")
    for linha in matriz:
        linha_formatada = []
        for numero in linha:
            string_hex = f'0x{numero:02x}'
            linha_formatada.append(string_hex)
        print(" ".join(linha_formatada))
    print("-------------------------------")