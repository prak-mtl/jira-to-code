#!/bin/bash

echo "🚀 Setting up Persona-Driven AI Framework..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GEMINI_API_KEY"
fi

# Create .ai directory structure
echo "📁 Creating .ai directory structure..."
mkdir -p .ai/{rules,workflow}

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your GEMINI_API_KEY"
echo "  2. Run: source venv/bin/activate"
echo "  3. Test: python test_workflow.py"
echo "  4. Start API: python main.py"
echo ""

