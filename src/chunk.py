import os 
import json

def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

folder = "../data"
all_chunks = []

for file in os.listdir(folder):
    if file.endswith(".txt"):
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            text = f.read()
            chunks = chunk_text(text)
            all_chunks.extend(chunks)

with open("../embeddings/chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=4)
    
print(f"Total de chunks criados: {len(all_chunks)}")