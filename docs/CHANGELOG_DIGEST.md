# 🎉 Digest v2.0 - Nouvelles Fonctionnalités

**Date:** 2026-03-29
**Version:** 2.0

---

## 🆕 **Ce qui a changé**

### ✨ **1. Mode Full Database**

**Argument:** `--full-database`

**Avant:**
```bash
python main.py digest  # Seulement les nouveautés (24h)
```

**Maintenant:**
```bash
python main.py digest --full-database  # TOUTE la base de données
```

**Use case:**
- Résumé hebdomadaire de toute votre veille
- Partager votre base avec un collègue
- Vue d'ensemble après un gros `update --days 30`

---

### 🔄 **2. Fréquence Daily/Weekly**

**Argument:** `--frequency daily|weekly`

**Nouveau comportement:**
```bash
# Mode daily (défaut) - Tous les jours
python main.py digest --send

# Mode weekly - SEULEMENT LE LUNDI
python main.py digest --frequency weekly --send
```

**Si ce n'est pas lundi:**
```
⏭️  Weekly digest mode: Today is not Monday. Skipping.
```

**Use case:**
- Automatisation cron : le script s'exécute tous les jours mais n'envoie que le lundi
- Digest hebdomadaire sans gérer la logique cron

---

### 🛡️ **3. Minimum 10 Documents**

**Comportement automatique:**

Si **aucun nouveau document** trouvé (0 nouveautés), le système récupère automatiquement les **10 derniers documents** de la base.

**Avant:**
```
Aucun nouveau document trouvé aujourd'hui correspondant à vos critères.
[Email vide envoyé]
```

**Maintenant:**
```
⚠ No new documents found. Getting last 10 from database...
✓ Retrieved 10 recent documents
[Email avec les 10 derniers]
```

**Use case:**
- Week-ends ou vacances : pas de nouveautés mais vous recevez quand même du contenu
- Base bien remplie : jamais d'email vide

---

## 📊 **Comparaison des Modes**

| Mode | Commande | Fetch Nouveau | Source | Fréquence |
|------|----------|---------------|--------|-----------|
| **Daily Standard** | `digest` | ✅ 24h | ArXiv + Blogs | Quotidien |
| **Daily Full DB** | `digest --full-database` | ❌ Non | ChromaDB | Quotidien |
| **Weekly Standard** | `digest --frequency weekly` | ✅ 7 jours | ArXiv + Blogs | Lundi uniquement |
| **Weekly Full DB** | `digest --frequency weekly --full-database` | ❌ Non | ChromaDB | Lundi uniquement |

---

## 📧 **Exemples d'Emails**

### Daily Digest (nouveautés)
```
Subject: Tech Watch Daily Digest - 29/03/2026 - 12 documents
Header: 🎯 Tech Watch Daily Digest
Subtitle: Video Popularity Project Edition
Stats: Nouveaux Daily: 12 articles | Base Totale: 150 documents
```

### Weekly Digest (nouveautés semaine)
```
Subject: Tech Watch Weekly Digest - 29/03/2026 - 45 documents
Header: 🎯 Tech Watch Weekly Digest
Subtitle: Video Popularity Project Edition
Stats: Nouveaux Weekly: 45 articles | Base Totale: 150 documents
```

### Full Database
```
Subject: Tech Watch - Full Database Summary (150 docs) - 29/03/2026
Header: 🎯 Tech Watch Daily Digest
Subtitle: 📚 Full Database Summary
Stats: Articles dans ce Digest: 150 articles | Base Totale: 150 documents
```

---

## 🔧 **Modification Technique**

### Fichiers Modifiés

1. **`src/cli/commands.py`**
   - Fonction `digest()` : Ajout de `--full-database` et `--frequency`
   - Logique de récupération des 10 derniers si aucun nouveau
   - Vérification du jour pour le mode weekly

2. **`src/email/mailer.py`**
   - Fonction `send_digest()` : Ajout de `digest_type` et `full_database`
   - Fonction `_format_html_digest()` : Adaptation du HTML selon le mode
   - Subject line dynamique

