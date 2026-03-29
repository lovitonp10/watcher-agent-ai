# Sources du Tech Watch Agent 🔍

Documentation complète des sources d'information surveillées par l'agent.

## 📚 Vue d'Ensemble

Le Tech Watch Agent récupère du contenu depuis **3 types de sources** :

1. **📄 ArXiv** - Papers scientifiques (IA, ML, NLP)
2. **🤗 Hugging Face** - Daily Papers (derniers modèles et recherches)
3. **📰 Engineering Blogs** - Blogs techniques des GAFAM et startups

Tous les contenus sont **filtrés par mots-clés** pour ne garder que ce qui t'intéresse !

---

## 1️⃣ ArXiv (Papers Scientifiques)

### Catégories Surveillées

```python
cs.AI  - Artificial Intelligence
cs.CL  - Computation and Language (NLP)
cs.LG  - Machine Learning
```

### Ce qui est récupéré

- ✅ Papers publiés dans les **derniers 7 jours** (configurable)
- ✅ Titre, abstract, auteurs, catégories
- ✅ Lien direct vers le PDF
- ✅ Filtré par tes **mots-clés** (LLMOps, RAG, etc.)

### Exemple de contenu

```
Titre: "RAGatouille: Improving Retrieval with Reranking"
Auteurs: John Doe, Jane Smith
Catégorie: cs.AI, cs.CL
Abstract: We introduce RAGatouille, a framework for...
URL: https://arxiv.org/abs/2024.12345
```

### API Utilisée

- **Source** : ArXiv API officielle
- **Package** : `arxiv` (Python)
- **Limite** : 20 papers par catégorie (configurable)
- **Gratuit** : ✅ Oui, aucune clé API requise

---

## 2️⃣ Hugging Face Daily Papers

### Ce qui est récupéré

- ✅ Papers mis en avant par Hugging Face **quotidiennement**
- ✅ Les modèles et techniques les plus populaires
- ✅ Papers avec code et démos
- ✅ Filtré par tes **mots-clés**

### Exemple de contenu

```
Titre: "Mistral-7B: Outperforming Llama 2 13B"
Source: Hugging Face Daily Papers
Abstract: We introduce Mistral 7B, a language model...
URL: https://huggingface.co/papers/2310.06825
```

### API Utilisée

- **Source** : https://huggingface.co/api/daily_papers
- **Gratuit** : ✅ Oui, API publique
- **Limite** : 20 papers (configurable)

---

## 3️⃣ Engineering Blogs (RSS)

### Blogs Surveillés

#### 🔴 **Netflix Tech Blog**
- **URL** : https://netflixtechblog.com/
- **Sujets** : Streaming, ML at scale, Infrastructure, Data Engineering
- **Fréquence** : 1-2 articles/mois

#### 🔵 **Meta AI Blog**
- **URL** : https://ai.meta.com/blog/
- **Sujets** : LLMs (Llama), Computer Vision, Research
- **Fréquence** : 2-3 articles/semaine

#### 🏠 **Airbnb Engineering**
- **URL** : https://medium.com/airbnb-engineering
- **Sujets** : ML Platform, Search & Ranking, Data Science
- **Fréquence** : 1-2 articles/mois

#### 🚗 **Uber Engineering**
- **URL** : https://www.uber.com/blog/engineering/
- **Sujets** : ML Platform, Real-time Systems, Forecasting
- **Fréquence** : 2-3 articles/mois

#### 🔵 **Google AI Blog**
- **URL** : https://blog.research.google/
- **Sujets** : Transformers, Gemini, Research breakthroughs
- **Fréquence** : 3-5 articles/semaine

#### 🟢 **OpenAI Blog**
- **URL** : https://openai.com/blog/
- **Sujets** : GPT, DALL-E, Research updates
- **Fréquence** : 1-2 articles/mois

#### 🔵 **DeepMind Blog**
- **URL** : https://deepmind.google/blog/
- **Sujets** : AlphaFold, Reinforcement Learning, Gemini
- **Fréquence** : 1-2 articles/semaine

### Exemple de contenu

```
Titre: "How Netflix Uses ML for Content Recommendations"
Source: Netflix Tech Blog
Published: 2024-03-15
Abstract: At Netflix, we process billions of events...
URL: https://netflixtechblog.com/...
```

