"""
ArXiv paper scraper using the arxiv Python package.
"""
import arxiv
import time
from datetime import datetime, timedelta
from typing import List
from rich.console import Console

from .models import Document

console = Console()


class ArxivScraper:
    """Scraper for fetching papers from ArXiv."""

    def __init__(self, categories: List[str], days_back: int = 7, max_results: int = 20):
        """
        Initialize ArXiv scraper.

        Args:
            categories: List of ArXiv categories (e.g., ["cs.AI", "cs.CL"])
            days_back: Number of days to look back
            max_results: Maximum results per category
        """
        self.categories = categories
        self.days_back = days_back
        self.max_results = max_results
        self.client = arxiv.Client()

    def fetch_papers(self, keywords: List[str]) -> List[Document]:
        """
        Fetch papers from ArXiv and filter by keywords.

        Args:
            keywords: List of keywords to filter papers

        Returns:
            List of Document objects
        """
        console.print(f"[cyan]Fetching papers from ArXiv ({self.categories})...[/cyan]")

        all_documents = []
        cutoff_date = datetime.now() - timedelta(days=self.days_back)

        for i, category in enumerate(self.categories):
            max_retries = 2
            retry_count = 0

            while retry_count <= max_retries:
                try:
                    # ArXiv rate limiting: wait 15 seconds between requests (strict limit)
                    if i > 0 or retry_count > 0:
                        wait_time = 15 if retry_count == 0 else 45  # 45s on retry
                        console.print(f"[dim]Waiting {wait_time}s for rate limit...[/dim]")
                        time.sleep(wait_time)

                    # Build search query
                    query = f"cat:{category}"

                    # Search ArXiv
                    search = arxiv.Search(
                        query=query,
                        max_results=self.max_results,
                        sort_by=arxiv.SortCriterion.SubmittedDate,
                        sort_order=arxiv.SortOrder.Descending
                    )

                    for result in self.client.results(search):
                        # Filter by date
                        if result.published.replace(tzinfo=None) < cutoff_date:
                            continue

                        # Create document
                        doc = Document(
                            title=result.title,
                            abstract=result.summary.replace("\n", " "),
                            url=result.entry_id,
                            source="arxiv",
                            published_date=result.published.replace(tzinfo=None),
                            authors=[author.name for author in result.authors],
                            categories=[cat for cat in result.categories],
                        )

                        # Filter by keywords
                        if doc.matches_keywords(keywords):
                            all_documents.append(doc)
                            console.print(f"  ✓ Found: [green]{doc.title[:80]}...[/green]")

                    # Success - break retry loop
                    break

                except Exception as e:
                    if "429" in str(e) and retry_count < max_retries:
                        retry_count += 1
                        console.print(f"[yellow]Rate limited on {category}, retrying ({retry_count}/{max_retries})...[/yellow]")
                    else:
                        console.print(f"[red]Error fetching from {category}: {e}[/red]")
                        break

        console.print(f"[green]✓ Fetched {len(all_documents)} papers from ArXiv[/green]\n")
        return all_documents
