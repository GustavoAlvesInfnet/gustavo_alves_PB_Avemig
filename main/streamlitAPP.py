
import streamlit as st
import random
import pandas as pd
from bs4 import BeautifulSoup
import requests

#
import xml.etree.ElementTree as ET
import geopandas as gpd
from shapely.geometry import Point

#
import matplotlib.pyplot as plt

#
from scrapping import *
from LLM import *
from API import *



def chat():
    st.write("Pergunte sobre espécies de aves extintas")

    st.title("Chatbot")

    user_question = st.chat_input("Digite sua pergunta:")

    if user_question:
        # faz uma requisição para a API passando o user question
        headers = {'Content-Type': 'text/plain'}
        response = requests.post('http://localhost:8000/avesCHAT/', data=user_question, headers=headers)

        if response.status_code == 200:
            response_tratada = response.text.replace(r"\n", "\n")
            st.write(f"Chatbot: {response_tratada}")
        else:
            st.write("Erro ao fazer a requisição para a API.")

    

@st.cache_data
def introducao():
    st.title("Avemigos - Programa de análise da vida de aves")

    # Problema
    st.subheader("Curioso para saber mais sobre as aves? Suas famílias e especies? Os seus habitats?")
    st.write("Este projeto consiste em uma solução para aqueles que querem saber mais sobre pássaros mas não sabem por onde começar. Avemigos têm como objetivo dar um norte para qualquer curioso sobre nossos amigos de penas e disseminar informações que podem ajudar o tópico 15 dos Objetivos de Desenvolvimento Sustentável (ODS) da Agenda 2030.")

    # gera um numero aleatorio para escolher uma imagem de aves
    random_number = random.randint(1, 6)
    if random_number == 1:
        subtitle = "Alcedo atthis - Guarda-rios"
    elif random_number == 2:
        subtitle = "Sicalis flaveola - Canário-da-terra-verdadeiro"
    elif random_number == 3:
        subtitle = "Ficedula hypoleuca - Papa-moscas"
    elif random_number == 4:
        subtitle = "Hirundo rustica - Andorinha-das-chaminés"
    elif random_number == 5:
        subtitle = "Ara chloropterus - Arara-vermelha"
    elif random_number == 6:
        subtitle = "Agapornis fischeri - Lovebirds"
    
    st.image(f"./images/{random_number}.jpg", caption=subtitle, width=600)

    st.subheader("Links úteis para as iniciativas e fontes de inspiração do projeto:")
    st.write("https://www.birdlife.org/")
    st.write("https://www.birds.cornell.edu/")
    st.write("https://www.ebird.org/")
    st.write("https://www.wikiaves.com.br")
    st.write("https://avibase.bsc-eoc.org/avibase.jsp?lang=EN")


    st.subheader("Funcionalidades:")
    st.write('''
        \n1. Na aba 'Informações gerais' consiga informações como nome das espécies de uma ordem ou familia, vejam se estão extintas, quem as nomeou e seu país de origem;
        \n2. Em mapa veja um heatmap das espécies de aves no Brasil';
        \n3. Em notícias veja noticias do site https://ebird.org/region/BR/posts;
        \n4. Em upload selecione um arquivo no formato .csv e carregue seus dados para uma análise;
        \n5. No botão 'Resumos' obtenha resumos de um report do site https://www.birdlife.org/papers-reports/ obtido via scrapping;
        \n6. No botão 'Classificação' obtenha a classificação de todos os report do site https://www.birdlife.org/papers-reports/ obtido via scrapping;
        \n7. No botão 'Chat' obtenha uma resposta de uma pergunta sobre os pássaros extintos da IA ou passe uma requisição POST;
        \n8. No botão 'Dahsboard' obtenha um dashboard com informações sobre os dados do projeto;
        \n9. Usando requisições vcs poderão usar quaisquer das requisições de http://127.0.0.1:8000/docs incluindo uma curiosidade sobre aves do modelo distilbert/distilgpt2;
        \n10. Para rodar o programa execute o arquivo 'main.py' (caso esteja usando Windowns, caso não esteja terá que rodar separadamente o streamlit.py e o API.py usando o comando 'streamlit run .\main\streamlitAPP.py' e 'uvicorn main.API:app --reload');
        \n11. Para ter acesso ao chatbot rode o comando 'setx GROQ_API_KEY {API_KEY}' caso esteja no windows ou 'export GROQ_API_KEY={API_KEY}' caso esteja no linux, obs: vou deixar a minha chave no PDF e no comentário da entrega;''')




