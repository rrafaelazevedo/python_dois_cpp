import numpy as np
import streamlit as st

class BackPropagation:

    def __init__(self, entradas: np.ndarray, saidas: np.ndarray, 
                 camadas: list, lr: float, decaimento: float) -> None:

        """
        Inicializa o objeto da rede neural com os parâmetros 
        necessários para o treinamento

        :param entradas: array 2D com as entradas da base de dados a ser ajustada
        :param saidas: array 2D com as saídas da base de dados a ser ajustada
        :param camadas: lista com a quantidade de neurônios em cada camada escondida
        :param lr: taxa de aprendizado para amortizar os gradientes
        :param decaimento: valor para decair a taxa de aprendizado a cada época
        quantidade de épocas
        """

        if len(camadas) < 1:
            raise ValueError("Precisa de pelo menos uma camada escondida para a rede neural")
        
        if entradas.shape[0] != saidas.shape[0]:
            raise ValueError("O número de linhas das entradas e saídas precisam ser iguais")

        self.entradas = entradas
        self.saidas = saidas

        camada_entrada = entradas.shape[1]
        camadas.insert(0, camada_entrada)
        camada_saida = saidas.shape[1]
        camadas.append(camada_saida)
        self.camadas = tuple(camadas)

        self.lr = lr
        self.decaimento = decaimento

        self.pesos = []
        for i in range(0, len(self.camadas) - 1):
            pesos = np.random.uniform(low=-1, high=1, 
                                      size=(self.camadas[i], self.camadas[i + 1]))
            self.pesos.append(pesos)
        
        self.historico_erros = []
    
    def __repr__(self) -> str:
        """
        Retorna a representação de uma instancia da classe BackPropagation
        """
        return f"BackPropagation(entradas={self.entradas.shape}, " \
               f"saidas={self.saidas.shape}, " \
               f"camadas={self.camadas}, " \
               f"lr={self.lr}, " \
               f"decaimento={self.decaimento})"
    
    def sigmoide(self, camada: np.ndarray) -> np.ndarray:
        """
        Calcula a função sigmoide para ativar os neurônios da rede neural

        :param camada: array 2D com os valores das camadas da rede neural
        """
        return 1 / (1 + np.exp(-camada))
    
    def derivada_sigmoide(self, sig: np.ndarray) -> np.ndarray:
        """
        Calcula a derivada da função sigmoide para ajustar os pesos 
        da rede neural

        :param sig: array 2D com as ativações da rede neural
        """
        return sig * (1 - sig)
        
    def propagacao_para_frente(self, camada_entrada: np.ndarray) -> list:
        """
        Realiza a propagação para frente para calcular as ativações 
        da rede neural

        :param camada_entrada: array 2D com as entradas da base de dados
        """

        ativacao = np.atleast_2d(camada_entrada)
        self.ativacoes = [ativacao]

        for pesos in self.pesos:
            proxima_camada = ativacao.dot(pesos)
            ativacao = self.sigmoide(proxima_camada)
            self.ativacoes.append(ativacao)
    
    def propagacao_para_tras(self, camada_saida: np.ndarray) -> tuple:
        """
        Realiza a propagação para trás para ajustar os pesos da rede neural

        :param camada_saida: array 2D com as saídas da base de dados
        """

        derivada_erro = (camada_saida - self.ativacoes[-1]) * (-1)
        derivada_sig_saida = self.derivada_sigmoide(self.ativacoes[-1])
        derivada_vermelha = derivada_erro * derivada_sig_saida

        derivadas_acumuladas = [derivada_vermelha]

        for camada in range(len(self.ativacoes) - 2, 0, -1):
            derivada_camada_sig = \
                self.derivada_sigmoide(self.ativacoes[camada])
            derivada_camada = self.pesos[camada].T
            derivada_anterior = derivadas_acumuladas[-1]

            derivada_laranja = derivada_camada * derivada_camada_sig
            derivada_acumulada = derivada_anterior.dot(derivada_laranja)
            derivadas_acumuladas.append(derivada_acumulada)

        derivadas_acumuladas = derivadas_acumuladas[::-1]

        for indice_pesos in range(0, len(self.pesos)):
            derivada_azul = self.ativacoes[indice_pesos].T
            derivada_acumulada = derivadas_acumuladas[indice_pesos]
            gradiente = derivada_azul.dot(derivada_acumulada)

            self.pesos[indice_pesos] += -self.lr * gradiente

    def predizer(self, entradas: np.ndarray) -> np.ndarray:
        """
        Prediz as saídas com base nas entradas fornecidas e os pesos 
        atuais da rede neural

        :param entradas: array 2D com as entradas a serem preditas
        """
        self.propagacao_para_frente(entradas)
        return self.ativacoes[-1]
    
    def calcula_erro_geral(self) -> float:
        """
        Calcula o erro geral da rede neural para a base de dados
        """

        saidas_preditas = self.predizer(self.entradas)

        erros = 0.50 * (saidas_preditas - self.saidas) ** 2
        erro_geral = np.mean(erros)

        return erro_geral
        
    
    def treinar(self, epocas):
        """
        Treina a rede neural com base nos parâmetros fornecidos

        :param epocas: quantidade de épocas para treinar a rede neural
        :param mostrar_resultados_a_cada: porcentagem de épocas para mostrar
        """

        # fazer uma barra de progresso no streamlit
        texto_progresso = "Treinando a rede neural..."
        barra = st.progress(0, texto_progresso)
        
        for epoca in range(epocas):

            for iteracao in range(len(self.entradas)):

                camada_entrada = self.entradas[iteracao]
                self.propagacao_para_frente(camada_entrada=camada_entrada)

                camada_saida = self.saidas[iteracao]                
                self.propagacao_para_tras(camada_saida=camada_saida)

            ultimo_erro = self.calcula_erro_geral()
            self.historico_erros.append(ultimo_erro)

            self.lr = self.lr * (1 - self.decaimento)

            barra.progress(value=(epoca + 1) / epocas, 
                           text=texto_progresso + \
                           f"""{epoca + 1}/{epocas} ({(epoca + 1) / epocas:.2%}) | 
                           Erro: {ultimo_erro:.4f} | 
                           Taxa de aprendizado: {self.lr:.6f}""")


