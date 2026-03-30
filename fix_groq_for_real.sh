#!/bin/bash
# Fix Groq configuration by commenting out LLM_BASE_URL in .env

echo "🔧 Fixing Groq configuration..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    exit 1
fi

# Backup .env
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
echo "✓ Backup created"

# Comment out LLM_BASE_URL if it exists
sed -i 's/^LLM_BASE_URL=/#LLM_BASE_URL=/' .env
echo "✓ LLM_BASE_URL commented out (not needed for Groq)"

# Ensure LLM_PROVIDER is set to groq
if grep -q "^LLM_PROVIDER=" .env; then
    sed -i 's/^LLM_PROVIDER=.*/LLM_PROVIDER=groq/' .env
    echo "✓ LLM_PROVIDER set to groq"
else
    echo "LLM_PROVIDER=groq" >> .env
    echo "✓ LLM_PROVIDER added"
fi

# Ensure LLM_MODEL is set correctly
if grep -q "^LLM_MODEL=" .env; then
    sed -i 's/^LLM_MODEL=.*/LLM_MODEL=mixtral-8x7b-32768/' .env
    echo "✓ LLM_MODEL set to mixtral-8x7b-32768"
else
    echo "LLM_MODEL=mixtral-8x7b-32768" >> .env
    echo "✓ LLM_MODEL added"
fi

echo ""
echo "✅ Configuration fixed!"
echo ""
echo "Current Groq settings:"
grep "^LLM_PROVIDER=" .env
grep "^LLM_MODEL=" .env
grep "^#LLM_BASE_URL=" .env || echo "(LLM_BASE_URL not set - good for Groq)"
