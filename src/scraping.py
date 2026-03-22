import requests
from bs4 import BeautifulSoup
import os
import re

urls = [
    "https://science.nasa.gov/universe/exoplanets/discovery-alert-an-ice-cold-earth/",
    "https://science.nasa.gov/universe/exoplanets/nasa-webb-looks-at-earth-sized-habitable-zone-exoplanet-trappist-1-e/",
    "https://www.nasa.gov/universe/exoplanets/nasas-tally-of-planets-outside-our-solar-system-reaches-6000/"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

os.makedirs("../data", exist_ok=True)

for i, url in enumerate(urls, start=1):
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, "html.parser")

        article_body = soup.find("div", class_=["article-body", "wysiwyg", "text"])
        if article_body:
            paragraphs = article_body.find_all(["p", "h1", "h2", "h3", "li"])
        else:
            paragraphs = soup.find_all(["p", "h1", "h2", "h3"])

        text_parts = []
        for elem in paragraphs:
            txt = elem.get_text(strip=True)
            if txt:
                text_parts.append(txt)

        full_text = "\n\n".join(text_parts)
        
        full_text = re.sub(r'\n{3,}', '\n\n', full_text).strip()

        filename = f"../data/artigo_{i}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"Artigo {i} salvo com sucesso! ({len(full_text)} caracteres) → {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar {url}: {e}")
    except Exception as e:
        print(f"Erro inesperado no artigo {i}: {e}")