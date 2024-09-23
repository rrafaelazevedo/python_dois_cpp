from itertools import product
import numpy as np
import pandas as pd

# função para criar todas as linhas de restrição do tipo 1:
# Não é possível haver mais de uma matéria numa mesma sala, momento e dia
def restricao_um(prob, a, b, c, d, dict_variaveis):
    variacao_vertical = list(product(b, c, d))
    variacao_horizontal = list(product(a))

    for i, vv in enumerate(variacao_vertical):
    
        linha_restricao = []
        for vh in variacao_horizontal:
            variavel_array = np.insert(vv, 0, vh)
            variavel_tupla = tuple(variavel_array)
            variavel_pulp = dict_variaveis[variavel_tupla]
            linha_restricao.append(variavel_pulp)

        prob += (sum(linha_restricao) <= 1, f"Restricao_1_{i}")

    return prob

# função para criar todas as linhas de restrição do tipo 2:
# Uma mesma matéria não pode estar em mais de uma sala de aula no mesmo momento e dia
def restricao_dois(prob, a, b, c, d, dict_variaveis):

    variacao_vertical = list(product(a, c, d))
    variacao_horizontal = list(product(b))
    for i, vv in enumerate(variacao_vertical):    
        linha_restricao = []
        for vh in variacao_horizontal:
            variavel_array = np.insert(vv, 1, vh)
            variavel_tupla = tuple(variavel_array)
            variavel_pulp = dict_variaveis[variavel_tupla]
            linha_restricao.append(variavel_pulp)

        prob += (sum(linha_restricao) <= 1, f"Restricao_2_{i}")

    return prob

# função para criar as linhas de restrição do tipo 3:
# Cada matéria pode dar, no máximo, duas aulas por dia e por sala de aula
def restricao_tres(prob, a, b, c, d, dict_variaveis):
    variacao_vertical = list(product(a, b, d))
    variacao_horizontal = list(product(c))
    for i, vv in enumerate(variacao_vertical):    
        linha_restricao = []
        for vh in variacao_horizontal:
            variavel_array = np.insert(vv, 2, vh)
            variavel_tupla = tuple(variavel_array)
            variavel_pulp = dict_variaveis[variavel_tupla]
            linha_restricao.append(variavel_pulp)

        prob += (sum(linha_restricao) <= 2, f"Restricao_3_{i}")

    return prob

# função para criar as linhas de restrição do tipo 4:
# Cada matéria tem um número mínimo de aulas semanais a serem dadas.
def restricao_quatro(prob, a, b, c, d, dict_variaveis, materias, aulas_minimas_semanais):

    variacao_horizontal = list(product(d, c))
    variacao_vertical = list(product(a, b))

    for i, vv in enumerate(variacao_vertical):
        linha_restricao = []
        for j, vh in enumerate(variacao_horizontal):
            variavel_array = np.insert(vv, 2, vh[::-1])
            variavel_tupla = tuple(variavel_array)
            variavel_pulp = dict_variaveis[variavel_tupla]
            linha_restricao.append(variavel_pulp)

        id_materia = vv[0]
        nm_materia = materias[id_materia]
        qtd_aulas_semanais = aulas_minimas_semanais[nm_materia]

        prob += (sum(linha_restricao) >= qtd_aulas_semanais, f"Restricao_4_{i}")

    return prob

# função para criar as linhas de restrição do tipo 5:
# Aplica as restrições do tipo pessoais
def restricao_cinco(prob, dict_variaveis, materias, dias, 
                    momentos, salas, df_restricoes_pessoais):

    contador_restricoes = 0
    for i, linha in df_restricoes_pessoais.iterrows():
        for momento in momentos:
            if linha[momento] == 0:
                id_materia = materias.index(linha['materia'])
                id_momento = momentos.index(momento)
                id_dia = dias.index(linha['dia'])

                for nm_sala in salas:
                    id_sala = salas.index(nm_sala)

                    variavel_pulp = dict_variaveis[(id_materia, id_sala, id_momento, id_dia)]

                    prob += (variavel_pulp == 0, f"Restricao_5_{contador_restricoes}")
                    contador_restricoes += 1
    
    return prob

# a função abaixo cria uma lista com todas as restrições e suas configurações
def monta_lista_restricoes(prob, a, b, c, d, dict_variaveis,
                            aulas_minimas_semanais,
                            materias, salas, momentos, dias,
                            *, df_restricoes_pessoais=None):
    restricoes = [
        {
            "argumentos": [prob, a, b, c, d, dict_variaveis],
            "callable": restricao_um
        },
        {
            "argumentos": [prob, a, b, c, d, dict_variaveis],
            "callable": restricao_dois            
        },
        {
            "argumentos": [prob, a, b, c, d, dict_variaveis],
            "callable": restricao_tres
        },
        {
            "argumentos": [prob, a, b, c, d, dict_variaveis, materias, 
                           aulas_minimas_semanais],
            "callable": restricao_quatro
        }
    ]

    if isinstance(df_restricoes_pessoais, pd.DataFrame):
        restricoes.append(
            {
                "argumentos": [prob, dict_variaveis, materias, dias, 
                                momentos, salas, df_restricoes_pessoais],
                "callable": restricao_cinco
            }
        )
    
    return restricoes