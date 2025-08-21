# ============================================================
# 🐢 Sistema de Monitoramento de Ninhos - v0.01
# ============================================================

# ============================================================
#                 BASE DE DADOS INICIAL
# ============================================================

ninhos = [
    ['Praia Norte', 102, 'intacto', '🟢 estavel', 12, False],
    ['Praia Central', 89, 'danificado', '🔴 critico', 3, True],
    ['Praia Sul', 120, 'ameaçado', '🟠 sob observaçao', 7, False],
    ['Praia Central', 75, 'intacto', '🟢 estavel', 2, False],
    ['Praia Norte', 60, 'danificado', '🔴 critico', 5, True],
    ['Praia Norte', 144, 'ameaçado', '🔴 critico', 12, True],
    ['Praia Central', 178, 'danificado', '🟠 sob observaçao', 38, False],
    ['Praia Sul', 79, 'intacto', '🔴 critico', 49, True],
    ['Praia Norte', 141, 'danificado', '🟠 sob observaçao', 40, True],
    ['Praia Central', 107, 'danificado', '🟠 sob observaçao', 13, True],
    ['Praia Central', 129, 'intacto', '🔴 critico', 46, True],
    ['Praia Sul', 123, 'ameaçado', '🟢 estavel', 10, True],
    ['Praia Norte', 74, 'danificado', '🔴 critico', 38, True],
    ['Praia Central', 145, 'danificado', '🟠 sob observaçao', 17, False],
    ['Praia Norte', 117, 'ameaçado', '🟢 estavel', 49, True],
    ['Praia Sul', 108, 'ameaçado', '🟢 estavel', 44, True],
    ['Praia Central', 137, 'intacto', '🟠 sob observaçao', 32, True],
    ['Praia Norte', 102, 'danificado', '🟠 sob observaçao', 28, False],
    ['Praia Norte', 66, 'ameaçado', '🔴 critico', 35, True],
    ['Praia Central', 23, 'ameaçado', '🟠 sob observaçao', 24, False],
    ['Praia Norte', 86, 'intacto', '🟠 sob observaçao', 4, True],
    ['Praia Norte', 79, 'ameaçado', '🔴 critico', 18, True],
    ['Praia Norte', 94, 'intacto', '🟠 sob observaçao', 22, False],
    ['Praia Norte', 96, 'danificado', '🔴 critico', 4, True],
    ['Praia Central', 49, 'ameaçado', '🟢 estavel', 1, False],
    ['Praia Norte', 139, 'intacto', '🟢 estavel', 29, True],
    ['Praia Sul', 108, 'ameaçado', '🟠 sob observaçao', 46, False],
    ['Praia Central', 108, 'danificado', '🔴 critico', 28, True]]

# ============================================================
#           CONVERSÃO PARA LISTA DE DICIONÁRIOS
# ============================================================
# Definição dos nomes das colunas para conversão para dicionário
nomes_colunas = ["regiao", "quantidade_ovos", "status", "risco", "dias_para_eclosao", "predadores"]

# Convertar a a lista para uma lista de dicionarios( ninhos--> ninhos_dados)
ninhos_dados = []
for ninho_list in ninhos:
    ninhos_dados.append(dict(zip(nomes_colunas, ninho_list)))

# ============================================================
#           CONSTANTES PARA VALIDAÇÃO DE ENTRADA
# ============================================================

REGIOES_MAP = {
    "1": "Praia Norte",
    "2": "Praia Central",
    "3": "Praia Sul"}
STATUS_MAP = {
    "1": "intacto",
    "2": "ameaçado",
    "3": "danificado"}
RISCO_MAP = {
    "1": "🟢 estavel",
    "2": "🟠 sob observaçao",
    "3": "🔴 critico"}

# Também mantemos as listas originais para uso em outras funções, se necessário
REGIOES_VALIDAS = list(REGIOES_MAP.values())
STATUS_VALIDOS = list(STATUS_MAP.values())
RISCO_VALIDOS = list(RISCO_MAP.values())


# ============================================================
#                 FUNÇÕES DE ESTATÍSTICA
# ============================================================

def total_ninhos(data, risco=None):
    """
    Retorna o número total de ninhos registrados.

    Args:
        data (list)   :  Lista de dicionários contendo os dados dos ninhos.
        risco (str)   :  Filtro, por nivel de risco(estavel,sob observaçao,critico) do ninho.

    returns:
        int ou str    : Número total de ninhos (ou mensagem de erro, se a base estiver vazia).
    """
    if not data:
        return "Nenhum dado disponível para análise de risco."

    if risco is None:
        return len(data)
    risco = risco.lower()
    return sum(1 for ninho in data if ' '.join(ninho['risco'].split()[1:]) == risco)


