import os
import numpy as np

S_BOX = [
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
]

ROUND_CONSTANT_MAP = {
    1: 0x01,
    2: 0x02,
    3: 0x04,
    4: 0x08,
    5: 0x10,
    6: 0x20,
    7: 0x40,
    8: 0x80,
    9: 0x1B,
    10: 0x36
}

def expansao_da_chave(chave):
    # usar aqui pra quando a chave for um texto para teste
    lista_de_caracteres = [ord(c) for c in list(chave)]

    # usar aqui para chave conforme pede no arquivo do trabalho, ex: 20,1,94,33,199,0,48,9,31,94,112,40,59,30,100,248
    #lista_de_caracteres = chave.split(',') # criar lista dos char
    #lista_de_caracteres_hex = [] # transforma para hex
    #for num_str in lista_de_caracteres:
    #    num_int = int(num_str)
    #    lista_de_caracteres_hex.append(f'0x{num_int:02X}')

    matriz_estado_original = np.array(lista_de_caracteres).reshape((4, 4), order='F') # cria a matriz estado

    print(matriz_estado_original)

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

        # no final do loop, atualiza o valor da roundkey
        round_key_atual_pos = round_key_atual_pos + 1

    aaa = 1

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




def cifrar():
    print("\n=== CIFRAR ===")

    msg = obter_msg_bytes()
    tamanho_bloco = 16
    chave = input("Informe a chave: ").strip()

    expansao_da_chave(chave)

    # aqui fazer logica para colocar o padding no final da msg

    for i in range(0, len(msg), tamanho_bloco):
        bloco = msg[i: i + tamanho_bloco]

def obter_msg_bytes():
    while True:
        print("1 - Texto")
        print("2 - Arquivo")
        tipo_mensagem = input("Informe o que deseja cifrar: ").strip()
        if tipo_mensagem == '1':
            msg_text = input("Digite a sua mensagem: ")
            return msg_text.encode('utf-8')
        elif tipo_mensagem == '2':
            caminho_file = input("Informe o caminho completo para o arquivo: ")
            if not os.path.exists(caminho_file):
                print(f"\nErro: O arquivo '{caminho_file}' não foi encontrado. Tente novamente.\n")
            else:
                with open(caminho_file, 'rb') as file:
                    conteudo_bytes = file.read()
                    return conteudo_bytes
        else:
            print("\n=== Opção inválida ===\n")

def decifrar() :
    print("tchau")


while True:
    print("\n=== MENU PRINCIPAL ===")
    print("1 - Cifrar mensagem")
    print("2 - Decifrar mensagem")
    print("0 - Sair")
    
    opcao = input("Escolha uma opção: ").strip()

    if opcao == '1' or opcao.lower() == 'c':
        cifrar()
    elif opcao == '2' or opcao.lower() == 'd':
        decifrar()
    elif opcao == '0':
        print("Saindo do programa...")
        break
    else:
        print("Opção inválida! Tente novamente.")

# pergunta se é decifrar ou cifrar

# 1 - expandir chaves
# 2 - dividir mensagem em blocos
# 3 - preencher ultimo bloco

# 4 - loop
# 4.1 - cifrar bloco
# 4.2 - persistir



# matriz