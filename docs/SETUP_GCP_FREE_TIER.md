# ☁️ Setup Google Cloud Platform - VM Gratuite à Vie

Google Cloud offre une **e2-micro VM gratuite** en permanence (pas seulement 1 an).

---

## 💰 Coût: 0€/mois (Forever Free)

- ✅ **1 VM e2-micro gratuite** (0.25-1 vCPU, 1GB RAM)
- ✅ **30GB disque** gratuit
- ✅ **1GB réseau sortant/mois** gratuit (Nord Amérique)
- ✅ **Pas de limite de temps** (contrairement à AWS qui limite à 1 an)

**Régions éligibles:** us-west1, us-central1, us-east1

---

## 🚀 Étape 1: Créer un Compte GCP

1. Aller sur https://cloud.google.com/free
2. S'inscrire (carte bancaire requise mais **pas de débit** si vous restez dans le free tier)
3. Vous obtenez 300$ de crédit pour 90 jours + Always Free tier

---

## 🚀 Étape 2: Créer une VM e2-micro

### A. Aller dans Compute Engine

```
https://console.cloud.google.com/compute/instances
```

Cliquer "Create Instance"

### B. Configuration de la VM

**Nom:** `tech-watch-agent`

**Région:** `us-central1` (Iowa) - **Obligatoire pour free tier**

**Zone:** `us-central1-a`

**Machine configuration:**
- Series: **E2**
- Machine type: **e2-micro** (0.25-1 vCPU, 1 GB memory)
- ✅ Cette config est **gratuite à vie**

**Boot disk:**
- Operating System: **Ubuntu**
- Version: **Ubuntu 22.04 LTS**
- Boot disk type: **Standard persistent disk**
- Size: **30 GB** (max gratuit)

**Firewall:**
- ☑️ Allow HTTP traffic
- ☑️ Allow HTTPS traffic

Cliquer **"Create"**

---

## 🚀 Étape 3: Connexion SSH

### A. Dans la console GCP

Cliquer sur **"SSH"** à côté de votre instance.

Une fenêtre de terminal s'ouvre.

### B. Mettre à jour le système

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 🚀 Étape 4: Installer Ollama + Mistral

```bash
# Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Démarrer Ollama en service
sudo systemctl start ollama
sudo systemctl enable ollama

# Télécharger Mistral 7B
ollama pull mistral

# Vérifier
ollama list
```

---

## 🚀 Étape 5: Installer Python + Watcher

```bash
# Installer Python et git
sudo apt install -y python3.10 python3-pip python3-venv git

# Cloner votre repo
cd ~
git clone https://github.com/VOTRE_USERNAME/tech-watch-agent.git watcher
cd watcher

# Créer venv et installer dépendances
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Étape 6: Configurer .env

```bash
nano .env
```

Coller:
```bash
# LLM Provider (Ollama local)
LLM_PROVIDER=ollama
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=mistral

# Keywords (Video Popularity)
KEYWORDS=Video Understanding,Multimodal AI,Vision-Language Models,VLM,Video Popularity,Social Media Algorithm,TikTok Algorithm,Instagram Algorithm,Video Virality,Engagement Prediction,Creator Economy,Content Recommendation,Explainable AI,XAI,SHAP,Attention Mechanism,Video Classification,Cross-Platform Analysis

# Data ingestion
DAYS_TO_FETCH=1
MAX_RESULTS_PER_SOURCE=15

# Email Configuration
EMAIL_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=votre-app-password
EMAIL_FROM=votre-email@gmail.com
EMAIL_TO=votre-email@gmail.com
EMAIL_USE_TLS=true
```

**Sauvegarder:** `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 🚀 Étape 7: Tester Manuellement

```bash
source venv/bin/activate
python main.py digest --preview
```

Si ça marche, tester l'envoi:
```bash
python main.py digest --send
```

---

## 🚀 Étape 8: Configurer le Cron

```bash
crontab -e
```

Choisir nano (option 1), puis ajouter:

