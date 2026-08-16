def chunk_text(text, chunk_size=1000, overlap=200):

    """
        args:
            split text into overlapping chunks
            text(str) --> input text
            chunk_size(int) --> max character per chunk
            overlap(int) --> overlapping character b/w two chunks
        returns:
            list[str] --> list of text chunks
    """
    chunks =[]
    start = 0
    while start <len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks