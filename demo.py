#!/usr/bin/env python3
"""
Demo script to showcase MongoDB Atlas Agentic RAG capabilities
"""

import time
from config import mongo_client
from ingest_data import ingest_data
from planning import generate_response
from memory import clear_session_memory
import uuid

def run_demo():
    """Run a comprehensive demo of the agentic RAG system"""
    
    print("🎬 MongoDB Atlas Agentic RAG Demo")
    print("=" * 50)
    
    # Create a demo session
    session_id = str(uuid.uuid4())
    print(f"🆔 Demo Session ID: {session_id}")
    
    # Demo queries with explanations
    demo_queries = [
        {
            "query": "What was MongoDB's latest acquisition?",
            "description": "Testing vector search with knowledge base query",
            "expected_tool": "vector_search_tool"
        },
        {
            "query": "Calculate 15 * 23 + 45",
            "description": "Testing calculator tool with mathematical expression",
            "expected_tool": "calculator_tool"
        },
        {
            "query": "What are the key features of MongoDB Atlas?",
            "description": "Testing vector search for product information",
            "expected_tool": "vector_search_tool"
        },
        {
            "query": "What is the revenue growth mentioned in the report?",
            "description": "Testing vector search for financial information",
            "expected_tool": "vector_search_tool"
        },
        {
            "query": "Tell me about MongoDB's cloud strategy",
            "description": "Testing follow-up question with context",
            "expected_tool": "vector_search_tool"
        }
    ]
    
    print("\n🚀 Starting demo queries...")
    print("-" * 30)
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n{i}. {demo['description']}")
        print(f"   Query: {demo['query']}")
        print(f"   Expected tool: {demo['expected_tool']}")
        
        try:
            print("   🤔 Processing...")
            start_time = time.time()
            
            response = generate_response(session_id, demo['query'])
            
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"   ⏱️  Response time: {response_time:.2f}s")
            print(f"   🤖 Response: {response}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Small delay between queries
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    
    # Show session statistics
    try:
        from planning import analyze_conversation_context
        context = analyze_conversation_context(session_id)
        
        print("\n📊 Session Statistics:")
        print(f"   Total messages: {context.get('total_messages', 0)}")
        print(f"   User messages: {context.get('user_messages', 0)}")
        print(f"   Assistant messages: {context.get('assistant_messages', 0)}")
        
        topics = context.get('conversation_topics', [])
        if topics and topics != ["Unable to extract topics"]:
            print(f"   Main topics: {', '.join(topics[:3])}")
    
    except Exception as e:
        print(f"   Error getting statistics: {str(e)}")
    
    print("\n💡 Try the interactive interfaces:")
    print("   python main.py          # Command line")
    print("   streamlit run streamlit_app.py  # Web interface")

def run_quick_test():
    """Run a quick test to verify basic functionality"""
    
    print("🧪 Quick Functionality Test")
    print("=" * 30)
    
    try:
        # Test basic imports
        from config import mongo_client, openai_client
        print("✅ Configuration loaded")
        
        # Test MongoDB connection
        mongo_client.admin.command('ping')
        print("✅ MongoDB connection working")
        
        # Test OpenAI connection
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("✅ OpenAI connection working")
        
        # Test basic agent functionality
        session_id = str(uuid.uuid4())
        response = generate_response(session_id, "Hello, how are you?")
        print("✅ Agent response generated")
        
        print("\n🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_quick_test()
    else:
        run_demo()

