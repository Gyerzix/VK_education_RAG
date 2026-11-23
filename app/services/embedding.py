from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-m3"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts: list[str]) -> list[list[float]]:

    embeddings = model.encode(
        texts,
        batch_size=8,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return embeddings.tolist()
