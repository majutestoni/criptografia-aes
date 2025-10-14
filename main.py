
def cifrar():
    print("oi")
    

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