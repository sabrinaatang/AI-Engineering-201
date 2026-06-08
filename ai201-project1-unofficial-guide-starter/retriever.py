import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from ingestion_pipeline import chunk_text, clean_text, URLS, scrape_url  # Reuse methods from pipeline.py

# Configuration
CHROMA_PATH = "./chroma_db"  # Folder to store ChromaDB data
CHROMA_COLLECTION = "retrieval_chunks"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 200
OVERLAP = 50

# Initialize embedding function and ChromaDB PersistentClient
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL_NAME
)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)  # PersistentClient for database persistence
collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=embedding_function
)

# Function to embed and store chunks in bulk
def embed_and_store_chunks():
    """
    Scrape, clean, chunk, and store embeddings in ChromaDB in bulk.
    """
    all_documents = []
    all_metadatas = []
    all_ids = []
    chunk_id = 0

    for i, url in enumerate(URLS):
        print(f"Processing URL {i + 1}/{len(URLS)}: {url}")
        raw_text = scrape_url(url)
        if raw_text:
            cleaned_text = clean_text(raw_text)
            chunks = chunk_text(cleaned_text, CHUNK_SIZE, OVERLAP)

            # Collect chunks, metadata, and IDs for bulk insertion
            for position, chunk in enumerate(chunks):
                all_documents.append(chunk)
                all_metadatas.append({
                    "source": f"url_{i + 1}",
                    "position": position,
                    "url": url
                })
                all_ids.append(f"chunk_{chunk_id}")
                chunk_id += 1

            print(f"Collected {len(chunks)} chunks for URL {i + 1}")

    # Bulk add all chunks to ChromaDB
    if all_documents:
        collection.add(
            documents=all_documents,
            metadatas=all_metadatas,
            ids=all_ids
        )
        print(f"Stored {collection.count()} total chunks in the vector database.")
    else:
        print("No chunks to store.")

# Function to retrieve top-k relevant chunks
def retrieve_chunks(query, top_k=5):
    """
    Retrieve the top-k most relevant chunks for a given query.
    """
    if collection.count() == 0:
        print("No chunks found in the database. Please embed and store chunks first.")
        return []

    # Perform the semantic search
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    # Extract and format results
    retrieved_chunks = []
    for document, metadata, distance in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        retrieved_chunks.append({
            "text": document,
            "source": metadata["source"],
            "position": metadata["position"],
            "url": metadata["url"],
            "distance": distance
        })

    return retrieved_chunks

# Test retrieval with evaluation queries
def test_retrieval():
    """
    Test the retrieval system with predefined queries.
    """
    queries = [
        "Where can I find information regarding the majors and minors offered at UC Irvine?",
        "What are the differences between Middle Earth and Mesa Court Housing?",
        "What free legal emergency support resources are available to me at UCI?"
    ]

    for i, query in enumerate(queries):
        print(f"\nQuery {i + 1}: {query}")
        results = retrieve_chunks(query, top_k=5)
        for result in results:
            print(f"Chunk: {result['text']}")
            print(f"Source: {result['source']}, Position: {result['position']}, URL: {result['url']}")
            print(f"Distance: {result['distance']}\n")

if __name__ == "__main__":
    # Embed and store chunks
    embed_and_store_chunks()

    # Test retrieval
    test_retrieval()