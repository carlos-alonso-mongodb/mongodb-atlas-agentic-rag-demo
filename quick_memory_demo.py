#!/usr/bin/env python3
"""
Quick Memory Demo - Shows key memory capabilities in a simple format
"""

from planning import generate_response
from memory import retrieve_session_history, get_session_summary
import uuid

def quick_memory_demo():
    """Run a quick demonstration of memory capabilities"""
    
    print("🧠 Quick Memory Demo")
    print("=" * 40)
    
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}")
    
    # Demo conversation
    print("\n📝 Demo Conversation:")
    print("-" * 20)
    
    # Step 1: User introduces themselves
    print("\n1. User: My name is Alice and I'm a data scientist at Microsoft")
    response1 = generate_response(session_id, "My name is Alice and I'm a data scientist at Microsoft")
    print(f"   Assistant: {response1[:100]}...")
    
    # Step 2: User asks about their info
    print("\n2. User: What's my name and where do I work?")
    response2 = generate_response(session_id, "What's my name and where do I work?")
    print(f"   Assistant: {response2}")
    
    # Step 3: User expresses interest
    print("\n3. User: I'm interested in MongoDB Atlas for my machine learning projects")
    response3 = generate_response(session_id, "I'm interested in MongoDB Atlas for my machine learning projects")
    print(f"   Assistant: {response3[:100]}...")
    
    # Step 4: User asks about their interests
    print("\n4. User: What am I interested in?")
    response4 = generate_response(session_id, "What am I interested in?")
    print(f"   Assistant: {response4}")
    
    # Step 5: User asks for recommendations
    print("\n5. User: Can you recommend a database for my ML projects?")
    response5 = generate_response(session_id, "Can you recommend a database for my ML projects?")
    print(f"   Assistant: {response5[:150]}...")
    
    # Show memory statistics
    print(f"\n📊 Memory Statistics:")
    print("-" * 20)
    
    history = retrieve_session_history(session_id)
    print(f"Total messages: {len(history)}")
    print(f"User messages: {len([m for m in history if m['role'] == 'user'])}")
    print(f"Assistant messages: {len([m for m in history if m['role'] == 'assistant'])}")
    
    # Show session summary
    print(f"\n📋 Session Summary:")
    print("-" * 20)
    summary = get_session_summary(session_id)
    print(summary)
    
    print(f"\n✅ Memory demo completed!")
    print(f"\n💡 Key Memory Features Demonstrated:")
    print(f"   • Context continuity across questions")
    print(f"   • User information retention")
    print(f"   • Interest tracking")
    print(f"   • Personalized recommendations")
    print(f"   • Session history management")

if __name__ == "__main__":
    quick_memory_demo()
