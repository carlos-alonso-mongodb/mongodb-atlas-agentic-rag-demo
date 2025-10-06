#!/usr/bin/env python3
"""
Test script to verify the MongoDB Atlas Agentic RAG Demo setup
"""

import os
import sys
from dotenv import load_dotenv

def test_environment_variables():
    """Test if all required environment variables are set"""
    print("🔍 Testing environment variables...")
    
    load_dotenv()
    
    required_vars = [
        "MONGODB_URI",
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🔍 Testing imports...")
    
    try:
        import pymongo
        print("✅ pymongo imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pymongo: {e}")
        return False
    
    try:
        import openai
        print("✅ openai imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import openai: {e}")
        return False
    
    try:
        import streamlit
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import streamlit: {e}")
        return False
    
    try:
        import langchain
        print("✅ langchain imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain: {e}")
        return False
    
    return True

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("\n🔍 Testing MongoDB connection...")
    
    try:
        from config import mongo_client
        # Test connection by pinging the database
        mongo_client.admin.command('ping')
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🔍 Testing OpenAI connection...")
    
    try:
        from config import openai_client
        # Test connection by making a simple API call
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("✅ OpenAI connection successful")
        return True
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

def test_project_structure():
    """Test if all required files exist"""
    print("\n🔍 Testing project structure...")
    
    required_files = [
        "config.py",
        "ingest_data.py",
        "tools.py",
        "memory.py",
        "planning.py",
        "main.py",
        "streamlit_app.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files exist")
        return True

def main():
    """Run all tests"""
    print("🧪 MongoDB Atlas Agentic RAG Demo - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Project Structure", test_project_structure),
        ("Imports", test_imports),
        ("MongoDB Connection", test_mongodb_connection),
        ("OpenAI Connection", test_openai_connection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 You can now run:")
        print("  python main.py          # Command line interface")
        print("  streamlit run streamlit_app.py  # Web interface")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

