"""
Brave Search API client for PDF manual discovery.
Uses GET https://api.search.brave.com/res/v1/web/search with X-Subscription-Token.
"""

import os

import httpx

from models import ManualCandidate

BRAVE_API_BASE = "https://api.search.brave.com/res/v1/web/search"
DEFAULT_COUNT = 20


async def search_pdf_manuals(
    query: str,
    *,
    count: int = DEFAULT_COUNT,
) -> list[ManualCandidate]:
    """
    Search Brave for PDF manual URLs. Returns only results whose URL ends with .pdf.
    Raises on HTTP errors or missing BRAVE_API_KEY.
    """
    api_key = os.environ.get("BRAVE_API_KEY")
    if not api_key:
        raise ValueError("BRAVE_API_KEY is not set")

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(
            BRAVE_API_BASE,
            headers={"X-Subscription-Token": api_key},
            params={"q": query, "count": count},
        )
        resp.raise_for_status()

    data = resp.json()
    results = data.get("web", {}).get("results") or []
    candidates: list[ManualCandidate] = []
    for r in results:
        url = (r.get("url") or "").strip()
        if not url.lower().endswith(".pdf"):
            continue
        title = (r.get("title") or "").strip() or None
        candidates.append(ManualCandidate(url=url, title=title))
    return candidates
