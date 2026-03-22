import requests
from bs4 import BeautifulSoup
import os

urls = [
    "https://science.nasa.gov/universe/exoplanets/discovery-alert-an-ice-cold-earth/",
    "https://science.nasa.gov/universe/exoplanets/nasa-webb-looks-at-earth-sized-habitable-zone-exoplanet-trappist-1-e/",
    "https://www.nasa.gov/universe/exoplanets/nasas-tally-of-planets-outside-our-solar-system-reaches-6000/"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

os.makedirs("../data", exist_ok=True)

for i, url in enumerate(urls):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")

    text = ""
    for p in paragraphs:
        text += p.get_text() + "\n"

    with open(f"../data/artigo_{i+1}.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Artigo {i+1} salvo!")