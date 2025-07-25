# Variaveis

log_entradas=[]
tentativas=[]

def inserir_dados():
    """
    Função para coletar novos dados.
    Retorna um dicionário com os dados inseridos ou None se o usuário optar por voltar.
    """
    print("\n--- Inserir Novos Dados ---")
    print("Digite 'voltar' a qualquer momento para retornar ao menu principal.")

    local = input("Qual o nome do local? ").strip()
    if local.lower() == 'voltar':
        return None # Indica que o usuário quer voltar

    while True: # Loop para garantir que o número de ovos seja um inteiro válido
        num_ovos_str = input("Número de ovos? ")
        if num_ovos_str.lower() == 'voltar':
            return None
        try:
            numero_de_ninhos = int(num_ovos_str)
            break # Sai do loop se a conversão for bem-sucedida
        except ValueError:
            print("Valor incorreto para o número de ovos. Por favor, digite um número inteiro.")

    estatus = input("Status? ").strip()
    if estatus.lower() == 'voltar':
        return None

    # Retorna os dados como um dicionário
    return {"local": local, "numero_de_ninhos": numero_de_ninhos, "estatus": estatus}


#bloco_menu_principal

while True:
    print('==========================================================================')
    print('        TURTLE LAB v.001 🐢')
    print("1- Inserir novos dados")
    print("2- Ver estatisticas ")
    print("3- Ver log de entradas")
    print("4- Corrigir uma entrada")
    print("0- sair")

    try:
        #entrada
        opt_menu=int(input('Digite uma opção do menu:  '))
    except ValueError:
        print('\nVALOR INCORRETO, digite uma opção válida')
        continue

    match opt_menu:
        case 1:
           # print("\nInserindo novos dados!")
            inserir_dados()
        case 2:
            print("\nEstatisticas atuais")
        case 3:
            print("\nLog de entradas")
        case 4:
            print("\nInserindo novos dados!")
        case 0:
            print("Terminando")
            break