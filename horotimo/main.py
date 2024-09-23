import pulp as plp
import pandas as pd
import streamlit as st
from formatacoes.gera_tabelas import gerar_visualizacao_professores, gerar_visualizacao_escola
from modelo.horotimo import rodar_modelo
from constantes import materias, salas, momentos, dias
from utils.utils import gera_tabela_restricoes_pessoais

def main():

    # todos os campos são desenhados de cima para baixo, na sequência de aparecimento
    # do código!!! Os componentes podem ser desenhados no documento (parte central da
    # tela) ou na barra lateral (sidebar).
    
    # Componentes são os elementos da tela para preenchimento da tela e inserção de
    # dados da tela para as variáveis do código!!!


    # escreve o título na topo da página
    st.title(body="Horótimo")

    # escreve um texto logo abaixo do título
    st.write("Soluções em Grades Horárias")

    # na barra lateral, cria um componente de digitação de texto. Esse campo deve
    # receber o nome das matérias que deverão ser consideradas pelo modelo
    nm_materia = st.sidebar.text_input(
        label="Insira uma matéria",
        placeholder="Digite o nome da matéria"
    )

    # se o nome da matéria digitada não for 'vazia' e não estiver previamente
    # sido adicionada, incluí-la na lista de materias que serão candidatas a entrar
    # no Horótimo posteriormente
    if nm_materia != "" and nm_materia not in materias:
        materias.append(nm_materia)

    # desenha um campo na barra lateral com as matérias adicionadas pelo campo de
    # texto das matérias. Nesse campo, as matérias selecionadas  serão guardadas 
    # na variável 'nm_materias'. Essa variável será passada para rodar o modelo
    nm_materias = st.sidebar.multiselect(
                                    label="Materias adicionadas:",
                                    options=materias,
                                    default=materias
                                    )
    
    st.sidebar.divider()

    # na barra lateral, cria um componente de digitação de texto. Esse campo deve
    # receber o nome das salas/turmas que deverão ser consideradas pelo modelo
    nm_sala = st.sidebar.text_input(
        label="Insira um sala de aula",
        placeholder="Digite o nome da sala"
    )

    # se o nome da sala/turma digitada não for 'vazia' e não estiver previamente
    # sido adicionada, incluí-la na lista de salas que serão candidatas a entrar
    # no Horótimo posteriormente
    if nm_sala != "" and nm_sala not in salas:
        salas.append(nm_sala)
    
    # desenha um campo na barra lateral com as salas adicionadas pelo campo de
    # texto das salas. Nesse campo, as matérias selecionadas  serão guardadas 
    # na variável 'nm_salas'. Essa variável será passada para rodar o modelo
    nm_salas = st.sidebar.multiselect(
        label="Salas adicionadas:",
        options=salas,
        default=salas
    )

    st.sidebar.divider()

    # na barra lateral, cria um componente de digitação de texto de salas. 
    # Esse campo deve receber o nome dos momentos de aulas que serão candidatas
    # para rodar o modelo
    nm_momento = st.sidebar.text_input(
        label="Insira um momento",
        placeholder="Digite um momento"
    )

    # se o nome do momento digitado não for 'vazio' e não estiver previamente
    # sido adicionado, incluí-lo na lista de momentos que serão candidatos a entrar
    # no Horótimo posteriormente
    if nm_momento != "" and nm_momento not in momentos:
        momentos.append(nm_momento)

    # desenha um campo na barra lateral com os momentos adicionados pelo campo de
    # texto de momentos. Nesse campo, os momentos selecionados  serão guardados 
    # na variável 'nm_momentos'. Essa variável será passada para rodar o modelo
    nm_momentos = st.sidebar.multiselect(
        label="Momentos adicionados",
        options=momentos,
        default=momentos
    )

    st.sidebar.divider()

    # na barra lateral, cria um componente de digitação de texto de dias. 
    # Esse campo deve receber o nome dos dias de aulas que serão candidatos
    # para rodar o modelo
    nm_dia = st.sidebar.text_input(
        label="Insira um dia",
        placeholder="Digite um dia"
    )

    # se o nome do dia digitado não for 'vazio' e não estiver previamente
    # sido adicionado, incluí-lo na lista de dias que serão candidatos a entrar
    # no Horótimo posteriormente
    if nm_dia != "" and nm_dia not in dias:
        dias.append(nm_dia)
    
    # desenha um campo na barra lateral com os dias adicionados pelo campo de
    # texto de dias. Nesse campo, os dias selecionados  serão guardados 
    # na variável 'nm_dias'. Essa variável será passada para rodar o modelo
    nm_dias = st.sidebar.multiselect(
        label="Dias adicionados",
        options=dias,
        default=dias
    )

    st.sidebar.divider()

    # na barra lateral, cria um texto iniciando a seção de aulas mínimas semanais
    # para cada matéria.
    st.sidebar.write(
        "Aulas mínimas semanais por matéria"
    )

    # percorre as matérias selecionadas pelo multiselect das matérias e cria
    # campos de inserção de números para adicionar a quantidade de aulas mínimas
    # semanais para cada matéria (selecionada)
    aulas_minimas_semanais = {}
    for nm_materia in nm_materias:
        aulas_minimas_semanais[nm_materia] = \
        st.sidebar.number_input(
            f"Aulas mínimas {nm_materia}",
            min_value=1,
            max_value=10,
            value=1,
            key=nm_materia
        )
    
    # a função abaixo cria um dataframe com os nomes as matérias, momentos e dias
    # selecionados para o usuário preencher as restrições pessoais. As restrições
    # pessoais são do tipo: o professor da matéria não pode dar aula em determinado
    # dia(s) e momento(s). A função retorna um dataframe se houver matérias, momentos
    # e dias selecionados.
    df = gera_tabela_restricoes_pessoais(
        nm_materias, nm_momentos, nm_dias
    )

    # se a função devolver um objeto do tipo pd.DataFrame, cria um botão para
    # permitir o download do DataFrame na forma de um csv
    if df is not None:
        st.sidebar.download_button(
            label="Baixar o modelo padrão das restrições pessoais",
            data=df.to_csv(index=False, sep=","),
            file_name="restricoes_pessoais.csv",
            mime="text/csv"
        )

    # cria um campo que permite o upload de um arquivo csv com as restrições
    # pessoais. Esse arquivo deve estar no padrão dos dados inseridos anteriormente    
    file = st.sidebar.file_uploader(
        label="Carregue o arquivo de restrições pessoais",
        type="csv"
        )

    # cria um botão na seção de barra lateral
    botao = st.sidebar.button(
        label="Rodar Horótimo"
    )

    # se o usuário clicou no botão, a variável 'botao' recebe True
    if botao == True:
        
        if file is not None:
            # Se o usuário carregou o arquivo de restrições pessoais
            df_restricoes_pessoais = \
            pd.read_csv(file, sep=";")
        else:
            # se o usuário não carregou o arquivo de restrições pessoais
            df_restricoes_pessoais = None

        # chama a função que roda o modelo horotimo passando todas as variáveis
        # necessárias.
        prob = rodar_modelo(
            nm_materias, nm_salas, nm_momentos, nm_dias,
            aulas_minimas_semanais, df_restricoes_pessoais
        )

        # se o modelo resolveu o problema, então: prob.status = 1
        # plp.LpStatus é um dicionário padrão do pulp para traduzir os
        # códigos do problema para uma string.
        # plp.LpStatus = {0: "Not Solved", 1: "Optimal", 2: "Infeasible" ...}
        if plp.LpStatus[prob.status] != "Optimal":
            # mostra uma mensagem de erro na tela se não for Optimal
            st.error(
                ":x: Não foi possível encontrar solução para " \
                "os dados fornecidos"
            )
            return

        # se não entrar no 'if' acima, então o problema foi resolvido (Optimal)

        # cria um subtitulo no documento central
        st.subheader("Visualização da grade por salas")

        # a função 'gerar_visualizacao_escola' retorna os dataframes com as aulas
        # encaixadas para cada sala de aula
        salas_df = gerar_visualizacao_escola(
            prob,
            nm_materias,
            nm_salas,
            nm_momentos,
            nm_dias
        )

        # itera as salas de aula selecionadas e mostra na tela as tabelas das aulas
        for nm_sala in nm_salas:
            df_sala = salas_df[nm_sala]
            st.write(f"Sala: {nm_sala}")
            st.write(df_sala)
        
        # cria mais um subtitulo no documento central
        st.subheader(
            "Visualização da grade por professores."
        )

        # a função 'gerar_visualizacao_professores' retorna um dicionário
        # com dataframes da solução para cada professor (matéria)
        materias_df = gerar_visualizacao_professores(
            salas_df,
            nm_materias,
            nm_salas,
            nm_momentos,
            nm_dias
        )

        # mostra na tela as tabelas da solução para cada professor (matéria)
        for nm_materia in nm_materias:
            df_materia = materias_df[nm_materia]
            st.write(f"Matéria: {nm_materia}")
            st.write(df_materia)
        
        # mostra uma mensagem de sucesso!!!
        st.success(
            ":white_check_mark: Grade horária gerada com sucesso!!"
            )

# se esse arquivo for executado pelo comando 'streamlit run main.py',
# o 'if' abaixo vai entrar e executar a função 'main'!!!
if __name__ == "__main__":
    main()