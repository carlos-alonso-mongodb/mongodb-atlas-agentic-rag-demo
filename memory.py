from config import memory_collection, openai_client
from datetime import datetime
from typing import List, Dict, Optional
import json

def store_chat_message(session_id: str, role: str, content: str, metadata: Optional[Dict] = None) -> None:
    """
    Store a chat message in the memory collection
    """
    message = {
        "session_id": session_id,
        "role": role,
        "content": content,
        "timestamp": datetime.now(),
        "metadata": metadata or {}
    }
    
    try:
        memory_collection.insert_one(message)
    except Exception as e:
        print(f"Error storing chat message: {e}")

def retrieve_session_history(session_id: str, limit: Optional[int] = None) -> List[Dict]:
    """
    Retrieve chat history for a specific session
    """
    try:
        query = {"session_id": session_id}
        cursor = memory_collection.find(query).sort("timestamp", 1)
        
        if limit:
            cursor = cursor.limit(limit)
        
        messages = []
        for msg in cursor:
            messages.append({
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg["timestamp"],
                "metadata": msg.get("metadata", {})
            })
        
        return messages
    
    except Exception as e:
        print(f"Error retrieving session history: {e}")
        return []

def get_session_summary(session_id: str) -> str:
    """
    Generate a summary of the session using OpenAI
    """
    try:
        messages = retrieve_session_history(session_id)
        if not messages:
            return "No previous conversation history."
        
        # Create a conversation summary
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in messages[-10:]  # Last 10 messages
        ])
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the key points and context from this conversation in 2-3 sentences."
                },
                {
                    "role": "user",
                    "content": f"Conversation:\n{conversation_text}"
                }
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error generating session summary: {e}")
        return "Unable to generate session summary."

def store_important_facts(session_id: str, facts: List[str]) -> None:
    """
    Store important facts learned during the session
    """
    try:
        for fact in facts:
            memory_collection.insert_one({
                "session_id": session_id,
                "type": "important_fact",
                "content": fact,
                "timestamp": datetime.now()
            })
    except Exception as e:
        print(f"Error storing important facts: {e}")

def retrieve_important_facts(session_id: str) -> List[str]:
    """
    Retrieve important facts from the session
    """
    try:
        cursor = memory_collection.find({
            "session_id": session_id,
            "type": "important_fact"
        }).sort("timestamp", 1)
        
        return [doc["content"] for doc in cursor]
    
    except Exception as e:
        print(f"Error retrieving important facts: {e}")
        return []

def clear_session_memory(session_id: str) -> bool:
    """
    Clear all memory for a specific session
    """
    try:
        result = memory_collection.delete_many({"session_id": session_id})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Error clearing session memory: {e}")
        return False

def get_user_preferences(session_id: str) -> Dict:
    """
    Extract and store user preferences from conversation
    """
    try:
        messages = retrieve_session_history(session_id)
        if not messages:
            return {}
        
        # Analyze conversation for preferences
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in messages
        ])
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Extract user preferences and interests from this conversation. Return as JSON with categories like 'topics_of_interest', 'communication_style', 'preferred_detail_level', etc."
                },
                {
                    "role": "user",
                    "content": f"Conversation:\n{conversation_text}"
                }
            ],
            temperature=0.3
        )
        
        try:
            preferences = json.loads(response.choices[0].message.content)
            return preferences
        except json.JSONDecodeError:
            return {"raw_preferences": response.choices[0].message.content}
    
    except Exception as e:
        print(f"Error extracting user preferences: {e}")
        return {}

def store_long_term_memory(session_id: str, memory_type: str, content: str) -> None:
    """
    Store long-term memory that persists across sessions
    """
    try:
        memory_collection.insert_one({
            "session_id": session_id,
            "type": f"long_term_{memory_type}",
            "content": content,
            "timestamp": datetime.now(),
            "persistent": True
        })
    except Exception as e:
        print(f"Error storing long-term memory: {e}")

def retrieve_long_term_memory(memory_type: str, limit: int = 10) -> List[Dict]:
    """
    Retrieve long-term memory of a specific type
    """
    try:
        cursor = memory_collection.find({
            "type": f"long_term_{memory_type}",
            "persistent": True
        }).sort("timestamp", -1).limit(limit)
        
        return list(cursor)
    
    except Exception as e:
        print(f"Error retrieving long-term memory: {e}")
        return []

