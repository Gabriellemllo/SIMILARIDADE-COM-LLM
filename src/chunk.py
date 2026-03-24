import os
import re
import json

def limpar_texto(texto):
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    return texto.strip()

def chunk_text(text, chunk_size=400, overlap=100):
    if not text or len(text) == 0:
        return []
    
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        
        if end < text_len:
            for i in range(end, start + chunk_size // 2, -1):
                if text[i-1] in '.!?;\n':
                    end = i
                    break
            else:
                while end > start and text[end-1] not in ' \n':
                    end -= 1
        
        chunk = text[start:end].strip()
        
        if chunk and len(chunk) > 50:
            chunks.append(chunk)
        
        start += chunk_size - overlap
        
        if start >= text_len:
            break
    
    return chunks

FOLDER = "../data"
OUTPUT_FILE = "../embeddings/chunks.json"

CHUNK_SIZE = 400
OVERLAP = 100

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

all_chunks = []

for file in sorted(os.listdir(FOLDER)):
    if file.endswith(".txt"):
        caminho = os.path.join(FOLDER, file)
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
        
        conteudo_limpo = limpar_texto(conteudo)
        chunks = chunk_text(conteudo_limpo, CHUNK_SIZE, OVERLAP)
        
        all_chunks.extend(chunks)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)