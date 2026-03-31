#!/usr/bin/env python3
"""Quick test for video popularity insights generation."""

from src.email import EmailService

# Initialize with dummy SMTP config (we won't send emails)
email_service = EmailService(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_user="test@test.com",
    smtp_password="dummy",
    from_email="test@test.com",
    use_tls=True,
    llm_provider="ollama",
    llm_model="mistral",
    llm_api_key="ollama",
    llm_base_url="http://localhost:11434",
    llm_temperature=0.3,
)

# Test documents
test_docs = [
    {
        "title": "Video Understanding with Multimodal Transformers",
        "abstract": "We propose a multimodal approach for video understanding using vision and audio features.",
        "source": "arxiv"
    },
    {
        "title": "With a Little Help From My Friends: Collective Manipulation in Risk-Controlling Recommender Systems",
        "abstract": "Risk-controlling recommender systems are vulnerable to coordinated adversarial user behavior.",
        "source": "arxiv"
    },
    {
        "title": "TikTok Engagement Prediction using Deep Learning",
        "abstract": "We predict video popularity on TikTok using CNN features and engagement metrics.",
        "source": "arxiv"
    }
]

print("Testing Video Popularity Insights Generation\n" + "="*50)

for i, doc in enumerate(test_docs, 1):
    print(f"\n{i}. {doc['title'][:60]}...")
    print("-" * 50)

    # Try with LLM first, will fallback automatically if it fails
    insight = email_service._generate_video_popularity_insight(doc, use_llm=True)

    # Remove HTML tags for console display
    import re
    clean_insight = re.sub('<[^<]+?>', '', insight)
    print(clean_insight)
    print()

print("\n✅ Test completed!")
