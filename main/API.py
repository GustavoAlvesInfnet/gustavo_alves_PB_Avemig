import csv
from fastapi import FastAPI, Request
from pydantic import BaseModel
import pandas as pd
from fastapi import Query

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