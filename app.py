import streamlit as st

from scraper import scrape
from chunking import chunk_text
from vectorstore import index_exists, load_index_and_texts, build_and_save, search
from rag import built_prompt
# from llm import call_groq
from rag import built_prompt, call_ollama

st.title("Web Crawler RAG Agent")

url = st.text_input("Website URL")
question = st.text_input("Your question")

if st.button("Ask"):
    if not url or not question:
        st.warning("Please enter both a URL and a question.")
        st.stop()

    try:
        text = scrape(url)
    except ValueError as e:
        st.error(f"Couldn't fetch that page: {e}")
        st.stop()

    if index_exists(url, current_text=text):
        st.info("Already indexed and up to date. Loading from disk.")
    else:
        st.info("Refreshing the index for this page...")
        with st.spinner("Chunking, embedding, and indexing..."):
            chunks = chunk_text(text)
            build_and_save(url, chunks, page_text=text)

    index, texts = load_index_and_texts(url)

    if index.ntotal == 0:
        st.error("The index for this page contains no content.")
        st.stop()

    retrieved_chunks, scores = search(index, texts, question, k=8)

    prompt = built_prompt(question, retrieved_chunks)

    try:
        with st.spinner("Thinking..."):
            answer = call_ollama(prompt)
    except (TimeoutError, RuntimeError) as error:
        st.error(str(error))
        st.stop()

    st.subheader("Answer")
    st.write(answer)

    with st.expander("Retrieved chunks"):
        for chunk in retrieved_chunks:
            st.write(chunk)
            st.divider()