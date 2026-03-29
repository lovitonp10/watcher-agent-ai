# 🚀 Utilisation Quotidienne - Tech Watch Agent

Guide de référence pour l'utilisation quotidienne du Tech Watch Agent.

---

## ⚡ Démarrage Rapide (3 commandes)

```bash
# 1. Activer l'environnement
cd watcher && source venv/bin/activate

# 2. Récupérer les nouveaux contenus
python main.py update

# 3. Poser des questions
python main.py chat
```

**Exemples de questions:**
```
> Quelles sont les dernières techniques pour prédire la viralité vidéo ?
> Comment TikTok optimise son algorithme de recommandation ?
> Résume les avancées en explainability pour les modèles multimodaux
```

Tapez `exit` pour quitter.

---

## 💻 Commandes Principales

| Commande | Usage |
|----------|-------|
| `python main.py update` | Récupérer les nouveaux contenus |
| `python main.py update --days 30` | Récupérer 30 jours de contenus |
| `python main.py chat` | Chat interactif avec la base |
| `python main.py search "..."` | Recherche rapide |
| `python main.py stats` | Statistiques de la base |
| `python main.py info` | Voir la configuration actuelle |
| `python main.py clear --yes` | Vider la base (⚠️ destructif) |

---

## 📧 Email Digest

### Digest Quotidien (nouveautés 24h)
```bash
python main.py digest --preview      # Prévisualiser
python main.py digest --send         # Envoyer par email
```

### Digest Hebdomadaire (lundi uniquement)
```bash
python main.py digest --frequency weekly --send
```

### Résumé de Toute la Base
```bash
python main.py digest --full-database --preview
python main.py digest --full-database --send
```

### Combo Hebdo Complet (recommandé pour lundi matin)
```bash
python main.py digest --frequency weekly --full-database --send
```

**📚 Plus d'infos**: Voir [docs/DIGEST_OPTIONS.md](docs/DIGEST_OPTIONS.md)

---

## ⚙️ Personnalisation

Toute la configuration métier est dans `configs/*.yaml`. Les secrets (API keys, SMTP) restent dans `.env`.

### Modifier les Mots-Clés
```bash
nano configs/keywords.yaml
```

### Ajouter/Supprimer des Sources
```bash
nano configs/sources.yaml
```

### Modifier les Catégories ArXiv
```bash
nano configs/arxiv_categories.yaml
```

### Configuration LLM (Provider, Modèle, Température)
```bash
nano configs/llm.yaml
# llm_provider: ollama | openai | mistral | anthropic | groq
# llm_model: mistral | gpt-4 | claude-sonnet-4-6 | ...
# llm_temperature: 0.1
```
**Secrets LLM** (API keys) restent dans `.env` :
```bash
nano .env
# LLM_API_KEY=your-key-here
# LLM_BASE_URL=http://localhost:11434
```

### Configuration Ingestion (Jours, Max Résultats)
```bash
nano configs/ingestion.yaml
# days_to_fetch: 7
# max_results_per_source: 15
```

### Configuration RAG (Chunks, Embeddings, Vector DB)
```bash
nano configs/rag.yaml
# chunk_size: 1000
# chunk_overlap: 200
# embedding_model: sentence-transformers/all-MiniLM-L6-v2
# top_k_results: 5
# chroma_db_path: ./data/chroma_db
```

### Configuration Digest (Qualité Résumé, Max Articles)
```bash
nano configs/digest.yaml
# summary_mode: short | full
# max_articles_in_email: 15
# max_docs_for_summary: 50
```

**💡 Mode "full" recommandé pour :**
- Digest hebdomadaire complet (`--frequency weekly --full-database`)
- Quand tu veux un résumé très détaillé et précis
- Si ton LLM est rapide (Groq, Claude, GPT-4)

**⚡ Mode "short" recommandé pour :**
- Digest quotidien rapide
- Ollama local (plus lent)
- Beaucoup de documents (>30)

### Configuration Email (SMTP, Credentials)
```bash
nano .env
# EMAIL_ENABLED=true
# SMTP_HOST=smtp.gmail.com
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
# EMAIL_FROM=your-email@gmail.com
# EMAIL_TO=recipient@example.com
```

---

## 🔧 Maintenance

### Vérifier qu'Ollama Tourne
```bash
ollama list                    # Liste les modèles
curl http://localhost:11434    # Test connexion
```

Si erreur:
```bash
ollama serve                   # Démarrer Ollama
```

### Vérifier la Configuration
```bash
python main.py info            # Voir config actuelle
./verify_setup.sh              # Vérification complète
```

### Mettre à Jour les Dépendances
```bash
pip install --upgrade -r requirements.txt
```

---

## 🎯 Workflows Recommandés

### Usage Quotidien
```bash
source venv/bin/activate
python main.py update          # Nouveautés du jour
python main.py chat            # Poser questions
```

### Recherche Ciblée
```bash
python main.py search "video virality prediction"
python main.py search "TikTok algorithm" --verbose
python main.py search "multimodal AI" --source arxiv
```

### Résumé Hebdomadaire (lundi)
```bash
python main.py update --days 7
python main.py digest --frequency weekly --full-database --send
```

### Charger Beaucoup de Contenu
```bash
python main.py update --days 30
python main.py stats
python main.py digest --full-database --preview
```

