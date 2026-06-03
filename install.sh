#!/bin/bash
set -e

echo "════════════════════════════════════════════════════════════"
echo "  Installing MAC-SPOT globally..."
echo "════════════════════════════════════════════════════════════"

INSTALL_DIR="$HOME/.mac-spot-app"

# Clean up any existing installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing installation..."
    rm -rf "$INSTALL_DIR"
fi

# Clone the repository
git clone https://github.com/Jyotiraditya21-bug/MAC-SPOT.git "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Create a virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv .venv

# Install dependencies and package
echo "Installing requirements..."
./.venv/bin/pip install -q -e .

# Add alias to ~/.zshrc if it doesn't already exist
ALIAS_LINE='alias mac-spot="'$INSTALL_DIR'/.venv/bin/mac-spot"'
if ! grep -q "alias mac-spot=" ~/.zshrc 2>/dev/null; then
    echo "" >> ~/.zshrc
    echo "$ALIAS_LINE" >> ~/.zshrc
    echo "✔ Added global 'mac-spot' alias to ~/.zshrc"
else
    echo "✔ Global alias is already configured in ~/.zshrc"
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  Successfully installed MAC-SPOT!"
echo "  To start using it immediately, run:"
echo "  source ~/.zshrc && mac-spot setup"
echo "════════════════════════════════════════════════════════════"