def media_ovos(data, risco=None):
    """
    Retorna a media de ovos por ninho

    Args:
        data (list)   :  Lista de dicionários contendo os dados dos ninhos.
        risco (str)   :  Filtro, por nivel de risco(estavel,sob observaçao,critico) do ninho.

    returns:
        float ou str  :   Media dos ovos(none se não ouver dados)
    """
    if not data:
        return "Nenhum dado disponível para análise de risco."

    # filtragem por risco
    if risco is not None:
        risco = risco.lower()
        data = [ninho for ninho in data if ' '.join(ninho['risco'].split()[1:]) == risco]
        if not data:
            return None
    total_ovos = sum(ninho['quantidade_ovos'] for ninho in data)
    return total_ovos / len(data)


def ninhos_eclodir(data, days=None):
    """
    Retorna a contagem de ninhos com dias para eclosão igual ou inferior ao especificado.

    Args:
        data (list)   :  Lista de dicionários contendo os dados dos ninhos.
        days(int)     :  Número máximo de dias para eclosão (padrão: 5)

    Returns:
        int           :  Quantidade de ninhos que eclodirão dentro do período especificado
    """
    count = 0
    if days is None:
        for ninho in data:
            if ninho['dias_para_eclosao'] <= 5:
                count += 1
    else:
        for ninho in data:
            if ninho['dias_para_eclosao'] <= days:
                count += 1
    return count


def regiao_risco(data, risco):
    """
    Identifica a(s) regiões) com mais ninhos do risco especificado.

    Args:
        data (list)   :  Lista de dicionários contendo os dados dos ninhos.
        risco (str)   :  Filtro, por nivel de risco(estavel,sob observaçao,critico) do ninho.

    Returns:
        str           :  Mensagem formatada com o resultado da análise
    """
    # Validações iniciais
    if not data:
        return "Nenhum dado disponível para análise de risco."

    if not isinstance(risco, str):
        return "O risco deve ser uma string."

    risco = risco.lower()  # Apenas padroniza minúsculas e espaços

    # Contagem por região
    contagem_regioes = {}
    for ninho in data:
        risco_ninho = ' '.join(ninho['risco'].split()[1:])
        if risco_ninho.lower() == risco:
            regiao = ninho['regiao']
            contagem_regioes[regiao] = contagem_regioes.get(regiao, 0) + 1

    # Verifica se encontrou resultados
    if not contagem_regioes:
        return f"Nenhum ninho classificado como '{risco}' foi encontrado."

    # Encontra o valor máximo
    max_ninhos = max(contagem_regioes.values())
    regioes_top = [regiao for regiao, count in contagem_regioes.items()
                   if count == max_ninhos]

    # Formata a resposta
    if len(regioes_top) == 1:
        return f" {regioes_top[0]} ({max_ninhos} ninhos)"
    else:
        return f" {', '.join(regioes_top)} ({max_ninhos} ninhos cada)"


def ninhos_predadores_status(data, status_input):
    """
    Conta quantos ninhos têm presença de predadores e possuem um determinado status.

    Args:
        data (list): Lista de dicionários contendo os dados dos ninhos.
        status_input (str): Status a ser filtrado (ex: 'intacto', 'danificado').

    Returns:
        int: Número de ninhos com predadores e com o status especificado.
    """
    count = 0
    for ninho in data:
        if ninho['predadores'] is True and ninho['status'] == status_input:
            count += 1
    return count


# ============================================================
#                 Funções do Menu Interativo
# ============================================================


def exibir_opcoes(opcoes_map):
    """Função auxiliar para exibir as opções do mapa."""
    for chave, nome in opcoes_map.items():
        print(f" {chave}) {nome}")


