CHUNK_SIZE = 150
CHUNK_OVERLAP = 20
MIN_CHUNK_SIZE = 15


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP, min_chunk_size: int = MIN_CHUNK_SIZE) -> list[str]:
    """
    Разбивает текст на чанки с перекрытием.

    Args:
        text: исходный текст документа
        chunk_size: максимальное количество слов в чанке
        overlap: количество повторяющихся слов
        min_chunk_size: минимальное количество слов в чанке

    Returns:
        Список текстовых фрагментов
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size должен быть больше 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap должен быть >= 0 и меньше chunk_size")

    if min_chunk_size <= 0 or min_chunk_size > chunk_size:
        raise ValueError("Некорректное значение min_chunk_size")

    words = text.split()

    if not words:
        return []

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]

        if len(chunk_words) < min_chunk_size:
            break

        chunks.append(" ".join(chunk_words))

    return chunks
