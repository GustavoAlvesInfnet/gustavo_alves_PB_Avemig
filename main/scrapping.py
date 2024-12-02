
# https://www.birdlife.org/papers-reports/
# preciso dos hrefs dentro de <div class="c-search-result__result"> > <div class="c-search-result__footer"> > <a class="c-btn c-btn--line c-btn--black c-btn--md" href="https://www.birdlife.org/papers-reports/conservation-investment-strategy-for-resident-and-migratory-birds-of-the-choco-andean-region-in-northwest-ecuador/">

import requests
from bs4 import BeautifulSoup
import json
import os
from PyPDF2 import PdfReader
def scrapping_reports():
    url = "https://www.birdlife.org/papers-reports/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontre os elementos que contêm os links
    elements = soup.find_all('div', class_='c-search-result__result')

    # Extraia os links e salve em um dicionário
    links_dict = {}
    for element in elements:
        footer = element.find('div', class_='c-search-result__footer')
        links_a = footer.find_all('a')
        for link in links_a:
            if link['href'].endswith('.pdf'):
                span_text = link.find('span', class_='u-sr-only').text
                span_text = span_text.replace("to read ", "")  # Remove o "to read"
                links_dict[span_text] = link['href']

    print(links_dict)
    

    #salva os links em um arquivo json

    with open('.\data\links.json', 'w') as f:
        json.dump(links_dict, f)

#confere se o arquivo json existe
if not os.path.exists('.\data\links.json'):
    scrapping_reports()

def extrair_texto_pdf(chave):
    # lê o json
    with open('.\data\links.json', 'r') as f:
        links_dict = json.load(f)

    # imprime os links
    for key, value in links_dict.items():
        print("Chave:",key,"-", "Valor:",value)
    # faz o dowload do pdf no link especificado pelo usuário pela chave do dict
    #chave = input("Digite a chave do PDF que você deseja baixar: ")
    if chave in links_dict:
        #acha o value com base na chave
        for key, value in links_dict.items():
            if key == chave:
                url_pdf = f"https://www.birdlife.org{value}"
                break
        response = requests.get(url_pdf)
        nome_arquivo = chave.replace(":", "_") + ".pdf"
        with open(f".//data/PDFs//{nome_arquivo}", "wb") as arquivo:
            arquivo.write(response.content)
        print(f"PDF {nome_arquivo} baixado com sucesso!")
        #transforma o pdf em texto
        with open(f".//data/PDFs//{nome_arquivo}", "rb") as arquivo_pdf:
            leitor_pdf = PdfReader(arquivo_pdf)
            num_paginas = len(leitor_pdf.pages)
            texto = ""
            for pagina in range(num_paginas):
                texto += leitor_pdf.pages[pagina].extract_text()
            #quantos tokens tem o texto
            #tokens = len(texto.split())
            #print(f"O PDF {nome_arquivo} possui {tokens} tokens.")

            #pega os 1000 primeiros tokens
            primeiros_tokens = texto.split()[:1000]
            texto_leve = " ".join(primeiros_tokens)

            #quantos tokens tem o texto leve
            #tokens_leve = len(texto_leve.split())
            #print(f"O PDF {nome_arquivo} possui {tokens_leve} tokens.")



            
        
            #salva o texto
            nome_arquivo_txt = nome_arquivo.replace(".pdf", ".txt")
            with open(f".//data/textos//{nome_arquivo_txt}", "w", encoding="utf-8") as arquivo_txt:
                arquivo_txt.write(texto_leve)
    else:
        print(f"A chave {chave} não foi encontrada no dicionário.")

def extrair_todos_textos(chave, v_apagar):
    # lê o json
    with open('.\data\links.json', 'r') as f:
        links_dict = json.load(f)

    # imprime os links
    for key, value in links_dict.items():
        print("Chave:",key,"-", "Valor:",value)
    # faz o dowload do pdf no link especificado pelo usuário pela chave do dict
    #chave = input("Digite a chave do PDF que você deseja baixar: ")
    if chave in links_dict:
        #acha o value com base na chave
        for key, value in links_dict.items():
            if key == chave:
                url_pdf = f"https://www.birdlife.org{value}"
                break
        response = requests.get(url_pdf)
        nome_arquivo = chave.replace(":", "_") + ".pdf"
        with open(f".//data/PDFs//{nome_arquivo}", "wb") as arquivo:
            arquivo.write(response.content)
        print(f"PDF {nome_arquivo} baixado com sucesso!")
        #transforma o pdf em texto
        with open(f".//data/PDFs//{nome_arquivo}", "rb") as arquivo_pdf:
            leitor_pdf = PdfReader(arquivo_pdf)
            num_paginas = len(leitor_pdf.pages)
            texto = ""
            for pagina in range(num_paginas):
                texto += leitor_pdf.pages[pagina].extract_text()
            #quantos tokens tem o texto
            #tokens = len(texto.split())
            #print(f"O PDF {nome_arquivo} possui {tokens} tokens.")

            #pega os 1000 primeiros tokens
            texto = texto.replace("..", "")
            primeiros_tokens = texto.split()[:500]
            texto_leve = " ".join(primeiros_tokens)

            #quantos tokens tem o texto leve
            #tokens_leve = len(texto_leve.split())
            #print(f"O PDF {nome_arquivo} possui {tokens_leve} tokens.")



            nome_arquivo_txt = nome_arquivo.replace(".pdf", ".txt")
            if v_apagar == True:
                #apaga o pdf
                with open(f".//data/textos//todos_textos.txt", "w", encoding="utf-8") as arquivo_txt:
                    arquivo_txt.write("\n" + nome_arquivo_txt + ":" + texto_leve)
            #salva todos os textos em um único arquivo txt
            with open(f".//data/textos//todos_textos.txt", "a", encoding="utf-8") as arquivo_txt:
                arquivo_txt.write("\n" + nome_arquivo_txt + ":" + texto_leve)
    else:
        print(f"A chave {chave} não foi encontrada no dicionário.")