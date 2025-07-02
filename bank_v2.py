# Permitir deposito, saque, extrato, casdastrar usuário e cadastrar conta corrente.
import time
from datetime import datetime

def menu():
    while True:
        print("\n================= Menu =================\n")
        print("\t[1] Depositar")
        print("\t[2] Sacar")
        print("\t[3] Extrato")
        print("\t[4] Cadastrar novo usuário: ")
        print("\t[5] Cadastrar nova conta: ")
        print("\t[0] Sair")

        try:
            return int(input("\nSelecione a opção desejada: "))
        except ValueError as error:
            print(f"Entrada inválida. Por favor, digite um número. Detalhes do erro: {error}")
        

def depositar(saldo, extrato):
    try:
        deposito = float(input("\nDigite o valor a ser depositado: "))

        if deposito > 0:
            saldo += deposito
            extrato += f"\tDepósito: R$ {deposito:.2f} ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')})\n"
            print(f"R$ {deposito:.2f} depositado com sucesso.")
        else:
            print("Operação falhou! O valor de depósito deve ser positivo.")
    except ValueError:
        print("Operação falhou! Valor inválido. Digite um número.")
            
    return saldo, extrato

def sacar(*, extrato, saldo, numero_saques, limite, LIMITE_SAQUES):
    try:
        saque = float(input("\nDigite o valor a ser sacado: "))
        
        if saque <= 0:
            print("Operação falhou! O valor de saque deve ser positivo.")
        elif saque > saldo:
            print("Operação falhou! Saldo insuficiente.")
        elif saque > limite:
            print(f"Operação falhou! O limite máximo por saque é de R$ {limite:.2f}.")
        elif numero_saques >= LIMITE_SAQUES:
            print(f"Operação falhou! Limite diário de {LIMITE_SAQUES} saques excedido.")
        else:
            saldo -= saque
            numero_saques += 1
            extrato += f"\tSaque: R$ {saque:.2f} ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')})\n"
            print(f"R$ {saque:.2f} sacado com sucesso.")
    except ValueError:
        print("Operação falhou! Valor inválido. Digite um número.")
            
    return extrato, saldo, numero_saques

def valida_cpf(cpf_str):
    cpf_limpo = cpf_str.replace(".", "").replace("-", "")
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        print("CPF inválido! Digite apenas números e certifique-se de ter 11 dígitos.")
        return False, None
    return True, cpf_limpo

def demonstrativo(extrato, saldo, cpf=None, nome_cliente=None, numero_saques=0):
    print("\t========================= EXTRATO =========================\n")
    """
    if cpf:
        cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        print(f"\tCPF: {cpf_formatado}")
        if nome_cliente:
            print(f"\tCliente: {nome_cliente}")
    """
    print("\t===========================================================")
    print(extrato or "\tNenhuma movimentação realizada.\n")
    print(f"\tNúmero de saques diários: {numero_saques}")
    print(f"\tSaldo atual: R$ {saldo:.2f}\n")
    print("\t===========================================================")

def cadastrar_usuario(lista_usuarios):
    nome = input("Digite o nome completo do novo cliente: ").upper()
    
    try:
        
        cpf_digitado = input("Digite o CPF do cliente (somente números, sem pontos ou traços): ")
        valido, cpf_final = valida_cpf(cpf_digitado)
        
        if not valido:
            print("Cadastro de usuário cancelado devido a CPF inválido.")
            return lista_usuarios 
        
        for usuario in lista_usuarios:
            if usuario["cpf"] == cpf_final: 
                print("CPF já cadastrado. Usuário não adicionado.")
                return lista_usuarios 

        nascimento_str = input("Digite a data de nascimento (dd/mm/aaaa): ")
        nascimento = datetime.strptime(nascimento_str, "%d/%m/%Y")
        
        endereco = input("Digite o endereço no seguinte formato: Logradouro, número, bairro, cidade / sigla estado: ").upper()
        
        novo_usuario = {
            "nome": nome,
            "nascimento": nascimento.strftime("%d/%m/%Y"),
            "cpf": cpf_final, 
            "endereco": endereco         
        }
        
        lista_usuarios.append(novo_usuario)
        print("Usuário cadastrado com sucesso!")
    except ValueError as error:
        print(f"Erro ao cadastrar novo usuário. Verifique o formato da data (dd/mm/aaaa). Detalhe do erro: {error}")
            
    return lista_usuarios

def cadastrar_conta(lista_contas, lista_usuarios):
    if not lista_usuarios:
        print("Nenhum usuário cadastrado. Cadastre um usuário antes de criar uma conta.")
        return lista_contas

    cpf_digitado = input("Digite o CPF do usuário para associar a conta: ")
    valido, cpf_para_busca = valida_cpf(cpf_digitado)

    if not valido:
        print("CPF inválido. Cadastro de conta cancelado.")
        return lista_contas

    usuario_encontrado = next(
        (usuario for usuario in lista_usuarios if usuario["cpf"] == cpf_para_busca), None
    )

    if usuario_encontrado is None:
        print("Usuário não encontrado com o CPF informado. Cadastre o usuário primeiro.")
        return lista_contas

    AGENCIA = "0001"
    numero_conta = len(lista_contas) + 1 

    nova_conta = {
        "agencia": AGENCIA,
        "numero_conta": numero_conta,
        "usuario": usuario_encontrado, 
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0,
    }

    lista_contas.append(nova_conta)
    print(f"Conta cadastrada com sucesso! Agência: {AGENCIA}, Número da conta: {numero_conta}")
    print(f"Titular: {usuario_encontrado['nome']}, CPF: {usuario_encontrado['cpf']} \n")

    return lista_contas

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    
    lista_usuarios = []
    lista_contas = [] 
    
    while True:
        opcao = menu()
    
        match opcao:
            # Deve ser possivel depositar valores positivos para conta bancária
            case 1:
                saldo, extrato = depositar(saldo, extrato)
            
            # Permitir realizar 3 saques diários         
            case 2:
                extrato, saldo, numero_saques = sacar(extrato=extrato, saldo=saldo, numero_saques=numero_saques, limite=limite, LIMITE_SAQUES=LIMITE_SAQUES)
                
            # imprime o extrato       
            case 3:
                demonstrativo(extrato, saldo, numero_saques=numero_saques)
            
            # cadastro de usuarios
            case 4:
                lista_usuarios = cadastrar_usuario(lista_usuarios)
                
            # cadastro de contas     
            case 5:
                lista_contas = cadastrar_conta(lista_contas, lista_usuarios)
            # para a execução do sistema 
            case 0:
                print("Saindo do sistema. Obrigado!")
                break
            
            # opção invalida     
            # NOTA* tbm posso usar default no lugar de case _:
            case _:
                print("Opção inválida. Tente novamente.")
            
        time.sleep(0)
        input("\nPressione Enter para continuar...")

main()