3. **`.github/workflows/weekly-digest.yml`**
   - Nouveau workflow pour le digest hebdomadaire (lundi)

---

## 🧪 **Tests**

### Test Local
```bash
# 1. Charger des données
python main.py update --days 7

# 2. Test digest standard
python main.py digest --preview

# 3. Test full database
python main.py digest --full-database --preview

# 4. Test weekly (skip si pas lundi)
python main.py digest --frequency weekly --preview

# 5. Script de test automatique
./test_digest.sh
```

### Test GitHub Actions

**Daily Digest:**
1. Aller sur https://github.com/USERNAME/tech-watch-agent/actions
2. Sélectionner "Daily Tech Watch Digest"
3. Cliquer "Run workflow"

**Weekly Digest:**
1. Sélectionner "Weekly Tech Watch Digest (Monday)"
2. Cliquer "Run workflow" (va skip si pas lundi)

---

## 🚀 **Migration depuis v1.0**

### Si vous aviez un cron quotidien

**Avant (v1.0):**
```bash
45 8 * * * cd /path/watcher && venv/bin/python main.py digest
```

**Maintenant (v2.0) - Aucun changement nécessaire !**
```bash
45 8 * * * cd /path/watcher && venv/bin/python main.py digest
# Fonctionne exactement pareil, mais avec le bonus des 10 derniers si pas de nouveautés
```

### Si vous voulez ajouter le weekly

**Option A: Remplacer le daily par weekly**
```bash
# Lundi seulement
45 8 * * * cd /path/watcher && venv/bin/python main.py digest --frequency weekly --send
```

**Option B: Daily + Weekly combo**
```bash
# Daily du mardi au dimanche
45 8 * * 2-7 cd /path/watcher && venv/bin/python main.py digest --send

# Weekly le lundi (full database)
45 8 * * 1 cd /path/watcher && venv/bin/python main.py digest --frequency weekly --full-database --send
```

---

## 💡 **Best Practices**

### 1. **Daily pour la veille quotidienne**
```bash
python main.py digest --send
```
→ Nouveautés des dernières 24h, ou 10 derniers si rien

### 2. **Weekly Full Database le lundi**
```bash
python main.py digest --frequency weekly --full-database --send
```
→ Vue d'ensemble complète de toute votre base chaque lundi

### 3. **Full Database à la demande**
```bash
python main.py update --days 30  # Charger beaucoup de contenu
python main.py digest --full-database --send  # Partager avec équipe
```
→ Parfait pour onboarding ou partage

### 4. **Preview avant envoi**
```bash
python main.py digest --full-database --preview
```
→ Toujours vérifier avant d'envoyer

---

## 🐛 **Troubleshooting**

### "Database is empty"
```bash
# Solution: Charger des données
python main.py update --days 7
```

### Weekly ne s'exécute pas
```bash
# Normal si ce n'est pas lundi
# Pour forcer le test: utiliser --preview (sans --frequency weekly)
python main.py digest --preview
```

### Email subject incorrect
```bash
# Vérifier la version du code
grep "def send_digest" src/email/mailer.py
# Doit inclure: digest_type: str = "Daily", full_database: bool = False
```

---

## 📚 **Documentation**

- **Guide complet:** [DIGEST_OPTIONS.md](DIGEST_OPTIONS.md)
- **Automation:** [AUTOMATION_OPTIONS.md](AUTOMATION_OPTIONS.md)
- **GitHub Actions:** [SETUP_GITHUB_ACTIONS.md](SETUP_GITHUB_ACTIONS.md)

---

## 🎯 **Quick Commands**

```bash
# Standard daily digest
python main.py digest --send

# Full database summary
python main.py digest --full-database --send

# Weekly (Monday only)
python main.py digest --frequency weekly --send

# Weekly full database (Monday only)
python main.py digest --frequency weekly --full-database --send

# Preview any mode
python main.py digest --full-database --preview
```

---

**🎉 Enjoy your new powerful digest system!**
