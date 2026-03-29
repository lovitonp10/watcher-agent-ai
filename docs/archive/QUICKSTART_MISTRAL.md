# Démarrage Rapide avec Mistral AI 🚀

Guide en français pour configurer Tech Watch Agent avec Mistral AI en 5 minutes.

## Pourquoi Mistral AI ?

- 🇫🇷 **Excellent en français** (meilleur que GPT-4)
- 💰 **30-50% moins cher qu'OpenAI**
- ⚡ **Très rapide** et performant
- 🇪🇺 **Souveraineté européenne** (serveurs en Europe)
- 🎓 **Parfait pour la recherche** technique et scientifique

## Étape 1 : Obtenir une clé API Mistral

1. Créer un compte : https://console.mistral.ai/
2. Aller dans "API keys" : https://console.mistral.ai/api-keys/
3. Cliquer sur "Create new key"
4. Copier la clé (elle commence par des lettres/chiffres aléatoires)

💡 **Crédit gratuit** : Mistral offre des crédits gratuits pour tester !

## Étape 2 : Installation

```bash
cd watcher

# Installation automatique
./setup.sh

# OU installation manuelle
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Étape 3 : Configuration

```bash
# Copier le template Mistral
cp .env.mistral .env

# Éditer le fichier .env
nano .env  # ou vim, code, n'importe quel éditeur
```

**Modifier cette ligne dans `.env`** :
```bash
LLM_API_KEY=votre-clé-mistral-ici
```

Remplacez `votre-clé-mistral-ici` par votre vraie clé API.

### Configuration Complète

Voici un exemple de `.env` complet pour Mistral :

```bash
# LLM Configuration
LLM_PROVIDER=mistral
LLM_API_KEY=votre-clé-ici
LLM_MODEL=mistral-large-latest
LLM_TEMPERATURE=0.1

# Base de données vectorielle
CHROMA_DB_PATH=./data/chroma_db

# Configuration de l'ingestion
DAYS_TO_FETCH=7
MAX_RESULTS_PER_SOURCE=20
KEYWORDS=LLMOps,RAG,Time Series,Forecasting,GenAI,LLM

# RAG
TOP_K_RESULTS=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Embeddings (local, pas besoin de clé API)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Étape 4 : Tester la Configuration

```bash
# Activer l'environnement virtuel si pas déjà fait
source venv/bin/activate

# Tester la connexion à Mistral
python test_llm.py
```

Vous devriez voir :
```
✓ Generator initialized
✓ Generation successful!
✅ LLM provider is working correctly!
```

## Étape 5 : Utiliser l'Agent

### 1. Mettre à jour la base de connaissances

```bash
python main.py update
```

Cela va :
- ✅ Récupérer les papers d'ArXiv (IA, ML, NLP)
- ✅ Récupérer les papers Hugging Face
- ✅ Scraper les blogs techniques (Netflix, Meta, etc.)
- ✅ Filtrer par vos mots-clés
- ✅ Stocker dans une base vectorielle locale

**Durée** : ~2-3 minutes la première fois

### 2. Poser des questions en français !

```bash
python main.py chat
```

Exemples de questions :

```
You: Quelles sont les dernières techniques de RAG ?

You: Comment Meta utilise les LLMs pour l'évaluation ?

You: Résume-moi les avancées récentes en time series forecasting

You: Quelles sont les meilleures pratiques en LLMOps ?

You: Quels sont les nouveaux modèles de language sortis cette semaine ?
```

**Sortir du chat** : Tapez `exit` ou `quit`

### 3. Recherche rapide

```bash
# Question unique sans entrer en mode chat
python main.py search "Quelles sont les techniques de RAG les plus récentes?"
```

### 4. Statistiques

```bash
python main.py stats
```

Affiche :
- Nombre de documents
- Nombre de chunks
- Sources (ArXiv, blogs, etc.)

## Commandes Utiles

```bash
# Mettre à jour (à faire régulièrement)
python main.py update

# Chat interactif
python main.py chat

# Recherche rapide
python main.py search "votre question"

# Stats
python main.py stats

# Info configuration
python main.py info

# Effacer la base
python main.py clear --yes
```

## Choisir un Modèle Mistral

