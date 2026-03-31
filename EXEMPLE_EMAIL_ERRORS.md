# Exemples d'affichage dans l'email digest

## ✅ Cas 1 : LLM Success - Insights générés

```
🏷️ Multimodal & VLM
📅 2026-03-30
TikTok Engagement Prediction using Multimodal Deep Learning

📄 Summary
We predict video popularity on TikTok using CNN features, audio analysis, and 
engagement metrics (CTR, watch time, shares) to forecast viral content...

🎯 For Video Popularity Project
🎯 Levers:
• Apply multimodal fusion (vision+audio+text) for richer feature extraction
• Adapt their engagement scoring formula (CTR weight = 0.4, shares = 0.3)
• Use CNN architecture for efficient frame-level feature encoding

💰 Benefits:
• 15-20% improvement in prediction accuracy on short videos (<60s)
• Platform-specific metrics → alignment with real TikTok algorithm
```

**État** : LLM a réussi, insights de qualité affichés.

---

## ⚠️ Cas 2 : LLM Failure - Erreur affichée + Fallback utilisé

```
🏷️ Multimodal & VLM
📅 2026-03-30
AdaptToken: Entropy-based Adaptive Token Selection for Long Videos

📄 Summary
Long video understanding remains challenging for MLLMs due to high memory cost.
We propose AdaptToken to reduce tokens while maintaining performance...

🎯 For Video Popularity Project
🎯 Levers:
• Apply temporal modeling for video sequence analysis
• Optimize for long-form video processing efficiency

💰 Benefits:
• Better capture of video dynamics → +15% accuracy
• Handle 60s+ videos → broader coverage

⚠️ LLM analysis failed:
litellm.BadRequestError: GroqException - {"error":{"message":"Invalid API Key"}}
Using keyword-based fallback analysis above
```

**État** : LLM a échoué (API key invalide), fallback keyword utilisé, erreur visible pour debug.

---

## ⚪ Cas 3 : Paper Non Pertinent - Filtré par le LLM

```
🏷️ AI Agents & Reasoning
📅 2026-03-30
SOLE-R1: Video-Language Reasoning for On-Robot Reinforcement Learning

📄 Summary
Vision-language models (VLMs) have shown impressive capabilities, motivating 
efforts for robot reinforcement learning and autonomous manipulation...

🎯 For Video Popularity Project
Not directly applicable to video popularity prediction
```

**État** : LLM a analysé et **intelligemment filtré** (robotique ≠ vidéos TikTok). 
**Ce n'est PAS une erreur**, c'est intentionnel.

---

## 🔧 Types d'erreurs affichées

### 1. API Key invalide
```
⚠️ LLM analysis failed:
GroqException - Invalid API Key
Using keyword-based fallback analysis above
```
**Solution** : Configurer LLM_API_KEY dans .env (voir GROQ_SETUP.md)

### 2. Rate Limit dépassé
```
⚠️ LLM analysis failed:
Rate limit exceeded (30 req/min)
Using keyword-based fallback analysis above
```
**Solution** : Attendez 1 minute ou utilisez un autre provider

### 3. Timeout
```
⚠️ LLM analysis failed:
Request timeout after 60s
Using keyword-based fallback analysis above
```
**Solution** : Vérifiez votre connexion internet ou augmentez le timeout

### 4. Erreur API temporaire
```
⚠️ LLM analysis failed:
Service temporarily unavailable (503)
Using keyword-based fallback analysis above
```
**Solution** : Réessayez plus tard, le service Groq est temporairement down

---

## 📊 Statistiques typiques

Sur un digest de **50 articles** :

| Statut | Quantité | % |
|--------|----------|---|
| ✅ LLM Success | 45 | 90% |
| ⚠️ LLM Failure (fallback) | 2 | 4% |
| ⚪ Filtered (not relevant) | 3 | 6% |

**Avec Groq gratuit** :
- Limite : 30 requêtes/minute
- Pour 50 articles : ~2-3 minutes de génération
- Taux d'échec typique : <5%

---

## 🎯 Avantages de l'affichage des erreurs

1. **Transparence** : Vous savez immédiatement si le LLM fonctionne
2. **Debug** : Les erreurs affichées permettent de diagnostiquer rapidement
3. **Fiabilité** : Le fallback garantit que vous avez toujours des insights
4. **Suivi** : Vous pouvez surveiller la santé du système via l'email

---

## 🔄 Configuration recommandée

Pour minimiser les erreurs :

1. **Utilisez Groq** (rapide, fiable, gratuit) → [GROQ_SETUP.md](GROQ_SETUP.md)
2. **Vérifiez votre API key** : Testez avec `python test_groq_insights.py`
3. **Surveillez vos limites** : 30 req/min = largement suffisant pour digests
4. **Le fallback fonctionne** : Même sans LLM, vous avez des insights contextuels

---

## 📧 Questions fréquentes

### "Pourquoi j'ai beaucoup d'erreurs ?"
→ API key invalide ou expirée. Reconfigurez dans `.env`

### "Est-ce grave si le LLM échoue ?"
→ Non, le fallback keyword génère des insights corrects (mais moins précis)

### "Comment désactiver les messages d'erreur ?"
→ Pas recommandé, mais vous pouvez mettre `use_llm=False` dans mailer.py ligne 117

### "'Not directly applicable' c'est une erreur ?"
→ **NON**, c'est une décision intelligente du LLM qui filtre les papiers non pertinents
