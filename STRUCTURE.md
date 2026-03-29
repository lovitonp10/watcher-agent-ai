# Structure du Projet 🏗️

Documentation de l'architecture et de l'organisation du code.

## 📁 Arborescence

```
watcher/
├── 📋 Configuration
│   ├── .env                    # Variables d'environnement (non versionné)
│   ├── .env.example            # Template de configuration
│   ├── .gitignore              # Fichiers ignorés par Git
│   ├── config.py               # Configuration centralisée (Pydantic)
│   └── requirements.txt        # Dépendances Python
│
├── 📖 Documentation
│   ├── README.md               # Vue d'ensemble du projet
│   ├── QUICKSTART.md           # Guide de démarrage rapide
│   ├── SOURCES.md              # Sources de données
│   ├── STRUCTURE.md            # Ce fichier - Architecture
│   └── docs/                   # Documentation détaillée
│       ├── EMAIL_SETUP.md      # Configuration email
│       ├── PROVIDERS.md        # Providers LLM
│       ├── MISTRAL_FREE.md     # Mistral gratuit
│       └── archive/            # Anciennes versions
│
├── 🎯 Points d'Entrée
│   ├── main.py                 # CLI principal (Typer)
│   ├── setup.sh                # Script d'installation
│   ├── schedule_digest.sh      # Script cron pour email
│   └── Makefile                # Commandes make
│
├── 🧪 Tests
│   ├── test_ingestion.py       # Test des scrapers
│   ├── test_database.py        # Test ChromaDB
│   ├── test_llm.py             # Test LLM provider
│   └── test_e2e.py             # Test end-to-end complet
│
├── 📂 Code Source (src/)
│   ├── __init__.py
│   │
│   ├── ingestion/              # Module d'ingestion de données
│   │   ├── __init__.py
│   │   ├── models.py           # Modèle Document (Pydantic)
│   │   ├── arxiv_scraper.py    # Scraper ArXiv
│   │   ├── huggingface_scraper.py  # Scraper HuggingFace
│   │   ├── blog_scraper.py     # Scraper RSS blogs
│   │   └── orchestrator.py     # Coordination de tous les scrapers
│   │
│   ├── database/               # Module base vectorielle
│   │   ├── __init__.py
│   │   └── vector_db.py        # Wrapper ChromaDB + embeddings
│   │
│   ├── rag/                    # Module RAG (Retrieval + Generation)
│   │   ├── __init__.py
│   │   ├── retriever.py        # Recherche vectorielle
│   │   ├── generator.py        # Génération LLM (LiteLLM)
│   │   └── pipeline.py         # Pipeline RAG complet
│   │
│   ├── email/                  # Module email digest
│   │   ├── __init__.py
│   │   └── mailer.py           # Service SMTP
│   │
│   └── cli/                    # Module CLI
│       ├── __init__.py
│       └── commands.py         # Commandes Typer
│
└── 💾 Données
    └── data/
        ├── chroma_db/          # Base ChromaDB (auto-créé)
        └── test_*/             # Bases de test (nettoyables)
```

---

## 🏛️ Architecture Globale

```
┌─────────────┐
│   CLI       │  Typer + Rich
│  (Typer)    │
└──────┬──────┘
       │
       ├─────► Ingestion ────► ArXiv API
       │       Orchestrator    HuggingFace API
       │                       RSS Feeds (feedparser)
       │            │
       │            ▼
       │       ┌────────────┐
       │       │  Document  │  Pydantic Model
       │       │   Model    │
       │       └─────┬──────┘
       │             │
       ├─────────────┘
       │
       ├─────► Database ─────► ChromaDB (local)
       │       (Vector DB)     Sentence-Transformers
       │                       (embeddings locaux)
       │            │
       │            ▼
       │       ┌────────────┐
       │       │   Chunks   │  Text chunks + metadata
       │       │  + Vectors │
       │       └─────┬──────┘
       │             │
       ├─────────────┘
       │
       ├─────► RAG Pipeline
       │       │
       │       ├─► Retriever ──► Recherche vectorielle
       │       │                 Top-K chunks
       │       │
       │       └─► Generator ──► LiteLLM
       │                         OpenAI / Mistral / HuggingFace / Anthropic / Ollama
       │            │
       │            ▼
       │       ┌────────────┐
       │       │  Réponse   │  Answer + Sources
       │       │  + Sources │
       │       └─────┬──────┘
       │             │
       └─────────────┘
       │
       └─────► Email Service ──► SMTP (Gmail, etc.)
               (HTML digest)
```

---

## 📦 Modules Détaillés

### 1. Ingestion (`src/ingestion/`)

**Rôle** : Récupérer et normaliser les contenus depuis différentes sources.

