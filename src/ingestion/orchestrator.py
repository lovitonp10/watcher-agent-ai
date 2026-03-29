"""
Orchestrator for coordinating all data ingestion sources.
"""
from typing import List
from rich.console import Console

from .models import Document
from .arxiv_scraper import ArxivScraper
from .huggingface_scraper import HuggingFaceScraper
from .blog_scraper import BlogScraper

console = Console()


class IngestionOrchestrator:
    """Coordinates fetching from all sources."""

    def __init__(
        self,
        arxiv_categories: List[str],
        blog_feeds: dict,
        keywords: List[str],
        days_back: int = 7,
        max_results: int = 20,
        competitor_feeds: dict = None,
    ):
        """
        Initialize orchestrator with all scrapers.

        Args:
            arxiv_categories: List of ArXiv categories to monitor
            blog_feeds: Dictionary of blog RSS feeds
            keywords: Keywords for filtering
            days_back: Number of days to look back
            max_results: Maximum results per source
            competitor_feeds: Dictionary of competitor RSS feeds (optional)
        """
        self.keywords = keywords
        self.competitor_feeds = competitor_feeds or {}

        self.arxiv_scraper = ArxivScraper(
            categories=arxiv_categories,
            days_back=days_back,
            max_results=max_results,
        )

        self.hf_scraper = HuggingFaceScraper(
            days_back=days_back,
            max_results=max_results,
        )

        self.blog_scraper = BlogScraper(
            blog_feeds=blog_feeds,
            days_back=days_back,
        )

    def fetch_all(self) -> List[Document]:
        """
        Fetch documents from all sources.

        Returns:
            List of all fetched documents
        """
        console.print("\n[bold cyan]🔍 Starting data ingestion...[/bold cyan]\n")

        all_documents = []

        # Fetch from ArXiv
        try:
            arxiv_docs = self.arxiv_scraper.fetch_papers(self.keywords)
            all_documents.extend(arxiv_docs)
        except Exception as e:
            console.print(f"[red]Failed to fetch from ArXiv: {e}[/red]\n")

        # Fetch from Hugging Face
        try:
            hf_docs = self.hf_scraper.fetch_papers(self.keywords)
            all_documents.extend(hf_docs)
        except Exception as e:
            console.print(f"[red]Failed to fetch from Hugging Face: {e}[/red]\n")

        # Fetch from blogs
        try:
            blog_docs = self.blog_scraper.fetch_posts(self.keywords)
            all_documents.extend(blog_docs)
        except Exception as e:
            console.print(f"[red]Failed to fetch from blogs: {e}[/red]\n")

        # Remove duplicates based on URL
        unique_docs = self._deduplicate(all_documents)

        console.print(f"\n[bold green]✅ Total documents fetched: {len(unique_docs)}[/bold green]")
        console.print(f"[dim]Filtered by keywords: {', '.join(self.keywords)}[/dim]\n")

        return unique_docs

    def _deduplicate(self, documents: List[Document]) -> List[Document]:
        """Remove duplicate documents based on URL."""
        seen_urls = set()
        unique_docs = []

        for doc in documents:
            url_str = str(doc.url)
            if url_str not in seen_urls:
                seen_urls.add(url_str)
                unique_docs.append(doc)

        duplicates = len(documents) - len(unique_docs)
        if duplicates > 0:
            console.print(f"[yellow]Removed {duplicates} duplicate(s)[/yellow]")

        return unique_docs

    def fetch_competitors(self, max_per_competitor: int = 5) -> List[Document]:
        """
        Fetch latest posts from competitors WITHOUT keyword filtering.
        Always retrieves the N most recent posts from each competitor.

        Args:
            max_per_competitor: Maximum posts to fetch per competitor (default: 5)

        Returns:
            List of competitor documents
        """
        if not self.competitor_feeds:
            console.print("[yellow]No competitor feeds configured[/yellow]")
            return []

        console.print("\n[bold cyan]🎯 Fetching competitor news...[/bold cyan]\n")

        try:
            competitor_docs = self.blog_scraper.fetch_competitor_posts(
                competitor_feeds=self.competitor_feeds,
                max_per_competitor=max_per_competitor
            )
            return competitor_docs
        except Exception as e:
            console.print(f"[red]Failed to fetch competitor news: {e}[/red]\n")
            return []
