# Configuration Email 📧

Guide complet pour recevoir automatiquement le digest quotidien par email.

## 🎯 Vue d'ensemble

Le système peut vous envoyer chaque matin à 8h45 (ou l'heure de votre choix) un email contenant :
- ✅ **Résumé AI** des nouvelles découvertes
- ✅ **Liste des nouveaux papers et articles** avec liens directs
- ✅ **Statistiques** de votre base de connaissances
- ✅ **Format HTML élégant** et responsive

## 📋 Configuration Rapide

### Étape 1 : Configurer les paramètres email dans `.env`

Éditez votre fichier `.env` :

```bash
# Activer les emails
EMAIL_ENABLED=true

# Configuration SMTP (exemple Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=votre-mot-de-passe-application
EMAIL_FROM=votre-email@gmail.com
EMAIL_TO=destination@example.com
EMAIL_USE_TLS=true
```

### Étape 2 : Tester la configuration

```bash
python main.py test-email
```

Si tout est OK, vous verrez :
```
✅ Email configuration is correct!
```

### Étape 3 : Tester l'envoi du digest

```bash
# Preview sans envoyer
python main.py digest --preview

# Envoyer réellement
python main.py digest
```

### Étape 4 : Automatiser avec cron (Linux/Mac)

```bash
# Éditer le crontab
crontab -e

# Ajouter cette ligne pour exécution à 8h45 chaque jour
45 8 * * * /chemin/vers/watcher/schedule_digest.sh
```

## 🔐 Configuration par Provider Email

### Gmail (Recommandé)

1. **Activer l'authentification à 2 facteurs** :
   - Aller sur https://myaccount.google.com/security
   - Activer "Validation en deux étapes"

2. **Créer un mot de passe d'application** :
   - Aller sur https://myaccount.google.com/apppasswords
   - Sélectionner "Mail" et "Autre (nom personnalisé)"
   - Nommer "Tech Watch Agent"
   - Copier le mot de passe généré (16 caractères)

3. **Configuration `.env`** :
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=mot-de-passe-application-16-caracteres
EMAIL_FROM=votre-email@gmail.com
EMAIL_TO=destination@gmail.com  # Peut être le même
EMAIL_USE_TLS=true
```

### Outlook / Hotmail

```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=votre-email@outlook.com
SMTP_PASSWORD=votre-mot-de-passe
EMAIL_FROM=votre-email@outlook.com
EMAIL_TO=destination@outlook.com
EMAIL_USE_TLS=true
```

### Yahoo Mail

```bash
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=votre-email@yahoo.com
SMTP_PASSWORD=mot-de-passe-application  # Générer sur account.yahoo.com
EMAIL_FROM=votre-email@yahoo.com
EMAIL_TO=destination@example.com
EMAIL_USE_TLS=true
```

### Serveur SMTP personnalisé

```bash
SMTP_HOST=mail.votredomaine.com
SMTP_PORT=587  # ou 465 pour SSL
SMTP_USER=votre-utilisateur
SMTP_PASSWORD=votre-mot-de-passe
EMAIL_FROM=noreply@votredomaine.com
EMAIL_TO=votre-email@example.com
EMAIL_USE_TLS=true  # false si port 465 (SSL)
```

## ⏰ Planification Automatique

### Linux / Mac (cron)

1. **Rendre le script exécutable** :
```bash
chmod +x schedule_digest.sh
```

2. **Éditer le script** et mettre le bon chemin :
```bash
nano schedule_digest.sh
# Modifier SCRIPT_DIR vers votre dossier watcher
```

3. **Configurer cron** :
```bash
crontab -e
```

4. **Ajouter la tâche** :

```bash
# Tous les jours à 8h45
45 8 * * * /chemin/complet/vers/watcher/schedule_digest.sh

# Exemples d'autres horaires :
# Lundi-Vendredi à 9h00
0 9 * * 1-5 /chemin/vers/schedule_digest.sh

# Tous les jours à 7h30
30 7 * * * /chemin/vers/schedule_digest.sh

# Deux fois par jour (8h et 18h)
0 8,18 * * * /chemin/vers/schedule_digest.sh
```

5. **Vérifier que cron est actif** :
```bash
crontab -l  # Lister les tâches cron
```

### Windows (Planificateur de tâches)

1. **Créer `schedule_digest.bat`** :
```batch
@echo off
cd C:\chemin\vers\watcher
call venv\Scripts\activate
python main.py digest
echo Digest sent at %date% %time% >> digest.log
```

2. **Ouvrir le Planificateur de tâches** :
   - Rechercher "Planificateur de tâches" dans Windows
   - Cliquer sur "Créer une tâche simple"

3. **Configuration** :
   - **Nom** : Tech Watch Digest
   - **Déclencheur** : Quotidien à 8h45
   - **Action** : Démarrer un programme
   - **Programme** : `C:\chemin\vers\watcher\schedule_digest.bat`

4. **Options avancées** :
   - ✅ Exécuter même si l'utilisateur n'est pas connecté
   - ✅ Exécuter avec les autorisations maximales

### Docker (Bonus)

Créer un `docker-compose.yml` :

```yaml
version: '3.8'

services:
  tech-watch-digest:
    build: .
    environment:
      - EMAIL_ENABLED=true
      - SMTP_HOST=${SMTP_HOST}
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
    volumes:
      - ./data:/app/data
    command: sh -c "while true; do python main.py digest && sleep 86400; done"
```

## 🧪 Tests et Débogage

### Test basique
```bash
python main.py test-email
```

### Preview du digest (sans envoyer)
```bash
python main.py digest --preview
```

### Envoyer manuellement
```bash
python main.py digest
```

### Désactiver temporairement
```bash
python main.py digest --no-send
```

### Voir les logs
```bash
# Logs cron
tail -f digest.log

# Logs système
tail -f /var/log/syslog | grep CRON
```

## 🔧 Dépannage

### "Authentication failed"

**Gmail** :
- Vérifiez que vous utilisez un **mot de passe d'application**, pas votre mot de passe normal
- Activer l'authentification à 2 facteurs : https://myaccount.google.com/security
- Générer un mot de passe d'application : https://myaccount.google.com/apppasswords

**Outlook** :
- Vérifier que l'option "Accès moins sécurisé" est activée (non recommandé)
- Ou utiliser OAuth2 (configuration avancée)

### "Connection refused"

- Vérifier le `SMTP_HOST` et `SMTP_PORT`
- Vérifier que le firewall n'est pas bloquant
- Essayer avec `EMAIL_USE_TLS=false` si port 465

### "Timeout"

- Problème réseau ou firewall
- Tester avec `telnet smtp.gmail.com 587`
- Vérifier la connexion internet

### Cron ne s'exécute pas

```bash
# Vérifier que cron est actif
sudo systemctl status cron

# Vérifier les logs
grep CRON /var/log/syslog

# Tester le script manuellement
bash schedule_digest.sh

# Vérifier les permissions
ls -l schedule_digest.sh
```

### Email non reçu

- Vérifier les **spams/courrier indésirable**
- Vérifier `EMAIL_TO` dans `.env`
- Tester avec `python main.py digest`
- Vérifier les logs : `tail digest.log`

## 📊 Format du Digest

Le digest contient :

### Section 1 : Résumé AI
Résumé intelligent généré par Mistral/GPT des principales découvertes

### Section 2 : Statistiques
- Nombre de nouveaux documents
- Total en base de données
- Répartition par source

### Section 3 : Nouveaux Contenus
Liste organisée par source :
- ArXiv papers
- Hugging Face papers
- Blog posts (Netflix, Meta, etc.)

Chaque document inclut :
- 📌 Titre (cliquable)
- 📅 Date de publication
- 📝 Résumé court
- 🔗 Lien direct

### Format
- HTML responsive (lisible sur mobile)
- Fallback texte brut
- Style professionnel et élégant

## 🎨 Personnalisation

### Changer l'heure d'envoi

Modifier la crontab :
```bash
# 7h30 au lieu de 8h45
30 7 * * * /chemin/vers/schedule_digest.sh
```

### Envoyer à plusieurs destinataires

Modifier le script pour boucler sur plusieurs emails :

```python
# Dans digest command
for email in ["email1@example.com", "email2@example.com"]:
    email_service.send_digest(to_email=email, ...)
```

### Changer la période (plus que 24h)

Modifier dans `digest` command :
```python
days_back=1,  # Changer à 2 ou 7 jours
```

### Filtrer par source

Modifier le script pour filtrer :
```python
# Seulement ArXiv
documents = [d for d in documents if d.source == "arxiv"]
```

## 💡 Conseils

1. **Commencez avec un preview** : `python main.py digest --preview`
2. **Testez manuellement** avant d'automatiser
3. **Utilisez Gmail** avec mot de passe d'application (plus simple)
4. **Vérifiez les spams** la première fois
5. **Consultez digest.log** en cas de problème
6. **Exécutez update avant digest** pour avoir les données fraîches

## 🔒 Sécurité

- ⚠️ **Ne commitez JAMAIS le fichier `.env`** (il contient vos mots de passe)
- ✅ Utilisez des **mots de passe d'application** (Gmail, Yahoo)
- ✅ Activez **l'authentification à 2 facteurs**
- ✅ `.gitignore` contient déjà `.env`

## 📚 Commandes Utiles

```bash
# Tester la config email
python main.py test-email

# Preview du digest
python main.py digest --preview

# Envoyer le digest
python main.py digest

# Envoyer sans mettre à jour
python main.py digest --no-send

# Éditer le cron
crontab -e

# Voir les crons actifs
crontab -l

# Désactiver temporairement
# Commenter la ligne dans crontab avec #
```

---

Besoin d'aide ? Ouvrez une issue sur GitHub !