#### `models.py`
```python
class Document(BaseModel):
    """Modèle standardisé pour tous les documents."""
    title: str
    abstract: str
    url: HttpUrl
    source: str
    published_date: datetime
    authors: Optional[list[str]]
    categories: Optional[list[str]]

    def matches_keywords(self, keywords: list[str]) -> bool
    def to_dict(self) -> dict
```

#### `arxiv_scraper.py`
- **Package** : `arxiv` (Python)
- **API** : ArXiv API officielle
- **Filtrage** : Par catégorie (cs.AI, cs.CL, cs.LG) et date
- **Sortie** : Liste de `Document`

#### `huggingface_scraper.py`
- **API** : https://huggingface.co/api/daily_papers
- **Filtrage** : Par date
- **Sortie** : Liste de `Document`

#### `blog_scraper.py`
- **Package** : `feedparser`
- **Format** : RSS/Atom feeds
- **Nettoyage** : BeautifulSoup pour enlever HTML
- **Sortie** : Liste de `Document`

#### `orchestrator.py`
```python
class IngestionOrchestrator:
    """Coordonne tous les scrapers."""
    def fetch_all(self) -> List[Document]:
        # 1. Fetch ArXiv
        # 2. Fetch HuggingFace
        # 3. Fetch Blogs
        # 4. Deduplicate
        # 5. Filter by keywords
        return unique_documents
```

---

### 2. Database (`src/database/`)

**Rôle** : Stockage et recherche vectorielle locale.

#### `vector_db.py`

```python
class VectorDatabase:
    """Wrapper ChromaDB avec embeddings locaux."""

    def __init__(self, db_path, embedding_model, ...):
        self.embedding_model = SentenceTransformer(...)
        self.client = chromadb.PersistentClient(...)
        self.collection = self.client.get_or_create_collection(...)
        self.text_splitter = RecursiveCharacterTextSplitter(...)

    def add_documents(self, documents: List[Dict]) -> int:
        # 1. Chunk le texte (titre + abstract)
        # 2. Génère les embeddings
        # 3. Stocke dans ChromaDB avec metadata
        # 4. Check duplicates

    def search(self, query: str, top_k: int) -> List[Dict]:
        # 1. Génère embedding de la query
        # 2. Recherche vectorielle dans ChromaDB
        # 3. Retourne top-k chunks + metadata

    def get_stats(self) -> Dict:
        # Statistiques de la base
```

**Embeddings** :
- Modèle : `sentence-transformers/all-MiniLM-L6-v2`
- Dimension : 384
- Local, gratuit, rapide

**Chunking** :
- Splitter : `RecursiveCharacterTextSplitter`
- Chunk size : 1000 caractères
- Overlap : 200 caractères

**Metadata stockée** :
- doc_id, title, url, source, published_date, chunk_index

---

### 3. RAG (`src/rag/`)

**Rôle** : Retrieval-Augmented Generation.

#### `retriever.py`

```python
class Retriever:
    """Recherche de documents pertinents."""

    def retrieve(self, query: str, top_k: int) -> List[Dict]:
        # Recherche vectorielle via VectorDatabase

    def format_context(self, results: List[Dict]) -> str:
        # Formate les chunks en contexte pour le LLM

    def get_sources(self, results: List[Dict]) -> List[Dict]:
        # Extrait les sources uniques
```

#### `generator.py`

```python
class Generator:
    """Génération de réponses via LLM."""

    def __init__(self, provider, api_key, model, ...):
        # Support multi-provider via LiteLLM
        # OpenAI, Mistral, HuggingFace, Anthropic, Ollama

    def generate(self, query: str, context: str, sources: List) -> Dict:
        # 1. Format le prompt avec contexte
        # 2. Appel LLM via LiteLLM
        # 3. Retourne answer + sources

    def generate_summary(self, documents: List[Dict]) -> str:
        # Génère un résumé de plusieurs documents
```

**Prompt Template** :
```
System: You are an AI assistant specialized in AI/ML research.
Answer based STRICTLY on the provided context.
Always cite your sources.

Context: {context}

User: {query}
```

#### `pipeline.py`

```python
class RAGPipeline:
    """Pipeline RAG complet."""

    def __init__(self, vector_db, provider, api_key, ...):
        self.retriever = Retriever(vector_db)
        self.generator = Generator(provider, api_key, ...)

    def query(self, question: str) -> Dict:
        # 1. Retrieve relevant chunks
        # 2. Format context
        # 3. Generate answer
        # 4. Return answer + sources + metadata

    def display_response(self, result: Dict):
        # Affichage formaté avec Rich
```

---

### 4. Email (`src/email/`)

**Rôle** : Envoi de digest quotidien par email.

#### `mailer.py`

