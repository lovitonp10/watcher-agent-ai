# Mistral GRATUIT via HuggingFace 🆓

Guide pour utiliser les modèles Mistral open-source **GRATUITEMENT** via HuggingFace Inference API.

## 🎯 Pourquoi cette option ?

- 🆓 **100% Gratuit** (pas de carte de crédit, pas de coût par token)
- ⚡ **Rapide** (hébergé sur les serveurs HuggingFace)
- 🔓 **Open Source** (modèles Mistral-7B et Mixtral-8x7B)
- 🌍 **Aucune limite** (rate limit raisonnable mais généreux)
- 🔒 **Vie privée** (meilleure que les API commerciales)

## 📋 Configuration en 3 Étapes

### Étape 1 : Obtenir un Token HuggingFace (Gratuit)

1. Créer un compte sur HuggingFace : https://huggingface.co/join
2. Aller dans Settings > Access Tokens : https://huggingface.co/settings/tokens
3. Cliquer sur "New token"
   - **Name** : "Tech Watch Agent"
   - **Type** : Read (suffit pour l'inference)
4. Copier le token (commence par `hf_...`)

💡 **C'est gratuit** et ça donne accès à tous les modèles open-source !

### Étape 2 : Configurer le Projet

```bash
cd watcher

# Copier le template HuggingFace
cp .env.mistral-hf-free .env

# Éditer .env
nano .env
```

**Modifier cette ligne** :
```bash
LLM_API_KEY=hf_votre_token_ici
```

Votre `.env` devrait ressembler à ça :
```bash
LLM_PROVIDER=huggingface
LLM_API_KEY=hf_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
LLM_MODEL=huggingface/mistralai/Mistral-7B-Instruct-v0.3
LLM_TEMPERATURE=0.1
```

### Étape 3 : Tester

```bash
# Tester la connexion
python test_llm.py

# Utiliser l'agent
python main.py update
python main.py chat
```

## 🤖 Modèles Mistral Gratuits Disponibles

### Mistral-7B-Instruct-v0.3 (Recommandé)

```bash
LLM_MODEL=huggingface/mistralai/Mistral-7B-Instruct-v0.3
```

- ✅ **Taille** : 7 milliards de paramètres
- ✅ **Qualité** : Excellente pour la plupart des tâches
- ✅ **Vitesse** : Rapide (~2-5 secondes par réponse)
- ✅ **Contexte** : 32k tokens
- 🎯 **Usage** : Idéal pour le Tech Watch Agent

### Mixtral-8x7B-Instruct-v0.1 (Plus Puissant)

```bash
LLM_MODEL=huggingface/mistralai/Mixtral-8x7B-Instruct-v0.1
```

- ✅ **Taille** : 8 experts de 7B (MoE)
- ✅ **Qualité** : Comparable à GPT-3.5 Turbo
- ⚠️ **Vitesse** : Plus lent (~10-20 secondes)
- ✅ **Contexte** : 32k tokens
- 🎯 **Usage** : Pour les tâches complexes

## 🆚 Comparaison avec Mistral AI Payant

| Critère | HuggingFace (Gratuit) | Mistral AI (Payant) |
|---------|----------------------|---------------------|
| **Prix** | 🆓 Gratuit | €0.9 - €9 / 1M tokens |
| **Modèle** | Mistral-7B, Mixtral-8x7B | Mistral Large, Medium, Small |
| **Qualité** | ⭐⭐⭐ Très bon | ⭐⭐⭐⭐⭐ Excellent |
| **Vitesse** | ⚡⚡⚡ Rapide | ⚡⚡⚡⚡⚡ Très rapide |
| **Limites** | Rate limit raisonnable | Pas de limite |
| **Usage** | Personnel, prototypage | Production |

## 💡 Quand Utiliser Quoi ?

### Utiliser HuggingFace GRATUIT si :
- ✅ Tu débutes et veux tester
- ✅ Usage personnel ou prototypage
- ✅ Budget limité (étudiant, projets perso)
- ✅ Pas besoin de la meilleure qualité absolue
- ✅ Tu veux expérimenter sans frais

### Passer à Mistral AI Payant si :
- 💰 Tu as besoin de la meilleure qualité
- 💰 Usage en production
- 💰 Besoin de vitesse maximale
- 💰 Support client et SLA

## ⚙️ Configuration Avancée

### Changer de Modèle

Dans `.env`, modifie `LLM_MODEL` :

```bash
# Mistral 7B (recommandé, rapide)
LLM_MODEL=huggingface/mistralai/Mistral-7B-Instruct-v0.3

# Mixtral 8x7B (plus puissant, plus lent)
LLM_MODEL=huggingface/mistralai/Mixtral-8x7B-Instruct-v0.1

# Llama 3 8B (alternative)
LLM_MODEL=huggingface/meta-llama/Llama-3-8B-Instruct

# Gemma 7B (Google)
LLM_MODEL=huggingface/google/gemma-7b-it
```

### Optimiser la Vitesse

Si les réponses sont trop lentes :

```bash
# Utiliser le modèle 7B au lieu de Mixtral
LLM_MODEL=huggingface/mistralai/Mistral-7B-Instruct-v0.3

# Réduire le contexte
TOP_K_RESULTS=3  # Au lieu de 5

# Réduire la température
LLM_TEMPERATURE=0.05
```

### Utiliser un Endpoint Dédié (Payant mais plus rapide)

HuggingFace propose des "Inference Endpoints" dédiés :

1. Créer un endpoint : https://huggingface.co/inference-endpoints
2. Déployer Mistral-7B ou Mixtral
3. Configurer :
```bash
LLM_PROVIDER=huggingface
LLM_BASE_URL=https://votre-endpoint.aws.endpoints.huggingface.cloud
LLM_MODEL=huggingface/mistralai/Mistral-7B-Instruct-v0.3
```

**Prix** : ~€0.60/heure (facturation à la seconde, pause automatique)

## 🔧 Dépannage

### "Model is loading, please retry"

L'API HuggingFace "réveille" les modèles à la demande. Première requête = lente (~20-30s).

**Solution** : Réessayer ou attendre quelques secondes.

```bash
# Le test peut échouer la première fois
python test_llm.py  # Peut prendre 30s

# Deuxième essai sera rapide
python test_llm.py  # ~2-5s
```

### "Rate limit exceeded"

HuggingFace gratuit a des limites raisonnables.

**Solution** :
- Attendre quelques minutes
- Ou utiliser un token différent
- Ou upgrader vers Inference Endpoints

### Réponses de mauvaise qualité

**Solutions** :
1. Utiliser Mixtral au lieu de Mistral-7B :
```bash
LLM_MODEL=huggingface/mistralai/Mixtral-8x7B-Instruct-v0.1
```

2. Augmenter le contexte :
```bash
TOP_K_RESULTS=10
```

3. Ajuster la température :
```bash
LLM_TEMPERATURE=0.2  # Plus créatif
```

### Token invalide

Vérifier que :
- Le token commence par `hf_`
- Tu as copié le token complet
- Le token est de type "Read" minimum

Régénérer : https://huggingface.co/settings/tokens

## 🚀 Utilisation

Une fois configuré, utilise normalement :

```bash
# Mettre à jour la base
python main.py update

# Poser des questions (GRATUIT !)
python main.py chat

# Recherche rapide
python main.py search "Quelles sont les dernières techniques de RAG?"

# Digest quotidien par email
python main.py digest
```

## 💰 Coûts Estimés

| Usage | HuggingFace | Mistral AI Payant |
|-------|-------------|-------------------|
| **30 questions/jour** | 🆓 **GRATUIT** | €2-5/mois |
| **100 questions/jour** | 🆓 **GRATUIT** | €8-15/mois |
| **Production** | 🆓 **GRATUIT** (avec limites) | €50-200/mois |

## 🎓 Pour les Étudiants / Chercheurs

HuggingFace gratuit est **PARFAIT** pour :
- 📚 Recherche académique
- 🎓 Projets étudiants
- 🧪 Prototypage
- 📊 Veille technologique
- 🤖 Apprentissage du ML

## 🔄 Passer de HuggingFace à Mistral AI Payant

C'est simple, juste changer dans `.env` :

```bash
# De HuggingFace gratuit
LLM_PROVIDER=huggingface
LLM_API_KEY=hf_token

# À Mistral AI payant
LLM_PROVIDER=mistral
LLM_API_KEY=votre-clé-mistral
LLM_MODEL=mistral-large-latest
```

Pas besoin de réinstaller quoi que ce soit !

## 📚 Ressources

- **HuggingFace Hub** : https://huggingface.co/mistralai
- **Mistral-7B** : https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3
- **Mixtral-8x7B** : https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1
- **Inference API Docs** : https://huggingface.co/docs/api-inference/
- **Pricing** : https://huggingface.co/pricing

## 🎉 Résumé

**Pour commencer GRATUITEMENT avec Mistral :**

```bash
# 1. Obtenir un token HuggingFace (gratuit)
# https://huggingface.co/settings/tokens

# 2. Configurer
cp .env.mistral-hf-free .env
nano .env  # Mettre ton token hf_...

# 3. Tester
python test_llm.py

# 4. Utiliser !
python main.py update
python main.py chat
```

**C'est tout ! 🚀 Profite de Mistral GRATUITEMENT !**

---

Des questions ? Ouvre une issue sur GitHub !
