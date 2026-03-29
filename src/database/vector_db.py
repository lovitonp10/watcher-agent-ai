"""
Vector database implementation using ChromaDB.
"""
import os
import warnings

# Suppress ONNX Runtime warnings
os.environ['ORT_LOGGING_LEVEL'] = '3'
warnings.filterwarnings('ignore', category=UserWarning)

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
from pathlib import Path
from rich.console import Console
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

console = Console()


class VectorDatabase:
    """Manages document storage and retrieval in ChromaDB."""

    def __init__(
        self,
        db_path: Path,
        collection_name: str = "tech_watch",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """
        Initialize vector database.

        Args:
            db_path: Path to ChromaDB storage
            collection_name: Name of the collection
            embedding_model: HuggingFace embedding model
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize embedding model
        console.print(f"[cyan]Loading embedding model: {embedding_model}...[/cyan]")
        self.embedding_model = SentenceTransformer(embedding_model)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Tech Watch Agent knowledge base"},
        )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        console.print(f"[green]✓ Vector database initialized at {self.db_path}[/green]")
        console.print(f"[dim]Collection: {self.collection_name} | Documents: {self.collection.count()}[/dim]\n")

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        return self.text_splitter.split_text(text)

    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def document_exists(self, doc_id: str) -> bool:
        """
        Check if a document already exists in the database.

        Args:
            doc_id: Unique document identifier

        Returns:
            True if document exists, False otherwise
        """
        try:
            results = self.collection.get(
                where={"doc_id": doc_id},
                limit=1,
            )
            return len(results["ids"]) > 0
        except Exception:
            return False

    def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        """
        Add documents to the vector database.

        Args:
            documents: List of document dictionaries from ingestion

        Returns:
            Number of documents successfully added
        """
        console.print(f"[cyan]Adding {len(documents)} documents to vector database...[/cyan]")

        added_count = 0
        skipped_count = 0

        for doc in documents:
            try:
                doc_id = doc["doc_id"]

                # Check for duplicates
                if self.document_exists(doc_id):
                    console.print(f"[yellow]  ⊘ Skipped (duplicate): {doc['title'][:60]}...[/yellow]")
                    skipped_count += 1
                    continue

                # Combine title and abstract for chunking
                full_text = f"{doc['title']}\n\n{doc['abstract']}"

                # Chunk the text
                chunks = self._chunk_text(full_text)

                # Generate embeddings
                embeddings = self._generate_embeddings(chunks)

                # Prepare metadata for each chunk
                chunk_ids = [f"{doc_id}:chunk:{i}" for i in range(len(chunks))]
                metadatas = [
                    {
                        "doc_id": doc_id,
                        "title": doc["title"],
                        "url": doc["url"],
                        "source": doc["source"],
                        "published_date": doc["published_date"],
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                    }
                    for i in range(len(chunks))
                ]

                # Add to ChromaDB
                self.collection.add(
                    ids=chunk_ids,
                    embeddings=embeddings,
                    documents=chunks,
                    metadatas=metadatas,
                )

                added_count += 1
                console.print(f"[green]  ✓ Added: {doc['title'][:60]}... ({len(chunks)} chunks)[/green]")

            except Exception as e:
                console.print(f"[red]  ✗ Error adding {doc.get('title', 'unknown')}: {e}[/red]")

        console.print(f"\n[bold green]✅ Added {added_count} new documents[/bold green]")
        if skipped_count > 0:
            console.print(f"[yellow]⊘ Skipped {skipped_count} duplicates[/yellow]")
        console.print(f"[dim]Total documents in database: {self.collection.count()}[/dim]\n")

        return added_count

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents.

        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of relevant document chunks with metadata
        """
        # Generate query embedding
        query_embedding = self._generate_embeddings([query])[0]

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata,
        )

        # Format results
        formatted_results = []
        if results["ids"] and len(results["ids"]) > 0:
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None,
                })

        return formatted_results

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        total_chunks = self.collection.count()

        # Get unique documents
        all_docs = self.collection.get(include=["metadatas"])
        unique_doc_ids = set()
        sources = {}

        for metadata in all_docs["metadatas"]:
            unique_doc_ids.add(metadata["doc_id"])
            source = metadata.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1

        return {
            "total_chunks": total_chunks,
            "total_documents": len(unique_doc_ids),
            "sources": sources,
        }

    def clear_collection(self):
        """Clear all documents from the collection."""
        console.print("[yellow]Clearing collection...[/yellow]")
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(self.collection_name)
        console.print("[green]✓ Collection cleared[/green]")
