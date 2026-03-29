# LLM Providers Guide 🤖

Tech Watch Agent supporte plusieurs providers LLM grâce à **LiteLLM**. Choisissez celui qui vous convient !

## 🔥 Mistral AI (Recommandé pour les francophones)

[Mistral AI](https://mistral.ai/) - Excellent rapport qualité/prix, modèles puissants, français natif.

### Configuration

1. **Créer un compte** : https://console.mistral.ai/
2. **Générer une clé API** : https://console.mistral.ai/api-keys/
3. **Configurer `.env`** :

```bash
# Provider
LLM_PROVIDER=mistral
LLM_API_KEY=votre-clé-mistral-ici

# Choisir un modèle
LLM_MODEL=mistral-large-latest        # Le plus puissant
# LLM_MODEL=mistral-medium-latest     # Équilibré
# LLM_MODEL=mistral-small-latest      # Rapide et économique
# LLM_MODEL=open-mixtral-8x7b         # Open source

# Optionnel
LLM_TEMPERATURE=0.1
```

### Modèles disponibles

| Modèle | Usage | Prix (input/output) | Contexte |
|--------|-------|---------------------|----------|
| `mistral-large-latest` | Production, tâches complexes | €3/€9 par 1M tokens | 128k |
| `mistral-medium-latest` | Équilibré | €2.5/€7.5 par 1M tokens | 32k |
| `mistral-small-latest` | Rapide, économique | €0.9/€2.7 par 1M tokens | 32k |
| `open-mixtral-8x7b` | Open source | €0.7/€0.7 par 1M tokens | 32k |

### Pourquoi Mistral ?

- ✅ **Excellent en français** (natif)
- ✅ **Moins cher qu'OpenAI** (30-50% d'économies)
- ✅ **Souveraineté européenne** (données en Europe)
- ✅ **Très performant** sur les tâches techniques
- ✅ **Modèles open source** disponibles

---

## 🟢 OpenAI (GPT-4, GPT-3.5)

Le classique, très performant mais plus cher.

### Configuration

```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-votre-clé-openai
LLM_MODEL=gpt-4-turbo-preview
```

### Modèles

- `gpt-4-turbo-preview` - Le plus puissant (€10/€30 par 1M tokens)
- `gpt-4` - Stable (€30/€60 par 1M tokens)
- `gpt-3.5-turbo` - Rapide et économique (€0.5/€1.5 par 1M tokens)

**API Key** : https://platform.openai.com/api-keys

---

## 🟣 Anthropic Claude

Excellent pour les réponses longues et nuancées.

### Configuration

```bash
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-votre-clé-anthropic
LLM_MODEL=claude-sonnet-4-6
```

### Modèles

- `claude-opus-4-6` - Le plus puissant (€15/€75 par 1M tokens)
- `claude-sonnet-4-6` - Équilibré (€3/€15 par 1M tokens)
- `claude-haiku-4-5` - Rapide (€0.25/€1.25 par 1M tokens)

**API Key** : https://console.anthropic.com/

---

## 🆓 HuggingFace (Mistral Gratuit !)

Utilise les modèles Mistral **GRATUITEMENT** via l'API HuggingFace Inference. Parfait pour débuter !

### Configuration

1. **Créer un compte** : https://huggingface.co/join (gratuit)
2. **Générer un token** : https://huggingface.co/settings/tokens
3. **Configurer `.env`** :

```bash
LLM_PROVIDER=huggingface
LLM_API_KEY=hf_votre_token_ici
LLM_MODEL=huggingface/mistralai/Mistral-7B-Instruct-v0.3
```

### Modèles gratuits

- `huggingface/mistralai/Mistral-7B-Instruct-v0.3` - Recommandé, rapide
- `huggingface/mistralai/Mixtral-8x7B-Instruct-v0.1` - Plus puissant

### Pourquoi HuggingFace ?

- ✅ **100% gratuit** (pas de carte de crédit)
- ✅ **Modèles Mistral open-source**
- ✅ **Hébergé sur le cloud** (pas besoin de GPU)
- ✅ **Rate limit généreux**
- ⚠️ Première requête peut être lente (~30s cold start)

