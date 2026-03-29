"""
Retriever for fetching relevant documents from the vector database.
"""
from typing import List, Dict, Any
from rich.console import Console

from src.database import VectorDatabase

console = Console()


class Retriever:
    """Handles document retrieval from vector database."""

    def __init__(self, vector_db: VectorDatabase, top_k: int = 5):
        """
        Initialize retriever.

        Args:
            vector_db: Vector database instance
            top_k: Number of documents to retrieve
        """
        self.vector_db = vector_db
        self.top_k = top_k

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        filter_by_source: str | None = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: User query
            top_k: Override default top_k
            filter_by_source: Optional filter by source

        Returns:
            List of relevant document chunks with metadata
        """
        k = top_k if top_k is not None else self.top_k

        # Build metadata filter
        metadata_filter = None
        if filter_by_source:
            metadata_filter = {"source": filter_by_source}

        # Search vector database
        results = self.vector_db.search(
            query=query,
            top_k=k,
            filter_metadata=metadata_filter,
        )

        return results

    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into context string.

        Args:
            results: Retrieved document chunks

        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant documents found."

        context_parts = []

        for i, result in enumerate(results, 1):
            metadata = result["metadata"]
            document = result["document"]

            context_parts.append(
                f"[Document {i}]\n"
                f"Title: {metadata['title']}\n"
                f"Source: {metadata['source']}\n"
                f"URL: {metadata['url']}\n"
                f"Published: {metadata['published_date']}\n"
                f"Content:\n{document}\n"
            )

        return "\n---\n\n".join(context_parts)

    def get_sources(self, results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Extract source information from results.

        Args:
            results: Retrieved document chunks

        Returns:
            List of source dictionaries
        """
        seen_urls = set()
        sources = []

        for result in results:
            metadata = result["metadata"]
            url = metadata["url"]

            if url not in seen_urls:
                seen_urls.add(url)
                sources.append({
                    "title": metadata["title"],
                    "url": url,
                    "source": metadata["source"],
                    "published_date": metadata["published_date"],
                })

        return sources
