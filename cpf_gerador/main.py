from random import randint

print('#########################################################################')
print('\t\t\tVALIDAÇÃO/GERADOR DE CPF')
print('#########################################################################')

while True:
    op = input('\t\t\t1.Validar CPF\n\t\t\t2.Gerar CPF\n')
    if not op == '1' and not op == '2':
        print('ERRO!!! Digite uma opção válida!\n')
        continue
    if op == '1':
        cpf_digitado = input(
            'Digite um cpf para ser validado(apenas números): ')

        if not cpf_digitado.isnumeric():  # verifica se o usuario digitou apenas números
            print('Erro!!! Digite apenas números')
            continue
        if len(cpf_digitado) < 11 or len(cpf_digitado) > 11:  # verifica a quantidade de digitos
            print('Erro!! O cpf deve conter 11 digitos')
        cpf_modificado = list(cpf_digitado[0:9])

        num = 10
        soma_total_1 = 0
        for pegar_num in cpf_modificado:  # laço para descobrir o digito1
            pegar_num = int(pegar_num)
            soma_total_1 = (pegar_num*num)+soma_total_1
            num -= 1
            if num == 1:
                break

        conta = 11-(soma_total_1 % 11)
        if conta > 9:
            digito_1 = 0
        else:
            digito_1 = conta
        digito_1 = str(digito_1)
        cpf_modificado.append(digito_1)

        num = 11
        soma_total_2 = 0
        for pegar_num in cpf_modificado:
            pegar_num = int(pegar_num)
            soma_total_2 = (pegar_num*num)+soma_total_2
            num -= 1
            if num == 1:
                break

        conta = 11-(soma_total_2 % 11)
        if conta > 9:
            digito_2 = 0
        else:
            digito_2 = conta
        digito_2 = str(digito_2)
        cpf_modificado.append(digito_2)
        cpf = cpf_digitado
        cpf_digitado = list(cpf_digitado)

        if cpf_digitado == cpf_modificado:
            print(f'O CPF: {cpf} é valido')
        else:
            print(f'O CPF: {cpf} é inválido')

        op_sair = input('Deseja continuar s/n ? ')
        if op_sair == 'n':
            break
    else:
        numero = str(randint(100000000, 999999999))
        cpf_aleatorio = numero
        cpf_aleatorio = list(cpf_aleatorio)
        num = 10
        soma_total_1 = 0
        for pegar_num in cpf_aleatorio:  # laço para descobrir o digito1
            pegar_num = int(pegar_num)
            soma_total_1 = (pegar_num*num)+soma_total_1
            num -= 1
            if num == 1:
                break

        conta = 11-(soma_total_1 % 11)
        if conta > 9:
            digito_1 = 0
        else:
            digito_1 = conta
        digito_1 = str(digito_1)
        cpf_aleatorio.append(digito_1)

        num = 11
        soma_total_2 = 0
        for pegar_num in cpf_aleatorio:
            pegar_num = int(pegar_num)
            soma_total_2 = (pegar_num*num)+soma_total_2
            num -= 1
            if num == 1:
                break

        conta = 11-(soma_total_2 % 11)
        if conta > 9:
            digito_2 = 0
        else:
            digito_2 = conta
        digito_2 = str(digito_2)
        cpf_aleatorio.append(digito_2)
        cpf = "".join(cpf_aleatorio)
        print(f'O CPF gerado é: {cpf}')

    op_sair = input('Deseja continuar s/n ? ')
    if op_sair == 'n':
        break