---

## 🐛 Problèmes Fréquents

### "Connection refused" / Ollama ne répond pas
```bash
# Solution
ollama serve
```

### "Model not found"
```bash
# Solution
ollama pull mistral
```

### "Database is empty"
```bash
# Solution
python main.py update --days 7
```

### Email ne s'envoie pas
```bash
# Vérifier config email
python main.py test-email

# Vérifier .env
nano .env
# EMAIL_ENABLED=true
# SMTP_*, EMAIL_*
```

### ArXiv rate limiting (HTTP 429)
```bash
# Réduire le nombre de catégories
nano configs/arxiv_categories.yaml
# Commenter les catégories optionnelles
```

### Ollama trop lent
Alternatives:
- **Groq** (gratuit, ultra-rapide) → [docs/SETUP_GITHUB_ACTIONS.md](docs/SETUP_GITHUB_ACTIONS.md)
- **Mistral AI** (~2€/mois) → [docs/ALTERNATIVES.md](docs/ALTERNATIVES.md)

---

## 🤖 Automatisation

### Cron Local (digest quotidien à 8h45)
```bash
crontab -e

# Ajouter:
45 8 * * * cd /path/to/watcher && venv/bin/python main.py digest --send
```

### GitHub Actions (gratuit, PC peut être éteint)
Voir [docs/SETUP_GITHUB_ACTIONS.md](docs/SETUP_GITHUB_ACTIONS.md)

### Google Cloud (VM gratuite à vie)
Voir [docs/SETUP_GCP_FREE_TIER.md](docs/SETUP_GCP_FREE_TIER.md)

**📚 Toutes les options**: [docs/AUTOMATION_OPTIONS.md](docs/AUTOMATION_OPTIONS.md)

---

## 📊 Fichiers de Configuration

### Secrets (`.env`)
| Fichier | Contenu |
|---------|---------|
| `.env` | API keys, SMTP credentials, secrets |

### Configuration Métier (`configs/*.yaml`)
| Fichier | Contenu |
|---------|---------|
| `configs/keywords.yaml` | 39 mots-clés pour filtrer les contenus |
| `configs/sources.yaml` | 27 blogs RSS + tags |
| `configs/arxiv_categories.yaml` | 5 catégories ArXiv actives |
| `configs/llm.yaml` | Provider, modèle, température LLM |
| `configs/ingestion.yaml` | Paramètres de récupération (jours, max résultats) |
| `configs/rag.yaml` | Vector DB, chunks, embeddings |
| `configs/digest.yaml` | Options email digest (mode résumé, max articles) |

### Données
| Fichier | Contenu |
|---------|---------|
| `data/chroma_db/` | Base vectorielle (créée automatiquement) |

---

## 📚 Documentation Complète

| Fichier | Usage |
|---------|-------|
| **[README.md](README.md)** | Vue d'ensemble du projet |
| **[INSTALL.md](INSTALL.md)** | Guide d'installation complet |
| **[STRUCTURE.md](STRUCTURE.md)** | Architecture du code |
| **[SOURCES.md](SOURCES.md)** | Sources de données (blogs, ArXiv) |
| **[docs/AUTOMATION.md](docs/AUTOMATION.md)** | Automatisation (GitHub, Cron, GCP) |
| **[docs/ALTERNATIVES.md](docs/ALTERNATIVES.md)** | Alternatives LLM (Groq, OpenAI, etc.) |
| **[docs/DIGEST_OPTIONS.md](docs/DIGEST_OPTIONS.md)** | Options digest détaillées |
| **[PROJECT_STATUS.md](PROJECT_STATUS.md)** | État du projet après réorganisation |

---

## ⚡ One-Liners Utiles

### Copy-Paste Quotidien
```bash
cd watcher && source venv/bin/activate && python main.py update && python main.py chat
```

### Digest Complet du Lundi
```bash
cd watcher && source venv/bin/activate && python main.py digest --frequency weekly --full-database --send
```

### Charger 30 Jours et Chercher
```bash
cd watcher && source venv/bin/activate && python main.py update --days 30 && python main.py search "video virality"
```

### Vérifier que Tout Marche
```bash
cd watcher && ./verify_setup.sh
```

---

## 🎯 Cas d'Usage Spécifiques

### Rechercher sur un Concurrent (VidIQ, TubeBuddy)
```bash
python main.py search "VidIQ thumbnail optimization"
python main.py search "TubeBuddy analytics"
```

### Suivre les Algos TikTok/Instagram
```bash
python main.py search "TikTok algorithm"
python main.py search "Instagram reels recommendation"
python main.py chat
> Quelles sont les dernières infos sur l'algo FYP de TikTok ?
```

### Explorer l'Explicabilité
```bash
python main.py search "SHAP explainability"
python main.py search "attention mechanism interpretability"
```

### Comparer Papiers ArXiv
```bash
python main.py chat
> Compare les approches récentes pour la prédiction de viralité vidéo
```

---

## 🎉 C'est Tout !

**Questions?** Consulte [PROJECT_STATUS.md](PROJECT_STATUS.md) ou [docs/](docs/)

**Besoin d'aide?** Lance `./verify_setup.sh` pour diagnostiquer les problèmes.

---

**🚀 Prêt à surveiller l'avenir de l'IA vidéo !**
