from pathlib import Path

import chromadb
from google import genai

from ingest import chunk_code, read_cpp_templates

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CHROMA_DIR = PROJECT_ROOT / "chroma_data"

# 1. Initialize the AI Client
# The SDK automatically looks for the GEMINI_API_KEY environment variable
client = genai.Client()

# 2. Initialize ChromaDB locally
# This creates a hidden folder called 'chroma_data' in your project
db = chromadb.PersistentClient(path=str(CHROMA_DIR))

# Create a "table" (called a collection in vector databases)
collection = db.get_or_create_collection(name="algo_templates")

def build_vector_database():
    print("--- Starting Phase 3: Building Vector Database ---")
    
    # 3. Run the ingestion logic from Phase 2
    raw_docs = read_cpp_templates(str(TEMPLATES_DIR))
    chunks = chunk_code(raw_docs, max_chunk_size=1200, overlap=150)
    
    print(f"Ready to embed and store {len(chunks)} chunks...\n")

    # 4. The Embedding & Storage Loop
    for idx, chunk in enumerate(chunks):
        text = chunk["content"]
        metadata = chunk["metadata"]
        
        # Create a unique ID for the database (e.g., "dijkstra.cpp_chunk_0")
        chunk_index = metadata.get("chunk_id", idx)
        chunk_id = f"{metadata['filename']}_chunk_{chunk_index}"
        
        # Call the external API to convert text to a mathematical vector
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        vector_array = response.embeddings[0].values
        
        # Save everything permanently to ChromaDB
        collection.upsert(
            documents=[text],
            metadatas=[metadata],
            ids=[chunk_id],
            embeddings=[vector_array]
        )
        print(f"Successfully stored: {chunk_id}")
        
    print(f"\nDatabase build complete! Vectors are saved in {CHROMA_DIR}")

if __name__ == "__main__":
    # If running from the root folder, make sure the path to templates is correct
    build_vector_database()