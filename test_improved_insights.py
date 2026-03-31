#!/usr/bin/env python3
"""Test improved insights generation."""

from src.email import EmailService
from config import Settings

settings = Settings()

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
        "title": "SOLE-R1: Video-Language Reasoning as the Sole Reward for On-Robot Reinforcement Learning",
        "abstract": "Vision-language models (VLMs) have shown impressive capabilities across diverse tasks, motivating efforts for robot reinforcement learning.",
        "source": "arxiv"
    },
    {
        "title": "AdaptToken: Entropy-based Adaptive Token Selection for MLLM Long Video Understanding",
        "abstract": "Long video understanding remains challenging for Multi-modal Large Language Models (MLLMs) due to high memory cost.",
        "source": "arxiv"
    },
    {
        "title": "See it to Place it: Evolving Macro Placements with Vision-Language Models",
        "abstract": "We propose using Vision-Language Models (VLMs) for macro placement in chip floorplanning, a complex optimization task.",
        "source": "arxiv"
    },
    {
        "title": "TikTok Engagement Prediction using Multimodal Deep Learning",
        "abstract": "We predict video popularity on TikTok using CNN features, audio analysis, and engagement metrics to forecast viral content.",
        "source": "arxiv"
    },
    {
        "title": "With a Little Help From My Friends: Collective Manipulation in Risk-Controlling Recommender Systems",
        "abstract": "Risk-controlling recommender systems are vulnerable to coordinated adversarial user behavior, allowing a small group to degrade recommendation quality.",
        "source": "arxiv"
    },
]

print("="*70)
print("IMPROVED INSIGHTS TEST")
print("="*70)

for i, doc in enumerate(test_docs, 1):
    print(f"\n{i}. {doc['title'][:60]}...")
    print("-" * 70)

    # Get insight
    insight = email_service._generate_video_popularity_insight(doc, use_llm=False)

    # Clean HTML
    import re
    clean = re.sub('<[^<]+?>', '', insight).replace('&nbsp;', ' ').strip()

    # Check if relevant or not
    if "Not directly applicable" in clean:
        print(f"✗ FILTERED OUT (not relevant)")
    else:
        print(f"✓ RELEVANT - Generated insights:")
        # Split and format for readability
        parts = clean.split('🎯 Levers:')
        if len(parts) > 1:
            levers_benefits = parts[1].split('💰 Benefits:')
            if len(levers_benefits) == 2:
                print(f"  Levers: {levers_benefits[0].strip()[:80]}...")
                print(f"  Benefits: {levers_benefits[1].strip()[:80]}...")

print("\n" + "="*70)
print("✅ Test completed!")
