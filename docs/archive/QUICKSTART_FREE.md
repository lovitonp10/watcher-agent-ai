# Démarrage GRATUIT - Email + Mistral 🆓📧

Guide pour utiliser Tech Watch Agent **100% GRATUITEMENT** avec email quotidien automatique !

## 🎯 Ce que tu vas obtenir

- 🆓 **LLM Mistral gratuit** via HuggingFace (pas de carte de crédit)
- 📧 **Email quotidien automatique** à 8h45 avec résumé AI
- 🤖 **Veille tech automatisée** sur ArXiv, HuggingFace, blogs
- 💰 **Zéro coût** (sauf si tu veux upgrader plus tard)

## ⚡ Installation Rapide (10 minutes)

### Étape 1 : Installer le projet

```bash
cd watcher
./setup.sh
source venv/bin/activate
```

### Étape 2 : Obtenir un Token HuggingFace (Gratuit)

1. **Créer un compte** : https://huggingface.co/join
2. **Générer un token** : https://huggingface.co/settings/tokens
   - Cliquer "New token"
   - Name : "Tech Watch Agent"
   - Type : Read
   - Copier le token (commence par `hf_...`)

### Étape 3 : Configurer Gmail pour les Emails

1. **Activer l'authentification à 2 facteurs** :
   - https://myaccount.google.com/security
   - Activer "Validation en deux étapes"

2. **Créer un mot de passe d'application** :
   - https://myaccount.google.com/apppasswords
   - Sélectionner "Mail" > "Autre" > "Tech Watch"
   - Copier le mot de passe (16 caractères)

### Étape 4 : Configuration

```bash
# Copier le template HuggingFace gratuit
cp .env.mistral-hf-free .env

# Éditer
nano .env
```

**Mettre à jour ces lignes** :

```bash
# LLM Mistral GRATUIT via HuggingFace
LLM_PROVIDER=huggingface
LLM_API_KEY=hf_ton_token_ici
LLM_MODEL=huggingface/mistralai/Mistral-7B-Instruct-v0.3

# Email Gmail
EMAIL_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=ton-email@gmail.com
SMTP_PASSWORD=ton-mot-de-passe-application-16-chars
EMAIL_FROM=ton-email@gmail.com
EMAIL_TO=ton-email@gmail.com
EMAIL_USE_TLS=true
```

### Étape 5 : Tester

```bash
# Tester le LLM
python test_llm.py

# Tester l'email
python main.py test-email

# Tester le digest (preview)
python main.py digest --preview
```

### Étape 6 : Automatiser l'Envoi Quotidien

```bash
# Éditer le crontab
crontab -e

# Ajouter cette ligne pour recevoir l'email à 8h45 chaque jour
45 8 * * * /home/lovitonp10/perso/agent-perso/watcher/schedule_digest.sh
```

Modifier le chemin dans la ligne ci-dessus avec ton chemin réel !

## ✅ C'est Prêt !

Maintenant, **chaque matin à 8h45**, tu recevras automatiquement par email :

📧 **Un email HTML élégant** avec :
- 🤖 Résumé AI par Mistral des nouvelles découvertes
- 📚 Liste des nouveaux papers ArXiv
- 🔬 Papers HuggingFace du jour
- 📰 Articles des blogs tech (Netflix, Meta, etc.)
- 📊 Statistiques de ta base de connaissances
- 🔗 Liens directs vers tous les contenus

## 💰 Coût Total : 0€

- ✅ HuggingFace Inference : **Gratuit** (rate limit raisonnable)
- ✅ Gmail SMTP : **Gratuit** (limite : 500 emails/jour)
- ✅ Embeddings locaux : **Gratuit** (sentence-transformers)
- ✅ ChromaDB local : **Gratuit**

## 🚀 Utilisation Quotidienne

### Recevoir le Digest Automatiquement

Le cron s'occupe de tout ! Chaque matin :
1. ✅ Récupère les nouveaux contenus
2. ✅ Les stocke dans ta base vectorielle
3. ✅ Génère un résumé AI avec Mistral
4. ✅ T'envoie un email élégant

### Poser des Questions Manuellement

```bash
# Chat interactif
python main.py chat

# Question rapide
python main.py search "Quelles sont les dernières techniques de RAG?"

# Voir les stats
python main.py stats
```

### Forcer une Mise à Jour

```bash
python main.py update
```

