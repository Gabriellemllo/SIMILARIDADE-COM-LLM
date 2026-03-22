# 🛡️ SIMILARIDADE-COM-LLM
Aplicação para busca por similaridade semântica em textos coletados da web, utilizando embeddings de LLM e índice vetorial FAISS.  
Desenvolvida como parte da avaliação da disciplina [Tópicos Avançados em IA].

👥 Equipe :

| Nome                         | Matrícula          |
|----------------------------- |--------------------|
| Maria Gabrielle de Melo      | 00000854105        |
| Elcio José Ferreira da Silva | 00000854166        |


📖 Caso de Uso  
Busca inteligente em conteúdos da web (neste caso, 3 artigos da NASA sobre exoplanetas).  
O sistema transforma textos em vetores semânticos (embeddings) e permite perguntas naturais, retornando os trechos mais relevantes — sem depender só de palavras-chave.

Exemplo:  
**Pergunta:** "How many exoplanets has NASA confirmed?"  
**Resposta principal (distância 0.4004):**  
"...The official number of exoplanets — planets outside our solar system — tracked by NAS... Reaches 6,000..."

🛠️ Tecnologias Utilizadas

**Scraping e Pré-processamento**  
- requests  
- beautifulsoup4  
- re (built-in)  

**Chunking e Armazenamento**  
- json (built-in)  

**Embeddings e Busca Semântica**  
- sentence-transformers (modelo: paraphrase-multilingual-MiniLM-L12-v2)  
- faiss-cpu  
- numpy  

**Interface**  
- Python puro (script interativo no terminal)  

**Gerenciamento**  
- requirements.txt  

🚀 Como Executar o Projeto

1. Clone o repositório
   
```bash
git clone https://github.com/Gabriellemllo/SIMILARIDADE-COM-LLM.git
cd SIMILARIDADE-COM-LLM
```

2- Instale todas as dependências de uma vez
```bash
pip install -r requirements.txt
```

📁 Estrutura de Pastas
```bash
SIMILARIDADE-COM-LLM/
├── data/                        # Textos originais baixados
│   ├── artigo_1.txt
│   ├── artigo_2.txt
│   └── artigo_3.txt
├── embeddings/                  # Resultados processados
│   ├── chunks.json              # 89 chunks de texto
│   └── faiss_index.index        # Índice vetorial FAISS
├── src/                         # Todos os scripts
│   ├── scraping.py              # Baixa páginas da web
│   ├── chunk.py                 # Limpa e divide texto em chunks
│   ├── embeddings_faiss.py      # Gera embeddings + cria índice
│   └── busca.py                 # Interface de busca no terminal
├── requirements.txt             # Lista de dependências
├── README.md                    # Esta documentação
```
