import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path

CHUNKS_PATH   = Path("../embeddings/chunks.json")
INDEX_PATH    = Path("../embeddings/faiss_index.index")
MODEL_NAME    = "paraphrase-multilingual-MiniLM-L12-v2"

TOP_K = 5  

print("=== Busca Semântica com LLM ===")
print("Carregando modelo e índice...")

model = SentenceTransformer(MODEL_NAME)

with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

index = faiss.read_index(str(INDEX_PATH))

print(f"→ Tudo carregado! {len(chunks)} chunks disponíveis.")
print("Digite sua pergunta (ou 'sair' para encerrar)\n")

while True:
    query = input("Sua pergunta: ").strip()
    if query.lower() in ['sair', 'exit', 'quit', 'q']:
        print("Encerrando...")
        break
    if not query:
        continue

    query_emb = model.encode([query], normalize_embeddings=True)

    distances, indices = index.search(query_emb.astype(np.float32), TOP_K)

    print(f"\nTop {TOP_K} resultados mais similares (menor distância = mais parecido):")
    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0]), 1):
        if idx == -1:
            continue
        chunk_text = chunks[idx]
        print(f"\n{rank}. Distância: {dist:.4f}")
        print(f"   {chunk_text[:300]}{'...' if len(chunk_text) > 300 else ''}")
        print("-" * 70)

    print()