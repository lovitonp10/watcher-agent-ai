#!/bin/bash
# Fix Groq configuration in .env

echo "🔧 Fixing Groq configuration..."

# Check if LLM_BASE_URL exists and comment it out for Groq
if grep -q "^LLM_BASE_URL=" .env; then
    echo "  - Commenting out LLM_BASE_URL (not needed for Groq)"
    sed -i 's/^LLM_BASE_URL=/#LLM_BASE_URL=/' .env
else
    echo "  - LLM_BASE_URL already commented or not present"
fi

echo "✅ Done!"
echo ""
echo "Groq will now use its default API endpoint (https://api.groq.com/openai/v1)"
echo ""
echo "Test with: python main.py digest --full-database --preview"
