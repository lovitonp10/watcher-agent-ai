#!/usr/bin/env python3
"""Check LLM configuration."""
from config import Settings

settings = Settings()

print("🔍 LLM Configuration Check\n")
print("="*60)

print(f"\n📋 From configs/llm.yaml:")
print(f"   Provider: {settings.llm_provider}")
print(f"   Model: {settings.llm_model}")
print(f"   Temperature: {settings.llm_temperature}")

print(f"\n🔐 From .env:")
print(f"   API Key: {settings.llm_api_key[:20]}..." if len(settings.llm_api_key) > 20 else f"   API Key: {settings.llm_api_key}")
print(f"   Base URL: {settings.llm_base_url}")

print("\n" + "="*60)

if settings.llm_provider == "groq":
    if settings.llm_api_key == "ollama":
        print("❌ ERROR: Provider is Groq but API key is 'ollama'")
        print("\n💡 Fix: Add your Groq API key to .env:")
        print("   LLM_API_KEY=gsk_your_groq_key_here")
        print("\n   Get a free key at: https://console.groq.com/keys")
    else:
        print("✅ Groq configuration looks OK")
        print(f"\n   Will use: groq/{settings.llm_model}")
elif settings.llm_provider == "ollama":
    print("✅ Using Ollama (local)")
    print(f"   Model: {settings.llm_model}")
    print("   Make sure 'ollama serve' is running")
else:
    print(f"ℹ️  Using provider: {settings.llm_provider}")
