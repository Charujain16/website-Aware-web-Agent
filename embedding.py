from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
def embed_text(texts):
    """Given a text, return its embedding using the specified model."""
    embedding = model.encode(texts)
    # cosine_similarity_1_2 = np.dot(embedding[0], embedding[1]) / (np.linalg.norm(embedding[0]) * np.linalg.norm(embedding[1]))
    # cosine_similarity_1_3 = np.dot(embedding[0], embedding[2]) / (np.linalg.norm(embedding[0]) * np.linalg.norm(embedding[2]))

    # print(f"Cosine similarity between text 1 and text 2: {cosine_similarity_1_2}")
    # print(f"Cosine similarity between text 1 and text 3: {cosine_similarity_1_3}")
    return embedding

if __name__ == "__main__":
    texts = [
    "The cat sat on the mat.",
    "A feline was resting on the rug.",
    "Stock markets fell sharply today."
    ]
    embeddings = embed_text(texts)
    print(embeddings.shape)