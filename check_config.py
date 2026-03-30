"""Check current LLM configuration"""
from config import Settings

settings = Settings()

print("=== Current LLM Configuration ===")
print(f"Provider: {settings.llm_provider}")
print(f"Model: {settings.llm_model}")
print(f"API Key (first 10 chars): {settings.llm_api_key[:10]}...")
print(f"Base URL: {settings.llm_base_url}")
print(f"Temperature: {settings.llm_temperature}")
