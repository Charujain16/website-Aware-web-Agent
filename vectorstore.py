import faiss
import numpy as np
import hashlib
import os
import pickle

from embedding import embed_text

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def url_to_id(url):
    """Convert a URL into a short, unique, filesystem-safe ID."""
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def content_hash(text):
    """Hash the page's scraped text, so we can detect if content changed."""
    return hashlib.sha256(text.encode()).hexdigest()


def _paths_for(url):
    uid = url_to_id(url)
    index_file = os.path.join(DATA_DIR, f"{uid}_faiss.index")
    texts_file = os.path.join(DATA_DIR, f"{uid}_texts.pkl")
    meta_file = os.path.join(DATA_DIR, f"{uid}_meta.pkl")
    return index_file, texts_file, meta_file


def build_and_save(url, chunks, page_text=None):
    """Embed the given chunks, build a FAISS index, and save it + texts + hash."""
    embeddings = embed_text(chunks)
    embeddings = np.array(embeddings).astype('float32')

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    index_file, texts_file, meta_file = _paths_for(url)

    faiss.write_index(index, index_file)

    with open(texts_file, 'wb') as f:
        pickle.dump(chunks, f)

    if page_text is not None:
        with open(meta_file, 'wb') as f:
            pickle.dump({"content_hash": content_hash(page_text)}, f)

    print(f"FAISS index and texts saved for URL: {url}")


def load_index_and_texts(url):
    """Load the FAISS index and chunk texts from disk for a given URL."""
    index_file, texts_file, _ = _paths_for(url)

    if not os.path.exists(index_file):
        raise FileNotFoundError(f"FAISS index file not found for URL: {url}")
    index = faiss.read_index(index_file)

    if not os.path.exists(texts_file):
        raise FileNotFoundError(f"Texts file not found for URL: {url}")
    with open(texts_file, 'rb') as f:
        texts = pickle.load(f)

    return index, texts


def index_is_valid_for_text(url, current_text):
    """Check whether the cached index's content hash matches the current page text."""
    _, _, meta_file = _paths_for(url)
    if not os.path.exists(meta_file):
        return False
    with open(meta_file, 'rb') as f:
        meta = pickle.load(f)
    return meta.get("content_hash") == content_hash(current_text)


def index_exists(url, current_text=None):
    """
    Check if a saved index+texts pair exists for this URL.
    If current_text is provided, also validate it against the cached content hash.
    """
    index_file, texts_file, _ = _paths_for(url)
    files_exist = os.path.exists(index_file) and os.path.exists(texts_file)

    if not files_exist:
        return False

    if current_text is not None:
        return index_is_valid_for_text(url, current_text)

    return True


def search(index, texts, question, k=8):
    """Embed a question, search the index, and return the top-k matching texts."""
    question_embedding = embed_text([question])
    question_embedding = np.array(question_embedding).astype('float32')
    faiss.normalize_L2(question_embedding)

    k = min(k, index.ntotal)
    distances, indices = index.search(question_embedding, k=k)

    retrieved = [texts[i] for i in indices[0] if 0 <= i < len(texts)]
    scores = [distances[0][pos] for pos in range(len(indices[0])) if 0 <= indices[0][pos] < len(texts)]
    return retrieved, scores


if __name__ == "__main__":
    url = "https://www.example.com"
    texts = [
        "The cat sat on the mat.",
        "A feline was resting on the rug.",
        "Stock markets fell sharply today."
    ]

    if index_exists(url):
        print("Index already exists — loading from disk.")
        index, loaded_texts = load_index_and_texts(url)
    else:
        print("First time seeing this URL — building and saving.")
        build_and_save(url, texts)
        index, loaded_texts = load_index_and_texts(url)

    print(f"Index has {index.ntotal} vectors.")
    print(loaded_texts)

    retrieved, scores = search(index, loaded_texts, "Where is the cat sitting?", k=2)
    for text, score in zip(retrieved, scores):
        print(f"Match: {text} (score: {score})")