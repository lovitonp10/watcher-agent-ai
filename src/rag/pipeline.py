"""
RAG Pipeline combining retrieval and generation.
"""
from typing import Dict, Any
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from src.database import VectorDatabase
from .retriever import Retriever
from .generator import Generator

console = Console()


class RAGPipeline:
    """End-to-end RAG pipeline."""

    def __init__(
        self,
        vector_db: VectorDatabase,
        provider: str = "openai",
        api_key: str = None,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.1,
        base_url: str = None,
        top_k: int = 5,
    ):
        """
        Initialize RAG pipeline with multi-provider support.

        Args:
            vector_db: Vector database instance
            provider: LLM provider (openai, mistral, anthropic, ollama)
            api_key: API key for the provider
            model: LLM model name
            temperature: Generation temperature
            base_url: Optional custom base URL (for Ollama, etc.)
            top_k: Number of documents to retrieve
        """
        self.retriever = Retriever(vector_db=vector_db, top_k=top_k)
        self.generator = Generator(
            provider=provider,
            api_key=api_key,
            model=model,
            temperature=temperature,
            base_url=base_url,
        )

    def query(
        self,
        question: str,
        top_k: int | None = None,
        filter_by_source: str | None = None,
        verbose: bool = False,
    ) -> Dict[str, Any]:
        """
        Process a user query through the RAG pipeline.

        Args:
            question: User question
            top_k: Override default top_k
            filter_by_source: Optional source filter
            verbose: Show retrieval details

        Returns:
            Dictionary with answer, sources, and metadata
        """
        if verbose:
            console.print(f"\n[bold cyan]Query:[/bold cyan] {question}\n")
            console.print("[dim]Retrieving relevant documents...[/dim]")

        # Retrieve relevant documents
        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
            filter_by_source=filter_by_source,
        )

        if not results:
            return {
                "answer": "I couldn't find any relevant documents in the knowledge base to answer your question. "
                          "Try updating the database with recent content or rephrase your query.",
                "sources": [],
                "num_sources": 0,
                "success": False,
            }

        if verbose:
            console.print(f"[green]✓ Found {len(results)} relevant chunks[/green]\n")

        # Format context and extract sources
        context = self.retriever.format_context(results)
        sources = self.retriever.get_sources(results)

        if verbose:
            console.print("[dim]Generating answer...[/dim]")

        # Generate answer
        result = self.generator.generate(
            query=question,
            context=context,
            sources=sources,
        )

        if verbose:
            console.print("[green]✓ Answer generated[/green]\n")

        # Add metadata
        result["num_sources"] = len(sources)
        result["num_chunks"] = len(results)

        return result

    def display_response(self, result: Dict[str, Any]):
        """
        Display RAG response in a formatted way.

        Args:
            result: Result from query()
        """
        # Display answer
        console.print(Panel(
            Markdown(result["answer"]),
            title="[bold green]Answer[/bold green]",
            border_style="green",
        ))

        # Display sources
        if result.get("sources"):
            console.print("\n[bold cyan]Sources:[/bold cyan]")
            for i, source in enumerate(result["sources"], 1):
                console.print(f"\n[yellow]{i}. {source['title']}[/yellow]")
                console.print(f"   [dim]Source: {source['source']} | Date: {source['published_date']}[/dim]")
                console.print(f"   [blue link={source['url']}]{source['url']}[/blue link]")

        console.print()
