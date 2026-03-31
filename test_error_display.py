#!/usr/bin/env python3
"""Test error display in email insights."""

from src.email import EmailService
from config import Settings
import re

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
        "title": "TikTok Engagement Prediction using Multimodal Deep Learning",
        "abstract": "We predict video popularity on TikTok using CNN features, audio analysis, and engagement metrics to forecast viral content.",
        "source": "arxiv"
    },
    {
        "title": "Robot Navigation in Unknown Environments",
        "abstract": "We propose a reinforcement learning approach for autonomous robot navigation using vision-language models.",
        "source": "arxiv"
    },
]

print("="*70)
print("ERROR DISPLAY TEST")
print("="*70)
print()
print(f"LLM Provider: {settings.llm_provider}")
print(f"API Key Valid: {bool(settings.llm_api_key and settings.llm_api_key != 'ollama')}")
print()
print("Expected behavior:")
print("  - If Groq API key invalid → Error displayed in email")
print("  - If paper not relevant → 'Not directly applicable' (no error)")
print()

for i, doc in enumerate(test_docs, 1):
    print(f"{i}. {doc['title'][:50]}...")
    print("-" * 70)

    # Generate insight (will try LLM, fallback on error)
    insight = email_service._generate_video_popularity_insight(doc, use_llm=True)

    # Check what's in the insight
    clean = re.sub('<[^<]+?>', '', insight).replace('&nbsp;', ' ')

    if "Not directly applicable" in clean:
        print("✓ Status: Filtered (not relevant)")
    elif "LLM analysis failed" in insight:
        print("✓ Status: LLM error → Fallback used")
        print("✓ Error message displayed in email:")
        # Extract error message
        error_match = re.search(r'⚠️ LLM analysis failed:</strong><br><span[^>]*>(.*?)</span>', insight)
        if error_match:
            error_text = error_match.group(1).strip()
            print(f"  → {error_text[:100]}...")
    else:
        print("✓ Status: LLM success → Insights generated")

    print()

print("="*70)
print("✅ Error display test completed!")
print()
print("Email behavior:")
print("  ✓ LLM success → Only insights shown")
print("  ✓ LLM failure → Insights + error banner")
print("  ✓ Not relevant → 'Not directly applicable'")
