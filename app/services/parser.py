import httpx

from bs4 import BeautifulSoup
from urllib.parse import urlparse


async def parse_url(url: str) -> dict:
    """Загружает HTML-страницу и извлекает основную информацию."""

    parsed_url = urlparse(url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        raise ValueError("Некорректный URL")

    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0,
        headers={
            "User-Agent": "RAG Project"
        }) as client:

        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    title = None

    og_title = soup.find("meta", property="og:title")

    if og_title:
        title = og_title.get("content")

    if not title:
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)

    if not title and soup.title:
        title = soup.title.get_text(strip=True)

    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "aside",
        "noscript"
    ]):
        element.decompose()

    content = soup.find("article")

    if not content:
        content = soup.find("main")

    if not content:
        content = soup.body

    if not content:
        raise ValueError("Не удалось извлечь содержимое страницы")

    text = content.get_text(separator="\n", strip=True)

    if not text:
        raise ValueError("Страница не содержит текста")

    return {
        "title": title or "Без названия",
        "url": str(response.url),
        "text": text
    }
