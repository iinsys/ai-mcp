#!/bin/bash

# AI & MCP Toolkit Setup Script
# This script sets up the development environment

set -e

echo "🚀 Setting up AI & MCP Toolkit development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version found"

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "✅ uv package manager found"
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install -e ".[dev,mcp]"

# Create initial directories if they don't exist
echo "📁 Creating project structure..."
mkdir -p tests
mkdir -p mcp-servers/template
mkdir -p tools/template
mkdir -p examples/basic
mkdir -p docs/tutorials

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.sh

# Initialize git hooks (if in a git repository)
if [ -d ".git" ]; then
    echo "🔗 Setting up git hooks..."
    # You can add pre-commit hooks here if needed
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run tests: ./scripts/test.sh"
echo "  3. Check the examples/ directory for sample code"
echo "  4. Read the documentation in docs/"
echo ""
echo "Happy coding! 🚀"