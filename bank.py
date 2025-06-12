saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# Permitir deposito, saque, extrato
def menu():
    print("\nMenu:\n")
    print("[1] Depositar")
    print("[2] Sacar")
    print("[3] Extrato")
    print("[0] Sair")

while True:
    menu()
    opcao = input("\nSelecione a opção desejada: ")
    
    try:
        opcao = int(opcao)
        match opcao:
            # Deve ser possivel depositar valores positivos para conta bancária
            case 1:
                deposito = input("\nDigite o valor a ser depositado: ")
                deposito = float(deposito)
                
                if deposito > 0:
                    saldo += deposito
                    extrato += f"Depósito: R$ {deposito:.2f}\n"
                    print(f"R$ {deposito:.2f} depositado com sucesso.")
                else:
                    print("Valor de depósito inválido.")
            
            # Permitir realizar 3 saques diários        
            case 2:
                saque = input("\nDigite o valor a ser sacado: ")
                saque = float(saque)
                
                if numero_saques < LIMITE_SAQUES:
                    # permitir realizar 3 saques diários
                    if saque <= 0:
                        print("Valor inválido. Digite um valor positivo.")
                    # verifica se existe saldo
                    elif saque > saldo:
                        print("Saldo insuficiente.")
                    # maximo de 500,00 por saque
                    elif saque > limite:
                        print(f"Limite por saque é de R$ {limite:.2f}.")
                    else:
                        saldo -= saque
                        numero_saques += 1
                        extrato += f"Saque: R$ {saque:.2f}\n"
                        print(f"R$ {saque:.2f} sacado com sucesso.")
                else:
                    print(f"Limite diário de {LIMITE_SAQUES} saques excedido. Tente novamente amanhã.")
             
            # imprime o extrato       
            case 3:
                print("\n===== EXTRATO =====")
                print(extrato if extrato else "Nenhuma movimentação realizada.")
                print(f"\nSaldo atual: R$ {saldo:.2f}")
                print("====================")
            
            # para a execução do sistema    
            case 0:
                break
            
            # opção invalida    
            case _:
                print("Opção inválida. Tente novamente.")
                
    except ValueError:
        print("Digite apenas números válidos.")
