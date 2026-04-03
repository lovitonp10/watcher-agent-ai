"""
Generator for creating LLM responses with retrieved context.
Supports multiple LLM providers via LiteLLM.
"""
from typing import List, Dict, Any
import os
from litellm import completion
from rich.console import Console

console = Console()


class Generator:
    """Handles response generation using LLM via LiteLLM."""

    def __init__(
        self,
        provider: str = "openai",
        api_key: str = None,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.1,
        base_url: str = None,
    ):
        """
        Initialize generator with multi-provider support.

        Args:
            provider: LLM provider (openai, mistral, anthropic, ollama)
            api_key: API key for the provider
            model: Model name
            temperature: Generation temperature
            base_url: Optional custom base URL (for Ollama, etc.)
        """
        self.provider = provider.lower()
        self.model = self._format_model_name(model)
        self.temperature = temperature

        # Fix HuggingFace base URL (they migrated to new endpoint in 2024)
        if self.provider == "huggingface" and not base_url:
            # New HuggingFace Inference API endpoint
            self.base_url = "https://api-inference.huggingface.co/models"
            console.print("[yellow]Note: Using HuggingFace Inference API (may have rate limits)[/yellow]")
        # For cloud providers (Groq, OpenAI, Anthropic, Mistral), ignore base_url from .env
        elif self.provider in ["groq", "openai", "anthropic", "mistral"] and base_url and "localhost" in base_url:
            # User has Ollama base_url in .env, but using cloud provider - ignore it
            console.print(f"[dim]Ignoring LLM_BASE_URL for {self.provider} (using default API endpoint)[/dim]")
            self.base_url = None
        else:
            self.base_url = base_url

        # Set API key in environment for LiteLLM
        if api_key:
            if self.provider == "openai":
                os.environ["OPENAI_API_KEY"] = api_key
            elif self.provider == "mistral":
                os.environ["MISTRAL_API_KEY"] = api_key
            elif self.provider == "anthropic":
                os.environ["ANTHROPIC_API_KEY"] = api_key
            elif self.provider == "groq":
                os.environ["GROQ_API_KEY"] = api_key
            elif self.provider == "huggingface":
                os.environ["HUGGINGFACE_API_KEY"] = api_key
                os.environ["HF_TOKEN"] = api_key  # Alternative env var

        # Set base URL only if it's defined and not a cloud provider
        if self.base_url and self.provider not in ["groq", "openai", "anthropic", "mistral"]:
            os.environ[f"{self.provider.upper()}_API_BASE"] = self.base_url

        # Log model (already contains provider prefix from _format_model_name)
        console.print(f"[dim]Using LLM: {self.model}[/dim]")

    def _format_model_name(self, model: str) -> str:
        """
        Format model name for LiteLLM provider prefix.

        Args:
            model: Model name

        Returns:
            Properly formatted model name with provider prefix
        """
        # If model already has provider prefix, return as is
        if model.startswith(("huggingface/", "mistral/", "anthropic/", "ollama/", "groq/")):
            return model

        # Handle sentence-transformers models
        if model.startswith("sentence-transformers"):
            return model

        # Add provider prefix for LiteLLM
        if self.provider == "mistral" and not model.startswith("mistral/"):
            return f"mistral/{model}"
        elif self.provider == "anthropic" and not model.startswith("anthropic/"):
            return f"anthropic/{model}"
        elif self.provider == "ollama" and not model.startswith("ollama/"):
            return f"ollama/{model}"
        elif self.provider == "groq" and not model.startswith("groq/"):
            return f"groq/{model}"
        elif self.provider == "huggingface":
            # HuggingFace models already have org/model format
            if "/" in model:
                return f"huggingface/{model}"
            return model

        return model

    def _create_system_prompt(self, context: str) -> str:
        """Create system prompt with context."""
        return f"""You are a helpful AI assistant specialized in AI/ML research and engineering.
Your task is to answer questions based on the provided context from recent papers, blog posts, and research articles.

IMPORTANT INSTRUCTIONS:
1. Base your answer STRICTLY on the provided context
2. Always cite your sources by referencing the document titles and URLs
3. If the context doesn't contain enough information, say so explicitly
4. Provide clear, concise, and technical answers
5. When discussing techniques or methods, include relevant details from the context
6. Format your citations as: [Source: Title](URL)

Context:
{context}"""

    def generate(
        self,
        query: str,
        context: str,
        sources: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Generate answer using LLM.

        Args:
            query: User query
            context: Retrieved context
            sources: List of source documents

        Returns:
            Dictionary with answer and sources
        """
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": self._create_system_prompt(context)},
                {"role": "user", "content": query},
            ]

            # Call LiteLLM with longer timeout for slow local LLMs
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "timeout": 1200,  # 20 minutes for slow LLMs
            }
            # Only add api_base if it's defined (not for cloud providers)
            if self.base_url:
                kwargs["api_base"] = self.base_url

            response = completion(**kwargs)

            # Extract answer
            answer = response.choices[0].message.content

            return {
                "answer": answer,
                "sources": sources,
                "success": True,
            }

        except Exception as e:
            console.print(f"[red]Error generating response: {e}[/red]")
            return {
                "answer": f"Error generating response: {str(e)}",
                "sources": [],
                "success": False,
            }

    def generate_summary(self, documents: List[Dict[str, Any]], project_context: str = None, summary_mode: str = "short") -> str:
        """
        Generate a summary of multiple documents with optional project context.

        Args:
            documents: List of documents with metadata
            project_context: Optional project context to focus the summary
            summary_mode: "short" (title+abstract) or "full" (complete chunks content)

        Returns:
            Summary text
        """
        if not documents:
            return "No documents to summarize."

        # Format documents for summary with better handling of missing abstracts
        doc_list = []
        for i, doc in enumerate(documents, 1):
            # Use full content if available (mode=full), otherwise use short preview
            if summary_mode == "full" and doc.get('full_content'):
                # Use complete chunk content (can be long)
                content = doc['full_content']
                # Truncate to 2000 chars max per doc to avoid token explosion
                if len(content) > 2000:
                    content = content[:2000] + "\n[...content truncated...]"
            else:
                # Get content preview from multiple possible fields (short mode)
                content = (
                    doc.get('abstract') or
                    doc.get('summary') or
                    doc.get('description') or
                    doc.get('content_preview') or
                    'Contenu disponible via le lien'
                )
                # Truncate content
                if len(content) > 200:
                    content = content[:200] + "..."

            doc_list.append(
                f"{i}. **{doc['title']}**\n"
                f"   Source: {doc['source']} | Date: {doc['published_date']}\n"
                f"   {content}"
            )

        context = "\n\n".join(doc_list)

        # Build system prompt with optional project context
        system_prompt = """You are an AI research assistant specialized in AI/ML.

TASK: List the 4-5 most recent or interesting articles with their themes in a few words each.

FORMAT YOUR RESPONSE AS A SIMPLE LIST:
• Article #X (Source): Theme in 5-8 words
• Article #Y (Source): Theme in 5-8 words
• ...

Example:
• Article #1 (ArXiv): Video popularity prediction using multimodal transformers
• Article #2 (Meta): Instagram Reels recommendation algorithm improvements
• Article #3 (Netflix): A/B testing framework for video engagement

Keep it ultra-concise. Maximum 4-5 articles. Just list themes, no elaboration."""

        if project_context:
            system_prompt += f"\n\n{project_context}"

        # Prepare messages
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Summarize these recent AI/ML developments:\n\n{context}"
            },
        ]

        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "timeout": 1200,  # 20 minutes for slow local LLMs
            }
            if self.base_url:
                kwargs["api_base"] = self.base_url

            response = completion(**kwargs)

            return response.choices[0].message.content

        except Exception as e:
            console.print(f"[red]Error generating summary: {e}[/red]")
            return f"Error generating summary: {str(e)}"

    def generate_article_summary(self, title: str, content: str, max_words: int = 50) -> str:
        """
        Generate a concise summary for a single article.

        Args:
            title: Article title
            content: Article content (can be full chunks or abstract)
            max_words: Maximum words in summary

        Returns:
            Concise summary (1-2 sentences)
        """
        if not content or len(content) < 50:
            return "Résumé non disponible"

        # Truncate content to avoid token overflow
        content_truncated = content[:2000] if len(content) > 2000 else content

        messages = [
            {
                "role": "system",
                "content": "You are a technical writer. Summarize articles in 1-2 clear sentences (max 50 words). Focus on the main contribution or finding. Be concise and factual."
            },
            {
                "role": "user",
                "content": f"Summarize this article in 1-2 sentences:\n\nTitle: {title}\n\nContent: {content_truncated}"
            },
        ]

        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.3,  # Lower for consistency
                "max_tokens": 100,
                "timeout": 300,  # 5 minutes for short summaries
            }
            if self.base_url:
                kwargs["api_base"] = self.base_url

            response = completion(**kwargs)

            summary = response.choices[0].message.content.strip()
            return summary if summary else "Résumé non disponible"

        except Exception as e:
            console.print(f"[yellow]Warning: Failed to generate summary for '{title[:50]}...': {e}[/yellow]")
            return content_truncated[:200] + "..."  # Fallback to first 200 chars
