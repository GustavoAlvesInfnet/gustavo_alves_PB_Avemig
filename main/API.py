import csv
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import pandas as pd
from fastapi import Query

from transformers import pipeline

import subprocess
from fastapi.responses import JSONResponse

def run_uvicorn():
    comando = "uvicorn main.API:app --reload"
    subprocess.run(comando, shell=True)

if __name__ == "__main__":
    run_uvicorn()

app = FastAPI()

class Checklist(BaseModel):
    category: str
    english_name: str
    scientific_name: str
    authority: str
    range: str
    order: str
    family: str
    extinct: bool
    extinct_year: int

#curl http://localhost:8000/avesAPI/todas
#curl http://localhost:8000/avesAPI/todas?category=family
@app.get("/avesAPI/todas")
async def read_checklist(category: str = Query(None)):
    df = pd.read_csv("../data/eBird-Clements-v2023b-integrated-checklist-December-2023-2.csv")
    checklist = []
    for index, row in df.iterrows():
        if category is None or row["category"] == category:
            extinct = row["extinct"]
            if pd.notnull(extinct):
                extinct = bool(extinct)
            else:
                extinct = None
            checklist.append({
                "category": str(row["category"]),
                "english_name": str(row["English name"]),
                "scientific_name": str(row["scientific name"]),
                "authority": str(row["authority"]),
                "range": str(row["range"]),
                "order": str(row["order"]),
                "family": str(row["family"]),
                "extinct": extinct,
                "extinct_year": str(row["extinct year"]) if not pd.isnull(row["extinct year"]) else None
            })
    return {"aves": checklist}



class NovaEspecie(BaseModel):
    category: str
    english_name: str
    scientific_name: str
    authority: str
    range: str
    order: str
    family: str
    extinct: bool
    extinct_year: str

# curl -X POST -H "Content-Type: application/json; charset=latin1" -d '{"category": "AvesTeste", "english_name": "New Bird", "scientific_name": "Novus Avium", "authority": "Autoridade", "range": "Range", "order": "Ordem", "family": "Familia", "extinct": false, "extinct_year": ""}' http://localhost:8000/avesAPI/nova-especie
@app.post("/avesAPI/nova-especie")
async def criar_nova_especie(request: Request):
    try:
        nova_especie = NovaEspecie.model_validate(await request.json())
        df = pd.read_csv("../data/eBird-Clements-v2023b-integrated-checklist-December-2023-2.csv", encoding='latin1')
        nova_linha = pd.DataFrame([nova_especie.model_dump()])
        df = pd.concat([df, nova_linha])
        df.to_csv("../data/eBird-Clements-v2023b-integrated-checklist-December-2023-2.csv", index=False)
        return {"mensagem": "Nova espécie adicionada com sucesso!"}
    except Exception as e:
        return {"erro": str(e)}

# curl http://localhost:8000/avesAPI/todas?category=AvesTeste

# LLM - TP4
curiosity_context = """Example of response: Here are some curious things about birds:
\n-Crows and ravens
\nThese birds are known to be curious and intelligent. They have been observed digging clams at low tide and using traffic to crush them. They have also been seen following traffic. 
\n-Keas
\nThese birds are known to be inquisitive and playful, and they manipulate objects throughout their lives. 
\n-Evolution
\nBirds evolved from theropod dinosaurs during the Jurassic period, around 165–150 million years ago. 
\n-Origin of birds
\nThe scientific consensus is that birds are a group of maniraptoran theropod dinosaurs."""

class CuriosityResponse(BaseModel):
    curiosity: str

@app.get("/avesAPI/curiosidade")
async def curiosity_llm():
    try:
        pipe = pipeline("text-generation", model="distilbert/distilgpt2")
        question = f"{curiosity_context}. A curiosity of birds:"
        result = pipe(question, truncation=True, max_length=275)
        result = result[0]["generated_text"]
        result = result.replace(question, "")
        result = result.replace("\n", "")

        # Crie um objeto CuriosityResponse com a resposta gerada
        response = CuriosityResponse(curiosity=result)

        # Retorne o objeto CuriosityResponse como uma resposta JSON
        return response
    except Exception as e:
        # Trate o erro e retorne um código de erro adequado
        if isinstance(e, ConnectionError):
            raise HTTPException(status_code=503, detail="Serviço Indisponível")
        elif isinstance(e, TimeoutError):
            raise HTTPException(status_code=504, detail="Tempo de resposta excedido")
        else:
            raise HTTPException(status_code=500, detail="Erro interno do servidor")
    
@app.exception_handler(Exception)
async def handle_exception(request, exc):
    # Trate o erro e retorne um código de erro adequado
    if isinstance(exc, ConnectionError):
        return JSONResponse(status_code=503, content={"detail": "Serviço Indisponível"})
    elif isinstance(exc, TimeoutError):
        return JSONResponse(status_code=504, content={"detail": "Tempo de resposta excedido"})
    else:
        return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})