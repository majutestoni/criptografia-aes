import numpy as np
from Constants import *

def imprimir_matriz_hex(matriz):
    print("------------------------")
    for linha in matriz:
        print(" ".join(f"0x{byte:02X}" for byte in linha))
    print("------------------------")

def expandir_chave(chave: bytes):

    matriz_estado_original = np.array(list(chave)).reshape((4, 4), order='F') # cria a matriz estado

    lista_round_keys = [] # criando lista para guardar as round keys
    lista_round_keys.append(matriz_estado_original)

    round_key_atual_pos = 1

    for i in range(10):
        round_key_anterior = lista_round_keys[round_key_atual_pos - 1]

        round_key_atual_loop = np.zeros((4, 4), dtype=int)

        # 2 - rotacionar bytes
        palavra = rotacionar_bytes(round_key_anterior[:, 3])

        # 3 - substituição de palavra
        for j in range(len(palavra)):
            posicoes_s_box = obter_posicao_no_s_box(palavra[j])
            char_do_s_box = S_BOX[posicoes_s_box[0]][posicoes_s_box[1]]
            palavra[j] = char_do_s_box

        # 4 - geração da roundconstant
        round_constant = ROUND_CONSTANT_MAP.get(round_key_atual_pos)

        # 5 - XOR das etapas 3 e 4
        xor_etapa_5 = palavra[0] ^ round_constant
        palavra[0] = xor_etapa_5

        # 6 - XOR da etapa 5 com a 1a palavra da round key anterior
        primeira_palavra_round_key_anterior = round_key_anterior[:, 0]
        for k in range(len(palavra)):
            xor_etapa_6 = primeira_palavra_round_key_anterior[k] ^ palavra[k]
            palavra[k] = xor_etapa_6

        # adicionar palavra na round key atual
        round_key_atual_loop[0,0] = palavra[0]
        round_key_atual_loop[1,0] = palavra[1]
        round_key_atual_loop[2,0] = palavra[2]
        round_key_atual_loop[3,0] = palavra[3]

        # geracao das outras 3 palavras da round key
        for l in range(3):
            palavra_round_key_anterior = round_key_anterior[:, l + 1]
            palavra_anterior = round_key_atual_loop[:, l]
            round_key_atual_loop[0, l + 1] = palavra_round_key_anterior[0] ^ palavra_anterior[0]
            round_key_atual_loop[1, l + 1] = palavra_round_key_anterior[1] ^ palavra_anterior[1]
            round_key_atual_loop[2, l + 1] = palavra_round_key_anterior[2] ^ palavra_anterior[2]
            round_key_atual_loop[3, l + 1] = palavra_round_key_anterior[3] ^ palavra_anterior[3]

        lista_round_keys.append(round_key_atual_loop)

        #print(f"**** RoundKey={round_key_atual_pos} ****")
        #imprimir_matriz_hex(round_key_atual_loop)

        # no final do loop, atualiza o valor da roundkey
        round_key_atual_pos = round_key_atual_pos + 1

    return lista_round_keys

def rotacionar_bytes(palavra):
    aux = palavra.copy()
    aux[0] = palavra[1]
    aux[1] = palavra[2]
    aux[2] = palavra[3]
    aux[3] = palavra[0]
    return aux

def obter_posicao_no_s_box(char):
    linha = char >> 4
    coluna = char & 0x0F
    return linha, coluna