#!/bin/bash
# Verification script for reorganized Tech Watch Agent

echo "🔍 Verifying Tech Watch Agent Setup"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if in correct directory
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ Error: Run this script from the watcher/ directory${NC}"
    exit 1
fi

# Check venv
echo "1️⃣  Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ venv not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ venv exists${NC}"

# Activate venv
source venv/bin/activate

# Check Python
echo ""
echo "2️⃣  Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1)
echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"

# Check pyyaml
echo ""
echo "3️⃣  Checking dependencies..."
if python -c "import yaml" 2>/dev/null; then
    echo -e "${GREEN}✅ pyyaml installed${NC}"
else
    echo -e "${RED}❌ pyyaml not installed${NC}"
    echo -e "${YELLOW}   Run: pip install pyyaml==6.0.1${NC}"
fi

# Check typer
if python -c "import typer" 2>/dev/null; then
    TYPER_VERSION=$(python -c "import typer; print(typer.__version__)" 2>/dev/null || echo "unknown")
    echo -e "${GREEN}✅ typer $TYPER_VERSION installed${NC}"
else
    echo -e "${RED}❌ typer not installed${NC}"
fi

# Check YAML configs
echo ""
echo "4️⃣  Checking YAML configurations..."
if [ -f "configs/keywords.yaml" ]; then
    echo -e "${GREEN}✅ configs/keywords.yaml exists${NC}"
else
    echo -e "${RED}❌ configs/keywords.yaml missing${NC}"
fi

if [ -f "configs/sources.yaml" ]; then
    echo -e "${GREEN}✅ configs/sources.yaml exists${NC}"
else
    echo -e "${RED}❌ configs/sources.yaml missing${NC}"
fi

if [ -f "configs/arxiv_categories.yaml" ]; then
    echo -e "${GREEN}✅ configs/arxiv_categories.yaml exists${NC}"
else
    echo -e "${RED}❌ configs/arxiv_categories.yaml missing${NC}"
fi

# Test config loading
echo ""
echo "5️⃣  Testing configuration loading..."
python -c "
from config import Settings, BLOG_FEEDS, ARXIV_CATEGORIES
settings = Settings()
keywords = settings.keywords_list
print(f'✅ Keywords: {len(keywords)} loaded')
print(f'✅ Blog Feeds: {len(BLOG_FEEDS)} loaded')
print(f'✅ ArXiv Categories: {len(ARXIV_CATEGORIES)} loaded')
" 2>&1 | while read line; do
    if [[ $line == *"✅"* ]]; then
        echo -e "${GREEN}$line${NC}"
    elif [[ $line == *"❌"* ]]; then
        echo -e "${RED}$line${NC}"
    else
        echo "$line"
    fi
done

# Check .env
echo ""
echo "6️⃣  Checking .env file..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env exists${NC}"
    if grep -q "LLM_PROVIDER" .env; then
        PROVIDER=$(grep "LLM_PROVIDER" .env | cut -d'=' -f2)
        echo -e "${GREEN}   LLM Provider: $PROVIDER${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .env not found${NC}"
    echo -e "${YELLOW}   Copy .env.example and configure it${NC}"
fi

# Check Ollama (if using ollama)
if [ -f ".env" ] && grep -q "LLM_PROVIDER=ollama" .env; then
    echo ""
    echo "7️⃣  Checking Ollama..."
    if curl -s http://localhost:11434 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama is running${NC}"
    else
        echo -e "${YELLOW}⚠️  Ollama not running${NC}"
        echo -e "${YELLOW}   Start with: ollama serve${NC}"
    fi
fi

# Check database
echo ""
echo "8️⃣  Checking database..."
if [ -d "data/chroma_db" ]; then
    echo -e "${GREEN}✅ data/chroma_db exists${NC}"
    python main.py stats 2>&1 | grep "Documents:" | head -1 | while read line; do
        echo -e "${GREEN}   $line${NC}"
    done
else
    echo -e "${YELLOW}⚠️  data/chroma_db not found (will be created on first update)${NC}"
fi

# Summary
echo ""
echo "========================================="
echo -e "${GREEN}🎉 Verification Complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. pip install pyyaml==6.0.1 (if not installed)"
echo "  2. pip install --upgrade typer (if version < 0.24)"
echo "  3. python main.py update --days 7"
echo "  4. python main.py chat"
echo ""
echo "📖 Documentation: See PROJECT_STATUS.md"
echo ""