# Crie uma instância do SessionState
session_state = st.session_state

def informacoes():
    st.header("Informações gerais")
    st.write("Link para download: https://www.birds.cornell.edu/clementschecklist/introduction/updateindex/december-2023/2023b-citation-and-downloads/")


    # Lê o csv e mostra as informações
    df = pd.read_csv("./data/eBird-Clements-v2023b-integrated-checklist-December-2023.csv")

    # Retira a order nan
    df = df.dropna(subset=['order'])

    # retira as seguintes colunas: sort v2023b, species_code, taxon_concept_id, Clements v2023b change,text for website v2023b, name and authority, sort v2022,page 6.0
    df = df.drop(columns=['sort v2023b', 'species_code', 'taxon_concept_id', 'Clements v2023b change', 'text for website v2023b', 'name and authority', 'sort v2022', 'page 6.0'])

    # Permite selecionar category
    if 'category' not in st.session_state:
        st.session_state.category = df['category'].unique()[0]

    category = st.selectbox('Selecione uma categoria', df['category'].unique(), index=df['category'].unique().tolist().index(st.session_state.category))
    st.session_state.category = category

    # Filtra o dataframe para mostrar apenas as aves da categoria selecionada
    df_categoria = df.loc[df['category'] == category]

    # Permite selecionar order
    if 'order' not in st.session_state:
        st.session_state.order = None

    order_options = df_categoria['order'].unique() if category is not None else []
    order = st.selectbox('Selecione uma ordem', order_options, index=None)
    st.session_state.order = order

    # Permite selecionar family
    if 'family' not in st.session_state:
        st.session_state.family = None

    family_options = df_categoria.loc[df_categoria['order'] == order]['family'].unique() if category is not None and order is not None else []
    family = st.selectbox('Selecione uma família', family_options, index=None)
    st.session_state.family = family

    # Permite selecionar name
    if 'name' not in st.session_state:
        st.session_state.name = None

    name_options = df_categoria.loc[(df_categoria['order'] == order) & (df_categoria['family'] == family)]['scientific name'].unique() if category is not None and order is not None and family is not None else []
    name = st.selectbox('Selecione um nome científico', name_options, index=None)
    st.session_state.name = name

    # Checkbox para filtrar se foram extintos ou não
    # Se a coluna extinct for 1, mostra que a ave foi extinta
    extinct = st.checkbox('Mostrar apenas aves extintas')

    # Filtra o dataframe para mostrar apenas as aves da ordem e família selecionadas
    if name is not None:
        df = df_categoria.loc[(df_categoria['order'] == order) & (df_categoria['family'] == family) & (df_categoria['scientific name'] == name)]
        if extinct:
            df = df_categoria.loc[(df_categoria['order'] == order) & (df_categoria['family'] == family) & (df_categoria['scientific name'] == name) & (df_categoria['extinct'] == 1)]
        else:
            df = df_categoria.loc[(df_categoria['order'] == order) & (df_categoria['family'] == family) & (df_categoria['scientific name'] == name)]
    elif family is not None:
        df = df_categoria.loc[(df_categoria['order'] == order) & (df_categoria['family'] == family)]
        if extinct:
            df = df_categoria.loc[(df_categoria['order'] == order) & (df_categoria['family'] == family) & (df_categoria['extinct'] == 1)]
        else:
            df = df_categoria.loc[(df_categoria['order'] == order) & (df_categoria['family'] == family)]
    elif order is not None:
        df = df_categoria.loc[df_categoria['order'] == order]
        if extinct:
            df = df_categoria.loc[(df_categoria['order'] == order) & (df_categoria['extinct'] == 1)]
        else:
            df = df_categoria.loc[df_categoria['order'] == order]
    else:
        df = df_categoria
        if extinct:
            df = df_categoria.loc[df_categoria['extinct'] == 1]

    if st.button('Download CSV'):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Baixe o CSV",
            data=csv,
            file_name='informacoes.csv',
            mime='text/csv',
        )



    st.write(df)

    # faz um gráfico mostrando a quantidade de linhas por order
    # Obter a quantidade de linhas por ordem
    # Obter a quantidade de linhas por ordem
    ordens = df['order'].value_counts().nlargest(5)

    # Criar uma figura e um eixo
    fig, ax = plt.subplots()

    # Criar o gráfico
    ax.bar(ordens.index, ordens.values)
    ax.set_xlabel('Ordem')
    ax.set_ylabel('Quantidade de linhas')
    ax.set_title('5 Ordens com maior quantidade de linhas')
    ax.tick_params(axis='x', rotation=45)  # Inclinar os rótulos de dados das colunas em 45 graus
    fig.tight_layout()  # Ajustar o layout para evitar que os rótulos sejam cortados

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)


