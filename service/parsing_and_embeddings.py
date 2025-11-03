from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import fitz
from service.save_to_qdrant import save_to_qdrant
import uuid

#
# def load_bge_large(device="cpu"):
#     """Load the BAAI/bge-large-en embedding model."""
#     model = SentenceTransformer("BAAI/bge-large-en", device=device)
#     return model


def extract_two_column_text(pdf_path):
    """Extract text from a two-column PDF file using PyMuPDF."""
    print("aaaaaaaaaaa")
    text_content = []
    with fitz.open(pdf_path) as doc:
        print("one")
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            blocks = page.get_text("blocks")
            # Sort blocks top-to-bottom, left-to-right
            blocks.sort(key=lambda block: (block[1], block[0]))
            for block in blocks:
                text_content.append(block[4])

    return "\n".join(text_content)


def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    """Split text into recursive overlapping chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return text_splitter.split_text(text)


def generate_bge_embeddings(chunks,sessionid,userid):
    """Generate embeddings using sentence-transformers."""

    model = SentenceTransformer("BAAI/bge-large-en", device="cpu")
    processed_chunks = [f"Represent this sentence for retrieval: {chunk}" for chunk in chunks]

    embeddings = model.encode(
        processed_chunks,
        batch_size=8,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    collection_name=userid+"_"+sessionid
    save_to_qdrant(chunks, embeddings, collection_name=collection_name)
    return embeddings


if __name__ == "__main__":
    path = "/Users/saurabh/Rag_Langchain/AYU-36-364.pdf"
    userid= uuid.uuid4()
    sessionid="aaaaaaaaa"



    # Step 1: Extract text
    text = extract_two_column_text(path)
    print(f"✅ Extracted text length: {len(text)} characters")

    # Step 2: Split text into chunks
    chunks = split_text_into_chunks(text)
    print(f"✅ Total chunks created: {len(chunks)}")


    # Step 3: Generate embeddings
    embeddings = generate_bge_embeddings(chunks,sessionid, str(userid))

    # # Step 4: Print example
    print(f"✅ Generated embeddings for {len(embeddings)} chunks")
    print("\n🧩 First chunk:\n", chunks[0][:300], "...")
    print("\n🔢 First 10 dims of embedding:", embeddings[0][:10])

