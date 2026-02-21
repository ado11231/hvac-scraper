"""Shared Pydantic models for the scraper API."""

from pydantic import BaseModel


class ManualCandidate(BaseModel):
    url: str
    doc_type: str | None = None
    title: str | None = None
