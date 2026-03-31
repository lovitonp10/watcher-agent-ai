#!/usr/bin/env python3
"""Generate sample HTML to see how errors render in email."""

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

# Generate insights for a sample document
doc = {
    "title": "AdaptToken: Entropy-based Adaptive Token Selection for MLLM Long Video Understanding",
    "abstract": "Long video understanding remains challenging for Multi-modal Large Language Models (MLLMs) due to high memory cost. We propose AdaptToken, an entropy-based approach to dynamically select the most informative tokens.",
    "source": "arxiv"
}

print("="*70)
print("HTML ERROR RENDERING TEST")
print("="*70)
print()

# Try to generate insight (will fail with invalid Groq key)
insight_html = email_service._generate_video_popularity_insight(doc, use_llm=True)

print("Generated HTML insight:")
print("-" * 70)
print(insight_html)
print("-" * 70)
print()

# Show how it looks in a simple HTML preview
html_preview = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 20px; background: #f3f4f6; }}
        .card {{ background: white; border-radius: 12px; padding: 24px; max-width: 600px; margin: 20px auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .title {{ font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 16px; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="title">🏷️ Multimodal & VLM - AdaptToken Paper</div>
        <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px;'>
            <div style='font-weight: 700; color: #92400e; margin-bottom: 8px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;'>
                🎯 For Video Popularity Project
            </div>
            <div style='color: #78350f; font-size: 14px; line-height: 1.6;'>
                {insight_html}
            </div>
        </div>
    </div>
</body>
</html>
"""

# Save preview
preview_path = "email_error_preview.html"
with open(preview_path, "w", encoding="utf-8") as f:
    f.write(html_preview)

print(f"✅ HTML preview saved to: {preview_path}")
print(f"   Open it in a browser to see how the error renders in email")
print()
print("Expected appearance:")
print("  - Yellow/orange box with project name")
print("  - Levers and Benefits from keyword fallback")
print("  - Orange warning banner at bottom with error details")
print("  - Note about fallback being used")
