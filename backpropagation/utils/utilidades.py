import numpy as np

def normalizacao_min_max(entradas: np.ndarray) -> np.ndarray:
    """
    Normaliza as entradas entre 0 e 1

    :param entradas: array 2D com as entradas da base de dados
    :return: array 2D com as entradas normalizadas
    """
    return (entradas - entradas.min()) / (entradas.max() - entradas.min())

def desnormalizacao_min_max(entradas_normalizadas: np.ndarray, 
                            entradas: np.ndarray) -> np.ndarray:
    """
    Desnormaliza as entradas entre 0 e 1

    :param entradas_normalizadas: array 2D com as entradas normalizadas
    :param entradas: array 2D com as entradas da base de dados
    :return: array 2D com as entradas desnormalizadas
    """
    return entradas_normalizadas * (entradas.max() - entradas.min()) + entradas.min()

# funcao para calcular o erro medio absoluto
def r_quadrado(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calcula o coeficiente de determinação (R²) para avaliar a qualidade da predição

    :param y_true: array 2D com as saídas reais da base de dados
    :param y_pred: array 2D com as saídas preditas pela rede neural
    :return: coeficiente de determinação (R²)
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)