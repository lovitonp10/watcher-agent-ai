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
python main.py digest        # Envoyer digest email
python test_llm.py           # Tester config
```

---

## 📧 Email Digest & Filtrage Intelligent

Le système génère des emails quotidiens/hebdomadaires avec analyse par LLM de chaque article.

### 🎯 "For Video Popularity Project" - Filtrage Intelligent

Chaque article affiche une section **"For Video Popularity Project"** avec 3 statuts possibles :

#### ✅ Article Pertinent → Insights Générés
```
🎯 For Video Popularity Project
🎯 Levers:
• Apply entropy-based token selection for efficient video processing
• Implement cross-modal attention for engagement prediction

💰 Benefits:
• 40% memory reduction → process longer videos
• 15-20% accuracy improvement on complex scenes
```
**Signification** : Le LLM a analysé l'article et généré des insights actionnables pour votre projet.

#### ⚪ Article Non Pertinent → Filtré
```
🎯 For Video Popularity Project
Not directly applicable to video popularity prediction
```
**Signification** : Le LLM a **intelligemment filtré** l'article car il n'est pas pertinent (ex: robotique, chip design, médical). **Ce n'est PAS une erreur**, c'est une décision intentionnelle du LLM pour éviter le bruit.

Exemples d'articles filtrés :
- "Robot Reinforcement Learning" → Pas de rapport avec vidéos TikTok
- "Chip Floorplanning with VLMs" → Pas de rapport avec engagement vidéo
- "Medical Image Segmentation" → Pas de rapport avec popularité vidéo

#### ⚠️ Erreur LLM → Fallback Utilisé
```
🎯 For Video Popularity Project
⚠️ LLM analysis failed (timeout/error): [détails erreur]
Fallback analysis:
• Keyword-based insights generated
```
**Signification** : Le LLM a échoué (timeout, API error, rate limit) et le système a utilisé l'analyse par mots-clés. L'erreur est affichée pour le suivi.

### 🔧 Configuration & Documentation

- **[GROQ_SETUP.md](GROQ_SETUP.md)** - Configuration LLM (recommandé : Groq gratuit, 2-5s/article)
- **[EXEMPLE_EMAIL_ERRORS.md](EXEMPLE_EMAIL_ERRORS.md)** - Exemples visuels d'affichage d'erreurs dans l'email
- **[RESUME_AMELIORATIONS.md](RESUME_AMELIORATIONS.md)** - Résumé complet des améliorations apportées

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