```python
class EmailService:
    """Service d'envoi d'email."""

    def __init__(self, smtp_host, smtp_port, ...):
        # Configuration SMTP

    def send_digest(self, to_email, new_docs, summary, stats) -> bool:
        # 1. Format HTML digest
        # 2. Format plain text fallback
        # 3. Send via SMTP

    def _format_html_digest(self, ...) -> str:
        # Template HTML élégant avec :
        # - Résumé AI
        # - Statistiques
        # - Liste des nouveaux documents groupés par source

    def test_connection(self) -> bool:
        # Test de connexion SMTP
```

**Format Email** :
- HTML responsive
- Fallback texte brut
- Style : gradient header, sections colorées, liens cliquables

---

### 5. CLI (`src/cli/`)

**Rôle** : Interface en ligne de commande.

#### `commands.py`

```python
app = typer.Typer()  # Application Typer

@app.command()
def update(days, max_results):
    """Mettre à jour la base de connaissances."""
    # 1. Fetch documents via Orchestrator
    # 2. Add to VectorDatabase

@app.command()
def chat(source):
    """Chat interactif."""
    # 1. Initialize RAGPipeline
    # 2. Loop: get question → query → display

@app.command()
def search(query, top_k, source):
    """Recherche unique."""
    # Query + display

@app.command()
def digest(send, preview):
    """Générer et envoyer le digest quotidien."""
    # 1. Fetch last 24h
    # 2. Generate summary
    # 3. Send email

@app.command()
def stats():
    """Statistiques de la base."""

@app.command()
def test_email():
    """Tester la configuration email."""

@app.command()
def info():
    """Afficher la configuration."""

@app.command()
def clear():
    """Effacer la base."""
```

---

## 🔄 Flux de Données

### 1. Ingestion (`python main.py update`)

```
User command
    │
    ▼
┌─────────────────┐
│  CLI: update    │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ IngestionOrchestrator│
└─┬─────────┬────────┬┘
  │         │        │
  ▼         ▼        ▼
ArXiv  HuggingFace  Blogs
  │         │        │
  └────┬────┴────┬───┘
       │         │
       ▼         ▼
  [Document] [Document] ...
       │
       ▼
  Filter by keywords
       │
       ▼
  Deduplicate
       │
       ▼
┌──────────────┐
│ VectorDatabase│
│  .add_documents()│
└───────┬────────┘
        │
        ▼
   ┌─────────┐
   │ChromaDB │
   │ + Chunks│
   │ + Vectors│
   └─────────┘
```

### 2. Query (`python main.py chat`)

```
User question
    │
    ▼
┌──────────────┐
│ RAGPipeline  │
│   .query()   │
└──────┬───────┘
       │
       ├─► Retriever
       │      │
       │      ▼
       │  VectorDatabase.search()
       │      │
       │      ▼
       │  Top-K chunks + metadata
       │      │
       │      ▼
       │  Format context
       │
       └─► Generator
              │
              ▼
          LiteLLM (OpenAI/Mistral/...)
              │
              ▼
          Answer + Sources
              │
              ▼
          Display (Rich)
```

### 3. Email Digest (`python main.py digest`)

```
Cron trigger (8h45)
    │
    ▼
schedule_digest.sh
    │
    ▼
┌──────────────┐
│ CLI: digest  │
└──────┬───────┘
       │
       ├─► Ingestion (last 24h)
       │       │
       │       ▼
       │   New documents
       │
       ├─► Add to database
       │
       ├─► Generate summary (LLM)
       │
       └─► EmailService
               │
               ▼
           Format HTML
               │
               ▼
           Send SMTP
               │
               ▼
           User inbox ✉️
```

---

## 🧩 Technologies & Librairies

### Core

| Lib | Usage | Version |
|-----|-------|---------|
| **Python** | Langage | 3.10+ |
| **Pydantic** | Validation données | 2.5.3 |
| **python-dotenv** | Variables env | 1.0.0 |

### Ingestion

| Lib | Usage | Version |
|-----|-------|---------|
| **arxiv** | API ArXiv | 2.0.0 |
| **feedparser** | RSS parsing | 6.0.10 |
| **requests** | HTTP | 2.31.0 |
| **beautifulsoup4** | HTML parsing | 4.12.3 |

### Vector DB & Embeddings

| Lib | Usage | Version |
|-----|-------|---------|
| **chromadb** | Base vectorielle | 0.4.22 |
| **sentence-transformers** | Embeddings | 2.3.1 |

### RAG & LLM

| Lib | Usage | Version |
|-----|-------|---------|
| **langchain** | Orchestration RAG | 0.1.0 |
| **litellm** | Multi-provider LLM | 1.30.0 |
| **openai** | OpenAI SDK | 1.10.0 |

