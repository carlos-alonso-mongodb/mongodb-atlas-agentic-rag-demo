from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ai_agent_db")
EMBEDDINGS_COLLECTION = os.getenv("EMBEDDINGS_COLLECTION", "embeddings")
MEMORY_COLLECTION = os.getenv("MEMORY_COLLECTION", "chat_history")

# MongoDB cluster configuration
mongo_client = MongoClient(MONGODB_URI)
agent_db = mongo_client[DATABASE_NAME]
vector_collection = agent_db[EMBEDDINGS_COLLECTION]
memory_collection = agent_db[MEMORY_COLLECTION]

# OpenAI client configuration
openai_client = OpenAI(api_key=OPENAI_API_KEY)
OPENAI_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSIONS = 3072  # For text-embedding-3-large