## 📊 Limites de la Version Gratuite

### HuggingFace Gratuit

- ⏱️ **Cold start** : Première requête = 20-30s (modèle se "réveille")
- ⏱️ **Requêtes suivantes** : 2-5s
- 🔄 **Rate limit** : ~100-200 requêtes/jour (largement suffisant)
- 📝 **Qualité** : Très bonne (Mistral-7B ≈ GPT-3.5)

### Gmail SMTP

- 📧 **Limite** : 500 emails/jour (tu en envoies 1 seul !)
- ✅ **Pas de coût**

## 🔄 Upgrader Plus Tard (Optionnel)

Si tu veux **plus de performance**, tu peux facilement upgrader :

### Option 1 : Mistral AI Payant (~€2-5/mois)

```bash
# Dans .env, changer :
LLM_PROVIDER=mistral
LLM_API_KEY=ta-clé-mistral
LLM_MODEL=mistral-large-latest
```

**Avantages** :
- ⚡ Pas de cold start
- 🚀 Plus rapide (1-2s par requête)
- 🎯 Meilleure qualité (Mistral Large)
- 📈 Pas de rate limit

**Prix** : €0.9-9 / 1M tokens (~€2-5/mois pour 30-50 questions/jour)

### Option 2 : Ollama Local (Gratuit mais nécessite GPU)

```bash
# Installer Ollama
ollama pull mistral

# Dans .env :
LLM_PROVIDER=ollama
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=mistral
```

**Avantages** :
- 🆓 Totalement gratuit
- 🔒 Vie privée totale
- ⚡ Rapide si bon GPU

**Inconvénients** :
- 💻 Nécessite GPU puissant
- 📦 Téléchargement du modèle (~4GB)

## 🛠️ Personnalisation

### Changer l'Heure du Digest

```bash
crontab -e

# 7h30 au lieu de 8h45
30 7 * * * /chemin/vers/schedule_digest.sh

# Deux fois par jour (matin et soir)
0 8,18 * * * /chemin/vers/schedule_digest.sh
```

### Ajouter des Mots-Clés

Dans `.env` :
```bash
KEYWORDS=LLMOps,RAG,VotreSujet,Python,MLOps,Forecasting
```

### Changer le Nombre de Jours

```bash
DAYS_TO_FETCH=14  # 14 jours au lieu de 7
```

## 🆘 Dépannage

### "Model is loading" (HuggingFace)

**Normal la première fois !** Le modèle se réveille. Attendre 30s et réessayer.

```bash
python test_llm.py  # Première fois = lent
python test_llm.py  # Deuxième fois = rapide
```

### Email non reçu

1. ✅ Vérifier les **spams**
2. ✅ Vérifier `EMAIL_TO` dans `.env`
3. ✅ Tester : `python main.py test-email`
4. ✅ Vérifier Gmail : mot de passe d'**application**, pas mot de passe normal !

### Cron ne s'exécute pas

```bash
# Vérifier que cron est actif
crontab -l

# Tester le script manuellement
bash schedule_digest.sh

# Voir les logs
tail -f digest.log
```

### Rate limit HuggingFace

Si tu dépasses la limite gratuite :
- ⏰ Attendre quelques heures
- 🔄 Ou passer à Mistral AI payant (€2-5/mois)
- 🏠 Ou utiliser Ollama local (gratuit)

## 📚 Guides Détaillés

- 📧 **Email** : [EMAIL_SETUP.md](EMAIL_SETUP.md) - Configuration email complète
- 🆓 **Mistral Gratuit** : [MISTRAL_FREE.md](MISTRAL_FREE.md) - Détails HuggingFace
- 🤖 **Providers** : [PROVIDERS.md](PROVIDERS.md) - Tous les providers LLM
- 🚀 **Général** : [QUICKSTART.md](QUICKSTART.md) - Guide complet

## 🎉 Résumé

**Tu as maintenant** :
- ✅ Un agent de veille tech **100% automatisé**
- ✅ Mistral AI **gratuit** via HuggingFace
- ✅ Email quotidien **élégant** à 8h45
- ✅ Base vectorielle locale avec **tous les contenus**
- ✅ **Zéro coût** (upgrade optionnel plus tard)

**Profite de ta veille tech automatisée gratuite ! 🚀🤖**

---

Des questions ? Ouvre une issue sur GitHub ou consulte les guides détaillés !
