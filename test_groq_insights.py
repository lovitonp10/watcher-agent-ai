#!/usr/bin/env python3
"""Test Groq LLM for generating rich, contextual insights."""

from src.email import EmailService
from config import Settings
import time

settings = Settings()

print(f"Configuration:")
print(f"  Provider: {settings.llm_provider}")
print(f"  Model: {settings.llm_model}")
print(f"  API Key configured: {bool(settings.llm_api_key and settings.llm_api_key != 'ollama')}")
print()

if settings.llm_provider != "groq":
    print("❌ Error: LLM provider is not 'groq'")
    print("   Please check configs/llm.yaml")
    exit(1)

if not settings.llm_api_key or settings.llm_api_key == "ollama":
    print("❌ Error: Groq API key not configured")
    print("   Please add LLM_API_KEY=<your-groq-api-key> to .env file")
    print("   Get your free API key at: https://console.groq.com/keys")
    exit(1)

email_service = EmailService(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_user="test@test.com",
    smtp_password="dummy",
    from_email="test@test.com",
    use_tls=True,
    llm_provider=settings.llm_provider,
    llm_model=settings.llm_model,
    llm_api_key=settings.llm_api_key,
    llm_base_url=settings.llm_base_url,
    llm_temperature=settings.llm_temperature,
)

test_docs = [
    {
        "title": "AdaptToken: Entropy-based Adaptive Token Selection for MLLM Long Video Understanding",
        "abstract": "Long video understanding remains challenging for Multi-modal Large Language Models (MLLMs) due to high memory cost. We propose AdaptToken to reduce tokens while maintaining performance.",
        "source": "arxiv"
    },
    {
        "title": "TikTok Engagement Prediction using Multimodal Deep Learning",
        "abstract": "We predict video popularity on TikTok using CNN features, audio analysis, and engagement metrics (CTR, watch time, shares) to forecast viral content. We achieve 85% accuracy on 100k videos.",
        "source": "arxiv"
    },
    {
        "title": "SOLE-R1: Video-Language Reasoning as the Sole Reward for On-Robot Reinforcement Learning",
        "abstract": "Vision-language models (VLMs) have shown impressive capabilities across diverse tasks, motivating efforts for robot reinforcement learning and autonomous manipulation.",
        "source": "arxiv"
    },
    {
        "title": "Explainable AI for Social Media Recommendation Systems",
        "abstract": "We apply SHAP values and attention visualization to explain recommendation decisions in social media feeds, improving user trust and engagement by 20%.",
        "source": "arxiv"
    },
]

print("="*70)
print("GROQ LLM INSIGHTS TEST")
print("="*70)

for i, doc in enumerate(test_docs, 1):
    print(f"\n{i}. {doc['title'][:55]}...")
    print("-" * 70)

    start = time.time()
    insight = email_service._generate_video_popularity_insight(doc, use_llm=True)
    elapsed = time.time() - start

    # Clean HTML
    import re
    clean = re.sub('<[^<]+?>', '', insight).replace('&nbsp;', ' ').strip()

    print(f"⏱️  Generated in {elapsed:.2f}s")

    if "Not directly applicable" in clean:
        print(f"❌ FILTERED: Not relevant to video popularity")
    else:
        print(f"✅ RELEVANT - Generated insights:")
        print()
        # Format nicely
        if "🎯 Levers:" in clean and "💰 Benefits:" in clean:
            parts = clean.split("🎯 Levers:")
            if len(parts) > 1:
                levers_benefits = parts[1].split("💰 Benefits:")
                if len(levers_benefits) == 2:
                    levers = levers_benefits[0].strip()
                    benefits = levers_benefits[1].strip()
                    print(f"  🎯 LEVERS:")
                    for line in levers.split('\n'):
                        if line.strip():
                            print(f"    {line.strip()}")
                    print()
                    print(f"  💰 BENEFITS:")
                    for line in benefits.split('\n'):
                        if line.strip():
                            print(f"    {line.strip()}")
        else:
            print(f"  {clean}")

print("\n" + "="*70)
print("✅ Test completed!")
print("="*70)
