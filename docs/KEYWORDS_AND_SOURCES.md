# Keywords & Sources - Video Popularity Edition

Ce document liste tous les keywords et sources optimisés pour le projet **Video Popularity**.

---

## 🔍 Keywords (35 total)

### Multimodal AI & Video Understanding
- Video Understanding
- Multimodal AI
- Vision-Language Models (VLM)
- Video Popularity
- CLIP, ViT, VideoLLM
- Zero-Shot Classification

### Social Media & Algorithms
- Social Media Algorithm
- TikTok Algorithm
- Instagram Algorithm
- Video Virality
- Engagement Prediction
- Content Recommendation
- Cross-Platform Analysis
- Social Media Analytics
- User Engagement

### Video Features & Analysis
- Video Features
- Audio Features
- Scene Detection
- Video Classification
- Action Recognition
- Temporal Modeling
- Shot Boundary Detection
- Video Summarization
- Video Captioning
- Thumbnail Analysis
- Video Editing

### Explainability & Interpretability
- Explainable AI (XAI)
- SHAP
- Attention Mechanism

### Creator Economy & Tools
- Creator Economy
- VidIQ
- TubeBuddy
- Hootsuite Analytics
- Video SEO

### Deep Learning Architectures
- Multimodal Learning
- Transformer models

---

## 📰 Blog Sources (27 total)

### 🔬 AI/ML Research & Engineering (7)
1. **Netflix Tech Blog** - Recommendation systems, video encoding
2. **Meta AI** - Multimodal research, CLIP-like models
3. **Google AI Blog** - Video understanding, transformers
4. **OpenAI Blog** - GPT-4V, multimodal models
5. **DeepMind Blog** - AlphaFold, video prediction
6. **Hugging Face Blog** - Open-source models, CLIP variants
7. **Anthropic Blog** - Claude vision capabilities

### 📱 Social Media Platforms Engineering (6)
8. **Meta Engineering (Reels/Instagram)** - Recommendation algorithms
9. **TikTok Engineering** - Video virality, FYP algorithm insights
10. **Snapchat Engineering** - AR filters, video processing
11. **Pinterest Engineering** - Visual search, recommendations
12. **YouTube Engineering** - Video recommendations, engagement
13. **Twitter/X Engineering** - Timeline algorithms, video engagement

### 🎬 Video/Multimodal AI Companies (2)
14. **Runway ML Blog** - Video generation, editing AI
15. **Twelve Labs Blog** - Video understanding, search, multimodal embeddings

### 📊 Social Media Analytics & Competitors (3)
16. **Hootsuite Blog** - Social media analytics, engagement metrics
17. **Buffer Blog** - Content performance, posting strategies
18. **Sprout Social Insights** - Social listening, engagement analysis

### 💰 Creator Economy & Video Analytics (3)
19. **VidIQ Blog** - YouTube analytics, SEO, thumbnail optimization
20. **TubeBuddy Blog** - Creator tools, A/B testing, analytics
21. **Creator Economy Blog** - Creator trends, monetization

### 🏢 Tech Companies with Video/Recommendation Focus (4)
22. **Airbnb Engineering** - Recommendation systems, personalization
23. **Uber Engineering** - Real-time systems, ML at scale
24. **Spotify Engineering** - Audio/music recommendations, engagement
25. **LinkedIn Engineering** - Content recommendations, feed algorithms

### 🖼️ Computer Vision & Video Research (2)
26. **NVIDIA AI Blog** - GPU-accelerated video processing, models
27. **Papers with Code Blog** - Latest research implementations

---

## 📚 ArXiv Categories (6 active)

### Priority Categories (Always included)
1. **cs.CV** - Computer Vision
   - YOLO, CLIP, X-CLIP, video analysis, object detection, action recognition

2. **cs.MM** - Multimedia
   - Video/audio fusion, multimodal learning, cross-modal retrieval

3. **cs.AI** - Artificial Intelligence
   - General AI, reasoning, planning, explainability

4. **cs.LG** - Machine Learning
   - Model architectures, optimization, SHAP, interpretability

5. **cs.CL** - Computational Linguistics (NLP)
   - Caption analysis, sentiment, speech-to-text, language understanding

6. **cs.SI** - Social & Information Networks
   - **CRITICAL**: Virality prediction, social graphs, recommendation systems, engagement modeling

### Optional Categories (Commented out - uncomment if needed)
- **cs.SD** - Sound (Audio features, music analysis)
- **eess.AS** - Audio/Speech Processing (Voice clarity, prosody)
- **cs.HC** - Human-Computer Interaction (User engagement, UX)

---

## 🎯 Why These Choices?

### Keywords
Couvrent les 4 piliers du projet Video Popularity:
1. **Multimodal AI** - Vision + Audio + Text
2. **Social Media** - TikTok/Instagram specifics
3. **Features** - Video/audio extraction techniques
4. **Explainability** - SHAP, attention, interpretability

### Sources
- **Concurrents directs**: VidIQ, TubeBuddy (YouTube analytics)
- **Plateformes**: TikTok, Instagram, YouTube (algorithmes)
- **Recherche**: Meta AI, Google AI, Hugging Face (SOTA multimodal)
- **Industrie**: Netflix, Spotify (recommandation à grande échelle)

---

## 📝 Comment Modifier

### Ajouter un keyword
Éditez `.env`:
```bash
KEYWORDS="Video Understanding,Multimodal AI,YOUR_NEW_KEYWORD"
```

### Ajouter une source
Éditez `config.py` section `BLOG_FEEDS`:
```python
"Your Blog Name": "https://example.com/feed",
```

### Modifier les catégories ArXiv
Éditez `config.py` section `ARXIV_CATEGORIES`:
```python
ARXIV_CATEGORIES = [
    "cs.CV",  # Keep this
    "cs.MM",  # Keep this
    # Add or remove others
]
```

**⚠️ Note**: Chaque catégorie ArXiv ajoute ~10-15s de temps de processing à cause du rate limiting.

---

**Dernière mise à jour**: 2026-03-29
**Optimisé pour**: Video Popularity Project (TikTok/Instagram prediction & explainability)
