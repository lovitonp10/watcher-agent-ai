"""Test Groq LLM connection"""
from config import Settings
from src.rag.generator import Generator

settings = Settings()

print("=== Testing Groq Connection ===")
print(f"Provider: {settings.llm_provider}")
print(f"Model: {settings.llm_model}")

# Initialize generator
generator = Generator(
    provider=settings.llm_provider,
    api_key=settings.llm_api_key,
    model=settings.llm_model,
    temperature=settings.llm_temperature,
    base_url=settings.llm_base_url,
)

# Test with a simple summary
test_doc = {
    'title': 'Test Article',
    'source': 'Test',
    'published_date': '2026-03-30',
    'abstract': 'This is a test article about AI and machine learning.',
}

print("\nGenerating test summary...")
try:
    summary = generator.generate_article_summary(
        title=test_doc['title'],
        content=test_doc['abstract'],
        max_words=30
    )
    print(f"✅ Summary generated: {summary}")
except Exception as e:
    print(f"❌ Error: {e}")
