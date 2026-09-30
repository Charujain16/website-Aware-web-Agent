import requests

def call_ollama(prompt, model="llama3.2:3b"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )
    except requests.exceptions.Timeout as error:
        raise TimeoutError("Ollama took too long to generate a response.") from error
    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "Could not connect to Ollama at http://localhost:11434. Make sure Ollama is running."
        ) from error

    if not response.ok:
        try:
            detail = response.json().get("error")
        except ValueError:
            detail = None
        detail = detail or response.text.strip() or "No error details returned."
        raise RuntimeError(f"Ollama returned HTTP {response.status_code}: {detail}")

    data = response.json()
    answer = data.get("response")

    if not answer:
        raise ValueError("Ollama returned an empty response.")

    return answer

def built_prompt(question, chunks):
    context = "\n\n".join(chunks)

    prompt = f"""You are a helpful assistant that answers questions based on the provided context.
    If the answer is not contained within the context, respond with "I don't know".

    Context:
    {context}

    Question:
    {question}
    Answer:"""

    return prompt

if __name__ == "__main__":


    question = "What is the capital of France?"
    chunks = ["France is a country in Europe.", "The capital of France is Paris.", "France is known for its cuisine and culture.", "I live in India"]
    for i, chunk in enumerate(chunks):
        print(f"--- Retrieved chunk {i} ---")
        print(chunk)
        print()
    prompt = built_prompt(question, chunks)
    answer = call_ollama(prompt)
    print(answer)