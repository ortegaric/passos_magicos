# Passos Mágicos Dashboard

# Ricardo Ortea - FIAP - PósTech Data Analytics - 2024

## Bibliotecas

import pandas as pd 

import plotly.express as px

import streamlit as st 

## Configurações

st.set_page_config(page_title='Passos Mágicos', layout='wide', initial_sidebar_state='collapsed')

## Dados

dados = pd.read_csv('./data/dados_pede.csv', sep=';', index_col='id')

indicadores = ['ian', 'ida', 'ieg', 'iaa', 'ips', 'ipp', 'ipv', 'inde']

fases = [0, 1, 2, 3, 4, 5, 6, 7, 8]

dados_por_ano = dados[['ano', 'ian', 'ida', 'ieg', 'iaa', 'ips', 'ipp', 'ipv', 'inde']].groupby('ano', as_index=False).mean(numeric_only=True).round(2)

dados_atuais = dados[dados.ano == dados.ano.max()]

dados_ano_anterior = dados[dados.ano == dados.ano.max()-1]

alunos =  dados.aluno.values.tolist()

## Elementos da aplicação web

### Header

st.title('Passos Mágicos')

### Sidebar: Controles

with st.sidebar:

    st.sidebar.title('Controles', help='Filtros para as abas de análises dinâmicas e alunos')

    controle_indicadores = st.multiselect('Indicadores', indicadores, default=indicadores, help='Seleciona os indidicadores')

    controle_fase = st.multiselect('Fases', fases, default=fases, help='Seleciona a fase' )

    controle_ano = st.slider('Anos', min_value=dados.ano.min(), max_value=dados.ano.max(), step=1, help='Seleciona o período')

    controle_bolsista = st.radio('Instituições', ['Rede Pública', 'Rede Privada'], index=0, help='Seleciona as intituições')

    controle_aluno = st.selectbox('Aluno', alunos, index=0, help='Seleciona um aluno')

    dados_filtrados = dados[
        (dados.fase.isin(controle_fase)) &
        (dados.ano >= controle_ano) &
        (dados.bolsista == 0 if controle_bolsista == 'Rede Pública' else dados.bolsista == 1)
    ]

    dados_filtrados_por_ano = dados_filtrados.groupby('ano', as_index=False).mean(numeric_only=True).round(2)

    dados_do_aluno = dados[dados.aluno.isin([controle_aluno])]

### Gráficos
    
fig_indicadores_atual = px.bar(dados_por_ano.iloc[-1:],
                               y=indicadores, x='ano',
                               labels={'value':'Indicador', 'variable':'Indicadores'},
                               barmode='group', text_auto=True)
fig_indicadores_atual.update_layout(xaxis=dict(tickmode='array', tickvals=dados.ano.values.tolist()))


fig_indicadores_filtro = px.line(dados_filtrados_por_ano, 
                                y=controle_indicadores, x='ano',
                                markers=True,
                                labels={'value':'Indicador', 'variable':'Indicadores'})
fig_indicadores_filtro.update_layout(xaxis=dict(tickmode='array', tickvals=dados.ano.values.tolist()))


fig_indicadores_filtro_bar = px.bar(dados_filtrados_por_ano,
                               y=indicadores, x='ano',
                               labels={'value':'Indicador', 'variable':'Indicadores'},
                               barmode='group', text_auto=True)
fig_indicadores_filtro_bar.update_layout(xaxis=dict(tickmode='array', tickvals=dados.ano.values.tolist()))


fig_indicadores_aluno = px.bar(dados_do_aluno.iloc[-1:],
                               y=indicadores, x='ano',
                               labels={'value':'Indicador', 'variable':'Indicadores'},
                               barmode='group', text_auto=True)
fig_indicadores_aluno.update_layout(xaxis=dict(tickmode='array', tickvals=dados.ano.values.tolist()))


fig_indicadores_aluno_tempo = px.line(dados_do_aluno,
                                      y=indicadores, x='ano',
                                      markers=True,
                                      labels={'value':'Indicador', 'variable':'Indicadores'})
fig_indicadores_aluno_tempo.update_layout(xaxis=dict(tickmode='array', tickvals=dados.ano.values.tolist()))

### Layout

tab1, tab2, tab3, tab4 = st.tabs(['Dashboard', 'Análises', 'Alunos', 'Dados'])

with tab1:

    st.header(f'Dados de {dados_atuais.ano.unique()[0]}')

    st.text('Valores comparados aos do ano anterior')

    with st.container():

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric('ian', value=f'{dados_atuais.ian.mean():.2f}', delta=f'{dados_atuais.ian.mean()-dados_ano_anterior.ian.mean():.2f}')

            st.metric('ips', value=f'{dados_atuais.ips.mean():.2f}', delta=f'{dados_atuais.ips.mean()-dados_ano_anterior.ips.mean():.2f}')

        with col2:

            st.metric('ida', value=f'{dados_atuais.ida.mean():.2f}', delta=f'{dados_atuais.ida.mean()-dados_ano_anterior.ida.mean():.2f}')

            st.metric('ipp', value=f'{dados_atuais.ipp.mean():.2f}', delta=f'{dados_atuais.ipp.mean()-dados_ano_anterior.ipp.mean():.2f}')      

        with col3:

            st.metric('ieg', value=f'{dados_atuais.ieg.mean():.2f}', delta=f'{dados_atuais.ieg.mean()-dados_ano_anterior.ieg.mean():.2f}')

            st.metric('ipv', value=f'{dados_atuais.ipv.mean():.2f}', delta=f'{dados_atuais.ipv.mean()-dados_ano_anterior.ipv.mean():.2f}') 

        with col4:

            st.metric('iaa', value=f'{dados_atuais.iaa.mean():.2f}', delta=f'{dados_atuais.iaa.mean()-dados_ano_anterior.iaa.mean():.2f}')

            st.metric('inde', value=f'{dados_atuais.inde.mean():.2f}', delta=f'{dados_atuais.inde.mean()-dados_ano_anterior.inde.mean():.2f}')

    st.plotly_chart(fig_indicadores_atual, use_container_width=True)

    with st.expander('Saiba mais sobre os indicadores:'):

        st.markdown('**ian:** Indicador de Adequação de Nível')

        st.markdown('**ida:** Indicador de Desempenho Acadêmico')

        st.markdown('**ieg:** Indicador de Engajamento')

        st.markdown('**iaa:** Indicador de Autoavaliação')

        st.markdown('**ips:** Indicador Psicosocial')

        st.markdown('**ipp:** Indicador Psicopedagógico')

        st.markdown('**ipv:** Indicador de Ponto de Virada')

        st.markdown('**inde:** Indicador de Desenvolvimento Educacional')

