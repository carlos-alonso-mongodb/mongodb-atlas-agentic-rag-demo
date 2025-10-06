from config import mongo_client
from ingest_data import ingest_data
from planning import generate_response, analyze_conversation_context
from memory import clear_session_memory, retrieve_session_history
import uuid
import sys

def main():
    """
    Main function to run the AI agent demo
    """
    print("🤖 MongoDB Atlas Agentic RAG Demo")
    print("=" * 50)
    
    try:
        # Check if user wants to ingest data
        run_ingest = input("Ingest sample data? (y/n): ").lower().strip()
        if run_ingest == 'y':
            print("\n📚 Starting data ingestion...")
            if ingest_data():
                print("✅ Data ingestion completed successfully!")
            else:
                print("❌ Data ingestion failed. Please check your configuration.")
                return
        
        # Get or create session ID
        session_input = input("\nEnter a session ID (or press Enter for new session): ").strip()
        if session_input:
            session_id = session_input
        else:
            session_id = str(uuid.uuid4())
            print(f"🆔 New session created: {session_id}")
        
        # Show session info
        history = retrieve_session_history(session_id)
        if history:
            print(f"📝 Continuing session with {len(history)} previous messages")
        else:
            print("🆕 Starting new session")
        
        print("\n💬 Chat with the AI agent (type 'quit' to exit, 'help' for commands)")
        print("-" * 50)
        
        while True:
            try:
                user_query = input("\n👤 You: ").strip()
                
                if user_query.lower() == 'quit':
                    print("👋 Goodbye!")
                    break
                
                if user_query.lower() == 'help':
                    show_help()
                    continue
                
                if user_query.lower() == 'clear':
                    clear_session_memory(session_id)
                    print("🧹 Session memory cleared!")
                    continue
                
                if user_query.lower() == 'status':
                    show_session_status(session_id)
                    continue
                
                if not user_query:
                    print("❓ Please enter a query or type 'help' for commands.")
                    continue
                
                print("\n🤔 Thinking...")
                answer = generate_response(session_id, user_query)
                
                print(f"\n🤖 Assistant: {answer}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'quit' to exit.")
    
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)
    
    finally:
        mongo_client.close()
        print("\n🔌 Database connection closed.")

def show_help():
    """
    Show available commands
    """
    print("\n📋 Available Commands:")
    print("  help     - Show this help message")
    print("  clear    - Clear session memory")
    print("  status   - Show session status")
    print("  quit     - Exit the application")
    print("\n💡 Example queries:")
    print("  - What was MongoDB's latest acquisition?")
    print("  - Calculate 123 + 456")
    print("  - What are the key features of MongoDB Atlas?")
    print("  - Search for information about vector databases")

def show_session_status(session_id: str):
    """
    Show session status and statistics
    """
    try:
        context = analyze_conversation_context(session_id)
        
        print(f"\n📊 Session Status for {session_id}")
        print("-" * 40)
        
        if context.get("status") == "no_history":
            print("🆕 New session - no previous conversation")
        else:
            print(f"💬 Total messages: {context.get('total_messages', 0)}")
            print(f"👤 User messages: {context.get('user_messages', 0)}")
            print(f"🤖 Assistant messages: {context.get('assistant_messages', 0)}")
            
            topics = context.get('conversation_topics', [])
            if topics and topics != ["Unable to extract topics"]:
                print(f"📝 Main topics: {', '.join(topics[:3])}")
            
            patterns = context.get('user_question_patterns', {})
            if patterns:
                print(f"❓ Questions asked: {patterns.get('total_questions', 0)}")
                print(f"🔍 Most common question type: {patterns.get('most_common_type', 'none')}")
    
    except Exception as e:
        print(f"❌ Error getting session status: {str(e)}")

def run_demo_queries(session_id: str):
    """
    Run a set of demo queries to showcase the agent's capabilities
    """
    demo_queries = [
        "What was MongoDB's latest acquisition?",
        "Calculate 15 * 23 + 45",
        "What are the key features of MongoDB Atlas?",
        "Search for information about vector databases",
        "What is the revenue growth mentioned in the report?"
    ]
    
    print("\n🎯 Running demo queries...")
    print("-" * 30)
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{i}. Query: {query}")
        try:
            answer = generate_response(session_id, query)
            print(f"   Answer: {answer}")
        except Exception as e:
            print(f"   Error: {str(e)}")
        
        if i < len(demo_queries):
            input("\n   Press Enter to continue to next query...")

if __name__ == "__main__":
    main()