### Technologie

- **Format** : RSS/Atom feeds
- **Parser** : `feedparser` (Python)
- **Gratuit** : ✅ Oui, flux RSS publics
- **Filtré** : Par mots-clés uniquement

---

## ⚙️ Configuration des Sources

### Dans le Code ([config.py](config.py))

```python
# ArXiv Categories
ARXIV_CATEGORIES = ["cs.AI", "cs.CL", "cs.LG"]

# Blog RSS Feeds
BLOG_FEEDS = {
    "Netflix Tech Blog": "https://netflixtechblog.com/feed",
    "Meta AI": "https://ai.meta.com/blog/rss/",
    # ... etc
}
```

### Dans `.env` (Paramètres)

```bash
# Nombre de jours à récupérer
DAYS_TO_FETCH=7

# Nombre max de résultats par source
MAX_RESULTS_PER_SOURCE=20

# Mots-clés pour filtrer (TRÈS IMPORTANT !)
KEYWORDS=LLMOps,RAG,Time Series,Forecasting,GenAI,LLM,Transformer
```

---

## 🔍 Filtrage par Mots-Clés

**TOUS les contenus** sont filtrés par tes mots-clés avant d'être stockés !

### Comment ça marche ?

L'agent cherche tes mots-clés dans :
- ✅ Le **titre** du document
- ✅ L'**abstract/résumé**

Si **au moins 1 mot-clé** est trouvé → Le document est gardé ✅
Sinon → Le document est ignoré ❌

### Exemple

```bash
# Dans .env
KEYWORDS=RAG,LLM,Forecasting

# Paper ArXiv
Titre: "Improving RAG with Hybrid Search"
Abstract: "We propose a new RAG architecture..."
→ ✅ GARDÉ (contient "RAG")

# Blog Post
Titre: "How We Built Our Search Engine"
Abstract: "We use Elasticsearch for search..."
→ ❌ IGNORÉ (pas de mots-clés)
```

### Ajuster les Mots-Clés

Plus tu es **spécifique**, moins tu auras de bruit :

```bash
# Large (beaucoup de résultats)
KEYWORDS=AI,ML,LLM,Data

# Ciblé (résultats pertinents)
KEYWORDS=LLMOps,RAG,Vector Database,Embeddings

# Très spécifique (peu de résultats)
KEYWORDS=LangChain,ChromaDB,Mistral,Claude
```

---

## ➕ Ajouter de Nouvelles Sources

### Ajouter un Blog RSS

1. **Trouver l'URL du flux RSS** du blog
   - Chercher un lien RSS/Atom sur le site
   - Ou utiliser https://rss.app/ pour générer un flux

2. **Éditer [config.py](config.py)** :
   ```python
   BLOG_FEEDS = {
       "Netflix Tech Blog": "https://netflixtechblog.com/feed",
       # ... existing blogs

       # Ajouter ton nouveau blog
       "Ton Blog": "https://tonblog.com/feed",
   }
   ```

3. **Relancer** :
   ```bash
   python main.py update
   ```

### Exemples de Blogs à Ajouter

```python
# Startups/Scale-ups
"Stripe Engineering": "https://stripe.com/blog/engineering/rss",
"Spotify Engineering": "https://engineering.atspotify.com/feed/",
"GitHub Blog": "https://github.blog/feed/",

# Recherche
"Anthropic Blog": "https://www.anthropic.com/news/rss.xml",
"Mistral AI Blog": "https://mistral.ai/news/rss.xml",

# Français
"Doctolib Tech": "https://medium.com/feed/doctolib",
"Blablacar Tech": "https://medium.com/feed/blablacar-tech",
```

### Ajouter une Catégorie ArXiv

1. **Trouver la catégorie** : https://arxiv.org/category_taxonomy
2. **Éditer [config.py](config.py)** :
   ```python
   ARXIV_CATEGORIES = [
       "cs.AI",   # Artificial Intelligence
       "cs.CL",   # Computation and Language
       "cs.LG",   # Machine Learning

       # Ajouter une nouvelle catégorie
       "cs.CV",   # Computer Vision
       "stat.ML", # Machine Learning (Stats)
   ]
   ```

### Catégories ArXiv Populaires