with tab2:

    st.header(f'Análises dinâmicas', help='Utilize o controle na barra lateral para selecionar um aluno')

    st.text('Valores médios dos indicadores para os filtros selecionados')

    with st.container():

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric('ian', value=f'{dados_filtrados.ian.mean():.2f}')

            st.metric('ips', value=f'{dados_filtrados.ips.mean():.2f}')

        with col2:

            st.metric('ida', value=f'{dados_filtrados.ida.mean():.2f}')

            st.metric('ipp', value=f'{dados_filtrados.ipp.mean():.2f}')      

        with col3:

            st.metric('ieg', value=f'{dados_filtrados.ieg.mean():.2f}')

            st.metric('ipv', value=f'{dados_filtrados.ipv.mean():.2f}') 

        with col4:

            st.metric('iaa', value=f'{dados_filtrados.iaa.mean():.2f}')

            st.metric('inde', value=f'{dados_filtrados.inde.mean():.2f}')

    if dados_filtrados_por_ano.shape[0] >= 2:

        st.plotly_chart(fig_indicadores_filtro, use_container_width=True)

    else:

        st.plotly_chart(fig_indicadores_filtro_bar, use_container_width=True)

with tab3:

    st.header('Dados do aluno', help='Utilize o controle na barra lateral para selecionar um aluno')

    st.text('Cada linha é uma vida')

    st.markdown('---')

    with st.container():

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric('aluno', value=controle_aluno)

        with col2:

            st.metric('Ano', value=dados_do_aluno.ano.iloc[-1])

        with col3:

            st.metric('fase', value=dados_do_aluno.fase.iloc[-1])

        with col4:

            st.metric('pedra', value=dados_do_aluno.inde_pedra.iloc[-1])

    st.markdown('---')

    with st.container():

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric('ian', value=f'{dados_do_aluno.ian.iloc[-1]:.2f}', delta=f'{dados_do_aluno.ian.iloc[-1]-dados_do_aluno.ian.iloc[-2]:.2f}' if len(dados_do_aluno.ian) >=2 else '')

            st.metric('ips', value=f'{dados_do_aluno.ips.iloc[-1]:.2f}', delta=f'{dados_do_aluno.ips.iloc[-1]-dados_do_aluno.ips.iloc[-2]:.2f}' if len(dados_do_aluno.ips) >=2 else '')

        with col2:

            st.metric('ida', value=f'{dados_do_aluno.ida.iloc[-1]:.2f}', delta=f'{dados_do_aluno.ida.iloc[-1]-dados_do_aluno.ida.iloc[-2]:.2f}' if len(dados_do_aluno.ida) >=2 else '')

            st.metric('ipp', value=f'{dados_do_aluno.ipp.iloc[-1]:.2f}', delta=f'{dados_do_aluno.ipp.iloc[-1]-dados_do_aluno.ipp.iloc[-2]:.2f}' if len(dados_do_aluno.ipp) >=2 else '')    

        with col3:

            st.metric('ieg', value=f'{dados_do_aluno.ieg.iloc[-1]:.2f}', delta=f'{dados_do_aluno.ieg.iloc[-1]-dados_do_aluno.ieg.iloc[-2]:.2f}' if len(dados_do_aluno.ieg) >=2 else '')

            st.metric('ipv', value=f'{dados_do_aluno.ipv.iloc[-1]:.2f}', delta=f'{dados_do_aluno.ipv.iloc[-1]-dados_do_aluno.ipv.iloc[-2]:.2f}' if len(dados_do_aluno.ipv) >=2 else '')

        with col4:

            st.metric('iaa', value=f'{dados_do_aluno.iaa.iloc[-1]:.2f}', delta=f'{dados_do_aluno.iaa.iloc[-1]-dados_do_aluno.iaa.iloc[-2]:.2f}' if len(dados_do_aluno.iaa) >=2 else '')

            st.metric('inde', value=f'{dados_do_aluno.inde.iloc[-1]:.2f}', delta=f'{dados_do_aluno.inde.iloc[-1]-dados_do_aluno.inde.iloc[-2]:.2f}' if len(dados_do_aluno.inde) >=2 else '')

    st.plotly_chart(fig_indicadores_aluno, use_container_width=True)

    if dados_do_aluno.shape[0] >= 2:

        st.plotly_chart(fig_indicadores_aluno_tempo, use_container_width=True)

with tab4:

    st.header('Dados do estudo')

    st.text('Pesquise ou faça o download dos dados em formato CSV')

    st.dataframe(dados)


## Referências
    
    ### https://docs.streamlit.io/library/api-reference

