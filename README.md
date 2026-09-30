# Website-Aware Web Agent

A lightweight Retrieval-Augmented Generation (RAG) project that answers questions about a specific website by scraping the page content, splitting it into chunks, embedding the text, storing it in a FAISS vector index, and then retrieving the most relevant chunks for a user question.

## What it does

- Scrapes a target webpage and removes noisy HTML elements such as scripts, styles, headers, footers, and nav sections.
- Splits the cleaned text into manageable chunks with overlap.
- Encodes chunks using a SentenceTransformer model.
- Stores the embeddings in a FAISS index and caches them per URL.
- Retrieves the most relevant chunks for a question.
- Sends the retrieved context to an LLM (via Ollama by default) to generate an answer grounded in the website content.

## Project structure

- `app.py` — main Streamlit web UI
- `main.py` — command-line example flow
- `scraper.py` — retrieves and cleans page text
- `chunking.py` — splits text into chunks with overlap
- `embedding.py` — creates embeddings using `all-MiniLM-L6-v2`
- `vectorstore.py` — builds, saves, loads, and searches the FAISS index
- `rag.py` — builds prompts and calls Ollama
- `llm.py` — optional Groq/OpenAI-compatible API integration
- `requirements.txt` — Python dependencies

## Tech stack

- Python
- Streamlit
- BeautifulSoup4
- SentenceTransformers
- FAISS
- NumPy
- Ollama

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start Ollama locally and pull a model:

```bash
ollama serve
ollama pull llama3.2
```

> The app expects Ollama to be running at `http://localhost:11434`.

## Run the app

Start the Streamlit interface:

```bash
streamlit run app.py
```

Then:
1. Paste a website URL
2. Enter a question about that page
3. Click "Ask"

The app will scrape the page, build or refresh the index if needed, retrieve relevant chunks, and show the answer.

## Example workflow

- Input URL: `https://example.com`
- Input question: `What does this page say about pricing?`
- System behavior:
  - Fetch and clean webpage text
  - Split content into chunks
  - Embed and index the content
  - Search nearby relevant chunks
  - Send them to the LLM with a prompt
  - Display the generated answer

## Notes

- The vector index is cached on disk using a hash of the URL and page content, so it can avoid rebuilding for unchanged pages.
- The project is designed for local experimentation and small website-based Q&A use cases.
- For alternate LLM providers, see `llm.py` and the Groq/OpenAI-compatible setup there.
- This project is best suited for static or mostly static websites. For dynamic JavaScript-heavy pages, a browser automation tool may be needed to capture richer content.

Example:
https://www.gutenberg.org/files/1342/1342-h/1342-h.htm

https://www.python.org/about/

https://myanimelist.net/anime/1/Cowboy_Bebop

## License

This project is provided as-is for educational and experimental use.
