import os
import base64

from Cifrar import Cifrar
from Decifrar import Decifrar

def obter_msg_bytes():
    while True:
        print("1 - Texto")
        print("2 - Decifrar")
        tipo_mensagem = input("Informe o que deseja cifrar: ").strip()
        if tipo_mensagem == '1':
            c = Cifrar()
            # msg_text = input("Digite a sua mensagem: ")
            # chave_text = input("Digite a chave: ")
            
            # msg = msg_text.encode('utf-8')
            
            msg = b'DESENVOLVIMENTO!'
            chave = bytes([20, 1, 94, 33, 199, 0, 48, 9, 31, 94, 112, 40, 59, 30, 100, 248])
            msg_cifrada = c.cifrar(msg, chave)
            msg_str = base64.b64encode(msg_cifrada).decode('utf-8')
            print("Mensagem cifrada: " + msg_str)
            return msg_str
        elif tipo_mensagem == '2':
            d = Decifrar()
            msg_cifrada = input('Informe a mensagem cifrada:')
            chave = bytes([20, 1, 94, 33, 199, 0, 48, 9, 31, 94, 112, 40, 59, 30, 100, 248])
            msg_cifrada = base64.b64decode(msg_cifrada)
            msg = d.decifrar(msg_cifrada, chave)
            print("Mensagem decifrada: " + msg.decode('utf-8'))
            return msg

            # caminho_file = input("Informe o caminho completo para o arquivo: ")
            # if not os.path.exists(caminho_file):
            #     print(f"\nErro: O arquivo '{caminho_file}' não foi encontrado. Tente novamente.\n")
            # else:
            #     with open(caminho_file, 'rb') as file:
            #         conteudo_bytes = file.read()
            #         return conteudo_bytes
        else:
            print("\n=== Opção inválida ===\n")

def decifrarMsg() :
    print("tchau")


obter_msg_bytes()