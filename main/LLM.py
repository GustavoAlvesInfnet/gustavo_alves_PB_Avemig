from groq import Groq
import streamlit as st

@st.cache_data
def resumo_llama(texto):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Gere um resumo em PT-BR de no máximo 4 parágrafos para o seguinte texto: {texto}"
            }
        ],
        temperature=1,
        max_tokens=4000,
        top_p=1,
        stream=True,
        stop=None,
    )

    texto = ""
    for chunk in completion:
        texto += chunk.choices[0].delta.content or ""
    print(texto)
        

    return texto


def LLM_classifica(texto):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Classifique tendo como saída um json cada uma das 9 notícias abaixo em uma das categorias: Conservação e Protecao, Pesquisa e Descobertas, Ameaças e Declinio -> {texto}. A saída deve ser um json."
            }
        ],
        temperature=1,
        max_tokens=4000,
        top_p=1,
        stream=True,
        stop=None,
    )

    texto = ""
    for chunk in completion:
        texto += chunk.choices[0].delta.content or ""
    print(texto)
        

    return texto
