"""
RSS blog scraper for engineering blogs.
"""
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
from rich.console import Console
from bs4 import BeautifulSoup

from .models import Document

console = Console()


class BlogScraper:
    """Scraper for fetching posts from engineering blogs via RSS."""

    def __init__(self, blog_feeds: Dict[str, str], days_back: int = 7):
        """
        Initialize blog scraper.

        Args:
            blog_feeds: Dictionary of {blog_name: rss_url}
            days_back: Number of days to look back
        """
        self.blog_feeds = blog_feeds
        self.days_back = days_back

    def _clean_html(self, html_content: str) -> str:
        """Remove HTML tags and clean text."""
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        # Limit length
        return text[:500] + "..." if len(text) > 500 else text

    def _parse_date(self, entry) -> datetime:
        """Parse published date from feed entry."""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            return datetime(*entry.published_parsed[:6])
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            return datetime(*entry.updated_parsed[:6])
        else:
            return datetime.now()

    def fetch_posts(self, keywords: List[str]) -> List[Document]:
        """
        Fetch blog posts from RSS feeds and filter by keywords.

        Args:
            keywords: List of keywords to filter posts

        Returns:
            List of Document objects
        """
        console.print("[cyan]Fetching posts from Engineering Blogs...[/cyan]")

        all_documents = []
        cutoff_date = datetime.now() - timedelta(days=self.days_back)

        for blog_name, feed_url in self.blog_feeds.items():
            try:
                console.print(f"  Checking {blog_name}...")
                feed = feedparser.parse(feed_url)

                for entry in feed.entries:
                    try:
                        # Parse date
                        pub_date = self._parse_date(entry)

                        # Filter by date
                        if pub_date < cutoff_date:
                            continue

                        # Get content
                        abstract = ""
                        if hasattr(entry, 'summary'):
                            abstract = self._clean_html(entry.summary)
                        elif hasattr(entry, 'description'):
                            abstract = self._clean_html(entry.description)
                        else:
                            abstract = "No description available"

                        # Get authors
                        authors = None
                        if hasattr(entry, 'author'):
                            authors = [entry.author]

                        # Create document
                        doc = Document(
                            title=entry.title,
                            abstract=abstract,
                            url=entry.link,
                            source=blog_name.lower().replace(" ", "_"),
                            published_date=pub_date,
                            authors=authors,
                            categories=None,
                        )

                        # Filter by keywords
                        if doc.matches_keywords(keywords):
                            all_documents.append(doc)
                            console.print(f"    ✓ Found: [green]{doc.title[:70]}...[/green]")

                    except Exception as e:
                        console.print(f"[yellow]Warning: Skipped entry from {blog_name}: {e}[/yellow]")
                        continue

            except Exception as e:
                console.print(f"[red]Error fetching from {blog_name}: {e}[/red]")

        console.print(f"[green]✓ Fetched {len(all_documents)} posts from blogs[/green]\n")
        return all_documents

    def fetch_competitor_posts(self, competitor_feeds: Dict[str, str], max_per_competitor: int = 5) -> List[Document]:
        """
        Fetch latest posts from competitor blogs WITHOUT keyword filtering.
        Always retrieves the N most recent posts regardless of content.

        Args:
            competitor_feeds: Dictionary of {competitor_name: rss_url}
            max_per_competitor: Maximum number of posts to fetch per competitor

        Returns:
            List of Document objects
        """
        console.print("[cyan]Fetching competitor news (no keyword filtering)...[/cyan]")

        all_documents = []

        for competitor_name, feed_url in competitor_feeds.items():
            try:
                console.print(f"  Checking {competitor_name}...")
                feed = feedparser.parse(feed_url)

                # Collect all entries with dates
                entries_with_dates = []
                for entry in feed.entries:
                    try:
                        pub_date = self._parse_date(entry)
                        entries_with_dates.append((pub_date, entry))
                    except Exception as e:
                        console.print(f"[yellow]Warning: Could not parse entry date: {e}[/yellow]")
                        continue

                # Sort by date (most recent first)
                entries_with_dates.sort(key=lambda x: x[0], reverse=True)

                # Take only the N most recent posts
                recent_entries = entries_with_dates[:max_per_competitor]

                for pub_date, entry in recent_entries:
                    try:
                        # Get content
                        abstract = ""
                        if hasattr(entry, 'summary'):
                            abstract = self._clean_html(entry.summary)
                        elif hasattr(entry, 'description'):
                            abstract = self._clean_html(entry.description)
                        else:
                            abstract = "No description available"

                        # Get authors
                        authors = None
                        if hasattr(entry, 'author'):
                            authors = [entry.author]

                        # Create document
                        doc = Document(
                            title=entry.title,
                            abstract=abstract,
                            url=entry.link,
                            source=f"competitor_{competitor_name.lower().replace(' ', '_')}",
                            published_date=pub_date,
                            authors=authors,
                            categories=["competitor"],
                        )

                        all_documents.append(doc)
                        console.print(f"    ✓ Found: [green]{doc.title[:70]}...[/green]")

                    except Exception as e:
                        console.print(f"[yellow]Warning: Skipped entry from {competitor_name}: {e}[/yellow]")
                        continue

            except Exception as e:
                console.print(f"[red]Error fetching from {competitor_name}: {e}[/red]")

        console.print(f"[green]✓ Fetched {len(all_documents)} competitor posts[/green]\n")
        return all_documents
