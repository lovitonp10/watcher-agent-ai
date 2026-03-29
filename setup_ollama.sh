#!/bin/bash

# Tech Watch Agent - Setup Ollama (Gratuit, Local)

set -e

echo "🤖 Installation Tech Watch Agent avec Ollama (100% Gratuit)"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '(?<=Python )\d+\.\d+')
required_version="3.10"

if (( $(echo "$python_version < $required_version" | bc -l) )); then
    echo "❌ Python 3.10+ requis. Vous avez Python $python_version"
    exit 1
fi

echo "✓ Python $python_version détecté"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Création environnement virtuel..."
    python3 -m venv venv
else
    echo "✓ Environnement virtuel existe déjà"
fi

# Activate virtual environment
echo "🔌 Activation environnement virtuel..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Mise à jour pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📥 Installation dépendances Python..."
pip install -r requirements.txt > /dev/null 2>&1

echo "✓ Dépendances installées"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo ""
    echo "📥 Installation Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    echo "✓ Ollama installé"
else
    echo "✓ Ollama déjà installé"
fi

# Start Ollama service (in background)
echo "🚀 Démarrage service Ollama..."
ollama serve > /dev/null 2>&1 &
sleep 2

# Pull Mistral model
echo "📦 Téléchargement modèle Mistral (7B - ~4GB)..."
echo "   ⏳ Cela peut prendre quelques minutes..."
ollama pull mistral

echo "✓ Modèle Mistral téléchargé"

# Create .env
if [ ! -f ".env" ]; then
    echo "📝 Création fichier .env..."
    cat > .env << 'EOF'
# ============================================
# Tech Watch Agent - Configuration Ollama
# ============================================

# LLM Configuration (Ollama - 100% Gratuit, Local)
LLM_PROVIDER=ollama
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=mistral
LLM_TEMPERATURE=0.1

# Vector Database (Local)
CHROMA_DB_PATH=./data/chroma_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Veille Technique
KEYWORDS=LLMOps,RAG,Time Series,Forecasting,GenAI,LLM,Transformer,Fine-tuning
DAYS_TO_FETCH=7
MAX_RESULTS_PER_SOURCE=20

# RAG Configuration
TOP_K_RESULTS=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Email (Optionnel - Désactivé par défaut)
EMAIL_ENABLED=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=mot-de-passe-application
EMAIL_FROM=votre-email@gmail.com
EMAIL_TO=votre-email@gmail.com
EMAIL_USE_TLS=true
EOF
    echo "✓ Fichier .env créé"
else
    echo "✓ Fichier .env existe déjà"
fi

# Create data directory
mkdir -p data

echo ""
echo "✅ Installation terminée !"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Tech Watch Agent est prêt !"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Configuration :"
echo "   • LLM : Ollama + Mistral 7B (local, gratuit)"
echo "   • Base : ChromaDB (locale)"
echo "   • Coût : 0€"
echo ""
echo "🚀 Commandes disponibles :"
echo ""
echo "   # Activer l'environnement"
echo "   source venv/bin/activate"
echo ""
echo "   # Récupérer les contenus"
echo "   python main.py update"
echo ""
echo "   # Poser des questions"
echo "   python main.py chat"
echo ""
echo "   # Voir les statistiques"
echo "   python main.py stats"
echo ""
echo "   # Tester la configuration"
echo "   python test_llm.py"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Astuce : Ollama tourne en arrière-plan."
echo "   Pour l'arrêter : pkill ollama"
echo ""
