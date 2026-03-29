# Installation Tech Watch Agent 🚀

Guide complet pour installer et configurer Tech Watch Agent avec Ollama (100% gratuit).

---

## ⚡ Installation Automatique (5 minutes)

### Une seule commande :

```bash
./setup_ollama.sh
```

C'est tout ! Le script fait **automatiquement** :
- ✅ Crée l'environnement Python
- ✅ Installe toutes les dépendances
- ✅ Installe Ollama
- ✅ Télécharge Mistral 7B (~4GB)
- ✅ Configure le fichier .env

**Temps** : ~5 minutes (téléchargement du modèle inclus)

---

## 📋 Prérequis

- **Python 3.10+** (vérifier : `python3 --version`)
- **Espace disque** : ~5GB
- **Connexion internet** (pour télécharger le modèle)
- **OS** : Linux, macOS, ou WSL sur Windows

---

## 🔧 Installation Manuelle (si le script échoue)

### 1. Environnement Python

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer
source venv/bin/activate

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Installer Ollama

```bash
# Linux / macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Vérifier l'installation
ollama --version
```

### 3. Télécharger le Modèle

```bash
# Démarrer Ollama (dans un terminal séparé)
ollama serve

# Télécharger Mistral 7B
ollama pull mistral

# Vérifier
ollama list
```

### 4. Configuration

```bash
# Copier le template
cp .env.ollama .env

# Le fichier .env contient déjà tout !
# Pas besoin de le modifier pour commencer
```

---

## ✅ Vérification de l'Installation

### 1. Vérifier Ollama

```bash
# Liste des modèles installés
ollama list

# Devrait afficher :
# NAME         ID           SIZE     MODIFIED
# mistral      ...          4.1 GB   ...
```

### 2. Vérifier l'Environnement Python

```bash
# Activer l'environnement
source venv/bin/activate

# Vérifier les packages
pip list | grep -E "langchain|chromadb|sentence-transformers"
```

### 3. Tester la Configuration LLM

```bash
python test_llm.py
```

**Résultat attendu** :
```
✓ Generator initialized
✓ Generation successful!
✅ LLM provider is working correctly!
```

---

## 🎯 Premier Lancement

### 1. Récupérer les Contenus

```bash
source venv/bin/activate
python main.py update
```

Cela va :
- 🔍 Chercher sur ArXiv (papers IA/ML)
- 🤗 Chercher sur Hugging Face
- 📰 Scraper 7 blogs techniques
- 💾 Stocker dans ChromaDB (local)

**Temps** : ~2-3 minutes

### 2. Voir les Statistiques

```bash
python main.py stats
```

### 3. Poser une Question

```bash
python main.py chat
```

Tapez une question, par exemple :
```
You: Quelles sont les dernières techniques de RAG ?
```

---

## ⚙️ Configuration Avancée (Optionnel)

### Personnaliser les Mots-Clés

Éditez `.env` :

```bash
nano .env
```

Modifiez la ligne `KEYWORDS` :
```bash
# Par défaut
KEYWORDS=LLMOps,RAG,Time Series,Forecasting,GenAI,LLM

# Personnalisé
KEYWORDS=VotreSujet,Python,MachineLearning,DeepLearning
```

### Changer le Modèle Ollama

```bash
# Télécharger un autre modèle
ollama pull mixtral      # Plus puissant (26GB)
ollama pull llama3       # Meta Llama3 (4.7GB)

# Modifier .env
nano .env
# Changer : LLM_MODEL=mixtral
```

**Modèles disponibles** :
- `mistral` - 7B, rapide, léger (défaut)
- `mixtral` - 8x7B, très puissant
- `llama3` - Meta, excellent
- `llama3:70b` - Très puissant (40GB)

### Ajouter un Blog

Éditez `config.py` :

```python
BLOG_FEEDS["Stripe Engineering"] = "https://stripe.com/blog/engineering/rss"
```

### Ajouter une Catégorie ArXiv

Éditez `config.py` :

```python
ARXIV_CATEGORIES.append("cs.CV")  # Computer Vision
```

