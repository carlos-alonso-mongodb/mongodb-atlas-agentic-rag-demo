from config import vector_collection, openai_client, EMBEDDING_MODEL, EMBEDDING_DIMENSIONS
from ingest_data import get_embedding
import json
import re
import math

def vector_search_tool(user_input: str, limit: int = 5) -> list:
    """
    Perform vector search to retrieve relevant documents
    """
    print(f"DEBUG: vector_search_tool called with input: '{user_input}'")
    
    # Validate input
    if not user_input or not user_input.strip():
        print("ERROR: vector_search_tool received empty or invalid input")
        return []
    
    try:
        query_embedding = get_embedding(user_input)
        if not query_embedding:
            print("ERROR: Failed to generate embedding for vector search")
            return []
        
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "exact": True,
                    "limit": limit
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "metadata": 1
                }
            }
        ]
        
        results = vector_collection.aggregate(pipeline)
        return list(results)
    
    except Exception as e:
        print(f"Error in vector search: {e}")
        return []

def calculator_tool(user_input: str) -> str:
    """
    Safe calculator tool that evaluates mathematical expressions
    """
    try:
        # Clean the input to only allow safe mathematical operations
        safe_chars = set('0123456789+-*/.() ')
        if not all(c in safe_chars for c in user_input):
            return "Error: Invalid characters in mathematical expression"
        
        # Remove any potential dangerous functions
        if any(func in user_input.lower() for func in ['import', 'exec', 'eval', '__']):
            return "Error: Potentially unsafe expression"
        
        result = eval(user_input)
        return str(result)
    
    except Exception as e:
        return f"Error: {str(e)}"

def web_search_tool(query: str) -> str:
    """
    Simulated web search tool (placeholder for actual web search implementation)
    """
    # This is a placeholder - in a real implementation, you would integrate
    # with a web search API like Google Search API, Bing API, etc.
    return f"""Web search results for: {query}

Note: This is a demo environment. In a production system, this would integrate with a real web search API like Google Search API or Bing API to provide current, real-time information.

For MongoDB-related questions, please try asking about:
- MongoDB Atlas features
- Vector search capabilities  
- Database performance
- Recent acquisitions or financial information

The knowledge base contains MongoDB earnings reports and technical documentation that can provide detailed answers to these topics."""

def document_analysis_tool(document_text: str) -> dict:
    """
    Analyze a document and extract key information
    """
    try:
        # Use OpenAI to analyze the document
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the following document and extract key information including: main topics, key facts, important numbers, and summary."
                },
                {
                    "role": "user",
                    "content": f"Analyze this document:\n\n{document_text}"
                }
            ],
            temperature=0.3
        )
        
        analysis = response.choices[0].message.content
        
        return {
            "analysis": analysis,
            "word_count": len(document_text.split()),
            "char_count": len(document_text)
        }
    
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def hybrid_search_tool(user_input: str, limit: int = 5) -> list:
    """
    Perform hybrid search combining vector search with text search
    """
    try:
        # Vector search
        vector_results = vector_search_tool(user_input, limit)
        
        # Text search (using MongoDB's text search capabilities)
        text_results = vector_collection.find(
            {"$text": {"$search": user_input}},
            {"text": 1, "metadata": 1, "_id": 0}
        ).limit(limit)
        
        # Combine and deduplicate results
        all_results = []
        seen_texts = set()
        
        # Add vector search results
        for result in vector_results:
            if result["text"] not in seen_texts:
                result["search_type"] = "vector"
                all_results.append(result)
                seen_texts.add(result["text"])
        
        # Add text search results
        for result in text_results:
            if result["text"] not in seen_texts:
                result["search_type"] = "text"
                all_results.append(result)
                seen_texts.add(result["text"])
        
        return all_results[:limit]
    
    except Exception as e:
        print(f"Error in hybrid search: {e}")
        return vector_search_tool(user_input, limit)  # Fallback to vector search

def get_available_tools() -> dict:
    """
    Return information about available tools
    """
    return {
        "vector_search_tool": {
            "description": "Search for semantically similar documents using vector embeddings",
            "parameters": ["query", "limit (optional)"]
        },
        "calculator_tool": {
            "description": "Perform mathematical calculations",
            "parameters": ["mathematical_expression"]
        },
        "web_search_tool": {
            "description": "Search the web for current information",
            "parameters": ["search_query"]
        },
        "document_analysis_tool": {
            "description": "Analyze and extract key information from documents",
            "parameters": ["document_text"]
        },
        "hybrid_search_tool": {
            "description": "Combine vector and text search for comprehensive results",
            "parameters": ["query", "limit (optional)"]
        }
    }