Éditez `LLM_MODEL` dans `.env` :

### mistral-large-latest (Recommandé)
```bash
LLM_MODEL=mistral-large-latest
```
- 🎯 **Usage** : Production, tâches complexes
- 💰 **Prix** : €3/€9 par 1M tokens
- ⚡ **Qualité** : Excellent, comparable à GPT-4

### mistral-medium-latest (Équilibré)
```bash
LLM_MODEL=mistral-medium-latest
```
- 🎯 **Usage** : Équilibré qualité/prix
- 💰 **Prix** : €2.5/€7.5 par 1M tokens
- ⚡ **Qualité** : Très bon

### mistral-small-latest (Économique)
```bash
LLM_MODEL=mistral-small-latest
```
- 🎯 **Usage** : Tests, prototypage
- 💰 **Prix** : €0.9/€2.7 par 1M tokens
- ⚡ **Qualité** : Bon, rapide

### open-mixtral-8x7b (Open Source)
```bash
LLM_MODEL=open-mixtral-8x7b
```
- 🎯 **Usage** : Open source, économique
- 💰 **Prix** : €0.7/€0.7 par 1M tokens
- ⚡ **Qualité** : Bon

## Workflow Quotidien

```bash
# Le matin : mettre à jour
python main.py update

# Poser des questions
python main.py chat

# Ou recherche rapide
python main.py search "dernières avancées en RAG"
```

## Automatiser les Mises à Jour

### Linux/Mac (crontab)

```bash
crontab -e
```

Ajouter :
```bash
# Mise à jour quotidienne à 9h
0 9 * * * cd /chemin/vers/watcher && venv/bin/python main.py update
```

### Windows (Planificateur de tâches)

Créer `update.bat` :
```batch
@echo off
cd C:\chemin\vers\watcher
call venv\Scripts\activate
python main.py update
```

Planifier dans le Planificateur de tâches Windows.

## Personnalisation

### Ajouter des mots-clés

Éditez `KEYWORDS` dans `.env` :

```bash
KEYWORDS=LLMOps,RAG,Forecasting,VotreMotClé,Python,MLOps
```

### Changer la période de récupération

```bash
DAYS_TO_FETCH=14  # Récupérer 14 jours au lieu de 7
```

### Augmenter le nombre de résultats

```bash
TOP_K_RESULTS=10  # Retourner 10 sources au lieu de 5
```

## Dépannage

### "API key not found"

Vérifiez que `.env` contient :
```bash
LLM_API_KEY=votre-vraie-clé
```

Pas d'espaces avant/après !

### "Invalid API key"

- Copiez-collez votre clé depuis https://console.mistral.ai/api-keys/
- Vérifiez qu'elle commence bien par des caractères alphanumériques
- Recréez une nouvelle clé si nécessaire

### "Model not found"

Utilisez le nom exact :
```bash
LLM_MODEL=mistral-large-latest
```

Pas `mistral-large` ou `mistral-4` !

### Trop lent ?

1. Utilisez un modèle plus petit :
   ```bash
   LLM_MODEL=mistral-small-latest
   ```

2. Réduisez `TOP_K_RESULTS` :
   ```bash
   TOP_K_RESULTS=3
   ```

### Réponses pas assez précises ?

1. Utilisez le modèle le plus puissant :
   ```bash
   LLM_MODEL=mistral-large-latest
   ```

2. Augmentez le contexte :
   ```bash
   TOP_K_RESULTS=10
   ```

3. Mettez à jour plus souvent :
   ```bash
   python main.py update
   ```

## Coûts Estimés

Pour un usage typique (30 questions/jour) :

- **mistral-large-latest** : ~€2-5/mois
- **mistral-medium-latest** : ~€1-3/mois
- **mistral-small-latest** : ~€0.50-1/mois

💡 **Beaucoup moins cher qu'OpenAI** (30-50% d'économie) !

## Support

- **Guide des providers** : [PROVIDERS.md](PROVIDERS.md)
- **Guide complet** : [QUICKSTART.md](QUICKSTART.md)
- **Documentation Mistral** : https://docs.mistral.ai/

Bon monitoring de l'IA ! 🚀🔬
