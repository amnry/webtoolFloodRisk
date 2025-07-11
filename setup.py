#!/usr/bin/env python3
"""
Setup script for the Flood Risk Assessment Web Application with GPT-4 Chat
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def check_api_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n⚠️  OpenAI API key not found!")
        print("Please set your OpenAI API key using one of these methods:")
        print("1. Export as environment variable: export OPENAI_API_KEY='your-api-key-here'")
        print("2. Or set it in your shell profile (.bashrc, .zshrc, etc.)")
        print("3. Or run the app with: OPENAI_API_KEY='your-key' python app.py")
        return False
    else:
        print("✅ OpenAI API key found!")
        return True

def main():
    print("🚀 Setting up Flood Risk Assessment Web Application with GPT-4 Chat")
    print("=" * 60)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Check API key
    check_api_key()
    
    print("\n🎉 Setup complete!")
    print("\nTo run the application:")
    print("1. Set your OpenAI API key (see instructions above)")
    print("2. Run: python app.py")
    print("3. Open your browser to: http://localhost:5000")
    print("\nThe chatbox will appear in the bottom right corner of the webpage.")

if __name__ == "__main__":
    main() 