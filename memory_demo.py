#!/usr/bin/env python3
"""
Memory Capabilities Demo for MongoDB Atlas Agentic RAG
This script demonstrates the various memory features of the agent
"""

from planning import generate_response
from memory import (
    store_chat_message, 
    retrieve_session_history, 
    get_session_summary,
    get_user_preferences,
    store_important_facts,
    retrieve_important_facts,
    store_long_term_memory,
    retrieve_long_term_memory,
    clear_session_memory
)
import uuid
import time

def demo_session_memory():
    """Demonstrate session-based memory"""
    print("🧠 DEMO 1: Session Memory")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}")
    
    # Simulate a conversation
    conversation = [
        "My name is Carlos and I'm interested in MongoDB Atlas",
        "What are the key features of MongoDB Atlas?",
        "I'm particularly interested in vector search capabilities",
        "Can you tell me more about vector search in MongoDB?",
        "What was MongoDB's latest acquisition?"
    ]
    
    print("\n📝 Simulating conversation...")
    for i, message in enumerate(conversation, 1):
        print(f"\n{i}. User: {message}")
        response = generate_response(session_id, message)
        print(f"   Assistant: {response[:100]}...")
        time.sleep(1)  # Small delay for demo effect
    
    # Show session history
    print(f"\n📊 Session Statistics:")
    history = retrieve_session_history(session_id)
    print(f"   Total messages: {len(history)}")
    print(f"   User messages: {len([m for m in history if m['role'] == 'user'])}")
    print(f"   Assistant messages: {len([m for m in history if m['role'] == 'assistant'])}")
    
    # Show session summary
    print(f"\n📋 Session Summary:")
    summary = get_session_summary(session_id)
    print(f"   {summary}")
    
    return session_id

def demo_context_continuity():
    """Demonstrate how memory maintains context across questions"""
    print("\n\n🔄 DEMO 2: Context Continuity")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    
    # First, establish context
    print("1. Establishing context...")
    response1 = generate_response(session_id, "My name is Alice and I work at a tech startup")
    print(f"   User: My name is Alice and I work at a tech startup")
    print(f"   Assistant: {response1[:100]}...")
    
    # Ask follow-up questions that rely on memory
    follow_up_questions = [
        "What's my name?",
        "Where do I work?",
        "What kind of company do I work for?",
        "Can you recommend a database for my startup?"
    ]
    
    print("\n2. Testing context continuity...")
    for i, question in enumerate(follow_up_questions, 1):
        print(f"\n{i}. User: {question}")
        response = generate_response(session_id, question)
        print(f"   Assistant: {response}")
        time.sleep(1)
    
    return session_id

def demo_user_preferences():
    """Demonstrate user preference learning"""
    print("\n\n👤 DEMO 3: User Preference Learning")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    
    # Simulate user expressing preferences
    preference_conversation = [
        "I prefer detailed technical explanations",
        "I'm interested in MongoDB Atlas pricing",
        "I need information about vector search performance",
        "Can you explain MongoDB Atlas pricing in detail?",
        "What about vector search performance metrics?"
    ]
    
    print("📝 Simulating preference-based conversation...")
    for i, message in enumerate(preference_conversation, 1):
        print(f"\n{i}. User: {message}")
        response = generate_response(session_id, message)
        print(f"   Assistant: {response[:150]}...")
        time.sleep(1)
    
    # Extract user preferences
    print(f"\n🎯 Extracted User Preferences:")
    preferences = get_user_preferences(session_id)
    if preferences:
        for key, value in preferences.items():
            print(f"   {key}: {value}")
    else:
        print("   No preferences extracted yet")
    
    return session_id

def demo_important_facts():
    """Demonstrate important fact storage and retrieval"""
    print("\n\n💡 DEMO 4: Important Facts Memory")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    
    # Simulate conversation with important facts
    fact_conversation = [
        "MongoDB's latest acquisition was Voyage AI",
        "Voyage AI specializes in embedding and reranking models",
        "MongoDB Atlas has vector search capabilities",
        "What was MongoDB's latest acquisition?",
        "What does Voyage AI do?"
    ]
    
    print("📝 Simulating fact-based conversation...")
    for i, message in enumerate(fact_conversation, 1):
        print(f"\n{i}. User: {message}")
        response = generate_response(session_id, message)
        print(f"   Assistant: {response[:150]}...")
        time.sleep(1)
    
    # Store some important facts manually
    important_facts = [
        "MongoDB acquired Voyage AI for embedding technology",
        "Voyage AI provides state-of-the-art embedding models",
        "MongoDB Atlas supports vector search with embeddings"
    ]
    
    print(f"\n💾 Storing important facts...")
    store_important_facts(session_id, important_facts)
    
    # Retrieve and display facts
    print(f"\n📚 Retrieved Important Facts:")
    facts = retrieve_important_facts(session_id)
    for i, fact in enumerate(facts, 1):
        print(f"   {i}. {fact}")
    
    return session_id

