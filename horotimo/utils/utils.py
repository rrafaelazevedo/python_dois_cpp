import pandas as pd
from itertools import product

def gera_tabela_restricoes_pessoais(nm_materias:list, 
                                    nm_momentos:list, 
                                    nm_dias:list) -> pd.DataFrame:
    """
    :param nm_materias é uma lista com os nomes das matérias configuradas
    :param nm_momentos é uma lista com os nomes dos momentos configurados
    :param nm_dias é uma lista com os nomes dos dias configurados

    :retorna o dataframe com materias, momentos e dias para configurar a tabela
    com restrições pessoais
    """

    if len(nm_materias) > 0 and len(nm_momentos) > 0 and len(nm_dias) > 0:
        df = pd.DataFrame(data=product(nm_materias, nm_dias), columns=["materia", "dia"])
        for momento in nm_momentos:
            df[momento] = None
    
        return df