#!/bin/bash
# Script to build and publish the package to PyPI

set -e

echo "🔨 Building the package..."
python -m build

echo "🔍 Checking the built package..."
python -m twine check dist/*

echo "📦 Package built successfully!"
echo "🚀 To upload to PyPI, run:"
echo "   python -m twine upload dist/*"
echo ""
echo "🚀 To upload to TestPyPI first (recommended), run:"
echo "   python -m twine upload --repository nexus dist/*"
