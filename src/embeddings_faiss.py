import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os
from pathlib import Path

CHUNKS_PATH = Path("../embeddings/chunks.json")
INDEX_PATH  = Path("../embeddings/faiss_index.index")

MODEL = "paraphrase-multilingual-MiniLM-L12-v2"   

print("=== Gerando embeddings e índice FAISS ===")

print("Lendo chunks...")
if not CHUNKS_PATH.exists():
    print(f"Erro: {CHUNKS_PATH} não encontrado!")
    exit(1)

with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"→ Carregados {len(chunks)} chunks")

print(f"Carregando modelo: {MODEL}")
model = SentenceTransformer(MODEL)

print("Gerando vetores...")
embeddings = model.encode(
    chunks,
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True   
)

print(f"→ Shape dos embeddings: {embeddings.shape}")

print("Criando índice...")
d = embeddings.shape[1]                 
index = faiss.IndexFlatL2(d)             
index.add(embeddings.astype(np.float32))

faiss.write_index(index, str(INDEX_PATH))
print(f"→ Índice salvo em: {INDEX_PATH}")

print("\nPronto! Pasta embeddings/ agora tem:")
print(" - chunks.json")
print(" - faiss_index.index  ← esse é o mais importante para busca")