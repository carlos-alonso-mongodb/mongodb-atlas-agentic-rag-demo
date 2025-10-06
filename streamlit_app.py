import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from config import mongo_client
from ingest_data import ingest_data
from planning import generate_response, analyze_conversation_context
from memory import clear_session_memory, retrieve_session_history
from tools import get_available_tools
import uuid
import time

# Page configuration
st.set_page_config(
    page_title="MongoDB Agentic RAG Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00ed64;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f3e5f5;
        margin-right: 20%;
    }
    .tool-indicator {
        background-color: #fff3e0;
        padding: 0.5rem;
        border-radius: 5px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'data_ingested' not in st.session_state:
        st.session_state.data_ingested = False

def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">MongoDB Atlas Agentic RAG Demo</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Intelligent AI Agent with Vector Search, Memory, and Multi-Tool Capabilities</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Control Panel")
        
        # Session management
        st.subheader("Session Management")
        st.text(f"Session ID: {st.session_state.session_id[:8]}...")
        
        if st.button("New Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
        
        if st.button("Clear Memory"):
            clear_session_memory(st.session_state.session_id)
            st.session_state.messages = []
            st.success("Session memory cleared!")
            st.rerun()
        
        # Data ingestion
        st.subheader("Data Management")
        if not st.session_state.data_ingested:
            if st.button("Ingest Sample Data"):
                with st.spinner("Ingesting data and creating vector index..."):
                    if ingest_data():
                        st.session_state.data_ingested = True
                        st.success("Data ingested successfully!")
                    else:
                        st.error("Data ingestion failed!")
        
        # Available tools
        st.subheader("Available Tools")
        tools = get_available_tools()
        for tool_name, tool_info in tools.items():
            with st.expander(tool_name.replace('_', ' ').title()):
                st.write(f"**Description:** {tool_info['description']}")
                st.write(f"**Parameters:** {', '.join(tool_info['parameters'])}")
        
        # Session statistics
        st.subheader("Session Statistics")
        try:
            context = analyze_conversation_context(st.session_state.session_id)
            if context.get('status') != 'no_history':
                st.metric("Total Messages", context.get('total_messages', 0))
                st.metric("User Messages", context.get('user_messages', 0))
                st.metric("Assistant Messages", context.get('assistant_messages', 0))
            else:
                st.info("No conversation history yet")
        except Exception as e:
            st.error(f"Error loading statistics: {str(e)}")
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("Chat Interface")
        
        # Chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        
        # Chat input
        user_input = st.chat_input("Ask me anything about MongoDB, or try a calculation...")
        
        if user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Generate response
            with st.spinner("Thinking..."):
                try:
                    response = generate_response(st.session_state.session_id, user_input)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
    
    with col2:
        st.header("Quick Actions")
        
        # Demo queries
        st.subheader("Try These Queries:")
        demo_queries = [
            "What was MongoDB's latest acquisition?",
            "Calculate 15 * 23 + 45",
            "What are the key features of MongoDB Atlas?",
            "Search for information about vector databases",
            "What is the revenue growth mentioned in the report?"
        ]
        
        for query in demo_queries:
            if st.button(f"{query[:30]}...", key=f"demo_{query}"):
                st.session_state.messages.append({"role": "user", "content": query})
                with st.spinner("Thinking..."):
                    try:
                        response = generate_response(st.session_state.session_id, query)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Clear chat
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Built with MongoDB, OpenAI, and Streamlit | 
        <a href="https://www.mongodb.com/docs/atlas/atlas-vector-search/ai-agents/" target="_blank">Documentation</a>
    </div>
    """, unsafe_allow_html=True)

def show_analytics():
    """Show analytics and insights"""
    st.header("📈 Analytics & Insights")
    
    try:
        context = analyze_conversation_context(st.session_state.session_id)
        
        if context.get('status') == 'no_history':
            st.info("No conversation data available yet. Start chatting to see analytics!")
            return
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Messages", context.get('total_messages', 0))
        
        with col2:
            st.metric("User Messages", context.get('user_messages', 0))
        
        with col3:
            st.metric("Assistant Messages", context.get('assistant_messages', 0))
        
        # Topics visualization
        topics = context.get('conversation_topics', [])
        if topics and topics != ["Unable to extract topics"]:
            st.subheader("📝 Conversation Topics")
            for topic in topics[:5]:  # Show top 5 topics
                st.write(f"• {topic}")
        
        # Question patterns
        patterns = context.get('user_question_patterns', {})
        if patterns:
            st.subheader("❓ Question Patterns")
            st.write(f"Total questions: {patterns.get('total_questions', 0)}")
            st.write(f"Most common type: {patterns.get('most_common_type', 'none')}")
    
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

if __name__ == "__main__":
    main()

