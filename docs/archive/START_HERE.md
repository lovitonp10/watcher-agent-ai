# 🚀 Démarrage Ultra-Rapide

## Installation (5 minutes)

```bash
./setup_ollama.sh
```

C'est tout ! Le script installe **automatiquement** :
- ✅ Environnement Python
- ✅ Toutes les dépendances
- ✅ Ollama (serveur LLM local)
- ✅ Mistral 7B (modèle AI)
- ✅ Configuration .env

---

## Utilisation

### 1. Activer l'environnement

```bash
source venv/bin/activate
```

### 2. Récupérer les contenus

```bash
python main.py update
```

Récupère les papers et articles des 7 derniers jours.

### 3. Poser des questions

```bash
python main.py chat
```

**Exemples** :
```
You: Quelles sont les dernières techniques de RAG ?
You: Comment Meta utilise les LLMs ?
You: Résume les avancées en forecasting
```

---

## Commandes Principales

```bash
python main.py update        # Mettre à jour la base
python main.py chat          # Chat interactif
python main.py search "..."  # Recherche rapide
python main.py stats         # Statistiques
python test_llm.py           # Tester la config
```

---

## 💡 Coût

**0€** - Tout est gratuit et local !

---

## 📚 Documentation

- **README.md** - Vue d'ensemble complète
- **QUICKSTART.md** - Guide détaillé
- **SOURCES.md** - Personnaliser les sources

---

## 🆘 Problème ?

```bash
# Vérifier qu'Ollama tourne
ollama list

# Redémarrer Ollama
pkill ollama
ollama serve

# Tester
python test_llm.py
```

---

**🎉 C'est parti !** → `./setup_ollama.sh`
