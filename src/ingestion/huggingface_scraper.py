"""
Hugging Face Daily Papers scraper.
"""
import requests
from datetime import datetime, timedelta
from typing import List
from rich.console import Console

from .models import Document

console = Console()


class HuggingFaceScraper:
    """Scraper for Hugging Face daily papers."""

    def __init__(self, days_back: int = 7, max_results: int = 20):
        """
        Initialize Hugging Face scraper.

        Args:
            days_back: Number of days to look back
            max_results: Maximum number of papers to fetch
        """
        self.days_back = days_back
        self.max_results = max_results
        self.api_url = "https://huggingface.co/api/daily_papers"

    def fetch_papers(self, keywords: List[str]) -> List[Document]:
        """
        Fetch daily papers from Hugging Face.

        Args:
            keywords: List of keywords to filter papers

        Returns:
            List of Document objects
        """
        console.print("[cyan]Fetching papers from Hugging Face Daily Papers...[/cyan]")

        documents = []
        cutoff_date = datetime.now() - timedelta(days=self.days_back)

        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            papers = response.json()

            for paper in papers[:self.max_results]:
                try:
                    # Parse published date
                    pub_date_str = paper.get("publishedAt", "")
                    if pub_date_str:
                        pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00")).replace(tzinfo=None)
                    else:
                        pub_date = datetime.now()

                    # Filter by date
                    if pub_date < cutoff_date:
                        continue

                    # Build URL
                    paper_id = paper.get("paper", {}).get("id", "")
                    url = f"https://huggingface.co/papers/{paper_id}"

                    # Create document
                    doc = Document(
                        title=paper.get("title", ""),
                        abstract=paper.get("paper", {}).get("summary", "No abstract available"),
                        url=url,
                        source="huggingface",
                        published_date=pub_date,
                        authors=None,  # HF API doesn't always provide authors
                        categories=None,
                    )

                    # Filter by keywords
                    if doc.matches_keywords(keywords):
                        documents.append(doc)
                        console.print(f"  ✓ Found: [green]{doc.title[:80]}...[/green]")

                except Exception as e:
                    console.print(f"[yellow]Warning: Skipped paper due to error: {e}[/yellow]")
                    continue

        except requests.RequestException as e:
            console.print(f"[red]Error fetching from Hugging Face: {e}[/red]")
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")

        console.print(f"[green]✓ Fetched {len(documents)} papers from Hugging Face[/green]\n")
        return documents
