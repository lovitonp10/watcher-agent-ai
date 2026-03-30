"""
Configuration management for Tech Watch Agent.
Loads settings from .env and configs/*.yaml files.
"""
import os
from pathlib import Path
from typing import List, Dict
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


def load_yaml_config(filename: str) -> dict:
    """Load configuration from YAML file."""
    config_path = Path(__file__).parent / "configs" / filename
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


class Settings(BaseSettings):
    """Application settings loaded from environment variables and YAML configs."""

    # === Secrets from .env (API keys, credentials) ===
    llm_api_key: str = "ollama"
    llm_base_url: str | None = None  # Only needed for local Ollama, not for cloud providers

    # Email Configuration (secrets)
    email_enabled: bool = False
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = ""
    email_to: str = ""
    email_use_tls: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # === Configuration from YAML files (business logic) ===

    @property
    def llm_provider(self) -> str:
        """Load LLM provider from environment or YAML."""
        # Environment variable takes precedence (for GitHub Actions)
        env_provider = os.getenv("LLM_PROVIDER")
        if env_provider:
            return env_provider
        # Fallback to YAML config
        config = load_yaml_config("llm.yaml")
        return config.get("llm_provider", "ollama")

    @property
    def llm_model(self) -> str:
        """Load LLM model from environment or YAML."""
        # Environment variable takes precedence (for GitHub Actions)
        env_model = os.getenv("LLM_MODEL")
        if env_model:
            return env_model
        # Fallback to YAML config
        config = load_yaml_config("llm.yaml")
        return config.get("llm_model", "mistral")

    @property
    def llm_temperature(self) -> float:
        """Load LLM temperature from YAML."""
        config = load_yaml_config("llm.yaml")
        return config.get("llm_temperature", 0.1)

    @property
    def chroma_db_path(self) -> Path:
        """Load ChromaDB path from YAML."""
        config = load_yaml_config("rag.yaml")
        path_str = config.get("chroma_db_path", "./data/chroma_db")
        return Path(path_str)

    @property
    def days_to_fetch(self) -> int:
        """Load days to fetch from environment or YAML."""
        # Environment variable takes precedence (for GitHub Actions)
        env_days = os.getenv("DAYS_TO_FETCH")
        if env_days:
            return int(env_days)
        # Fallback to YAML config
        config = load_yaml_config("ingestion.yaml")
        return config.get("days_to_fetch", 7)

    @property
    def max_results_per_source(self) -> int:
        """Load max results per source from environment or YAML."""
        # Environment variable takes precedence (for GitHub Actions)
        env_max = os.getenv("MAX_RESULTS_PER_SOURCE")
        if env_max:
            return int(env_max)
        # Fallback to YAML config
        config = load_yaml_config("ingestion.yaml")
        return config.get("max_results_per_source", 15)

    @property
    def top_k_results(self) -> int:
        """Load top K results from YAML."""
        config = load_yaml_config("rag.yaml")
        return config.get("top_k_results", 5)

    @property
    def chunk_size(self) -> int:
        """Load chunk size from YAML."""
        config = load_yaml_config("rag.yaml")
        return config.get("chunk_size", 1000)

    @property
    def chunk_overlap(self) -> int:
        """Load chunk overlap from YAML."""
        config = load_yaml_config("rag.yaml")
        return config.get("chunk_overlap", 200)

    @property
    def embedding_model(self) -> str:
        """Load embedding model from YAML."""
        config = load_yaml_config("rag.yaml")
        return config.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")

    @property
    def digest_summary_mode(self) -> str:
        """Load digest summary mode from YAML."""
        config = load_yaml_config("digest.yaml")
        return config.get("summary_mode", "short")

    @property
    def digest_default_frequency(self) -> str:
        """Load default digest frequency from YAML."""
        config = load_yaml_config("digest.yaml")
        return config.get("default_frequency", "daily")

    @property
    def digest_max_articles_in_email(self) -> int:
        """Load max articles in email from YAML."""
        config = load_yaml_config("digest.yaml")
        return config.get("max_articles_in_email", 15)

    @property
    def digest_max_docs_for_summary(self) -> int:
        """Load max docs for summary from YAML."""
        config = load_yaml_config("digest.yaml")
        return config.get("max_docs_for_summary", 50)

    @property
    def keywords_list(self) -> List[str]:
        """Load keywords from environment or YAML config."""
        # Environment variable takes precedence (for GitHub Actions)
        # Expected format: comma-separated string
        env_keywords = os.getenv("KEYWORDS")
        if env_keywords:
            # Split by comma and strip whitespace
            return [kw.strip() for kw in env_keywords.split(",") if kw.strip()]
        # Fallback to YAML config
        config = load_yaml_config("keywords.yaml")
        if config and "keywords" in config:
            return config["keywords"]
        # Fallback to default if YAML not found
        return ["Video Understanding", "Multimodal AI", "Video Popularity"]

    @property
    def api_key(self) -> str:
        """Get the API key for the LLM provider."""
        if self.llm_api_key:
            return self.llm_api_key
        raise ValueError(f"No API key configured for provider: {self.llm_provider}")


# Supported LLM Providers and their models
LLM_PROVIDERS = {
    "openai": {
        "models": ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"],
        "default": "gpt-4-turbo-preview",
    },
    "mistral": {
        "models": [
            "mistral-large-latest",
            "mistral-medium-latest",
            "mistral-small-latest",
            "open-mistral-7b",
            "open-mixtral-8x7b",
        ],
        "default": "mistral-large-latest",
    },
    "anthropic": {
        "models": ["claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5"],
        "default": "claude-sonnet-4-6",
    },
    "ollama": {
        "models": ["llama3", "mistral", "mixtral", "phi"],
        "default": "mistral",
    },
    "groq": {
        "models": [
            "mixtral-8x7b-32768",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "gemma-7b-it",
        ],
        "default": "mixtral-8x7b-32768",
    },
}


def load_blog_feeds() -> Dict[str, str]:
    """Load blog feeds from YAML config."""
    config = load_yaml_config("sources.yaml")
    feeds = {}

    if config and "blog_feeds" in config:
        for category, blogs in config["blog_feeds"].items():
            # Skip competitor category (loaded separately)
            if category == "direct_competitors":
                continue
            for name, data in blogs.items():
                if isinstance(data, dict) and "url" in data:
                    feeds[name] = data["url"]
                else:
                    feeds[name] = data

    return feeds


def load_competitor_feeds() -> Dict[str, str]:
    """Load competitor feeds from YAML config."""
    config = load_yaml_config("sources.yaml")
    feeds = {}

    if config and "blog_feeds" in config:
        if "direct_competitors" in config["blog_feeds"]:
            competitors = config["blog_feeds"]["direct_competitors"]
            for name, data in competitors.items():
                if isinstance(data, dict) and "url" in data:
                    feeds[name] = data["url"]
                else:
                    feeds[name] = data

    return feeds


def load_arxiv_categories() -> List[str]:
    """Load ArXiv categories from YAML config."""
    config = load_yaml_config("arxiv_categories.yaml")
    if config and "active_categories" in config:
        return config["active_categories"]

    # Fallback to default
    return ["cs.CV", "cs.AI", "cs.LG", "cs.CL", "cs.SI"]


# Load configurations from YAML files
BLOG_FEEDS = load_blog_feeds()
COMPETITOR_FEEDS = load_competitor_feeds()
ARXIV_CATEGORIES = load_arxiv_categories()