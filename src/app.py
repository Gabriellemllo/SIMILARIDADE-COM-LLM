from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="Busca Semântica - Exoplanetas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


def executar_script(nome_arquivo, descricao):
    print(f"Executando {descricao}...")
    try:
        resultado = subprocess.run(
            ["python", nome_arquivo + ".py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        print(resultado.stdout)
        if resultado.stderr:
            print("Erro:", resultado.stderr)
        return True
    except Exception as e:
        print(f"Erro ao executar {descricao}: {e}")
        return False


def inicializar_dados():
    embeddings_dir = BASE_DIR / "embeddings"
    chunks_file = embeddings_dir / "chunks.json"
    index_file = embeddings_dir / "faiss_index.index"

    if not chunks_file.exists() or not index_file.exists():
        print("Dados não encontrados. Executando pipeline completo...")
        executar_script("scraping", "Scraping dos artigos")
        executar_script("chunk", "Divisão em chunks")
        executar_script("embeddings_faiss", "Geração de embeddings e índice")
        print("Pipeline completo executado com sucesso!")
    else:
        print("Dados já existem. Iniciando diretamente.")


# inicializar_dados()


print("Carregando modelo e índice...")
model = SentenceTransformer("all-MiniLM-L6-v2")

with open(BASE_DIR / "embeddings/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

index = faiss.read_index(str(BASE_DIR / "embeddings/faiss_index.index"))
print(f"Sistema pronto! {len(chunks)} chunks carregados.")


def buscar_semantica(pergunta, top_k=5):
    embedding_query = model.encode([pergunta], normalize_embeddings=True)
    distancias, indices = index.search(embedding_query.astype(np.float32), top_k)
    
    resultados = []
    for dist, idx in zip(distancias[0], indices[0]):
        if idx == -1:
            continue
        trecho = chunks[idx]
        resultados.append({
            "distancia": round(float(dist), 4),
            "trecho": trecho[:650] + "..." if len(trecho) > 650 else trecho
        })
    return resultados


class Query(BaseModel):
    pergunta: str


@app.get("/", response_class=HTMLResponse)
async def pagina_inicial():
    with open(BASE_DIR / "frontend/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/search")
async def buscar(q: Query):
    resultados = buscar_semantica(q.pergunta)
    return {"resultados": resultados}


@app.get("/health")
async def verificar_saude():
    return {"status": "ok", "chunks_carregados": len(chunks)}