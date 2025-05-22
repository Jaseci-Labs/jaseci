#!/usr/bin/env bash
set -e

# Build Jaclang VSCode Extension
cd "$(dirname "$0")/.."

npm install
npm install -g @vscode/vsce

vsce package

# Uncomment to install locally with VS Code or Cursor
# code --install-extension jaclang-*.vsix
# cursor --install-extension jaclang-*.vsix

echo "VSCE package built successfully."
