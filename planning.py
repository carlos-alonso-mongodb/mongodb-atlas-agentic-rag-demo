from config import openai_client, OPENAI_MODEL
from tools import (
    vector_search_tool, 
    calculator_tool, 
    web_search_tool, 
    document_analysis_tool,
    hybrid_search_tool,
    get_available_tools
)
from memory import (
    store_chat_message, 
    retrieve_session_history, 
    get_session_summary,
    get_user_preferences
)
import json
import re
from datetime import datetime

def clean_session_history(session_history: list) -> list:
    """
    Clean session history by removing non-serializable objects like datetime
    """
    cleaned_history = []
    for msg in session_history:
        cleaned_msg = {
            "role": msg.get("role", ""),
            "content": msg.get("content", "")
        }
        cleaned_history.append(cleaned_msg)
    return cleaned_history

def tool_selector(user_input: str, session_history: list = None) -> tuple:
    """
    Determine which tool to use based on user input and conversation history
    """
    # Get available tools information
    available_tools = get_available_tools()
    
    # Create system prompt for tool selection
    system_prompt = f"""
You are an AI agent that can use various tools to help users. Based on the user's input and conversation history, select the most appropriate tool.

Available tools:
{json.dumps(available_tools, indent=2)}

IMPORTANT TOOL SELECTION GUIDELINES:
1. Use vector_search_tool for questions about:
   - MongoDB (company, products, features, acquisitions, financials)
   - Database technology, vector databases, search capabilities
   - Information that might be in the knowledge base (MongoDB earnings reports, documentation)
   - Technical questions about databases, search, or AI/ML topics

2. Use calculator_tool for:
   - Mathematical expressions and calculations
   - Any query containing numbers and mathematical operations

3. Use web_search_tool for:
   - General knowledge questions not related to MongoDB/databases
   - Sports, entertainment, geography, history, science facts
   - Current events and real-time information
   - Questions about companies, people, places not in the knowledge base
   - Any factual question that's not about MongoDB, databases, or technical topics

4. Use document_analysis_tool when:
   - User provides a document to analyze
   - User asks to analyze specific text content

5. Use hybrid_search_tool for:
   - Complex queries that need both semantic and keyword matching
   - When you're unsure between vector and text search

6. Use "none" for:
   - Simple greetings and casual conversation
   - Questions asking for opinions or advice
   - Requests for explanations of concepts without specific facts

PRIORITY: Always try vector_search_tool first for MongoDB-related questions, database topics, or technical information.

Return a JSON object with the tool name and input: {{"tool": "tool_name", "input": "processed_input"}}
"""
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history if available
    if session_history:
        cleaned_history = clean_session_history(session_history[-5:])  # Last 5 messages for context
        messages.extend(cleaned_history)
    
    # Add current user input
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.1
        )
        
        tool_response = response.choices[0].message.content
        
        # Parse JSON response
        try:
            tool_call = json.loads(tool_response)
            selected_tool = tool_call.get("tool", "none")
            tool_input = tool_call.get("input", user_input)
            
            # Ensure tool_input is not empty if a tool is selected
            if selected_tool != "none":
                # Handle different input types
                if isinstance(tool_input, dict):
                    # Extract query from dictionary if it exists
                    if 'query' in tool_input:
                        tool_input = tool_input['query']
                    elif 'input' in tool_input:
                        tool_input = tool_input['input']
                    else:
                        # Convert dict to string as fallback
                        tool_input = str(tool_input)
                elif not isinstance(tool_input, str):
                    print(f"DEBUG: tool_input is not a string: {type(tool_input)}. Converting to string.")
                    tool_input = str(tool_input)
                
                if not tool_input or not tool_input.strip():
                    print(f"DEBUG: LLM returned empty input for tool '{selected_tool}'. Using original user_input.")
                    tool_input = user_input
        except json.JSONDecodeError:
            # Fallback parsing
            if "vector_search_tool" in tool_response:
                selected_tool = "vector_search_tool"
                tool_input = user_input
            elif "calculator_tool" in tool_response:
                selected_tool = "calculator_tool"
                tool_input = user_input
            elif "web_search_tool" in tool_response:
                selected_tool = "web_search_tool"
                tool_input = user_input
            elif "document_analysis_tool" in tool_response:
                selected_tool = "document_analysis_tool"
                tool_input = user_input
            elif "hybrid_search_tool" in tool_response:
                selected_tool = "hybrid_search_tool"
                tool_input = user_input
            else:
                selected_tool = "none"
                tool_input = user_input
        
        # Additional fallback logic for MongoDB-related queries
        mongodb_keywords = ["mongodb", "atlas", "vector", "database", "search", "acquisition", "revenue", "earnings", "financial"]
        if selected_tool == "web_search_tool" and any(keyword in user_input.lower() for keyword in mongodb_keywords):
            print("Overriding web_search_tool with vector_search_tool for MongoDB-related query")
            selected_tool = "vector_search_tool"
        
        # Fallback logic for general knowledge questions
        general_knowledge_keywords = ["country", "plays", "football", "soccer", "team", "club", "sport", "movie", "actor", "city", "capital", "population", "president", "prime minister", "cook", "recipe", "weather", "time", "explain", "how to", "what is", "who is", "where is", "when is", "why is"]
        if selected_tool == "none" and any(keyword in user_input.lower() for keyword in general_knowledge_keywords):
            print("Overriding 'none' with web_search_tool for general knowledge query")
            selected_tool = "web_search_tool"
        
        return selected_tool, tool_input
    
    except Exception as e:
        print(f"Error in tool selection: {e}")
        # Fallback logic based on keywords
        mongodb_keywords = ["mongodb", "atlas", "vector", "database", "search", "acquisition", "revenue", "earnings", "financial"]
        general_knowledge_keywords = ["country", "plays", "football", "soccer", "team", "club", "sport", "movie", "actor", "city", "capital", "population", "president", "prime minister", "cook", "recipe", "weather", "time", "explain", "how to", "what is", "who is", "where is", "when is", "why is"]
        
        if any(keyword in user_input.lower() for keyword in mongodb_keywords):
            return "vector_search_tool", user_input
        elif any(keyword in user_input.lower() for keyword in general_knowledge_keywords):
            return "web_search_tool", user_input
        else:
            return "none", user_input