---

## 📧 Configuration Email (Optionnel)

Pour recevoir un email quotidien avec les nouveautés.

### 1. Obtenir un Mot de Passe Application Gmail

1. Aller sur https://myaccount.google.com/security
2. Activer "Validation en deux étapes"
3. Aller sur https://myaccount.google.com/apppasswords
4. Créer un mot de passe pour "Mail"
5. Copier le mot de passe (16 caractères)

### 2. Configurer `.env`

```bash
nano .env
```

Modifier ces lignes :
```bash
EMAIL_ENABLED=true
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=mot-de-passe-application-16-chars
EMAIL_FROM=votre-email@gmail.com
EMAIL_TO=votre-email@gmail.com
```

### 3. Tester

```bash
python main.py test-email
python main.py digest --preview
```

### 4. Automatiser (8h45 chaque matin)

```bash
crontab -e
```

Ajouter :
```bash
45 8 * * * cd /home/votre-user/watcher && venv/bin/python main.py digest
```

---

## 🐛 Dépannage

### "ollama: command not found"

**Solution** : Réinstaller Ollama
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### "Connection refused" (Ollama)

**Cause** : Ollama ne tourne pas

**Solution** :
```bash
# Démarrer Ollama
ollama serve
```

Pour le laisser tourner en arrière-plan :
```bash
ollama serve > /dev/null 2>&1 &
```

### "Model not found"

**Solution** :
```bash
# Télécharger le modèle
ollama pull mistral

# Vérifier
ollama list
```

### Ollama Trop Lent

**Causes** : Pas de GPU, ou RAM insuffisante

**Solutions** :
```bash
# 1. Utiliser une version quantifiée (plus rapide)
ollama pull mistral:7b-instruct-q4_0

# 2. Ou passer à Mistral AI cloud (~2€/mois)
cp .env.mistral .env
nano .env  # Ajouter votre clé Mistral AI
```

### "No such file or directory: .env"

**Solution** :
```bash
cp .env.ollama .env
```

### Erreur Python "ModuleNotFoundError"

**Cause** : Environnement virtuel pas activé

**Solution** :
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Pas de Résultats après `update`

**Causes** : Mots-clés trop restrictifs

**Solutions** :
```bash
# 1. Élargir les mots-clés
nano .env
# KEYWORDS=AI,ML,LLM,RAG

# 2. Augmenter la période
# DAYS_TO_FETCH=14

# 3. Re-update
python main.py update
```

---

## 🔄 Désinstallation

```bash
# Arrêter Ollama
pkill ollama

# Supprimer l'environnement
rm -rf venv/

# Supprimer les données
rm -rf data/

# Désinstaller Ollama (optionnel)
# Linux
sudo rm -rf /usr/local/bin/ollama
sudo rm -rf ~/.ollama

# macOS
brew uninstall ollama
```

---

## 📊 Espace Disque Utilisé

- **Mistral 7B** : ~4GB
- **Embeddings model** : ~80MB
- **ChromaDB** (vide) : ~10MB
- **ChromaDB** (100 docs) : ~100MB
- **Environnement Python** : ~500MB
- **Total initial** : ~5GB

---

## 🚀 Prochaines Étapes

Une fois installé, consultez **[RUN.md](RUN.md)** pour l'utilisation quotidienne.

---

## 📚 Documentation Complète

- **[RUN.md](RUN.md)** - Utilisation quotidienne (ultra-court)
- **[SOURCES.md](SOURCES.md)** - Personnaliser les sources
- **[STRUCTURE.md](STRUCTURE.md)** - Architecture du code
- **[ALTERNATIVES.md](ALTERNATIVES.md)** - Autres providers LLM
- **[docs/](docs/)** - Guides détaillés

---

## 💰 Coût

**0€** - Tout est gratuit et local !

---

## 🎉 Installation Terminée !

Vous êtes prêt à utiliser Tech Watch Agent !

**Prochaine étape** → Voir **[RUN.md](RUN.md)** pour l'utilisation quotidienne.
