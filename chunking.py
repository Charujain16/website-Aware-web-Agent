from scraper import scrape


def chunk_text(text, chunk_size=1000, chunk_overlap=100):

    """Split the input text into chunks of specified size with optional overlap. """

    chunks = []
    current_chunk = ""
    text_length = len(text)

    paragraph = text.split("\n\n")    # Split the text into paragraphs based on double newlines
    print(f"Total paragraphs: {len(paragraph)}")  # Print the total number of paragraphs for debugging
    print(paragraph[:5])  # Print the first 5 paragraphs for debugging
    for para in paragraph:
        para_length = len(para)
        if para_length == 0:
            continue  # Skip empty paragraphs
        if para_length <= chunk_size:
            if len(current_chunk) + para_length > chunk_size:
                chunks.append(current_chunk.strip())
                chunk_overlap_char = current_chunk[-chunk_overlap:]
                current_chunk = chunk_overlap_char + para + "\n\n"
            else:
                current_chunk += para + "\n\n"   # If the paragraph is smaller than or equal to the chunk size, add it as a single chunk
        else:
            start = 0     # so that it start from the beginning of the paragraph
            while start < para_length:
                end = min(start + chunk_size, para_length)  # Determine the end index for the chunk
                chunks.append(para[start:end])  # Append the chunk to the list
                start += chunk_size - chunk_overlap   # Move the start index forward by chunk size minus overlap for the next chunk
    # Append the final leftover chunk if it contains any text
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks


if __name__ == "__main__":
    text = scrape("https://www.gutenberg.org/files/1342/1342-h/1342-h.htm")
    chunks = chunk_text(text, chunk_size=1000, chunk_overlap=100)

    print(f"Number of chunks: {len(chunks)}")
    print("--------------")
    print(chunks[100:200])