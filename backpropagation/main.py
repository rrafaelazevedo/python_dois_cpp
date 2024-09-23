from modelo.bp import BackPropagation
import numpy as np
import pandas as pd
import streamlit as st
from utils import utilidades
from plotly import express as px
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import datasets

def main():
    
    st.title("Rede Neural com BackPropagation")
    st.write("""O modelo BackPropagation é um algoritmo de 
             treinamento supervisionado para redes neurais 
             artificiais de múltiplas camadas""")

    st.sidebar.header("Configurações da Base de Dados")

    dados_importar = st.sidebar.selectbox("Selecione uma base de dados",
                                          ["MNIST", "Iris", "Breast Cancer"])
    
    if dados_importar == "MNIST":
        dataset = datasets.load_digits()
        X = dataset.data
        y = dataset.target
    elif dados_importar == "Iris":
        dataset = datasets.load_iris()
        X = dataset.data
        y = dataset.target
    elif dados_importar == "Breast Cancer":
        dataset = datasets.load_breast_cancer()
        X = dataset.data
        y = dataset.target
    
    X = np.atleast_2d(X)
    y = np.atleast_2d(y).T

    qtd_dados = X.shape[0]
    
    st.write(f"""**Base de Dados**: {dados_importar} - {X.shape}""")
    st.dataframe(np.concatenate([X, y], axis=1), width=800)

    tipo_problema = st.sidebar.radio("Tipo de problema",
                                    ("Classificação", "Regressão"))
    
    pct_teste = st.sidebar.slider("Porcentagem de dados para teste",
                                    min_value=0.1, max_value=0.3, 
                                    value=0.3)
    
    st.sidebar.text(f"treino: {(1 - pct_teste) * qtd_dados:.0f} - teste: {pct_teste * qtd_dados:.0f}")
    
    normalizar_entradas = st.sidebar.checkbox("Normalizar entradas")
    
    tratamento_saida = st.sidebar.radio("Normalizar ou binarizar saídas?", 
                                        ("Normalizar", "Binarizar", "Nenhum"))
    
    st.sidebar.divider()

    st.sidebar.header("Parâmetros do modelo")

    qtd_camadas = st.sidebar.slider("Quantidade de camadas escondidas",
                                    min_value=1, max_value=10, value=1)
    
    camadas = []
    for i in range(qtd_camadas):
        neuronios_camada = st.sidebar.number_input(f"Neurônios na camada {i+1}", 
                                      min_value=1, value=1,
                                      key=f"camada{i}")
        camadas.append(neuronios_camada)
    
    lr = st.sidebar.number_input("Taxa de aprendizado",
                                    min_value=0.0001, value=0.01)
    
    decaimento = st.sidebar.number_input("Decaimento da taxa de aprendizado",
                                    min_value=0.000001, value=0.0001,
                                    format="%.6f")
    
    epocas = st.sidebar.number_input("Épocas de treinamento",
                                    min_value=1, value=100)
    
    st.sidebar.divider()

    treinar = st.sidebar.button("Treinar modelo")

    if treinar:

        if normalizar_entradas:
            X = utilidades.normalizacao_min_max(X)
        
        if tratamento_saida == "Normalizar":
            y = utilidades.normalizacao_min_max(y)
        elif tratamento_saida == "Binarizar":
            lb = LabelBinarizer()
            y = lb.fit_transform(y)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=pct_teste)
        
        model = BackPropagation(X_train, y_train, camadas, lr, decaimento,)
        model.treinar(epocas=epocas)
        
        preds = model.predizer(X_test)
        
        if tratamento_saida == "Normalizar":
            preds = utilidades.desnormalizacao_min_max(preds, y)
            y_test = utilidades.desnormalizacao_min_max(y_test, y)
        elif tratamento_saida == "Binarizar":
            preds = lb.inverse_transform(preds)
            y_test = lb.inverse_transform(y_test)
        
        st.divider()
        st.write(f"**Relatório de resultados**")

        if tipo_problema == "Regressão":
            # st.write(f"R²: {utilidades.r_quadrado(y_test, preds)}")
            st.info(f":information_source: R²: {utilidades.r_quadrado(y_test, preds)}")
        elif tipo_problema == "Classificação":
            # st.write(classification_report(y_test, preds), output_dict=True)
            df_report = pd.DataFrame(
                classification_report(y_test, preds, output_dict=True)
            ).T
            st.dataframe(df_report, width=800)

        
        # plotar o erro geral num gráfico bonito com o plotly
        fig = px.line(model.historico_erros, title="Erro Geral por Época")
        fig.update_layout(xaxis_title="Épocas", yaxis_title="Erro Geral")
        st.plotly_chart(fig)
    

if __name__ == "__main__":
    main()