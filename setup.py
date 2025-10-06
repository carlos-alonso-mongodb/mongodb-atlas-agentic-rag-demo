#!/usr/bin/env python3
"""
Setup script for MongoDB Atlas Agentic RAG Demo
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    print("\n🔧 Setting up environment file...")
    
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists("env_example.txt"):
        shutil.copy("env_example.txt", ".env")
        print("✅ .env file created from template")
        print("⚠️  Please edit .env file with your credentials")
        return True
    else:
        print("❌ env_example.txt not found")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["logs", "data", "temp"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory already exists: {directory}")
    
    return True

def run_tests():
    """Run setup tests"""
    print("\n🧪 Running setup tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_setup.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print(f"❌ Tests failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your MongoDB Atlas URI and OpenAI API key")
    print("2. Run: python test_setup.py")
    print("3. Run: python main.py")
    print("4. Or run: streamlit run streamlit_app.py")
    print("\n📚 Documentation: README.md")

def main():
    """Main setup function"""
    print("🚀 MongoDB Atlas Agentic RAG Demo Setup")
    print("=" * 50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing dependencies", install_dependencies),
        ("Creating environment file", create_env_file),
        ("Creating directories", create_directories),
        ("Running tests", run_tests)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    show_next_steps()

if __name__ == "__main__":
    main()

