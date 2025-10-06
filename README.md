# MongoDB Atlas Agentic RAG Demo

A comprehensive demonstration of building AI agents with MongoDB Atlas, featuring vector search, memory management, and multi-tool capabilities using OpenAI for both reasoning and embeddings.

## 🚀 Features

- **Agentic RAG**: Intelligent retrieval-augmented generation with dynamic tool selection
- **Vector Search**: Semantic search using OpenAI embeddings and MongoDB Atlas Vector Search
- **Memory System**: Short-term and long-term memory for conversational context
- **Multi-Tool Support**: Calculator, web search, document analysis, and hybrid search
- **Interactive Interface**: Both command-line and Streamlit web interface
- **Session Management**: Persistent conversation history and user preferences

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  AI Agent      │───▶│   Response      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Tool Selection │
                    └─────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            ┌─────────────┐    ┌─────────────┐
            │ Vector      │    │ Calculator  │
            │ Search      │    │ Tool        │
            └─────────────┘    └─────────────┘
                    │
                    ▼
            ┌─────────────────┐
            │ MongoDB Atlas   │
            │ Vector Search   │
            └─────────────────┘
```

## 📋 Prerequisites

- MongoDB Atlas cluster (version 6.0.11+)
- OpenAI API key
- Python 3.8+

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd agentic-demo
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` with your credentials:
   ```
   MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/"
   OPENAI_API_KEY="<your-openai-api-key>"
   DATABASE_NAME="ai_agent_db"
   EMBEDDINGS_COLLECTION="embeddings"
   MEMORY_COLLECTION="chat_history"
   ```

4. **Set up MongoDB Atlas:**
   - Create a cluster on MongoDB Atlas
   - Add your IP address to the access list
   - Create a database user with read/write permissions

## 🚀 Usage

### Command Line Interface

```bash
python main.py
```

### Web Interface (Streamlit)

```bash
streamlit run streamlit_app.py
```

## 🧩 Components

### 1. Configuration (`config.py`)
- MongoDB connection setup
- OpenAI client configuration
- Environment variable management

### 2. Data Ingestion (`ingest_data.py`)
- PDF document processing
- OpenAI embedding generation
- Vector search index creation
- Custom document ingestion

### 3. Tools (`tools.py`)
- **Vector Search Tool**: Semantic document retrieval
- **Calculator Tool**: Mathematical operations
- **Web Search Tool**: Real-time information retrieval
- **Document Analysis Tool**: Text analysis and insights
- **Hybrid Search Tool**: Combined vector and text search

### 4. Memory System (`memory.py`)
- Session-based conversation storage
- User preference extraction
- Long-term memory management
- Conversation analytics

### 5. Planning Logic (`planning.py`)
- Intelligent tool selection
- Context-aware response generation
- Conversation flow management
- Multi-tool orchestration

## 🔧 Available Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `vector_search_tool` | Semantic document search | Knowledge base queries |
| `calculator_tool` | Mathematical calculations | Numerical operations |
| `web_search_tool` | Web information retrieval | Current events, real-time data |
| `document_analysis_tool` | Text analysis and insights | Document processing |
| `hybrid_search_tool` | Combined search methods | Comprehensive information retrieval |

## 📊 Memory System

### Short-term Memory
- Session-based conversation history
- Real-time context management
- User interaction tracking

### Long-term Memory
- Cross-session user preferences
- Important fact storage
- Conversation pattern analysis

## 🎯 Example Queries

```
"What was MongoDB's latest acquisition?"
"Calculate 15 * 23 + 45"
"What are the key features of MongoDB Atlas?"
"Search for information about vector databases"
"What is the revenue growth mentioned in the report?"
```

## 🔍 Vector Search Configuration

The demo uses OpenAI's `text-embedding-3-large` model with 3072 dimensions:

```python
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSIONS = 3072
```

## 📈 Analytics Features

- Conversation topic extraction
- Question pattern analysis
- User preference learning
- Session statistics
- Tool usage tracking

## 🚀 Advanced Features

### Hybrid Search
Combines vector search with MongoDB's text search for comprehensive results.

### Memory Management
- Automatic session management
- User preference learning
- Cross-session context retention

### Tool Orchestration
Intelligent tool selection based on:
- User query analysis
- Conversation context
- Available data sources

## 🔧 Customization

### Adding New Tools
1. Define tool function in `tools.py`
2. Add tool description to `get_available_tools()`
3. Update tool selection logic in `planning.py`

### Custom Data Sources
1. Modify `ingest_data.py` for your data format
2. Update embedding generation as needed
3. Adjust vector search parameters

### Memory Customization
1. Extend `memory.py` with custom memory types
2. Modify conversation analysis logic
3. Add custom user preference extraction

## 📚 Documentation References

- [MongoDB Atlas Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/)
- [MongoDB Atlas Search](https://www.mongodb.com/docs/atlas/atlas-search/)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review the code comments
3. Open an issue on GitHub
4. Contact the development team

## 🎉 Acknowledgments

- MongoDB Atlas for vector search capabilities
- OpenAI for embedding and language models
- Streamlit for the web interface
- The open-source community for various libraries

