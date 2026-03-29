# 📧 Options du Digest - Guide Complet

Le système de digest a été amélioré avec 3 nouvelles fonctionnalités puissantes.

---

## 🆕 **Nouvelles Fonctionnalités**

### 1. 📚 **Mode Full Database** (nouveau)
Résume **toute votre base de données** au lieu des nouveaux articles uniquement.

### 2. 🔄 **Fréquence Daily/Weekly** (nouveau)
- **Daily**: Tous les jours (par défaut)
- **Weekly**: Seulement le lundi

### 3. 🛡️ **Minimum 10 docs** (nouveau)
Si aucun nouveau document, le système récupère automatiquement les **10 derniers de la base**.

---

## 📖 **Syntaxe des Commandes**

### **A. Digest Quotidien Standard** (nouveautés)
```bash
python main.py digest --preview
python main.py digest --send
```

**Comportement:**
- Fetch les dernières 24h
- Si aucun nouveau doc → Prend les 10 derniers de la base
- Envoie un email "Daily Digest"

---

### **B. Digest Full Database** (toute la base)
```bash
python main.py digest --full-database --preview
python main.py digest --full-database --send
```

**Comportement:**
- **NE FETCH PAS** de nouveaux docs
- Résume **toute votre base de données** actuelle
- Parfait pour avoir une vue d'ensemble hebdomadaire

**Cas d'usage:**
- Le lundi matin pour résumer toute la semaine
- Après un gros `update --days 30`
- Pour partager votre veille avec un collègue

---

### **C. Digest Hebdomadaire** (lundi uniquement)
```bash
python main.py digest --frequency weekly --send
```

**Comportement:**
- **Ne s'exécute que le lundi** (sinon skip)
- Fetch les 7 derniers jours
- Envoie un email "Weekly Digest"

**Cron exemple:**
```bash
# Tous les jours à 8h45, mais n'envoie que le lundi
45 8 * * * cd /path/to/watcher && venv/bin/python main.py digest --frequency weekly --send
```

---

### **D. Digest Hebdomadaire Full Database** (combo)
```bash
python main.py digest --frequency weekly --full-database --send
```

**Comportement:**
- Ne s'exécute que le lundi
- Résume **toute la base de données**
- Email "Weekly Digest - Full Database Summary"

**💡 Cas d'usage ultime:** Veille hebdomadaire complète le lundi matin !

---

## 🎨 **Exemples d'Usage**

### Scénario 1: Veille Quotidienne
```bash
# Chaque jour à 8h45
crontab -e
45 8 * * * cd /home/user/watcher && venv/bin/python main.py digest --send
```

### Scénario 2: Résumé Hebdomadaire Complet (Lundi)
```bash
# Lundi à 8h45
45 8 * * * cd /home/user/watcher && venv/bin/python main.py digest --frequency weekly --full-database --send
```

### Scénario 3: Combo Daily + Weekly
```bash
# Daily du mardi au dimanche
45 8 * * 2-7 cd /home/user/watcher && venv/bin/python main.py digest --send

# Weekly le lundi
45 8 * * 1 cd /home/user/watcher && venv/bin/python main.py digest --frequency weekly --full-database --send
```

### Scénario 4: Tester en Local
```bash
# Preview quotidien
python main.py digest --preview

# Preview full database
python main.py digest --full-database --preview

# Forcer weekly (même si pas lundi)
# Note: Si ce n'est pas lundi, ça va skip automatiquement
python main.py digest --frequency weekly --preview
```

---

## 📊 **Différences Email**

### Daily Digest (nouveautés)
```
Subject: Tech Watch Daily Digest - 29/03/2026 - 12 documents
Header: Tech Watch Daily Digest | Video Popularity Project Edition
Stats: Nouveaux Daily: 12 articles
Title: 📚 Nouveaux Articles
```

### Weekly Digest (nouveautés semaine)
```
Subject: Tech Watch Weekly Digest - 29/03/2026 - 45 documents
Header: Tech Watch Weekly Digest | Video Popularity Project Edition
Stats: Nouveaux Weekly: 45 articles
Title: 📚 Nouveaux Articles
```

