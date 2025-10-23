import os
import base64

from Algoritmo import *

def cifrarMsg():
    print("\n=== CIFRAR ===")
    msg = b'DESENVOLVIMENTO!'
    chave = 'ABCDEFGHIJKLMNOP'
    cifrar(msg, chave)

    #msg = obter_msg_bytes()
    #chave = input("Informe a chave: ").strip()

def obter_msg_bytes():
    while True:
        print("1 - Texto")
        print("2 - Arquivo")
        tipo_mensagem = input("Informe o que deseja cifrar: ").strip()
        if tipo_mensagem == '1':
            # msg_text = input("Digite a sua mensagem: ")
            # chave_text = input("Digite a chave: ")
            
            # msg = msg_text.encode('utf-8')
            
            msg = b'DESENVOLVIMENTO!'
            chave = bytes([20, 1, 94, 33, 199, 0, 48, 9, 31, 94, 112, 40, 59, 30, 100, 248])
            msg_cifrada = cifrar(msg, chave)
            msg_str = base64.b64encode(msg_cifrada).decode('utf-8')
            print("Mensagem cifrada: " + msg_str)
            return msg_str
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

def decifrarMsg() :
    print("tchau")


obter_msg_bytes()
#
#while True:
#    print("\n=== MENU PRINCIPAL ===")
#    print("1 - Cifrar mensagem")
#    print("2 - Decifrar mensagem")
#    print("0 - Sair")
#    
#    #opcao = input("Escolha uma opção: ").strip()
#    opcao = "c"
#
#    if opcao == '1' or opcao.lower() == 'c':
#        cifrarMsg()
#    elif opcao == '2' or opcao.lower() == 'd':
#        decifrarMsg()
#    elif opcao == '0':
#        print("Saindo do programa...")
#        break
#    else:
#        print("Opção inválida! Tente novamente.")
#
## pergunta se é decifrar ou cifrar
#
## 1 - expandir chaves
## 2 - dividir mensagem em blocos
## 3 - preencher ultimo bloco')

# 4 - loop
# 4.1 - cifrar bloco
# 4.2 - persistir



# matriz