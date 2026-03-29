"""
CLI commands for Tech Watch Agent.
"""
import typer
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print as rprint
from pathlib import Path
from dotenv import load_dotenv

from config import Settings, BLOG_FEEDS, COMPETITOR_FEEDS, ARXIV_CATEGORIES
from src.ingestion import IngestionOrchestrator
from src.database import VectorDatabase
from src.rag import RAGPipeline
from src.email import EmailService

# Load environment variables
load_dotenv()

app = typer.Typer(
    name="tech-watch",
    help="Tech Watch Agent - Monitor and query AI/ML state-of-the-art",
    add_completion=False,
)
console = Console()


def _initialize_components():
    """Initialize database and RAG pipeline."""
    settings = Settings()

    # Initialize vector database
    vector_db = VectorDatabase(
        db_path=settings.chroma_db_path,
        embedding_model=settings.embedding_model,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    # Initialize RAG pipeline with multi-provider support
    rag = RAGPipeline(
        vector_db=vector_db,
        provider=settings.llm_provider,
        api_key=settings.api_key,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        base_url=settings.llm_base_url,
        top_k=settings.top_k_results,
    )

    return settings, vector_db, rag


@app.command()
def update(
    days: Optional[int] = typer.Option(None, "--days", help="Number of days to fetch"),
    max_results: Optional[int] = typer.Option(None, "--max", help="Max results per source"),
):
    """
    Update the knowledge base by fetching new papers and blog posts.
    """
    try:
        console.print(Panel.fit(
            "[bold cyan]Tech Watch Agent - Update Mode[/bold cyan]",
            border_style="cyan",
        ))

        settings = Settings()
        days_back = days if days else settings.days_to_fetch
        max_per_source = max_results if max_results else settings.max_results_per_source

        # Initialize orchestrator
        orchestrator = IngestionOrchestrator(
            arxiv_categories=ARXIV_CATEGORIES,
            blog_feeds=BLOG_FEEDS,
            keywords=settings.keywords_list,
            days_back=days_back,
            max_results=max_per_source,
            competitor_feeds=COMPETITOR_FEEDS,
        )

        # Fetch regular documents
        documents = orchestrator.fetch_all()

        # Fetch competitor news (always get latest 5 from each)
        competitor_documents = orchestrator.fetch_competitors(max_per_competitor=5)

        # Initialize database
        vector_db = VectorDatabase(
            db_path=settings.chroma_db_path,
            embedding_model=settings.embedding_model,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

        # Convert regular documents to dict format
        docs_to_add = []
        for doc in documents:
            doc_dict = doc.to_dict()
            doc_dict["doc_id"] = doc.doc_id
            docs_to_add.append(doc_dict)

        # Convert competitor documents to dict format
        competitor_docs_to_add = []
        for doc in competitor_documents:
            doc_dict = doc.to_dict()
            doc_dict["doc_id"] = doc.doc_id
            competitor_docs_to_add.append(doc_dict)

        # Add all to database
        all_docs = docs_to_add + competitor_docs_to_add
        if not all_docs:
            console.print("[yellow]No new documents found matching your criteria.[/yellow]")
            return

        added = vector_db.add_documents(all_docs)

        console.print(Panel.fit(
            f"[bold green]✅ Successfully updated knowledge base![/bold green]\n"
            f"[cyan]Regular content: {len(docs_to_add)} docs[/cyan]\n"
            f"[cyan]Competitor news: {len(competitor_docs_to_add)} docs[/cyan]\n"
            f"[green]Total added: {added} new documents[/green]",
            border_style="green",
        ))

    except Exception as e:
        console.print(f"[red]Error during update: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def chat(
    source: Optional[str] = typer.Option(None, "--source", help="Filter by source"),
):
    """
    Start an interactive chat session with your knowledge base.
    """
    try:
        console.print(Panel.fit(
            "[bold cyan]Tech Watch Agent - Chat Mode[/bold cyan]\n"
            "[dim]Ask questions about recent AI/ML developments. Type 'exit' or 'quit' to leave.[/dim]",
            border_style="cyan",
        ))

        # Initialize components
        settings, vector_db, rag = _initialize_components()

        # Display stats
        stats = vector_db.get_stats()
        console.print(f"\n[dim]Knowledge base: {stats['total_documents']} documents, {stats['total_chunks']} chunks[/dim]\n")

        # Chat loop
        while True:
            try:
                # Get user input
                question = Prompt.ask("\n[bold cyan]You[/bold cyan]")

                if question.lower() in ["exit", "quit", "q"]:
                    console.print("\n[yellow]Goodbye! 👋[/yellow]\n")
                    break

                if not question.strip():
                    continue

                # Process query
                console.print()
                result = rag.query(
                    question=question,
                    filter_by_source=source,
                    verbose=False,
                )

                # Display response
                rag.display_response(result)

            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye! 👋[/yellow]\n")
                break
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]\n")

    except Exception as e:
        console.print(f"[red]Error initializing chat: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    top_k: Optional[int] = typer.Option(None, "--top-k", help="Number of results"),
    source: Optional[str] = typer.Option(None, "--source", help="Filter by source"),
    verbose: bool = typer.Option(False, "--verbose", help="Show detailed output"),
):
    """
    Search the knowledge base with a single query.
    """
    try:
        # Initialize components
        settings, vector_db, rag = _initialize_components()

        # Process query
        result = rag.query(
            question=query,
            top_k=top_k,
            filter_by_source=source,
            verbose=verbose,
        )

        # Display response
        rag.display_response(result)

    except Exception as e:
        console.print(f"[red]Error during search: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def stats():
    """
    Display knowledge base statistics.
    """
    try:
        settings = Settings()

        vector_db = VectorDatabase(
            db_path=settings.chroma_db_path,
            embedding_model=settings.embedding_model,
        )

        stats = vector_db.get_stats()

        console.print(Panel.fit(
            "[bold cyan]Knowledge Base Statistics[/bold cyan]",
            border_style="cyan",
        ))

        console.print(f"\n[bold]Documents:[/bold] [green]{stats['total_documents']}[/green]")
        console.print(f"[bold]Chunks:[/bold] [green]{stats['total_chunks']}[/green]\n")

        console.print("[bold]Sources:[/bold]")
        for source, count in sorted(stats['sources'].items()):
            console.print(f"  • {source}: [green]{count}[/green] chunks")

        console.print()

    except Exception as e:
        console.print(f"[red]Error getting stats: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def clear(
    confirm: bool = typer.Option(False, "--yes", help="Skip confirmation"),
):
    """
    Clear all documents from the knowledge base.
    """
    try:
        if not confirm:
            response = Prompt.ask(
                "[yellow]Are you sure you want to clear the entire knowledge base?[/yellow]",
                choices=["yes", "no"],
                default="no",
            )
            if response != "yes":
                console.print("[dim]Cancelled.[/dim]")
                return

        settings = Settings()
        vector_db = VectorDatabase(
            db_path=settings.chroma_db_path,
            embedding_model=settings.embedding_model,
        )

        vector_db.clear_collection()
        console.print("[green]✓ Knowledge base cleared successfully[/green]")

    except Exception as e:
        console.print(f"[red]Error clearing database: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def info():
    """
    Display configuration information.
    """
    try:
        settings = Settings()

        console.print(Panel.fit(
            "[bold cyan]Tech Watch Agent Configuration[/bold cyan]",
            border_style="cyan",
        ))

        console.print(f"\n[bold]LLM Provider:[/bold] [green]{settings.llm_provider}[/green]")
        console.print(f"[bold]LLM Model:[/bold] {settings.llm_model}")
        console.print(f"[bold]LLM Temperature:[/bold] {settings.llm_temperature}")
        if settings.llm_base_url:
            console.print(f"[bold]LLM Base URL:[/bold] {settings.llm_base_url}")

        console.print(f"\n[bold]Database:[/bold] {settings.chroma_db_path}")
        console.print(f"[bold]Embedding Model:[/bold] {settings.embedding_model}")

        console.print(f"\n[bold]Keywords:[/bold] {', '.join(settings.keywords_list)}")
        console.print(f"[bold]Days to Fetch:[/bold] {settings.days_to_fetch}")
        console.print(f"[bold]Top-K Results:[/bold] {settings.top_k_results}")

        console.print(f"\n[bold]ArXiv Categories:[/bold]")
        for cat in ARXIV_CATEGORIES:
            console.print(f"  • {cat}")

        console.print(f"\n[bold]Blog Feeds:[/bold]")
        for name in BLOG_FEEDS.keys():
            console.print(f"  • {name}")

        console.print()

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def digest(
    send: bool = typer.Option(True, "--send/--no-send", help="Send email (default: yes)"),
    preview: bool = typer.Option(False, "--preview", help="Preview email without sending"),
    full_database: bool = typer.Option(False, "--full-database", help="Summarize entire database instead of just new docs"),
    frequency: str = typer.Option("daily", "--frequency", help="Digest frequency: 'daily' or 'weekly' (Monday only)"),
):
    """
    Generate and send digest email (daily or weekly).

    Use --full-database to get a summary of your entire knowledge base.
    Use --frequency weekly to only run on Mondays.
    """
    try:
        # Check frequency and skip if not the right day
        if frequency == "weekly":
            from datetime import datetime
            today = datetime.now().weekday()  # 0 = Monday, 6 = Sunday
            if today != 0:  # Not Monday
                console.print(f"[yellow]⏭️  Weekly digest mode: Today is not Monday. Skipping.[/yellow]")
                return

        digest_type = "Weekly" if frequency == "weekly" else "Daily"
        database_scope = "Full Database" if full_database else "New Content"

        console.print(Panel.fit(
            f"[bold cyan]Tech Watch Agent - {digest_type} Digest ({database_scope})[/bold cyan]",
            border_style="cyan",
        ))

        settings = Settings()

        # Check email configuration
        if not settings.email_enabled and send:
            console.print("\n[yellow]⚠ Email is disabled in configuration[/yellow]")
            console.print("[dim]Set EMAIL_ENABLED=true in .env to enable email sending[/dim]\n")
            return

        if not settings.email_to and send:
            console.print("\n[red]Error: EMAIL_TO is not configured[/red]")
            console.print("[dim]Set EMAIL_TO in .env with your email address[/dim]\n")
            raise typer.Exit(1)

        # Initialize database
        vector_db = VectorDatabase(
            db_path=settings.chroma_db_path,
            embedding_model=settings.embedding_model,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

        # Initialize competitor docs list (will be populated later)
        competitor_docs_to_add = []

        # Decide which documents to include
        if full_database:
            # Get ALL documents from database (including document content for summaries)
            console.print("\n[cyan]Loading entire knowledge base...[/cyan]")
            all_data = vector_db.collection.get(include=["metadatas", "documents"])

            if not all_data or not all_data.get("metadatas"):
                console.print("[yellow]⚠ Database is empty. Run 'python main.py update' first.[/yellow]")
                return

            # Deduplicate by doc_id and attach ALL chunks content as abstract
            # Separate competitor docs from regular docs
            seen_doc_ids = {}
            competitor_doc_ids = {}

            # Group chunks by doc_id
            doc_chunks = {}
            for i, metadata in enumerate(all_data["metadatas"]):
                doc_id = metadata.get("doc_id")
                if doc_id:
                    if doc_id not in doc_chunks:
                        doc_chunks[doc_id] = {
                            "metadata": metadata,
                            "chunks": []
                        }
                    if i < len(all_data["documents"]):
                        chunk_index = metadata.get("chunk_index", 0)
                        doc_chunks[doc_id]["chunks"].append((chunk_index, all_data["documents"][i]))

            # Process each document
            for doc_id, data in doc_chunks.items():
                metadata = data["metadata"]
                source = metadata.get("source", "")
                is_competitor = source.startswith("competitor_")

                # Sort chunks by index and join them
                sorted_chunks = sorted(data["chunks"], key=lambda x: x[0])
                full_content = "\n\n".join([chunk for _, chunk in sorted_chunks])

                # Extract abstract from full content (remove title if present)
                title = metadata.get("title", "")
                if full_content.startswith(title):
                    abstract = full_content[len(title):].strip()
                else:
                    abstract = full_content

                metadata["abstract"] = abstract[:500] if abstract else "No summary available"

                if is_competitor:
                    competitor_doc_ids[doc_id] = metadata
                else:
                    seen_doc_ids[doc_id] = metadata

            docs_to_add = list(seen_doc_ids.values())
            competitor_docs_to_add = list(competitor_doc_ids.values())
            documents = []  # We'll use docs_to_add directly

            console.print(f"[green]✓ Loaded {len(docs_to_add)} unique documents from database ({len(all_data['metadatas'])} chunks total)[/green]")
            console.print(f"[cyan]  Including {len(competitor_docs_to_add)} competitor news[/cyan]")

        else:
            # Fetch new documents (existing behavior)
            console.print("\n[cyan]Fetching latest content...[/cyan]")
            days_back = 7 if frequency == "weekly" else 1

            orchestrator = IngestionOrchestrator(
                arxiv_categories=ARXIV_CATEGORIES,
                blog_feeds=BLOG_FEEDS,
                keywords=settings.keywords_list,
                days_back=days_back,
                max_results=settings.max_results_per_source,
                competitor_feeds=COMPETITOR_FEEDS,
            )

            documents = orchestrator.fetch_all()

            # Fetch competitor news separately (always get latest 4-5 from each)
            competitor_documents = orchestrator.fetch_competitors(max_per_competitor=5)

            # Add new documents (regular content)
            docs_to_add = []
            for doc in documents:
                doc_dict = doc.to_dict()
                doc_dict["doc_id"] = doc.doc_id
                docs_to_add.append(doc_dict)

            # Add competitor documents to database as well
            competitor_docs_to_add = []
            for doc in competitor_documents:
                doc_dict = doc.to_dict()
                doc_dict["doc_id"] = doc.doc_id
                competitor_docs_to_add.append(doc_dict)

            # Add all to database
            added = vector_db.add_documents(docs_to_add + competitor_docs_to_add)

            console.print(f"[cyan]  Regular content: {len(docs_to_add)} docs[/cyan]")
            console.print(f"[cyan]  Competitor news: {len(competitor_docs_to_add)} docs[/cyan]")

            # If no new documents, get last 10 from database
            if len(docs_to_add) == 0:
                console.print("[yellow]⚠ No new documents found. Getting last 10 from database...[/yellow]")

                all_data = vector_db.collection.get(include=["metadatas", "documents"])
                if all_data and all_data.get("metadatas"):
                    # Group chunks by doc_id
                    doc_chunks = {}
                    for i, metadata in enumerate(all_data["metadatas"]):
                        doc_id = metadata.get("doc_id")
                        source = metadata.get("source", "")
                        # Skip competitor docs here (we'll get them separately)
                        if source.startswith("competitor_"):
                            continue

                        if doc_id:
                            if doc_id not in doc_chunks:
                                doc_chunks[doc_id] = {
                                    "metadata": metadata,
                                    "chunks": []
                                }
                            if i < len(all_data["documents"]):
                                chunk_index = metadata.get("chunk_index", 0)
                                doc_chunks[doc_id]["chunks"].append((chunk_index, all_data["documents"][i]))

                    # Process each document
                    seen_doc_ids = {}
                    for doc_id, data in doc_chunks.items():
                        metadata = data["metadata"]

                        # Sort chunks by index and join them
                        sorted_chunks = sorted(data["chunks"], key=lambda x: x[0])
                        full_content = "\n\n".join([chunk for _, chunk in sorted_chunks])

                        # Extract abstract
                        title = metadata.get("title", "")
                        if full_content.startswith(title):
                            abstract = full_content[len(title):].strip()
                        else:
                            abstract = full_content

                        metadata["abstract"] = abstract[:500] if abstract else "No summary available"
                        seen_doc_ids[doc_id] = metadata

                    # Sort by date and take last 10
                    all_docs = list(seen_doc_ids.values())
                    sorted_docs = sorted(
                        all_docs,
                        key=lambda x: x.get("published_date", "1970-01-01"),
                        reverse=True
                    )
                    docs_to_add = sorted_docs[:10]
                    console.print(f"[green]✓ Retrieved {len(docs_to_add)} recent documents[/green]")

                    # Also get competitor docs separately (no limit, always show all)
                    if not competitor_docs_to_add:
                        competitor_docs_to_add = []
                else:
                    console.print("[yellow]⚠ Database is empty. Run 'python main.py update' first.[/yellow]")
                    return

        # Get stats
        stats = vector_db.get_stats()

        # Generate summary using RAG
        console.print("\n[cyan]Generating AI summary...[/cyan]")
        rag = RAGPipeline(
            vector_db=vector_db,
            provider=settings.llm_provider,
            api_key=settings.api_key,
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            base_url=settings.llm_base_url,
            top_k=10,
        )

        if docs_to_add and len(docs_to_add) > 0:
            # Add Video Popularity project context
            project_context = """IMPORTANT CONTEXT: These articles are being reviewed for the "Video Popularity" project.
This is a multimodal AI project that predicts video popularity on TikTok/Instagram using:
- Visual features (scene detection, object recognition, aesthetic quality)
- Audio features (music, voice, sound effects)
- Textual features (captions, hashtags, descriptions)
- Temporal features (video editing patterns, transitions)

The project focuses on:
1. Predicting engagement/virality
2. Explaining WHY a video will perform (explainability via SHAP, attention mechanisms)
3. Cross-platform analysis (TikTok vs Instagram)

When summarizing, please mention how each article could benefit this project."""

            # Limit docs for summary to avoid token limits (configured in digest.yaml)
            max_docs = settings.digest_max_docs_for_summary
            docs_for_summary = docs_to_add[:max_docs] if full_database else docs_to_add

            # Enrich with full chunk content if summary mode is "full"
            if settings.digest_summary_mode == "full":
                console.print(f"[cyan]  Using full content mode - retrieving {len(docs_for_summary)} documents' complete chunks...[/cyan]")
                for doc in docs_for_summary:
                    doc_id = doc.get("doc_id")
                    if doc_id:
                        # Get all chunks for this document
                        chunks_data = vector_db.collection.get(
                            where={"doc_id": doc_id},
                            include=["documents"]
                        )
                        if chunks_data and chunks_data.get("documents"):
                            # Join all chunks to reconstruct full content
                            doc["full_content"] = "\n\n".join(chunks_data["documents"])
                console.print(f"[green]  ✓ Retrieved full content for {len(docs_for_summary)} documents[/green]")
            else:
                console.print(f"[dim]  Using short mode (title + abstract only)[/dim]")

            summary_result = rag.generator.generate_summary(
                docs_for_summary,
                project_context=project_context,
                summary_mode=settings.digest_summary_mode
            )

            # Check if summary generation failed
            if not summary_result or summary_result.startswith("Error"):
                console.print(f"[yellow]⚠ Summary generation failed: {summary_result}[/yellow]")
                summary_result = "Résumé indisponible - Erreur lors de la génération par le LLM. Vérifiez que Ollama est démarré."
        else:
            summary_result = "Aucun document disponible pour générer un résumé."

        console.print("[green]✓ Summary generated[/green]")

        # Debug: show first 100 chars of summary
        console.print(f"[dim]Summary preview: {summary_result[:100]}...[/dim]")

        # Preview mode
        if preview or not send:
            doc_count_label = f"Documents in digest: {len(docs_to_add)}"
            if full_database:
                doc_count_label = f"[bold]Full database:[/bold] {len(docs_to_add)} documents"
            else:
                doc_count_label = f"[bold]New documents:[/bold] {len(docs_to_add)}"

            console.print(Panel(
                f"{doc_count_label}\n"
                f"[bold]Total en base:[/bold] {stats['total_documents']} documents\n\n"
                f"[bold cyan]Résumé:[/bold cyan]\n{summary_result[:500]}...",
                title=f"[bold yellow]{digest_type} Digest Preview[/bold yellow]",
                border_style="yellow",
            ))

            if not send:
                console.print("\n[dim]Use --send to actually send the email[/dim]")
            return

        # Deduplicate documents by title before sending
        seen_titles = set()
        deduplicated_docs = []
        for doc in docs_to_add:
            title = doc.get('title', '').strip().lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                deduplicated_docs.append(doc)

        if len(docs_to_add) != len(deduplicated_docs):
            console.print(f"[yellow]⚠ Removed {len(docs_to_add) - len(deduplicated_docs)} duplicate articles[/yellow]")

        # Generate LLM summaries for each article (for better email display)
        console.print(f"\n[cyan]Generating individual article summaries with LLM...[/cyan]")
        for i, doc in enumerate(deduplicated_docs):
            try:
                # Get full content for this document from database
                doc_id = doc.get("doc_id")
                if doc_id:
                    chunks_data = vector_db.collection.get(
                        where={"doc_id": doc_id},
                        include=["documents"]
                    )
                    if chunks_data and chunks_data.get("documents"):
                        full_content = "\n\n".join(chunks_data["documents"])
                        # Generate summary with LLM
                        article_summary = rag.generator.generate_article_summary(
                            title=doc.get("title", ""),
                            content=full_content
                        )
                        doc["llm_summary"] = article_summary
                        if (i + 1) % 5 == 0:
                            console.print(f"  ✓ Generated {i + 1}/{len(deduplicated_docs)} summaries")
            except Exception as e:
                console.print(f"[yellow]  Warning: Failed to generate summary for article: {e}[/yellow]")
                doc["llm_summary"] = doc.get("abstract", "Résumé non disponible")[:200]

        console.print(f"[green]✓ Generated {len(deduplicated_docs)} article summaries[/green]")

        # Generate summaries for competitor docs too
        if competitor_docs_to_add:
            console.print(f"[cyan]Generating summaries for {len(competitor_docs_to_add)} competitor articles...[/cyan]")
            for doc in competitor_docs_to_add:
                try:
                    doc_id = doc.get("doc_id")
                    if doc_id:
                        chunks_data = vector_db.collection.get(
                            where={"doc_id": doc_id},
                            include=["documents"]
                        )
                        if chunks_data and chunks_data.get("documents"):
                            full_content = "\n\n".join(chunks_data["documents"])
                            article_summary = rag.generator.generate_article_summary(
                                title=doc.get("title", ""),
                                content=full_content
                            )
                            doc["llm_summary"] = article_summary
                except Exception as e:
                    doc["llm_summary"] = doc.get("abstract", "Résumé non disponible")[:200]
            console.print(f"[green]✓ Generated competitor summaries[/green]")

        # Send email
        console.print(f"\n[cyan]Sending {digest_type.lower()} email digest...[/cyan]")

        email_service = EmailService(
            smtp_host=settings.smtp_host,
            smtp_port=settings.smtp_port,
            smtp_user=settings.smtp_user,
            smtp_password=settings.smtp_password,
            from_email=settings.email_from,
            use_tls=settings.email_use_tls,
        )

        success = email_service.send_digest(
            to_email=settings.email_to,
            new_docs=deduplicated_docs,
            summary=summary_result,
            stats=stats,
            digest_type=digest_type,
            full_database=full_database,
            max_articles=settings.digest_max_articles_in_email,
            competitor_docs=competitor_docs_to_add,
        )

        if success:
            console.print(Panel.fit(
                f"[bold green]✅ {digest_type} digest sent successfully to {settings.email_to}![/bold green]",
                border_style="green",
            ))
        else:
            console.print("[red]Failed to send email. Check your SMTP configuration.[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error generating digest: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def test_email():
    """
    Test email configuration by sending a test message.
    """
    try:
        console.print(Panel.fit(
            "[bold cyan]Testing Email Configuration[/bold cyan]",
            border_style="cyan",
        ))

        settings = Settings()

        # Check configuration
        if not settings.email_enabled:
            console.print("\n[yellow]⚠ Email is disabled in configuration[/yellow]")
            console.print("[dim]Set EMAIL_ENABLED=true in .env to enable[/dim]\n")

        console.print(f"\n[bold]SMTP Host:[/bold] {settings.smtp_host}")
        console.print(f"[bold]SMTP Port:[/bold] {settings.smtp_port}")
        console.print(f"[bold]SMTP User:[/bold] {settings.smtp_user}")
        console.print(f"[bold]From:[/bold] {settings.email_from}")
        console.print(f"[bold]To:[/bold] {settings.email_to}")
        console.print(f"[bold]Use TLS:[/bold] {settings.email_use_tls}")

        if not settings.smtp_user or not settings.smtp_password:
            console.print("\n[red]Error: SMTP credentials not configured[/red]")
            console.print("[dim]Set SMTP_USER and SMTP_PASSWORD in .env[/dim]\n")
            raise typer.Exit(1)

        # Test connection
        email_service = EmailService(
            smtp_host=settings.smtp_host,
            smtp_port=settings.smtp_port,
            smtp_user=settings.smtp_user,
            smtp_password=settings.smtp_password,
            from_email=settings.email_from,
            use_tls=settings.email_use_tls,
        )

        success = email_service.test_connection()

        if success:
            console.print("\n[bold green]✅ Email configuration is correct![/bold green]")
            console.print("[dim]You can now use 'python main.py digest' to send daily digests[/dim]\n")
        else:
            console.print("\n[red]Email configuration test failed[/red]")
            console.print("[dim]Check EMAIL_SETUP.md for troubleshooting[/dim]\n")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"\n[red]Error testing email: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
