# Alternatives à HuggingFace (Cassé) 🔄

HuggingFace API Inference gratuite ne marche plus. Voici les meilleures alternatives.

## 🏆 Comparaison Rapide

| Provider | Prix | Qualité | Vitesse | Setup |
|----------|------|---------|---------|-------|
| **Mistral AI** | €2-3/mois | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ | 2 min |
| **Ollama** | Gratuit | ⭐⭐⭐⭐ | ⚡⚡⚡ | 5 min |
| **Groq** | Gratuit* | ⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ | 2 min |

*Groq gratuit avec limites (30 req/min)

---

## 1️⃣ Mistral AI (Recommandé)

### ✅ Avantages
- Très stable et rapide
- Excellent en français
- 5€ de crédit gratuit pour commencer
- Support client
- Production-ready

### 💰 Prix
- **Gratuit** : 5€ de crédit offert
- **Ensuite** : ~€2-3/mois pour usage quotidien
- **Mistral Small** : €0.9/M tokens
- **Mistral Large** : €3/M tokens

### 🚀 Installation

```bash
# 1. Créer compte et obtenir clé
# https://console.mistral.ai/

# 2. Utiliser le template
cp .env.mistral .env
nano .env

# Dans .env :
LLM_PROVIDER=mistral
LLM_API_KEY=votre-clé-mistral-ici
LLM_MODEL=mistral-large-latest

# 3. Tester
python test_llm.py

# 4. Utiliser
python main.py update
python main.py chat
```

### 🎯 Modèles Disponibles

```bash
# Large (le meilleur)
LLM_MODEL=mistral-large-latest

# Medium (équilibré)
LLM_MODEL=mistral-medium-latest

# Small (économique)
LLM_MODEL=mistral-small-latest
```

---

## 2️⃣ Ollama (Gratuit, Local)

### ✅ Avantages
- 100% gratuit
- Pas de limite de requêtes
- Données restent locales (vie privée)
- Fonctionne hors ligne
- Plusieurs modèles disponibles

### ⚠️ Inconvénients
- Nécessite ~4-8GB d'espace disque
- Plus lent sans GPU
- Installation plus longue

### 🚀 Installation

```bash
# 1. Installer Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Télécharger un modèle
ollama pull mistral          # 7B, rapide
# OU
ollama pull mixtral          # 8x7B, plus puissant
# OU
ollama pull llama3           # Meta, très bon

# 3. Vérifier
ollama list

# 4. Créer .env
cat > .env << 'EOF'
LLM_PROVIDER=ollama
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=mistral
LLM_TEMPERATURE=0.1

CHROMA_DB_PATH=./data/chroma_db
KEYWORDS=LLMOps,RAG,Time Series,Forecasting,GenAI,LLM
DAYS_TO_FETCH=7
TOP_K_RESULTS=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMAIL_ENABLED=false
EOF

# 5. Tester
python test_llm.py

# 6. Utiliser
python main.py update
python main.py chat
```

### 🎯 Modèles Disponibles

```bash
# Mistral 7B (rapide, léger)
ollama pull mistral
LLM_MODEL=mistral

# Mixtral 8x7B (puissant)
ollama pull mixtral
LLM_MODEL=mixtral

# Llama 3 8B (Meta)
ollama pull llama3
LLM_MODEL=llama3

# Llama 3 70B (très puissant, nécessite beaucoup de RAM)
ollama pull llama3:70b
LLM_MODEL=llama3:70b
```

### 📊 Espace Disque Requis

- **Mistral 7B** : ~4GB
- **Mixtral 8x7B** : ~26GB
- **Llama3 8B** : ~4.7GB
- **Llama3 70B** : ~40GB

---

## 3️⃣ Groq (Gratuit, Très Rapide)

### ✅ Avantages
- Gratuit avec rate limits
- **LE PLUS RAPIDE** (infrastructure custom)
- Bonne qualité (Mixtral, Llama3)
- Pas de carte de crédit requise

### ⚠️ Limites
- 30 requêtes/minute (gratuit)
- 14,400 requêtes/jour
- Largement suffisant pour usage personnel

### 🚀 Installation

```bash
# 1. Créer compte et obtenir clé
# https://console.groq.com/

# 2. Installer groq
pip install groq

# 3. Utiliser le template
cp .env.groq-free .env
nano .env

# Dans .env :
LLM_PROVIDER=groq
LLM_API_KEY=gsk_votre_clé_groq
LLM_MODEL=mixtral-8x7b-32768

# 4. Tester
python test_llm.py

# 5. Utiliser
python main.py update
python main.py chat
```

### 🎯 Modèles Disponibles

```bash
# Mixtral 8x7B (recommandé)
LLM_MODEL=mixtral-8x7b-32768

# Llama3 70B (très puissant)
LLM_MODEL=llama3-70b-8192

# Llama3 8B (rapide)
LLM_MODEL=llama3-8b-8192

# Gemma 7B (Google)
LLM_MODEL=gemma-7b-it
```

---

## 🤔 Quelle Option Choisir ?

### Pour Débuter Gratuitement
→ **Groq** (gratuit, rapide, simple)

### Pour Usage Quotidien
→ **Mistral AI** (stable, rapide, pas cher)

### Pour Maximum de Vie Privée
→ **Ollama** (local, gratuit, privé)

### Pour Production
→ **Mistral AI** (SLA, support, stable)

---

## 📊 Coût Réel (Usage Quotidien)

**30 questions/jour pendant 1 mois** :

| Provider | Coût/mois |
|----------|-----------|
| Groq | 0€ (dans les limites) |
| Ollama | 0€ |
| Mistral Small | ~1€ |
| Mistral Large | ~3€ |
| OpenAI GPT-3.5 | ~2€ |
| OpenAI GPT-4 | ~15€ |

---

## 🔄 Migration depuis HuggingFace

### Vous aviez HuggingFace ?

**Changer simplement dans `.env`** :

```bash
# AVANT (cassé)
LLM_PROVIDER=huggingface
LLM_API_KEY=hf_token
LLM_MODEL=huggingface/mistralai/Mistral-7B-Instruct-v0.3

# APRÈS - Option 1 : Mistral AI
LLM_PROVIDER=mistral
LLM_API_KEY=votre-clé-mistral
LLM_MODEL=mistral-large-latest

# OU Option 2 : Groq
LLM_PROVIDER=groq
LLM_API_KEY=gsk_votre_clé
LLM_MODEL=mixtral-8x7b-32768

# OU Option 3 : Ollama
LLM_PROVIDER=ollama
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=mistral
```

Pas besoin de changer quoi que ce soit d'autre !

---

## 🆘 Support

### Mistral AI
- **Docs** : https://docs.mistral.ai/
- **Console** : https://console.mistral.ai/
- **Status** : https://status.mistral.ai/

### Ollama
- **Docs** : https://ollama.ai/
- **Models** : https://ollama.ai/library
- **GitHub** : https://github.com/ollama/ollama

### Groq
- **Console** : https://console.groq.com/
- **Docs** : https://console.groq.com/docs
- **Pricing** : https://wow.groq.com/

---

## ⚡ Installation Express (Copy-Paste)

### Mistral AI
```bash
cp .env.mistral .env && nano .env && python test_llm.py
```

### Groq
```bash
pip install groq && cp .env.groq-free .env && nano .env && python test_llm.py
```

### Ollama
```bash
curl -fsSL https://ollama.ai/install.sh | sh && ollama pull mistral && python test_llm.py
```

---

**Choisis ton provider et je t'aide à le configurer ! 🚀**
