# 🤖 Setup GitHub Actions - Automatisation 100% Gratuite

Ce guide configure l'envoi automatique du digest quotidien via **GitHub Actions** (gratuit).

---

## 📋 Prérequis

1. Compte GitHub (gratuit)
2. Compte Groq (gratuit) - https://console.groq.com
3. Compte email avec SMTP (Gmail, Outlook, etc.)

---

## 🚀 Étape 1: Créer un compte Groq (LLM gratuit)

### Pourquoi Groq?
- ✅ **100% gratuit** (7k requests/jour)
- ✅ Ultra rapide (inference à 500 tokens/s)
- ✅ Compatible LiteLLM
- ✅ Pas besoin de serveur

### Inscription:

1. Aller sur https://console.groq.com
2. S'inscrire (gratuit)
3. Créer une API Key: https://console.groq.com/keys
4. Copier la clé (format: `gsk_...`)
---

## 🚀 Étape 2: Push le code sur GitHub

### A. Créer un repo GitHub (peut être privé)

```bash
# Sur GitHub.com, créer un nouveau repo
# Nom: tech-watch-agent
# Visibilité: Private (recommandé)
```

### B. Push le code

```bash
cd /home/lovitonp10/perso/agent-perso/watcher

# Initialiser git (si pas déjà fait)
git init
git add .
git commit -m "Initial commit - Tech Watch Agent"

# Ajouter le remote GitHub
git remote add origin https://github.com/VOTRE_USERNAME/tech-watch-agent.git

# Push
git branch -M main
git push -u origin main
```

---

## 🚀 Étape 3: Configurer les Secrets GitHub

Les secrets GitHub stockent vos credentials de façon sécurisée.

### A. Aller dans Settings > Secrets and variables > Actions

```
https://github.com/VOTRE_USERNAME/tech-watch-agent/settings/secrets/actions
```

### B. Ajouter ces secrets (cliquer "New repository secret"):

| Secret Name | Valeur | Exemple |
|-------------|--------|---------|
| `GROQ_API_KEY` | Votre clé Groq | `gsk_...` |
| `SMTP_HOST` | Serveur SMTP | `smtp.gmail.com` |
| `SMTP_PORT` | Port SMTP | `587` |
| `SMTP_USER` | Votre email | `votre-email@gmail.com` |
| `SMTP_PASSWORD` | App password | Voir ci-dessous ⬇️ |
| `EMAIL_FROM` | Email expéditeur | `votre-email@gmail.com` |
| `EMAIL_TO` | Email destinataire | `votre-email@gmail.com` |

---

## 📧 Étape 4: Configurer Gmail App Password

**⚠️ Important:** N'utilisez JAMAIS votre mot de passe Gmail normal !

### Pour Gmail:

1. Aller sur https://myaccount.google.com/security
2. Activer la **2-Step Verification** (obligatoire)
3. Aller sur https://myaccount.google.com/apppasswords
4. Créer un "App password" pour "Mail"
5. Copier le mot de passe généré (16 caractères)
6. Coller dans le secret `SMTP_PASSWORD`

### Pour Outlook/Hotmail:

- SMTP_HOST: `smtp-mail.outlook.com`
- SMTP_PORT: `587`
- SMTP_PASSWORD: Votre mot de passe Outlook (ou app password)

---

## 🚀 Étape 5: Vérifier le Workflow

Le fichier `.github/workflows/daily-digest.yml` est déjà créé.

### Vérifier qu'il est bien présent:

```bash
cat .github/workflows/daily-digest.yml
```

### Push les changements:

```bash
git add .github/workflows/daily-digest.yml
git commit -m "Add GitHub Actions workflow"
git push
```

---

## 🧪 Étape 6: Tester Manuellement

### A. Aller dans Actions tab sur GitHub

```
https://github.com/VOTRE_USERNAME/tech-watch-agent/actions
```

### B. Sélectionner "Daily Tech Watch Digest"

### C. Cliquer "Run workflow" > "Run workflow"

Cela va:
1. Installer les dépendances
2. Fetch les papers ArXiv + blogs
3. Générer le résumé avec Groq
4. Envoyer l'email

**Durée:** ~3-5 minutes

### D. Vérifier les logs

Si erreur, cliquer sur le job pour voir les logs détaillés.

---

## ⏰ Étape 7: Automatisation Quotidienne

Le cron est déjà configuré dans le workflow:

```yaml
schedule:
  - cron: '45 8 * * *'  # 8h45 UTC = 9h45 FR (hiver) / 10h45 FR (été)
```

### Modifier l'heure (optionnel):

Si vous voulez changer l'heure d'envoi:

```yaml
# Exemples:
- cron: '0 7 * * *'   # 7h00 UTC = 8h00 FR (hiver)
- cron: '30 9 * * *'  # 9h30 UTC = 10h30 FR (hiver)
- cron: '45 8 * * *'  # 8h45 UTC = 9h45 FR (hiver) [actuel]
```

**Format:** `minute heure jour mois jour_semaine`

**⚠️ Important:** GitHub Actions utilise **UTC**, pas heure locale !

---

## 📊 Monitoring

### Vérifier que ça marche:

1. **Logs GitHub Actions:**
   - https://github.com/VOTRE_USERNAME/tech-watch-agent/actions
   - Voir l'historique des runs

2. **Email reçu:**
   - Vérifier votre inbox tous les matins à 9h45

3. **Notifications:**
   - GitHub vous notifie si le workflow échoue

---

## 🔧 Dépannage

### Erreur "SMTP Authentication Failed"
- Vérifier que vous utilisez un **App Password** (pas votre mot de passe Gmail)
- Vérifier que la 2-Step Verification est activée

### Erreur "Groq API Key Invalid"
- Vérifier que la clé commence par `gsk_`
- Régénérer une clé sur https://console.groq.com/keys

### Workflow ne se lance pas automatiquement
- GitHub Actions peut avoir jusqu'à 15min de délai
- Vérifier que le repo n'est pas archivé
- Lancer manuellement pour tester

### Pas assez de résultats
- Augmenter `MAX_RESULTS_PER_SOURCE` dans le workflow
- Augmenter `DAYS_TO_FETCH`

---

## 💰 Coûts

### GitHub Actions (Gratuit)
- ✅ **2000 minutes/mois** gratuites
- ✅ Votre workflow: ~5 min/jour = **150 min/mois**
- ✅ **Largement suffisant !**

### Groq (Gratuit)
- ✅ **7000 requests/jour** gratuites
- ✅ Votre usage: ~1-2 requests/jour
- ✅ **Largement suffisant !**

### SMTP Email (Gratuit)
- ✅ Gmail: 500 emails/jour gratuits
- ✅ Votre usage: 1 email/jour
- ✅ **Largement suffisant !**

**Total: 0€/mois** 🎉

---

## 🎯 Avantages GitHub Actions

✅ **100% gratuit**
✅ **Zero maintenance** - Pas de serveur
✅ **PC peut être éteint** - Tourne dans le cloud
✅ **Logs accessibles** - Debug facile
✅ **Notifications d'erreur** - Vous êtes alerté si problème
✅ **Historique** - Voir tous les runs passés
✅ **Manual trigger** - Lancer à la demande

---

## 📚 Ressources

- GitHub Actions Cron: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule
- Groq Console: https://console.groq.com
- Gmail App Passwords: https://myaccount.google.com/apppasswords
- Cron Generator: https://crontab.guru/

---

**🚀 Vous êtes prêt ! Chaque matin à 9h45, vous recevrez votre digest automatiquement.**