def demo_long_term_memory():
    """Demonstrate long-term memory across sessions"""
    print("\n\n🗄️ DEMO 5: Long-Term Memory")
    print("=" * 50)
    
    # Create multiple sessions to simulate long-term memory
    sessions = []
    
    # Session 1: User introduces themselves
    session1 = str(uuid.uuid4())
    print("📝 Session 1: User introduction")
    response1 = generate_response(session1, "Hi, I'm Bob and I'm a data scientist at Google")
    print(f"   User: Hi, I'm Bob and I'm a data scientist at Google")
    print(f"   Assistant: {response1[:100]}...")
    
    # Store long-term memory
    store_long_term_memory(session1, "user_profile", "Bob is a data scientist at Google")
    sessions.append(session1)
    
    # Session 2: User asks about their interests
    session2 = str(uuid.uuid4())
    print(f"\n📝 Session 2: User interests")
    response2 = generate_response(session2, "I'm interested in machine learning and databases")
    print(f"   User: I'm interested in machine learning and databases")
    print(f"   Assistant: {response2[:100]}...")
    
    # Store long-term memory
    store_long_term_memory(session2, "user_interests", "Bob is interested in machine learning and databases")
    sessions.append(session2)
    
    # Session 3: Retrieve long-term memory
    session3 = str(uuid.uuid4())
    print(f"\n📝 Session 3: Memory retrieval")
    
    # Retrieve long-term memories
    profile_memories = retrieve_long_term_memory("user_profile")
    interest_memories = retrieve_long_term_memory("user_interests")
    
    print(f"\n🧠 Retrieved Long-Term Memories:")
    print(f"   Profile memories: {len(profile_memories)}")
    for memory in profile_memories:
        print(f"     - {memory['content']}")
    
    print(f"   Interest memories: {len(interest_memories)}")
    for memory in interest_memories:
        print(f"     - {memory['content']}")
    
    # Use memory in conversation
    context = f"Based on previous sessions, I know that {profile_memories[0]['content']} and {interest_memories[0]['content']}."
    print(f"\n💬 Using memory in conversation:")
    print(f"   Context: {context}")
    
    return sessions

def demo_memory_analytics():
    """Demonstrate memory analytics and insights"""
    print("\n\n📊 DEMO 6: Memory Analytics")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    
    # Simulate a longer conversation
    conversation = [
        "What is MongoDB?",
        "Tell me about vector search",
        "What are the pricing options?",
        "How does Atlas compare to other databases?",
        "What about security features?",
        "Can you explain the performance metrics?",
        "What support options are available?"
    ]
    
    print("📝 Simulating extended conversation...")
    for i, message in enumerate(conversation, 1):
        print(f"\n{i}. User: {message}")
        response = generate_response(session_id, message)
        print(f"   Assistant: {response[:100]}...")
        time.sleep(0.5)
    
    # Analyze conversation
    from planning import analyze_conversation_context
    context = analyze_conversation_context(session_id)
    
    print(f"\n📈 Conversation Analytics:")
    print(f"   Total messages: {context.get('total_messages', 0)}")
    print(f"   User messages: {context.get('user_messages', 0)}")
    print(f"   Assistant messages: {context.get('assistant_messages', 0)}")
    
    topics = context.get('conversation_topics', [])
    if topics and topics != ["Unable to extract topics"]:
        print(f"   Main topics: {', '.join(topics[:5])}")
    
    patterns = context.get('user_question_patterns', {})
    if patterns:
        print(f"   Question patterns: {patterns}")
    
    return session_id

def main():
    """Run all memory demos"""
    print("🧠 MongoDB Atlas Agentic RAG - Memory Capabilities Demo")
    print("=" * 70)
    
    try:
        # Run all demos
        demo_session_memory()
        demo_context_continuity()
        demo_user_preferences()
        demo_important_facts()
        demo_long_term_memory()
        demo_memory_analytics()
        
        print("\n\n🎉 All memory demos completed successfully!")
        print("\n💡 Key Memory Features Demonstrated:")
        print("   ✅ Session-based conversation history")
        print("   ✅ Context continuity across questions")
        print("   ✅ User preference learning")
        print("   ✅ Important fact storage and retrieval")
        print("   ✅ Long-term memory across sessions")
        print("   ✅ Conversation analytics and insights")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")

if __name__ == "__main__":
    main()
