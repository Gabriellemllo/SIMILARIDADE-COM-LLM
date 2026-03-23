from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pydantic import BaseModel

app = FastAPI(title="Busca Semântica NASA Exoplanetas")

# CORS pra front-end funcionar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega tudo uma única vez
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
with open("../embeddings/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)
index = faiss.read_index("../embeddings/faiss_index.index")

class Query(BaseModel):
    pergunta: str

@app.post("/search")
def search(q: Query):
    query_emb = model.encode([q.pergunta], normalize_embeddings=True)
    distances, indices = index.search(query_emb.astype(np.float32), 5)
    
    resultados = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1: continue
        resultados.append({
            "distancia": float(dist),
            "trecho": chunks[idx][:500] + "..." if len(chunks[idx]) > 500 else chunks[idx]
        })
    
    return {"resultados": resultados}