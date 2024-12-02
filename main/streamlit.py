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
from scrapping import *
from LLM import *



def chat():
    st.header("Dashboard")

    # Lê o csv e mostra as informações
    df = pd.read_csv("./data/eBird-Clements-v2023b-integrated-checklist-December-2023.csv")

    # Retira a order nan
    #df = df.dropna(subset=['range'])
    df = df.dropna(subset=['extinct'])

    # retira as seguintes colunas: sort v2023b, species_code, taxon_concept_id, Clements v2023b change,text for website v2023b, name and authority, sort v2022,page 6.0
    df = df.drop(columns=['sort v2023b', 'species_code', 'taxon_concept_id', 'Clements v2023b change', 'text for website v2023b', 'name and authority', 'sort v2022', 'page 6.0'])

    # filtra para pegar apenas as espécies
    df = df[df['category'] == 'species']
    df = df.drop(columns=['category'])

    # trasnforma o df em texto
    texto = df.to_string(index=False)
    # conta o número de tokens
    #num_tokens = len(texto.split())
    #st.write(f"O dataframe possui {num_tokens} tokens.")

    # salva em um csv
    df.to_csv('./data/extinctedBirds.csv', index=False)

    st.write(df)

    textoCSV = pd.read_csv('./data/extinctedBirds.csv')
    textoCSV = textoCSV.to_csv(index=False)
    groq_MC(textoCSV)


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
        \n6. Para ter acesso à API rode o comando 'uvicorn main.API:app --reload';
        \n7. Para ter acesso ao chatbot rode o comando 'setx GROQ_API_KEY {API_KEY}' caso esteja no windows ou 'export GROQ_API_KEY={API_KEY}' caso esteja no linux, obs: vou deixar a minha chave no PDF e no cmentário;''')




# Crie uma instância do SessionState
session_state = st.session_state

def informacoes():
    st.header("Informações gerais")


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
    st.write("Em construção")


# Usa um sidebar para fazer a paginação
page = st.sidebar.selectbox('Selecione uma opção', ["Chat", 'Introdução', 'Informações gerais', 'Mapa', 'Notícias', 'Upload', "Resumos"])


if page == "Chat":
    chat()
elif page == 'Introdução':
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
elif page == "Dashboard":
    dashboard()


