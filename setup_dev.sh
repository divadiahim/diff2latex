#!/bin/bash
# Development setup script for diff2latex

set -e

echo "🔧 Setting up diff2latex development environment..."

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade pip setuptools wheel build twine

# Install package in editable mode
echo "🔗 Installing package in editable mode..."
pip install -e .

# Install development dependencies
echo "🛠️  Installing development dependencies..."
pip install -r requirements.txt

echo "✅ Development environment ready!"
echo ""
echo "🧪 To test the package, run:"
echo "   python test_package.py"
echo ""
echo "🚀 To build and publish, run:"
echo "   ./publish.sh"