### Full Database
```
Subject: Tech Watch - Full Database Summary (150 docs) - 29/03/2026
Header: Tech Watch Daily Digest | 📚 Full Database Summary
Stats: Articles dans ce Digest: 150 articles
Title: 📚 Tous les Articles
```

---

## ⚙️ **GitHub Actions**

### Daily Digest (automatique)
Fichier: `.github/workflows/daily-digest.yml`

```yaml
schedule:
  - cron: '45 8 * * *'  # Tous les jours à 8h45 UTC
```

**Commande:**
```yaml
python main.py digest --send
```

---

### Weekly Digest (automatique)
Fichier: `.github/workflows/weekly-digest.yml`

```yaml
schedule:
  - cron: '45 8 * * 1'  # Lundi à 8h45 UTC
```

**Commande:**
```yaml
python main.py digest --send --frequency weekly
```

---

## 🔧 **Paramètres Détaillés**

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `--send` / `--no-send` | bool | `True` | Envoyer l'email ou non |
| `--preview` | bool | `False` | Afficher preview sans envoyer |
| `--full-database` | bool | `False` | Résumer toute la base au lieu des nouveautés |
| `--frequency` | str | `"daily"` | `"daily"` ou `"weekly"` (lundi uniquement) |

---

## 💡 **Astuces**

### 1. **Toujours tester avec --preview d'abord**
```bash
python main.py digest --full-database --preview
```

### 2. **Minimum 10 docs automatique**
Si pas de nouveautés, les 10 derniers sont automatiquement inclus. Pas besoin de gérer ça manuellement !

### 3. **Full database = Pas de fetch**
Le mode `--full-database` ne fetch **RIEN** de nouveau. Il résume uniquement ce qui est déjà dans ChromaDB.

Pour mettre à jour la base avant:
```bash
python main.py update --days 7
python main.py digest --full-database --send
```

### 4. **Weekly skips automatiquement**
Si vous lancez `--frequency weekly` un mardi, il affiche:
```
⏭️  Weekly digest mode: Today is not Monday. Skipping.
```

### 5. **Limite de 50 docs pour le résumé**
En mode `--full-database`, seuls les 50 premiers documents sont donnés au LLM pour le résumé (pour éviter de dépasser les tokens). Mais l'email contient les 15 premiers en détail.

---

## 🧪 **Tests Rapides**

```bash
# 1. Vérifier que la base a des documents
python main.py stats

# 2. Preview quotidien
python main.py digest --preview

# 3. Preview full database
python main.py digest --full-database --preview

# 4. Si base vide, charger des données
python main.py update --days 7

# 5. Tester l'envoi (remplacer par votre email)
python main.py digest --send --preview
```

---

## 📧 **Configuration Email**

Assurez-vous que votre `.env` contient:

```bash
EMAIL_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=votre-app-password  # Pas votre mot de passe normal !
EMAIL_FROM=votre-email@gmail.com
EMAIL_TO=destinataire@example.com
EMAIL_USE_TLS=true
```

---

## 🎯 **Cas d'Usage Recommandés**

### Pour un usage Personnel
```bash
# Daily simple
python main.py digest --send
```

### Pour un usage Professionnel
```bash
# Weekly complet le lundi
python main.py digest --frequency weekly --full-database --send
```

### Pour Partager avec l'Équipe
```bash
# Full database à la demande
python main.py update --days 30  # Charger 30 jours
python main.py digest --full-database --send  # Résumé complet
```

---

## 🚀 **Quick Start**

```bash
# 1. Charger des données (si base vide)
python main.py update --days 7

# 2. Tester le digest
python main.py digest --preview

# 3. Tester full database
python main.py digest --full-database --preview

# 4. Envoyer pour de vrai
python main.py digest --send
```

---

**🎉 Vous êtes prêt ! Profitez de vos nouveaux digests personnalisés !**