```python
"cs.AI"   - Artificial Intelligence
"cs.CL"   - Natural Language Processing
"cs.LG"   - Machine Learning
"cs.CV"   - Computer Vision
"cs.IR"   - Information Retrieval
"stat.ML" - Machine Learning (Statistics)
"cs.RO"   - Robotics
"cs.DB"   - Databases
```

---

## 📊 Statistiques des Sources

Pour voir d'où viennent tes documents :

```bash
python main.py stats
```

Exemple de sortie :
```
Documents: 156
Chunks: 478

Sources:
  • arxiv: 234 chunks (75 documents)
  • huggingface: 123 chunks (42 documents)
  • meta_ai: 67 chunks (22 documents)
  • netflix_tech_blog: 54 chunks (17 documents)
```

---

## 🔄 Fréquence de Mise à Jour

### Sources en Temps Réel

- **ArXiv** : Nouveaux papers chaque jour à ~18h (EDT)
- **Hugging Face** : Mise à jour quotidienne
- **Blogs** : Variable selon le blog (RSS polling)

### Recommandations

```bash
# Mise à jour quotidienne (recommandé)
45 8 * * * /chemin/vers/schedule_digest.sh

# Mise à jour 2x/jour (plus complet)
0 8,18 * * * /chemin/vers/schedule_digest.sh

# Mise à jour hebdomadaire (économique)
0 9 * * 1 /chemin/vers/schedule_digest.sh
```

---

## 🎯 Optimiser les Sources

### Pour Plus de Résultats

```bash
# Dans .env
DAYS_TO_FETCH=14           # 14 jours au lieu de 7
MAX_RESULTS_PER_SOURCE=50  # 50 au lieu de 20
KEYWORDS=AI,ML,LLM         # Mots-clés larges
```

### Pour Moins de Bruit

```bash
DAYS_TO_FETCH=3            # 3 jours seulement
MAX_RESULTS_PER_SOURCE=10  # 10 résultats max
KEYWORDS=LLMOps,RAG,Vector Search  # Très spécifique
```

### Pour des Sujets Spécifiques

**Time Series & Forecasting :**
```bash
ARXIV_CATEGORIES=["cs.LG", "stat.ML"]
KEYWORDS=Time Series,Forecasting,ARIMA,Prophet,LSTM,Transformer
```

**NLP & LLMs :**
```bash
ARXIV_CATEGORIES=["cs.CL", "cs.AI"]
KEYWORDS=LLM,GPT,BERT,Transformer,NLP,RAG,Embedding
```

**Computer Vision :**
```bash
ARXIV_CATEGORIES=["cs.CV", "cs.AI"]
KEYWORDS=Vision,YOLO,Segmentation,Detection,Diffusion,CLIP
```

---

## 🚫 Supprimer des Sources

### Désactiver Temporairement

**Commentez dans [config.py](config.py)** :
```python
BLOG_FEEDS = {
    "Netflix Tech Blog": "https://netflixtechblog.com/feed",
    # "Meta AI": "https://ai.meta.com/blog/rss/",  # Temporairement désactivé
}
```

### Filtrer par Source dans les Requêtes

```bash
# Chercher seulement dans ArXiv
python main.py chat --source arxiv

# Chercher seulement dans les blogs
python main.py search "LLMOps" --source meta_ai
```

---

## 📝 Résumé

| Source | Type | Gratuit | Fréquence | Filtrage |
|--------|------|---------|-----------|----------|
| **ArXiv** | Papers | ✅ | Quotidien | Mots-clés |
| **Hugging Face** | Papers | ✅ | Quotidien | Mots-clés |
| **Engineering Blogs** | Articles | ✅ | Variable | Mots-clés |

**Total de sources configurées** : 9 sources (3 ArXiv categories + 1 HF + 7 blogs)

**Personnalisables** : Oui, modifiez [config.py](config.py)

**Coût** : 0€ (toutes les sources sont gratuites et publiques)

---

## 🔧 Commandes Utiles

```bash
# Voir la configuration actuelle
python main.py info

# Tester l'ingestion
python test_ingestion.py

# Forcer une mise à jour
python main.py update

# Voir les statistiques
python main.py stats
```

---

Des questions sur les sources ? Consulte [config.py](config.py) ou ouvre une issue ! 🚀