def inserir_novo_ninho():
    """
    Coleta e valida os dados de entrada para registrar um novo ninho de tartaruga.

    O usuário pode digitar 'voltar' a qualquer momento para cancelar a operação.
    Todos os campos são validados antes de serem aceitos.

    Returns:
        dict: Dicionário com os dados do novo ninho no seguinte formato:
            {
                "regiao": str,
                "quantidade_ovos": int,
                "status": str,
                "risco": str,
                "dias_para_eclosao": int,
                "predadores": bool
            }
        None: Se o usuário cancelar a operação.
    """

    print("\n--- Inserir Novo Ninho ---")
    print("Digite 'voltar' a qualquer momento para retornar ao menu principal.")

    regiao = ""
    while True:
        print("\nEscolha a região:")
        exibir_opcoes(REGIOES_MAP)
        regiao_input = input("Digite a numeração correspondente à região: ").lower().strip()
        if regiao_input == 'voltar': return None
        if regiao_input in REGIOES_MAP:
            regiao = REGIOES_MAP[regiao_input]
            break
        print("Opção de região inválida. Tente novamente.")

    quantidade_ovos = 0
    while True:
        try:
            quantidade_ovos_str = input("Quantidade de ovos: ").strip()
            if quantidade_ovos_str.lower() == 'voltar': return None
            quantidade_ovos = int(quantidade_ovos_str)
            if quantidade_ovos <= 0:
                print("Quantidade de ovos deve ser um número positivo.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    status = ""
    while True:
        print("\nEscolha o status:")
        exibir_opcoes(STATUS_MAP)
        status_input = input("Digite a numeração correspondente ao status: ").lower().strip()
        if status_input == 'voltar': return None
        if status_input in STATUS_MAP:
            status = STATUS_MAP[status_input]
            break
        print("Opção de status inválida. Tente novamente.")

    risco = ""
    while True:
        print("\nEscolha o nível de risco:")
        exibir_opcoes(RISCO_MAP)
        risco_input = input("Digite a numeração correspondente ao risco: ").lower().strip()
        if risco_input == 'voltar': return None
        if risco_input in RISCO_MAP:
            risco = RISCO_MAP[risco_input]
            break
        print("Opção de risco inválida. Tente novamente.")

    dias_para_eclosao = 0
    while True:
        try:
            dias_para_eclosao_str = input("Dias para eclosão: ").strip()
            if dias_para_eclosao_str.lower() == 'voltar': return None
            dias_para_eclosao = int(dias_para_eclosao_str)
            if dias_para_eclosao <= 0:
                print("Dias para eclosão deve ser um número positivo.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    predadores = False
    while True:
        predadores_input = input("O ninho apresenta predadores? (Digite 's ou 1' para sim ou 'n ou 0' para não): ").strip().lower()
        if predadores_input == 'voltar': return None
        if predadores_input in ['sim', 's','1']:
            predadores = True
            break
        elif predadores_input in ['nao', 'n','0']:
            predadores = False
            break
        print("Entrada inválida. Por favor, digite para 'sim' ou 'nao'.")

    return {
        "regiao": regiao,
        "quantidade_ovos": quantidade_ovos,
        "status": status,
        "risco": risco,
        "dias_para_eclosao": dias_para_eclosao,
        "predadores": predadores}


def visualizar_relatorio(data):
    """Exibe todos os registros de ninhos em um formato tabular."""
    if not data:
        print("Nenhum registro para exibir.")
        return

    print("\n")
    print(" " * 32 + "RELATORIO DE REGISTROS")
    print("=" * 98)
    print(
        f"{'#' :<4} | {'Região':<15} | {'Ovos':<5} | {'Status':<12} | {'Risco':<20} | {'Dias p/ Ecl.':<15} | {'Predador?':<8} #")
    print("-" * 98)
    for i, ninho in enumerate(data):
        predador_str = "Sim" if ninho['predadores'] else "Não"
        print(
            f"{i + 1:<4} | {ninho['regiao']:<15} | {ninho['quantidade_ovos']:<5} | "
            f"{ninho['status']:<12} | {ninho['risco']:<20} | {ninho['dias_para_eclosao']:<15} | {predador_str:<11}"
        )
    print("=" * 98)


def consultar_estatisticas(data):
    """Exibe todas as estatísticas calculadas."""
    print("\n")
    print("-" * 70)
    print(" " * 3 + "ESTATISTICAS")
    print("-" * 70)
    print(" " * 2 + f"{' Total DE NINHOS:':<40}{total_ninhos(data):>10.0f}")
    print(" " * 2 + f"{' Média de ovos por Ninho com risco 🟢 :':<40}{media_ovos(data, 'estavel'):>10.2f}")
    print(" " * 2 + f"{' NINHOS PRESTES A ECLODIR (dias <= 5):':<40}{ninhos_eclodir(data):>10.0f}")
    print(" " * 2 + f"{' Região com mais ninhos sob RISCO 🔴 :':<40}{regiao_risco(data, 'critico')}")
    print(
        " " * 2 + f"{' Presença de predadores e danificados:':<39} {ninhos_predadores_status(data, 'danificado'):>10.0f}")
    print("-" * 70)

    M = input('Para mais estatisticas, digite 1 : ')
    if M == '1':
        print(" " * 2 + f"{' Total DE NINHOS 🟢 :':<40}{total_ninhos(data, 'estavel'):>10.0f}")
        print(" " * 2 + f"{' Total DE NINHOS 🟠 :':<40}{total_ninhos(data, 'sob observaçao'):>10.0f}")
        print(" " * 2 + f"{' Total DE NINHOS 🔴 :':<40}{total_ninhos(data, 'critico'):>10.0f}")
        print("_______")
        print(" " * 2 + f"{' Média de ovos por Ninho com risco 🟢 :':<40}{media_ovos(data, 'estavel'):>10.2f}")
        print(" " * 2 + f"{' Média de ovos por Ninho com risco 🟠 :':<40}{media_ovos(data, 'sob observaçao'):>10.2f}")
        print(" " * 2 + f"{' Média de ovos por Ninho com risco 🔴 :':<40}{media_ovos(data, 'critico'):>10.2f}")
        print("_______")
        print(" " * 2 + f"{' Região com mais ninhos sob RISCO 🟢 :':<40}{regiao_risco(data, 'Estavel')}")
        print(" " * 2 + f"{' Região com mais ninhos sob RISCO 🟠 :':<40}{regiao_risco(data, 'sob observaçao')}")
        print(" " * 2 + f"{' Região com mais ninhos sob RISCO 🔴 :':<40}{regiao_risco(data, 'critico')}")
        print("_______")
        print(
            " " * 2 + f"{' Presença de predadores e intacto:':<39} {ninhos_predadores_status(data, 'intacto'):>10.0f}")
        print(
            " " * 2 + f"{' Presença de predadores e ameaçado:':<39} {ninhos_predadores_status(data, 'ameaçado'):>10.0f}")
        print(
            " " * 2 + f"{' Presença de predadores e danificados:':<39} {ninhos_predadores_status(data, 'danificado'):>10.0f}")

        print("-" * 70)


# ============================================================
#                 CÓDIGO PRINCIPAL (MAIN)
# ============================================================

tentativas_incorretas = 0
LIMITE_TENTATIVAS = 3

while True:
    print("\n")
    print(" " * 8 + "🐢 SISTEMA DE MONITORAMENTO DE NINHOS ( v 0.01) ")
    print(" " * 8 + "      1- Inserir novos ninhos")
    print(" " * 8 + "      2- Visualizar relatório completo da semana")
    print(" " * 8 + "      3- Consultar estatísticas")
    print(" " * 8 + "      4- Exportar base de dados")
    print(" " * 8 + "      0- Encerrar o sistema")
    print("\n")
    try:

        inicio = int(input(" " * 12 + "Digite uma opção do menu: "))
        # Se a entrada for válida (um número), zera o contador de tentativas incorretas
        tentativas_incorretas = 0
    except ValueError:
        tentativas_incorretas += 1
        print(
            f'\nVALOR INCORRETO! Por favor, digite um número inteiro. Você tem {LIMITE_TENTATIVAS - tentativas_incorretas} tentativas restantes.')
        if tentativas_incorretas >= LIMITE_TENTATIVAS:
            print("\nLimite de tentativas incorretas atingido. Fechando o programa.")
            break
        continue

    # Lidar com opções válidas numericamente, mas fora do menu
    if inicio not in [0, 1, 2, 3, 4]:
        tentativas_incorretas += 1
        print(
            f'\nOPÇÃO INVÁLIDA. Por favor, digite um número de 0 a 3. Você tem {LIMITE_TENTATIVAS - tentativas_incorretas} tentativas restantes.')
        if tentativas_incorretas >= LIMITE_TENTATIVAS:
            print("\nLimite de tentativas incorretas atingido. Fechando o programa.")
            break
        continue
    else:
        # Se a entrada é um número e uma opção válida, zera o contador
        tentativas_incorretas = 0

    # Opções do Menu via Mach case
    match inicio:
        case 1:
            novo_ninho = inserir_novo_ninho()
            if novo_ninho:  # Se o usuário não digitou 'voltar'
                ninhos_dados.append(novo_ninho)
                print("Novo ninho inserido com sucesso!")
            else:
                print("Inserção de ninho cancelada.")
        case 2:
            visualizar_relatorio(ninhos_dados)
            input("\nPressione Enter para retornar ao menu principal...")

        case 3:
            consultar_estatisticas(ninhos_dados)
            input("\nPressione Enter para retornar ao menu principal...")

        case 4:
            print('\n Função em desenvolvimento')
            input("\nPressione Enter para retornar ao menu principal...")

        case 0:
            print("\nEncerrando o sistema. Até mais!")
            break