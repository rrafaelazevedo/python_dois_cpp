import pandas as pd
import numpy as np

def gerar_visualizacao_escola(prob, materias:list, salas:list, 
                              momentos:list, dias:list) -> dict:
    """
    :param prob é o objeto do problema montado com a FO e as restrições
    :param materias é o objeto 'list' com as matérias do problema
    :param salas é o objeto 'list' com as salas de aulas do problema
    :param momentos é o objeto 'list' com os momentos do problema
    :param dias é o objeto 'list' com os dias do problema

    :retorna um dicionário com os dataframes associados com as salas de aula.
    Por exemplo:

    6a: seg     ter     qua     qui
        mat     mat     por     cie
        por     mat     geo     por
                    ...
    
    6b: seg     ter     qua     qui
        por     por     cie     geo
        mat     geo     cie     mat
                    ...
    """

    # cria o dicionário e cria os dataframes vazios (que serão preenchidos abaixo)
    salas_df = {}
    for sala in salas:
        df_vazio = pd.DataFrame([], columns=dias, index=momentos)
        salas_df[sala] = df_vazio
    
    # Itera as variáveis do problema
    for variavel in prob.variables():

        # se a variável for igual a '1' (vai acontecer a aula)
        if variavel.varValue == 1:
            
            # o nome da variável vem no formato: H_(0,_0,_0,_0) que é convertido
            # pela lógica abaixo para uma lista: ['0', '0', '0', '0']
            indices_splitado = \
                variavel.name.replace("H_", "").replace("(", "").replace(")", "").split(",_")

            # a lista ['0', '0', '0', '0'] é convertido na lista [0, 0, 0, 0]
            # pela lógica abaixo
            id_materia, id_sala, id_momento, id_dia = list(map(int, indices_splitado))

            # converte os 'ids' em nomes das variáveis
            nm_materia = materias[id_materia]
            nm_sala = salas[id_sala]
            nm_momento = momentos[id_momento]
            nm_dia = dias[id_dia]

            # preenche as configurações da aula para o dataframe anteriormente vazio
            salas_df[nm_sala].loc[nm_momento, nm_dia] = nm_materia

    return salas_df

def gerar_visualizacao_professores(salas_df:dict, 
                                    materias:list, salas:list, 
                                    momentos:list, dias:list):
    
    """
    :param salas_df é um dicionário com dataframes. Esse objeto será o mesmo da saída
    da função 'gerar_visualizacao_escola'

    :param materias é o objeto 'list' com as matérias do problema
    :param salas é o objeto 'list' com as salas de aulas do problema
    :param momentos é o objeto 'list' com os momentos do problema
    :param dias é o objeto 'list' com os dias do problema

    :retorna um dicionário com os dataframes associados com as matérias.
    Por exemplo:

    mat: seg     ter     qua     qui
          6a      -       -       -
          6a     6b       -       -
                    ...
    
    por: seg     ter     qua     qui
          6b     6b       -       -
           -      -       -       -
                    ...
    """

    # cria o dicionário vazio
    materias_df = {}
    for nm_materia in materias:

        # cria o dataframe vazio para a matéria
        df_materia = pd.DataFrame(data=[], columns=dias, index=momentos)

        # itera todas as salas que a matéria possui aulas
        for nm_sala in salas:

            # pega a tabela de aulas da sala
            df_sala = salas_df[nm_sala]

            # pega os momentos e dias que a matéria dá aulas na sala...
            id_momentos, id_dias = np.where(df_sala == nm_materia)
            pares = zip(id_momentos, id_dias)

            # itera esses momentos e dias
            for id_momento, id_dia in pares:
                nm_momento = momentos[id_momento]
                nm_dia = dias[id_dia]

                # preenche no dataframe anteriormente vazio a sala de aula que o 
                # professor da matéria tem que estar num momento e dia
                df_materia.loc[nm_momento, nm_dia] = nm_sala

        # após preencher todas as salas de aula que o professor da matéria deve
        # dar suas aulas, atualizar o dicionário anteriormente vazio
        materias_df.update({nm_materia: df_materia})

    # após iterar por todas as matérias e todas as salas de aula, retorna o
    # dicionário com os dataframes (tabelas)
    return materias_df