def generate_response(session_id: str, user_input: str) -> str:
    """
    Main function to generate agent response using tools and memory
    """
    # Store user input
    store_chat_message(session_id, "user", user_input)
    
    # Retrieve session history
    session_history = retrieve_session_history(session_id)
    
    # Get session summary for context
    session_summary = get_session_summary(session_id)
    
    # Get user preferences
    user_preferences = get_user_preferences(session_id)
    
    # Select appropriate tool
    tool, tool_input = tool_selector(user_input, session_history)
    print(f"Tool selected: {tool}")
    
    # Prepare LLM input with conversation history
    llm_input = []
    
    # Add session summary if available
    if session_summary and session_summary != "No previous conversation history.":
        llm_input.append({
            "role": "system",
            "content": f"Previous conversation summary: {session_summary}"
        })
    
    # Add conversation history (cleaned)
    cleaned_history = clean_session_history(session_history)
    llm_input.extend(cleaned_history)
    
    # Add current user message
    llm_input.append({"role": "user", "content": user_input})
    
    # Process based on selected tool
    if tool == "vector_search_tool":
        context = vector_search_tool(tool_input)
        response = process_vector_search_response(llm_input, context, user_input)
    
    elif tool == "calculator_tool":
        response = calculator_tool(tool_input)
    
    elif tool == "web_search_tool":
        search_results = web_search_tool(tool_input)
        response = process_web_search_response(llm_input, search_results, user_input)
    
    elif tool == "document_analysis_tool":
        # For document analysis, we need the user to provide a document
        response = "Please provide a document to analyze. You can paste the text content here."
    
    elif tool == "hybrid_search_tool":
        context = hybrid_search_tool(tool_input)
        response = process_hybrid_search_response(llm_input, context, user_input)
    
    else:
        # General conversation
        system_message = "You are a helpful AI assistant. Respond to the user's prompt based on the conversation history."
        response = get_llm_response(llm_input, system_message)
    
    # Store the response
    store_chat_message(session_id, "assistant", response)
    
    return response

