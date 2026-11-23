from pathlib import Path
import chromadb

from app.services.embedding import generate_embeddings


BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_PATH = BASE_DIR / "data" / "chroma"
CHROMA_PATH.mkdir(parents=True, exist_ok=True)


client = chromadb.PersistentClient(path=str(CHROMA_PATH))


collection = client.get_or_create_collection(name="rag_chunks", metadata={"hnsw:space": "cosine"})


def index_chunks(chunks):
    if not chunks:
        return

    texts = [chunk.text for chunk in chunks]

    embeddings = generate_embeddings(texts)

    ids = [str(chunk.id) for chunk in chunks]

    metadatas = [{"document_id": chunk.document_id, "chunk_index": chunk.chunk_index} for chunk in chunks]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )


def search_chunks(query: str, top_k: int = 5) -> list[dict]:
    if not query.strip():
        return []

    if collection.count() == 0:
        return []

    query_embedding = generate_embeddings([query])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count())
    )

    search_results = []

    for i in range(len(results["ids"][0])):
        search_results.append({
            "chunk_id": int(results["ids"][0][i]),
            "document_id": results["metadatas"][0][i]["document_id"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i]
        })

    return search_results