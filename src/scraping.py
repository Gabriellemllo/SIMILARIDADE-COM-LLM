import requests
from bs4 import BeautifulSoup
import os
import re
import time

urls = [
    "https://periodicos.ufes.br/astronomia/article/view/43184",
    "https://periodicos.ufes.br/astronomia/article/view/38610",
    "https://teses.usp.br/teses/disponiveis/14/14131/tde-21062013-162408/pt-br.php",
    "http://repositorio.unb.br/handle/10482/30855"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/129.0.0.0 Safari/537.36"
}

os.makedirs("../data", exist_ok=True)

for i, url in enumerate(urls, start=1):
    print(f"[{i}/{len(urls)}] Tentando baixar: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"  Status: {response.status_code}")

        if response.status_code != 200:
            print(f"  Falhou com status {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "button"]):
            tag.decompose()

        main_content = soup.find(
            "div",
            class_=lambda x: x and any(
                word in x.lower() 
                for word in ["article", "content", "text", "abstract", "fulltext", "main", "body"]
            )
        )

        if main_content:
            full_text = main_content.get_text(separator="\n", strip=True)
        else:
            full_text = soup.get_text(separator="\n", strip=True)

        full_text = re.sub(r'\s+', ' ', full_text).strip()

        if len(full_text) < 300:
            print(f"  Texto curto ({len(full_text)} caracteres)")
            filename = f"../data/artigo_{i:02d}_RESUMO.txt"
        else:
            filename = f"../data/artigo_{i:02d}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_text)
        
        print(f"  Salvo! ({len(full_text)} caracteres) -> {filename}")

    except requests.exceptions.Timeout:
        print("  Timeout - site demorou demais")
    except requests.exceptions.ConnectionError:
        print("  Erro de conexao")
    except Exception as e:
        print(f"  Erro inesperado: {e}")

    time.sleep(2)

print("\nScraping finalizado!")
print("Verifique a pasta ../data")