def process_vector_search_response(messages: list, context: list, user_input: str) -> str:
    """
    Process vector search results and generate response
    """
    if not context:
        return "I couldn't find relevant information in the knowledge base to answer your question."
    
    # Format context for the LLM
    context_text = "\n\n".join([
        f"Document {i+1}:\n{doc['text']}" 
        for i, doc in enumerate(context)
    ])
    
    print(f"DEBUG: Retrieved {len(context)} documents for vector search")
    print(f"DEBUG: Context length: {len(context_text)} characters")
    
    system_message = f"""
Answer the user's question based on the retrieved context and conversation history.

Instructions:
1. First, understand what specific information the user is requesting
2. Then, locate the most relevant details in the context provided
3. Finally, provide a clear, accurate response that directly addresses the question

If the current question builds on previous exchanges, maintain continuity in your answer.
Use the provided context to give helpful, informative responses. If the context contains relevant information, synthesize it to answer the question. Only say 'I DON'T KNOW' if the context truly contains no relevant information at all.

Context:
{context_text}
"""
    
    return get_llm_response(messages, system_message)

def process_web_search_response(messages: list, search_results: str, user_input: str) -> str:
    """
    Process web search results and generate response
    """
    system_message = f"""
Answer the user's question based on the web search results and conversation history.

Web Search Results:
{search_results}

Provide a helpful response based on the search results. If the search results don't contain relevant information, let the user know.
"""
    
    return get_llm_response(messages, system_message)

def process_hybrid_search_response(messages: list, context: list, user_input: str) -> str:
    """
    Process hybrid search results and generate response
    """
    if not context:
        return "I couldn't find relevant information to answer your question."
    
    # Separate vector and text search results
    vector_results = [doc for doc in context if doc.get("search_type") == "vector"]
    text_results = [doc for doc in context if doc.get("search_type") == "text"]
    
    context_text = ""
    if vector_results:
        context_text += "Semantic Search Results:\n"
        context_text += "\n\n".join([
            f"Document {i+1}:\n{doc['text']}" 
            for i, doc in enumerate(vector_results)
        ])
    
    if text_results:
        context_text += "\n\nKeyword Search Results:\n"
        context_text += "\n\n".join([
            f"Document {i+1}:\n{doc['text']}" 
            for i, doc in enumerate(text_results)
        ])
    
    system_message = f"""
Answer the user's question based on the comprehensive search results (both semantic and keyword search).

Instructions:
1. Synthesize information from both semantic and keyword search results
2. Provide a comprehensive answer that addresses the user's question
3. If there are conflicting information, mention the different perspectives
4. Use the provided context to give helpful, informative responses. Synthesize the information to answer the question comprehensively.

Search Results:
{context_text}
"""
    
    return get_llm_response(messages, system_message)

def get_llm_response(messages: list, system_message: str) -> str:
    """
    Get response from OpenAI LLM
    """
    # Add system message
    system_msg = {"role": "system", "content": system_message}
    
    # Check if there's already a system message
    if any(msg.get("role") == "system" for msg in messages):
        messages.append(system_msg)
    else:
        messages = [system_msg] + messages
    
    try:
        response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.7
    )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating response: {str(e)}"

def analyze_conversation_context(session_id: str) -> dict:
    """
    Analyze the conversation context to provide insights
    """
    try:
        session_history = retrieve_session_history(session_id)
        if not session_history:
            return {"status": "no_history"}
        
        # Analyze conversation patterns
        user_messages = [msg for msg in session_history if msg["role"] == "user"]
        assistant_messages = [msg for msg in session_history if msg["role"] == "assistant"]
        
        return {
            "total_messages": len(session_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "conversation_topics": extract_topics(session_history),
            "user_question_patterns": analyze_question_patterns(user_messages)
        }
    
    except Exception as e:
        return {"error": str(e)}

def extract_topics(messages: list) -> list:
    """
    Extract main topics from conversation
    """
    try:
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in messages
        ])
        
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Extract the main topics discussed in this conversation. Return as a simple list."
                },
                {
                    "role": "user",
                    "content": f"Conversation:\n{conversation_text}"
                }
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.split('\n')
    
    except Exception as e:
        return ["Unable to extract topics"]

def analyze_question_patterns(user_messages: list) -> dict:
    """
    Analyze patterns in user questions
    """
    if not user_messages:
        return {}
    
    question_types = []
    for msg in user_messages:
        content = msg["content"].lower()
        if "?" in content:
            if "what" in content:
                question_types.append("factual")
            elif "how" in content:
                question_types.append("procedural")
            elif "why" in content:
                question_types.append("explanatory")
            else:
                question_types.append("general")
    
    return {
        "total_questions": len(question_types),
        "question_types": question_types,
        "most_common_type": max(set(question_types), key=question_types.count) if question_types else "none"
    }

