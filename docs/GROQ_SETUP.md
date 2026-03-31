# Configuration Groq pour Insights LLM

## 🚀 Quick Setup

### 1. Obtenir une API Key Groq (gratuite)

1. Visitez : https://console.groq.com/keys
2. Créez un compte gratuit
3. Cliquez sur "Create API Key"
4. Copiez la clé générée (format : `gsk_...`)

### 2. Configurer le fichier .env

Ouvrez le fichier `.env` dans le dossier `watcher/` et ajoutez/modifiez :

```bash
# LLM Configuration
LLM_API_KEY=gsk_VotreCléGroqIci...
LLM_BASE_URL=  # Laissez vide pour Groq (utilise l'endpoint par défaut)
```

**Important** : Remplacez `gsk_VotreCléGroqIci...` par votre vraie clé API Groq.

### 3. Vérifier la configuration

Le fichier `configs/llm.yaml` devrait déjà contenir :

```yaml
llm_provider: "groq"
llm_model: llama-3.3-70b-versatile
llm_temperature: 0.1
```

### 4. Tester

```bash
cd watcher
source venv/bin/activate
python test_groq_insights.py
```

Si ça fonctionne, vous verrez des insights générés par le LLM en ~2-5 secondes par article.

## 🎯 Avantages du LLM vs Keyword Fallback

### Avec LLM (Groq) ✅
```
🎯 Levers:
• Apply entropy-based token selection for efficient long video processing
• Implement adaptive frame sampling based on content importance
• Use attention mechanisms to identify key engagement moments

💰 Benefits:
• 40% reduction in memory cost for 60s+ videos → broader coverage
• 15-20% improvement in prediction accuracy on complex scenes
• Real-time inference enables live creator feedback
```

### Sans LLM (Keyword fallback) ⚠️
```
🎯 Levers:
• Apply temporal modeling for video sequence analysis
• Optimize for long-form video processing efficiency

💰 Benefits:
• Better capture of video dynamics → +15% accuracy
• Handle 60s+ videos → broader coverage
```

Le LLM génère des insights **beaucoup plus spécifiques** au contenu réel du papier !

## 🆓 Limites Gratuites Groq

- **Gratuit** : 30 requêtes/minute, 6000 requêtes/jour
- **Vitesse** : ~2-5 secondes par article (très rapide)
- **Modèle** : llama-3.3-70b-versatile (excellent pour l'analyse technique)

Largement suffisant pour vos digests quotidiens/hebdomadaires.

## 🔄 Fallback Automatique

Si Groq échoue (rate limit, timeout), le système bascule automatiquement sur l'analyse par mots-clés (rapide mais moins précise).

## 🧪 Test Complet

Une fois l'API key configurée :

```bash
# Test rapide
python test_groq_insights.py

# Test digest complet
python main.py digest --preview
```
