import os
import numpy as np
from expansaoChave import expansao_da_chave

def cifrar():
    print("\n=== CIFRAR ===")

    msg = obter_msg_bytes()
    tamanho_bloco = 16
    chave = input("Informe a chave: ").strip()

    round_keys = expansao_da_chave(chave)

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