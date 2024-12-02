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
                "content": f"Gere um resumo para o seguinte texto: {texto}"
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    texto = ""
    for chunk in completion:
        texto += chunk.choices[0].delta.content or ""
    print(texto)
        

    return texto


