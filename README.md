# Tech Watch Agent 🤖

Système de veille technologique automatisé avec RAG local, LLM gratuit et email quotidien.

**💡 100% Gratuit et Local** : Ollama + Mistral, aucune clé API requise.

---

## 🚀 Démarrage

### 1. Installation (5 min)
→ **[INSTALL.md](INSTALL.md)** - Guide complet

```bash
./setup_ollama.sh
```

### 2. Utilisation Quotidienne
→ **[RUN.md](RUN.md)** - Guide ultra-court

```bash
source venv/bin/activate
python main.py update
python main.py chat
```

---

## ✨ Ce que ça fait

- 🔍 **Surveille** : ArXiv, Hugging Face, 7+ blogs techniques
- 💾 **Stocke** : Base vectorielle locale (ChromaDB)
- 💬 **Répond** : Questions en langage naturel avec sources
- 📧 **Envoie** : Email quotidien avec résumé (optionnel)
- 🆓 **Gratuit** : Ollama local, aucun coût API

---

## 📊 Sources Surveillées

| Source | Contenu |
|--------|---------|
| **ArXiv** | Papers cs.AI, cs.CL, cs.LG |
| **Hugging Face** | Daily papers |
| **Netflix, Meta, Google AI** | Blogs techniques |
| **OpenAI, DeepMind** | Research blogs |
| **+ 3 autres** | Airbnb, Uber |

**Tous filtrés par vos mots-clés** → [SOURCES.md](SOURCES.md)

---

## 💻 Commandes

```bash
python main.py update        # Récupérer contenus
python main.py chat          # Poser questions
python main.py search "..."  # Recherche rapide
python main.py stats         # Statistiques
python test_llm.py           # Tester config
```

---

## 📚 Documentation

| Fichier | Usage |
|---------|-------|
| **[INSTALL.md](INSTALL.md)** | Installation complète |
| **[RUN.md](RUN.md)** | Utilisation quotidienne |
| **[SOURCES.md](SOURCES.md)** | Personnaliser sources |
| **[ALTERNATIVES.md](ALTERNATIVES.md)** | Autres LLM (Mistral AI, Groq) |
| **[STRUCTURE.md](STRUCTURE.md)** | Architecture code |

---

## 🛠️ Stack Technique

- **Ollama** + **Mistral 7B** - LLM local gratuit
- **ChromaDB** - Base vectorielle locale
- **Sentence Transformers** - Embeddings locaux
- **LangChain** - Orchestration RAG
- **Typer + Rich** - CLI élégante

---

## 💰 Coût

**0€** - 100% gratuit et local

---

## 🔄 Alternatives

Ollama est gratuit mais vous pouvez utiliser :
- **Mistral AI** (~2€/mois) - Plus rapide
- **Groq** (gratuit*) - Ultra-rapide
- **OpenAI** (~5€/mois) - GPT-4

Voir [ALTERNATIVES.md](ALTERNATIVES.md)

---

## 📄 Licence

MIT

---

**🚀 Installer** → [INSTALL.md](INSTALL.md)

**💻 Utiliser** → [RUN.md](RUN.md)
