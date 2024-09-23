import pulp as plp
from itertools import product
from restricoes.restricoes import monta_lista_restricoes
from pandas import DataFrame

def gerar_prob_horotimo(a, b, c, d):
    """
    :param a é uma coleção com todos os índices das matérias
    :param b é uma coleção com todos os índices das salas de aula
    :param c é uma coleção com todos os índices dos momentos de aula
    :param d é uma coleção com todos os índices dos dias de aula

    :retorna o problema configurado e resolvido (ou não resolvido)
    """

    # gera a combinatória completa de todos os índices de matérias, salas, 
    # momentos e dias
    variaveis_product = product(a, b, c, d)

    # converte o objeto do tipo 'product' para uma lista
    variaveis_list = list(variaveis_product)

    # configura o nome e o tipo do problema (maximização de aulas)
    prob = plp.LpProblem(name="Horotimo", sense=plp.LpMaximize)

    # cria o dicionário das variáveis do tipo 'pulp'
    dict_variaveis = plp.LpVariable.dicts(
                                name="H", 
                                indices=variaveis_list, 
                                cat=plp.LpBinary)
    
    # pega todos os valores do dicionário acima e insere-os na lista abaixo
    variaveis_pulp = []
    for variavel_pulp in dict_variaveis.values():
        variaveis_pulp.append(variavel_pulp)
    
    # adiciona a soma da lista com as variáveis 'pulp' no problema criado
    # anteriormente. Adicionou a FO no problema
    prob += (sum(variaveis_pulp), "Funcao_Objetivo")

    # devolve o objeto prob configurado com a FO, o nome e o tipo do problema
    return prob, dict_variaveis

def rodar_modelo(materias:list, salas:list, momentos:list, dias:list,
                 aulas_minimas_semanais:dict,
                 df_restricoes_pessoais:DataFrame):
    
    """
    :param materias é uma lista com os nomes das matérias configuradas
    :param salas é uma lista com os nomes das salas de aula configuradas
    :param momentos é uma lista com os nomes dos momentos de aula configurados
    :param dias é uma lista com os nomes dos dias de aula configurados
    
    :aulas_minimas_semanais é um dicionário com o número de aulas mínimas
    semanais para cada matéria. Por exemplo: {"mat": 4, "por": 2, "geo": 3, "cie": 3}

    :df_restricoes_pessoais é um dataframe (tabela) com as restrições do tipo pessoais

    :retorna o objeto 'prob' com todas as configurações e resolvido (ou não)
    """

    # converte os nomes das matérias, salas, momentos e dias em seus índices    
    a = range(len(materias))
    b = range(len(salas))
    c = range(len(momentos))
    d = range(len(dias))

    # configura inicialmente o problema (nome, tipo e FO)
    prob, dict_variaveis = \
        gerar_prob_horotimo(a, b, c, d)
    
    # monta uma lista com todas as restrições e suas configurações
    restricoes_rodar = \
        monta_lista_restricoes(prob, a, b, c, d, 
                            dict_variaveis, 
                            aulas_minimas_semanais,
                            materias, salas, momentos, dias,
                            df_restricoes_pessoais=df_restricoes_pessoais
                            )

    # percorre a lista com as restrições e aplica elas no objeto 'prob'
    for restricao_rodar in restricoes_rodar:
        prob = restricao_rodar["callable"](*restricao_rodar["argumentos"])
    
    # configura o solver que será usado na solução do problema e aplica o 
    # solver para tentar resolver o problema
    nm_solver = "PULP_CBC_CMD"
    solver = plp.get_solver(solver=nm_solver)
    prob.solve(solver=solver)

    return prob