@st.cache_data
def mapa():
    st.header("Heatmap das espécies de aves no Brasil")

    # Abrir o arquivo KML
    tree = ET.parse('data/ebird_hotspots.kml')
    root = tree.getroot()

    # Criar um dataframe com os dados do KML
    df = pd.DataFrame({
        'name': [p.find('name').text for p in root.findall('.//Placemark')],
        'geometry': [Point(float(coord.split(',')[0]), float(coord.split(',')[1])) for p in root.findall('.//Placemark') for coord in [p.find('Point/coordinates').text]]
    })

    # Converter o dataframe para um GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Extrair as coordenadas de latitude e longitude da coluna de geometria
    gdf['latitude'] = gdf['geometry'].apply(lambda x: x.y)
    gdf['longitude'] = gdf['geometry'].apply(lambda x: x.x)

    # Remover a coluna de geometria
    gdf = gdf.drop(columns=['geometry'])

    # Criar um mapa com os dados
    st.map(gdf)
        
# cache
@st.cache_data
def noticias():
    url = "https://ebird.org/region/BR/posts"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontre o elemento <ul class="NewsFeed-list">
    news_feed_list = soup.find('ul', class_='NewsFeed-list')

    # Encontre todos os elementos dentro do <ul class="NewsFeed-list">
    elements = news_feed_list.find_all('li')

    # Crie uma lista para armazenar as informações
    informacoes = []
    count = 0
    # Faça algo com os elementos, por exemplo, imprima seus textos
    for element in elements:
        if count == 7:
            break
        count += 1
        informacao = {
            'titulo': element.find('a').text.strip(),
            'link': element.find('a')['href'],
            'texto': element.find('p').text.strip(),
        }
        informacoes.append(informacao)

    # Crie um dataframe com as informações
    import pandas as pd
    df = pd.DataFrame(informacoes)

    # Use o Streamlit para exibir as informações
    st.title("Notícias de Aves no Brasil pelo site https://ebird.org/region/BR/posts")
    st.write(df)

def upload_file():
    # Serviços de upload e download
    uploaded_file = st.file_uploader('Selecione um arquivo CSV', type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, on_bad_lines='warn', encoding='latin-1', sep=';')
        st.write(df)

resumo_feito = False
def resumos():
    st.title("Resumos de reports do site https://www.birdlife.org/papers-reports/")
    st.button('Atualiza Scrapping', on_click=scrapping_reports())


    # permite ao usuário escolher uma chave de report

    with open('.\data\links.json', 'r') as f:
        links_dict = json.load(f)
    reports = list(links_dict.keys())
    report = st.selectbox('Selecione um report', reports)
    
    #st.button('Fazer Resumo', on_click=extrair_texto_pdf(report))
    def on_click(report):
        if st.button('Fazer Resumo'):
            global resumo_feito
            resumo_feito = True
            pass

    on_click(report)

    

    if resumo_feito:
        extrair_texto_pdf(report)
        report_tratado = report.replace(":", "_")

        with open(f'.\\data\\textos\\{report_tratado}.txt', 'r', encoding='latin1') as f:
            texto_leve_botao = f.read()
        st.subheader("Resumo:")
        st.write(resumo_llama(texto_leve_botao))


