#!/bin/bash

# setup_mac.sh - Automated Mac Environment Setup for Drug Shortage Predictor AI
# Run this script using: bash setup_mac.sh

echo "🚀 Starting Mac Environment Setup..."

# 1. Install Homebrew (if not installed)
if ! command -v brew &> /dev/null
then
    echo "🍺 Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add brew to PATH based on architecture
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew is already installed. Updating..."
    brew update
fi

# 2. Install Python & Node.js
echo "🐍 Installing Python 3.11 and Node.js..."
brew install python@3.11 node

# 3. Install VS Code
if ! command -v code &> /dev/null
then
    echo "💻 Installing Visual Studio Code..."
    brew install --cask visual-studio-code
else
    echo "✅ Visual Studio Code is already installed."
fi

# 4. Install Git (if not installed)
if ! command -v git &> /dev/null
then
    echo "🐙 Installing Git..."
    brew install git
else
    echo "✅ Git is already installed."
fi

echo "🎉 Setup Complete! You are ready to build the AI product."
echo "Python version: $(python3 --version)"
echo "Node version: $(node -v)"
echo "Next step: Navigate to the project directory and install python dependencies."
