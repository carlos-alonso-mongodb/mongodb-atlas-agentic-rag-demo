from config import vector_collection, openai_client, EMBEDDING_MODEL, EMBEDDING_DIMENSIONS
from pymongo.operations import SearchIndexModel
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
import json

def get_embedding(text: str, input_type: str = "document") -> list:
    """
    Generate embeddings using OpenAI's text-embedding-3-large model
    """
    # Validate input
    if not text or not isinstance(text, str) or not text.strip():
        print(f"Error: Invalid input for embedding generation. Input: '{text}'")
        return None
    
    # Ensure text is not too long (OpenAI has limits)
    if len(text) > 8000:  # Conservative limit
        text = text[:8000]
        print(f"Warning: Text truncated to 8000 characters for embedding generation")
    
    try:
        response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text.strip(),
            dimensions=EMBEDDING_DIMENSIONS
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def ingest_sample_data():
    """
    Ingest sample data from MongoDB earnings report PDF
    """
    # Chunk PDF data
    print("Loading PDF data...")
    loader = PyPDFLoader("https://investors.mongodb.com/node/13176/pdf")
    data = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, 
        chunk_overlap=20
    )
    documents = text_splitter.split_documents(data)
    print(f"Successfully split PDF into {len(documents)} chunks.")
    
    # Ingest chunked documents into collection
    print("Generating embeddings and ingesting documents...")
    docs_to_insert = []
    
    for i, doc in enumerate(documents):
        print(f"Processing document {i+1}/{len(documents)}")
        embedding = get_embedding(doc.page_content)
        
        if embedding:
            docs_to_insert.append({
                "text": doc.page_content,
                "embedding": embedding,
                "metadata": {
                    "source": "mongodb_earnings_report",
                    "chunk_id": i,
                    "page": doc.metadata.get("page", 0) if hasattr(doc, 'metadata') else 0
                }
            })
    
    if docs_to_insert:
        result = vector_collection.insert_many(docs_to_insert)
        print(f"Inserted {len(result.inserted_ids)} documents into the collection.")
    else:
        print("No documents were inserted. Check embedding generation process.")
        return False
    
    return True

def create_vector_search_index():
    """
    Create a vector search index on the embeddings collection
    """
    index_name = "vector_index"
    
    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "numDimensions": EMBEDDING_DIMENSIONS,
                    "path": "embedding",
                    "similarity": "cosine"
                }
            ]
        },
        name=index_name,
        type="vectorSearch"
    )
    
    try:
        vector_collection.create_search_index(model=search_index_model)
        print(f"Search index '{index_name}' creation initiated.")
    except Exception as e:
        print(f"Error creating search index: {e}")
        return False
    
    # Wait for index to be ready
    print("Polling to check if the index is ready. This may take up to a minute.")
    predicate = lambda index: index.get("queryable") is True
    
    while True:
        indices = list(vector_collection.list_search_indexes(index_name))
        if len(indices) and predicate(indices[0]):
            break
        time.sleep(5)
    
    print(f"{index_name} is ready for querying.")
    return True

def ingest_data():
    """
    Main function to ingest data and create search index
    """
    print("Starting data ingestion process...")
    
    # Check if data already exists
    existing_count = vector_collection.count_documents({})
    if existing_count > 0:
        print(f"Found {existing_count} existing documents. Skipping ingestion.")
        return True
    
    # Ingest sample data
    if not ingest_sample_data():
        return False
    
    # Create vector search index
    if not create_vector_search_index():
        return False
    
    print("Data ingestion completed successfully!")
    return True

def add_custom_documents(documents: list):
    """
    Add custom documents to the collection
    """
    docs_to_insert = []
    
    for i, doc_text in enumerate(documents):
        embedding = get_embedding(doc_text)
        
        if embedding:
            docs_to_insert.append({
                "text": doc_text,
                "embedding": embedding,
                "metadata": {
                    "source": "custom_document",
                    "chunk_id": i
                }
            })
    
    if docs_to_insert:
        result = vector_collection.insert_many(docs_to_insert)
        print(f"Inserted {len(result.inserted_ids)} custom documents.")
        return True
    
    return False