def dashboard():
    st.title("Dashboard")
    st.write("A ferramenta possui múltiplas funcionalidades, a seguir mostrarei como os dados são tratados em cada uma delas:")

    funcionalidades = ["Chat", "Resumo", "Classificação"]
    escolha = st.selectbox("Selecione a funcionalidade:", funcionalidades)

    #---------------------------------------------------------------------------------------------------
    if escolha == "Chat":
        st.subheader("Chat")
        st.write("A funcionalidade de chat recebe a base bruta, trata ela, envia para o modelo e devolve uma resposta de até 200 tokens sobre os pássaros extintos.")
        # conta o número de palavras em eBird-Clements-v2023b-integrated-checklist-December-2023
        df = pd.read_csv('./data/eBird-Clements-v2023b-integrated-checklist-December-2023.csv')
        texto = df.to_string(index=False)

        # conta o número de tokens    
        num_tokens_bruto = len(texto.split())


        df = df.dropna(subset=['extinct'])

        # retira as seguintes colunas: sort v2023b, species_code, taxon_concept_id, Clements v2023b change,text for website v2023b, name and authority, sort v2022,page 6.0
        df = df.drop(columns=['sort v2023b', 'species_code', 'taxon_concept_id', 'Clements v2023b change', 'text for website v2023b', 'name and authority', 'sort v2022', 'page 6.0'])

        # filtra para pegar apenas as espécies
        df = df[df['category'] == 'species']
        df = df.drop(columns=['category'])

        texto = df.to_string(index=False)
        num_tokens_tratado = len(texto.split())

        num_tokens_IA = 200

        # grafico com os tres num_tokens
            
        # Create a figure and axis
        fig, ax = plt.subplots()

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Define the data
        labels = ['Num. Tokens Bruto', 'Num. Tokens Tratado', 'Num. Tokens IA']
        values = [num_tokens_bruto, num_tokens_tratado, num_tokens_IA]

        # Create a bar chart com escala logarítmica no eixo y
        ax.bar(labels, values)
        ax.set_yscale('log')

        # Adiciona rótulos de dados acima das colunas
        for i, value in enumerate(values):
            ax.text(i, value + 1, str(value), ha='center', va='bottom')

        # Set the title and labels
        ax.set_title('Número de Tokens')
        ax.set_xlabel('Tipo de Token')
        ax.set_ylabel('Número de Tokens')

        # Show the plot
        st.pyplot(fig)

    #---------------------------------------------------------------------------------------------------
    elif escolha == "Resumo":
        st.subheader("Resumo")
        st.write("A funcionalidade de resumo recebe o texto de uma notícia com até 3500 tokens e resume ela em no máximo 4 parágrafos em PTBR")
        st.write("Exemplo do fluxo de dados com a notícia Making a Difference (2022)")

        #conta o número de palavras em Making a Difference (2022)
        with open('./data/textos/Making a Difference (2022).txt', 'r', encoding='latin1') as f:
            texto = f.read()

        resp = '''A BirdLife International é a maior parceria de conservação da natureza do mundo, presente em 119 países e trabalhando para proteger a vida selvagem em todo o planeta. Com um abordagem única de conservação em larga escala, a BirdLife International atua em 16 países megadiversos e trabalha com comunidades locais e governos para proteger espécies, habitats e ecossistemas.

    No último década, a BirdLife International alcançou resultados impressionantes, salvando espécies em risco de extinção, protegendo habitats críticos e apoianto políticas de conservação. Além disso, a parceria também desenvolveu capacidade de conservação em redes de organizações locais, capacitando mais de 35.000 pessoas em todo o mundo.

    Além disso, a BirdLife International também trabalha para restaurar florestas, proteger áreas marinhas e combater a perda de biodiversidade. Com uma visão de futuro de uma "mundo rico em biodiversidade com gente e natureza viva em harmonia, de forma equitativa e sustentável", a BirdLife International está comprometida em continuar trabalhando para proteger a vida selvagem e as nossas praias.'''


        # Define os valores
        num_tokens_bruto = len(texto.split())
        num_tokens_tratado = len(resp.split())

        # Cria um gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(['Bruto', 'Tratado'], [num_tokens_bruto, num_tokens_tratado])

        # Adiciona título e rótulos
        ax.set_title('Número de Tokens')
        ax.set_xlabel('Tipo de Token')
        ax.set_ylabel('Número de Tokens')

        # Adiciona rótulos de dados acima das barras
        for i, value in enumerate([num_tokens_bruto, num_tokens_tratado]):
            ax.text(i, value + 1, str(value), ha='center', va='bottom')

        # Mostra o gráfico
        st.pyplot(fig)

    #---------------------------------------------------------------------------------------------------
    elif escolha == "Classificação":
        st.subheader("Classificação")
        st.write("A funcionalidade de classificação recebe o texto de todas as noticias e classifica elas em 3 categorias: Conservação e Protecao, Pesquisa e Descobertas, Ameaças e Declinio")

        if os.path.exists(f".//data/textos//todos_textos.txt"):
            with open(".//data/textos//todos_textos.txt", "r", encoding="utf-8") as arquivo_txt:
                texto = arquivo_txt.read()
        resp = '''
                    [{
                        "title": "Conservation Investment Strategy for Resident and Migratory Birds of the Chocó-Andean Region in Northwest Ecuador (2022)",
                        "category": "Conservation and Protection"
                    },
                    {
                        "title": "Making a Difference (2022)",
                        "category": "Conservation and Protection"
                    },
                    {
                        "title": "State of the World’s Birds_ Taking the pulse of the planet (2018)",
                        "category": "Research and Discovery"
                    },
                    {
                        "title": "State of Africa’s Birds_ Indicators for our changing environment (2018)",
                        "category": "Research and Discovery"
                    },
                    {
                        "title": "Making a Difference (2016)",
                        "category": "Conservation and Protection"
                    },
                    {
                        "title": "Important Bird and Biodiversity Areas_ A global network for conserving nature and benefiting people (2014)",
                        "category": "Conservation and Protection"
                    },
                    {
                        "title": "Canada Warbler Full-life-cycle Conservation Action Plan (2021)",
                        "category": "Conservation and Protection"
                    },
                    {
                        "title": "Birds and Biodiversity Targets (2020)",
                        "category": "Research and Discovery"
                    },
                    {
                        "title": "State of the World’s Birds_ Taking the pulse of the planet (2018)",
                        "category": "Threats and Decline"
                    }
                    ]'''
        num_tokens_bruto = len(texto.split())
        num_tokens_tratado = len(resp.split())

        # Cria um gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(['Bruto', 'Tratado'], [num_tokens_bruto, num_tokens_tratado])

        # Adiciona título e rótulos
        ax.set_title('Número de Tokens')
        ax.set_xlabel('Tipo de Token')
        ax.set_ylabel('Número de Tokens')

        # Adiciona rótulos de dados acima das barras
        for i, value in enumerate([num_tokens_bruto, num_tokens_tratado]):
            ax.text(i, value + 1, str(value), ha='center', va='bottom')

        st.pyplot(fig)

        st.write("exemplo de classificação")
        #transforma o resp em um json
        resp = json.loads(resp)
        st.write(resp)