```bash
# Tech Watch Agent - Tous les jours à 8h45 (heure serveur UTC)
45 8 * * * cd /home/VOTRE_USERNAME/watcher && /home/VOTRE_USERNAME/watcher/venv/bin/python /home/VOTRE_USERNAME/watcher/main.py digest --send >> /home/VOTRE_USERNAME/watcher/cron.log 2>&1
```

**⚠️ Remplacer `VOTRE_USERNAME`** par votre username (voir avec `whoami`)

**Sauvegarder:** `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 🚀 Étape 9: Vérifier le Cron

### Voir les cron jobs actifs:
```bash
crontab -l
```

### Voir les logs:
```bash
tail -f ~/watcher/cron.log
```

### Tester le cron maintenant (sans attendre 8h45):
```bash
# Lancer manuellement la commande cron
cd ~/watcher && venv/bin/python main.py digest --send
```

---

## 📊 Monitoring

### Voir les logs en temps réel:
```bash
ssh vers-votre-vm
tail -f ~/watcher/cron.log
```

### Vérifier que Ollama tourne:
```bash
systemctl status ollama
curl http://localhost:11434
```

### Vérifier l'espace disque:
```bash
df -h
```

---

## 🔧 Maintenance

### Mettre à jour le code:
```bash
cd ~/watcher
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Redémarrer Ollama:
```bash
sudo systemctl restart ollama
```

### Voir les processus:
```bash
ps aux | grep python
ps aux | grep ollama
```

---

## 💡 Optimisations

### A. Libérer de la RAM

La e2-micro n'a que **1GB de RAM**. Pour optimiser:

```bash
# Limiter le cache Ollama
export OLLAMA_MAX_LOADED_MODELS=1
```

Ajouter dans `.bashrc`:
```bash
echo 'export OLLAMA_MAX_LOADED_MODELS=1' >> ~/.bashrc
```

### B. Augmenter le swap (si OOM)

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### C. Nettoyer le disque

```bash
# Nettoyer les packages
sudo apt autoremove -y
sudo apt clean

# Supprimer les vieux logs
find ~/watcher -name "*.log" -mtime +30 -delete
```

---

## 🛡️ Sécurité

### A. Configurer le firewall

```bash
# Installer UFW
sudo apt install ufw

# Autoriser SSH
sudo ufw allow ssh

# Activer le firewall
sudo ufw enable
```

### B. Désactiver le mot de passe root

```bash
sudo passwd -l root
```

### C. Mettre à jour régulièrement

```bash
# Ajouter un cron pour auto-update
sudo nano /etc/cron.weekly/auto-update
```

Coller:
```bash
#!/bin/bash
apt update && apt upgrade -y
```

Rendre exécutable:
```bash
sudo chmod +x /etc/cron.weekly/auto-update
```

---

## 💰 Rester dans le Free Tier

### Règles importantes:

✅ **VM e2-micro** dans us-central1/us-west1/us-east1
✅ **Max 30GB** de disque standard
✅ **Max 1GB** de trafic sortant/mois (Nord Amérique)

⚠️ **Éviter:**
- Changer le type de machine
- Déplacer hors des régions gratuites
- Augmenter le disque au-delà de 30GB
- Utiliser des IP statiques externes (5$/mois)

### Vérifier votre facturation:

```
https://console.cloud.google.com/billing
```

Si vous voyez 0€, c'est bon ! 🎉

---

## 🆚 GCP vs GitHub Actions

| Critère | GCP e2-micro | GitHub Actions |
|---------|--------------|----------------|
| **Coût** | 0€ (forever) | 0€ (2000 min/mois) |
| **Ollama** | ✅ Fonctionne | ❌ Nécessite API externe |
| **RAM** | 1GB | 7GB |
| **Setup** | Plus complexe | Plus simple |
| **Maintenance** | Manuelle | Automatique |
| **Contrôle** | Total | Limité |

**Mon conseil:**
- **GitHub Actions** si vous voulez **zero maintenance**
- **GCP** si vous voulez **Ollama local** et plus de contrôle

---

## 🚀 Vous êtes prêt !

Votre Tech Watch Agent tourne maintenant **24/7 gratuitement** dans le cloud Google ! ☁️

Chaque matin à 8h45 UTC (9h45 FR), vous recevrez votre digest automatiquement.