### CLI

| Lib | Usage | Version |
|-----|-------|---------|
| **typer** | CLI framework | 0.9.0 |
| **rich** | Formatting terminal | 13.7.0 |

---

## 🔧 Configuration (`config.py`)

```python
class Settings(BaseSettings):
    """Configuration centralisée avec Pydantic."""

    # LLM
    llm_provider: str = "openai"
    llm_api_key: str
    llm_model: str = "gpt-4-turbo-preview"
    llm_temperature: float = 0.1

    # Database
    chroma_db_path: Path = Path("./data/chroma_db")
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Ingestion
    days_to_fetch: int = 7
    max_results_per_source: int = 20
    keywords: str = "LLMOps,RAG,..."

    # RAG
    top_k_results: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Email
    email_enabled: bool = False
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    # ... etc

    @property
    def keywords_list(self) -> List[str]:
        return [k.strip() for k in self.keywords.split(",")]

# Sources
BLOG_FEEDS = {...}
ARXIV_CATEGORIES = [...]
LLM_PROVIDERS = {...}
```

Chargé depuis `.env` via `pydantic-settings`.

---

## 🧪 Tests

### `test_ingestion.py`
- Test des 3 scrapers
- Affichage table des résultats
- Vérification filtrage keywords

### `test_database.py`
- Test ChromaDB avec documents mock
- Test embeddings
- Test recherche vectorielle
- Test détection duplicates

### `test_llm.py`
- Test connexion au provider LLM
- Test génération simple
- Validation configuration

### `test_e2e.py`
- Pipeline complet : ingestion → database → RAG
- Avec questions réelles
- Mesure des performances

---

## 📊 Performance

### Ingestion
- **ArXiv** : ~5-10s pour 20 papers
- **HuggingFace** : ~2-5s
- **Blogs** : ~1-2s par blog
- **Total** : ~30-60s pour tout

### Base Vectorielle
- **Ajout documents** : ~1-2s par document (chunking + embeddings)
- **Recherche** : < 100ms pour top-5

### RAG
- **Retrieval** : < 100ms
- **Generation** :
  - OpenAI GPT-4 : 2-5s
  - Mistral Large : 1-3s
  - HuggingFace (gratuit) : 5-30s (cold start)
  - Ollama (local) : 5-15s

### Email
- **Format HTML** : < 1s
- **Envoi SMTP** : 1-3s

---

## 💾 Stockage

### Base ChromaDB
- **Taille** : ~50-100 MB pour 100 documents
- **Croissance** : ~1 MB par document
- **Location** : `./data/chroma_db/`

### Embeddings Model
- **Taille** : ~80 MB (téléchargé une fois)
- **Cache** : `~/.cache/torch/sentence_transformers/`

---

## 🔐 Sécurité

### Secrets
- ✅ `.env` dans `.gitignore`
- ✅ API keys jamais commités
- ✅ Mots de passe SMTP chiffrés en transit (TLS)

### Données
- ✅ Base vectorielle locale (pas de cloud)
- ✅ Embeddings locaux (pas d'API)
- ⚠️ Metadata contient URLs publiques

### API
- ✅ API keys via variables d'environnement
- ✅ Support OAuth2 possible (future)

---

## 🚀 Extension

### Ajouter un Nouveau Scraper

1. **Créer** `src/ingestion/mon_scraper.py` :
```python
class MonScraper:
    def fetch(self, keywords: List[str]) -> List[Document]:
        # Implémenter la logique
        return documents
```

2. **Ajouter** dans `orchestrator.py` :
```python
self.mon_scraper = MonScraper(...)
docs = self.mon_scraper.fetch(self.keywords)
all_documents.extend(docs)
```

### Ajouter un Nouveau Provider LLM

1. **Ajouter** dans `config.py` :
```python
LLM_PROVIDERS["mon_provider"] = {
    "models": [...],
    "default": "...",
}
```

2. **Supporter** dans `generator.py` :
```python
if self.provider == "mon_provider":
    os.environ["MON_PROVIDER_API_KEY"] = api_key
```

LiteLLM gère automatiquement le reste !

### Ajouter une Nouvelle Commande CLI

Dans `src/cli/commands.py` :
```python
@app.command()
def ma_commande(param: str):
    """Description de ma commande."""
    # Implémenter
```

---

## 📚 Ressources

- **ChromaDB Docs** : https://docs.trychroma.com/
- **LangChain Docs** : https://python.langchain.com/
- **LiteLLM Docs** : https://docs.litellm.ai/
- **Typer Docs** : https://typer.tiangolo.com/
- **Rich Docs** : https://rich.readthedocs.io/

---

**Besoin de plus de détails ?** → Consultez le code source directement ! 🔍
