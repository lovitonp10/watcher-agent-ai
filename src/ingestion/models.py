"""
Data models for ingested documents.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class Document(BaseModel):
    """Standardized document model for all ingested content."""

    title: str
    abstract: str
    url: HttpUrl
    source: str  # "arxiv", "huggingface", "netflix_blog", etc.
    published_date: datetime
    authors: Optional[list[str]] = None
    categories: Optional[list[str]] = None

    # Computed field for unique identification
    @property
    def doc_id(self) -> str:
        """Generate unique document ID based on URL."""
        return f"{self.source}:{str(self.url)}"

    def matches_keywords(self, keywords: list[str]) -> bool:
        """Check if document matches any of the provided keywords."""
        text = f"{self.title} {self.abstract}".lower()
        return any(keyword.lower() in text for keyword in keywords)

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "title": self.title,
            "abstract": self.abstract,
            "url": str(self.url),
            "source": self.source,
            "published_date": self.published_date.isoformat(),
            "authors": self.authors,
            "categories": self.categories,
        }