def classificacao():
    st.title("Classificação geral das notícias")

    def on_click():
        # apaga o arquivo
        if os.path.exists(".//data/textos//todos_textos.txt"):
            os.remove(".//data/textos//todos_textos.txt")

    if st.button('Atualiza Scrapping'):
        on_click()

    if not os.path.exists(f".//data/textos//todos_textos.txt"):
        with open('.\data\links.json', 'r') as f:
            links_dict = json.load(f)
        reports = list(links_dict.keys())

        count=0
        for chave in reports:
            if count == 0:
                v_apagar = True
            else:
                v_apagar = False
            count+=1
            extrair_todos_textos(chave, v_apagar)
    
    with open(".//data/textos//todos_textos.txt", "r", encoding="utf-8") as arquivo_txt:
        texto = arquivo_txt.read()

    st.write("O texto foi classificado como:")
    st.write(LLM_classifica(texto))


    #with open('./data/textos/.txt', 'r', encoding='latin1') as f:


# Usa um sidebar para fazer a paginação
page = st.sidebar.selectbox('Selecione uma opção', ['Introdução', 'Informações gerais', 'Mapa', 'Notícias', 'Upload', "Resumos", "Classificação",  "Chat", "Dashboard"])

if page == 'Introdução':
    introducao()
elif page == 'Informações gerais':
    informacoes()
elif page == 'Mapa':
    mapa()
elif page == 'Notícias':
    noticias()
elif page == 'Upload':
    upload_file()
elif page == "Resumos":
    resumos()
elif page == "Classificação":
    classificacao()
elif page == "Dashboard":
    dashboard()
elif page == "Chat":
    chat()


