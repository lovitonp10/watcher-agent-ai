#!/bin/bash
# Fix model name - remove groq/ prefix if present in LLM_MODEL

echo "🔧 Fixing model name prefix..."

# Remove groq/ prefix from LLM_MODEL if present
if grep -q "^LLM_MODEL=groq/" .env; then
    sed -i 's/^LLM_MODEL=groq\//LLM_MODEL=/' .env
    echo "✓ Removed groq/ prefix from LLM_MODEL"
else
    echo "✓ No prefix to remove"
fi

echo ""
echo "Current LLM_MODEL:"
grep "^LLM_MODEL=" .env

echo ""
echo "⚠️  IMPORTANT: Groq API Key Issue Detected!"
echo ""
echo "Your Groq API key appears to be invalid. Please:"
echo "1. Get a new API key from: https://console.groq.com/keys"
echo "2. Update your .env file:"
echo "   LLM_API_KEY=your_new_groq_key_here"
echo ""
echo "Current API key starts with: $(grep '^LLM_API_KEY=' .env | cut -d= -f2 | cut -c1-10)..."
