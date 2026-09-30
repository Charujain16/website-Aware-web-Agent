from vectorstore import index_exists, load_index_and_texts, build_and_save
from scraper import scrape
from rag import call_ollama, built_prompt
from embedding import embed_text
from chunking import chunk_text
import numpy as np
import faiss

url = input("Enter the website URL: ")
question = input("Enter your question: ")

if index_exists(url):
    print("Already indexed — loading from disk.")
else:
    print("Not indexed yet — building it now.")
    text = scrape(url)          
    chunks = chunk_text(text)
    build_and_save(url, chunks)
    print(f"Indexed {len(chunks)} chunks.")

index, texts = load_index_and_texts(url)
print(f"Index has {index.ntotal} vectors, {len(texts)} texts loaded.")

question_embedding = embed_text([question])
question_embedding = np.array(question_embedding).astype('float32')
faiss.normalize_L2(question_embedding)

if index.ntotal == 0:
    raise ValueError("The FAISS index contains no vectors.")


k = min(4, index.ntotal)
distances, indices = index.search(question_embedding, k=k)

retrieved_chunks = [texts[i] for i in indices[0] if i>=0 and i < len(texts)]
print("Number of retrieved chunks:", len(retrieved_chunks))

for i, chunk in enumerate(retrieved_chunks):
    print(f"\n--- Chunk {i} ---")
    print("Characters:", len(chunk))
prompt = built_prompt(question, retrieved_chunks)
answer = call_ollama(prompt)

print("Answer:", answer)