📚 **Guide complet** : [MISTRAL_FREE.md](MISTRAL_FREE.md)

---

## 🏠 Ollama (100% Local et Gratuit)

Modèles open source qui tournent sur votre machine. Parfait pour la vie privée !

### Configuration

1. **Installer Ollama** : https://ollama.ai/download
2. **Lancer un modèle** :
   ```bash
   ollama run llama3
   # ou
   ollama run mistral
   ollama run mixtral
   ```

3. **Configurer `.env`** :
   ```bash
   LLM_PROVIDER=ollama
   LLM_API_KEY=ollama
   LLM_BASE_URL=http://localhost:11434
   LLM_MODEL=llama3
   ```

### Modèles recommandés

- `llama3` - Méta, excellent (8B ou 70B)
- `mistral` - Rapide et performant (7B)
- `mixtral` - Très puissant (8x7B)
- `phi` - Compact et efficace (2.7B)

### Avantages

- ✅ **100% gratuit** (pas de coût par token)
- ✅ **Vie privée totale** (données locales)
- ✅ **Pas de limite** (pas de quota API)
- ❌ Nécessite un GPU/CPU puissant
- ❌ Plus lent que les API cloud

---

## 📊 Comparaison Rapide

| Provider | Prix | Qualité | Français | Privacy | Vitesse |
|----------|------|---------|----------|---------|---------|
| **Mistral** | 💰💰 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **OpenAI** | 💰💰💰 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Anthropic** | 💰💰💰 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Ollama** | 🆓 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

---

## 🔧 Configuration Avancée

### Changer de provider sans réinstaller

Modifiez simplement `.env` :

```bash
# De OpenAI à Mistral
LLM_PROVIDER=mistral
LLM_API_KEY=votre-clé-mistral
LLM_MODEL=mistral-large-latest
```

Relancez l'application, c'est tout !

### Plusieurs providers en parallèle

Vous pouvez garder plusieurs clés :

```bash
# Provider actif
LLM_PROVIDER=mistral
LLM_API_KEY=clé-mistral

# Clés de backup (changez LLM_PROVIDER pour switcher)
OPENAI_API_KEY=sk-clé-openai
MISTRAL_API_KEY=clé-mistral
ANTHROPIC_API_KEY=sk-ant-clé-anthropic
```

### Vérifier votre configuration

```bash
python main.py info
```

Affiche le provider, modèle, et toute la config.

---

## 💡 Recommandations par Usage

### Pour débuter (pas cher)
→ **Mistral Small** ou **GPT-3.5-turbo**

### Pour la production (qualité)
→ **Mistral Large** ou **GPT-4-turbo**

### Pour la vie privée (local)
→ **Ollama** avec Llama3 ou Mistral

### Pour le français
→ **Mistral** (n'importe quel modèle)

### Pour économiser
→ **Ollama** (gratuit) ou **Mistral Small**

---

## 🆘 Dépannage

### "API key not found"

Vérifiez que `.env` existe et contient :
```bash
LLM_API_KEY=votre-vraie-clé
```

### "Invalid API key"

- Vérifiez que la clé est correcte (copiez-collez depuis le dashboard)
- Pour Mistral : https://console.mistral.ai/api-keys/
- Pas d'espaces avant/après la clé

### "Model not found"

- Vérifiez le nom du modèle (voir tables ci-dessus)
- Pour Mistral : `mistral-large-latest` (pas `mistral-large`)
- Pour Ollama : le modèle doit être pullé (`ollama pull llama3`)

### "Connection refused" (Ollama)

```bash
# Vérifier qu'Ollama tourne
ollama list

# Lancer Ollama
ollama serve
```

---

## 📚 Ressources

- **Mistral AI** : https://mistral.ai/ | https://docs.mistral.ai/
- **OpenAI** : https://platform.openai.com/
- **Anthropic** : https://www.anthropic.com/
- **Ollama** : https://ollama.ai/
- **LiteLLM** (sous le capot) : https://docs.litellm.ai/

---

Besoin d'aide ? Ouvrez une issue sur GitHub !
