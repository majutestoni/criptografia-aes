import os
import base64

from Cifrar import Cifrar
from Decifrar import Decifrar

def obter_arquivo(nome_pasta):
    arquivos = [f for f in os.listdir(nome_pasta) if os.path.isfile(os.path.join(nome_pasta, f))]
    return os.path.join(nome_pasta, arquivos[0])

def cifrar_texto(c):
    msg_text = input("Digite a sua mensagem: ")
    msg_bytes = msg_text.encode('utf-8')

    chave = obter_chave()
    msg_cifrada = c.cifrar(msg_bytes, chave)
    msg_str = base64.b64encode(msg_cifrada).decode('utf-8')

    print("Mensagem cifrada: " + msg_str)

def cifrar_arquivo(c):
    caminho_arquivo = obter_arquivo('PARA_CIFRAR')

    with open(caminho_arquivo, 'rb') as f_in:
        arquivo_bytes = f_in.read()

    chave = obter_chave()
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_base, extensao = os.path.splitext(nome_arquivo)
    novo_nome = input(f"Informe o nome do arquivo cifrado sem a extensão (Enter para usar '{nome_arquivo}'): ").strip()
    if not novo_nome:
        novo_nome = nome_arquivo
    else:
        novo_nome = novo_nome + extensao

    arquivo_cifrado = c.cifrar(arquivo_bytes, chave)
    caminho_cifrado = os.path.join('CIFRADO', novo_nome)

    with open(caminho_cifrado, 'wb') as f_out:
        f_out.write(arquivo_cifrado)

    print("Arquivo cifrado! Salvo na pasta 'CIFRADO'")

def decifrar_texto(d):
    msg_cifrada = input('Informe a mensagem cifrada:')
    msg_cifrada_bytes = base64.b64decode(msg_cifrada)
    chave = obter_chave()
    msg_decifrada = d.decifrar(msg_cifrada_bytes, chave)

    print("Mensagem decifrada: " + msg_decifrada.decode('utf-8'))

def decifrar_arquivo(d):
    caminho_arquivo = obter_arquivo('CIFRADO')

    with open(caminho_arquivo, 'rb') as f_in:
        arquivo_bytes = f_in.read()

    chave = obter_chave()
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_base, extensao = os.path.splitext(nome_arquivo)
    novo_nome = input(f"Informe o nome do arquivo decifrado sem a extensão (Enter para usar '{nome_arquivo}'): ").strip()
    if not novo_nome:
        novo_nome = nome_arquivo
    else:
        novo_nome = novo_nome + extensao

    arquivo_decifrado = d.decifrar(arquivo_bytes, chave)
    caminho_decifrado = os.path.join('DECIFRADO', novo_nome)

    with open(caminho_decifrado, 'wb') as f_out:
        f_out.write(arquivo_decifrado)

    print("Arquivo decifrado! Salvo na pasta 'DECIFRADO'")

def menu_cifrar():
    c = Cifrar()
    while True:
        print("\n--- Cifrar ---")
        print("1 - Cifrar Texto")
        print("2 - Cifrar Arquivo")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            cifrar_texto(c)
            break
        elif escolha == '2':
            cifrar_arquivo(c)
            break
        else:
            print("\n Opção inválida")

def menu_decifrar():
    d = Decifrar()
    while True:
        print("\n--- Decifrar ---")
        print("1 - Decifrar Texto")
        print("2 - Decifrar Arquivo")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            decifrar_texto(d)
            break
        elif escolha == '2':
            decifrar_arquivo(d)
            break
        else:
            print("\n Opção inválida")

def criar_pastas():
    os.makedirs('PARA_CIFRAR', exist_ok=True)
    os.makedirs('CIFRADO', exist_ok=True)
    os.makedirs('DECIFRADO', exist_ok=True)

def obter_chave():
    chave_input = input("Informe a chave: ").strip()
    lista = [int(num.strip()) for num in chave_input.split(',')]
    return bytes(lista)

def menu_principal():
    criar_pastas()
    while True:
        print("\n--- Menu Principal ---")
        print("1 - Cifrar")
        print("2 - Decifrar")

        escolha = input("O que deseja fazer? ").strip()

        if escolha == '1':
            menu_cifrar()
        elif escolha == '2':
            menu_decifrar()
        else:
            print("\n Opção inválida")

menu_principal()