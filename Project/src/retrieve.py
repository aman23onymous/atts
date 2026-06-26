import os
import chromadb
from google import genai

# 1. Initialize the clients (just like in Phase 3)
client = genai.Client()
db = chromadb.PersistentClient(path="./chroma_data")

# Connect to the existing database table
collection = db.get_collection(name="algo_templates")

def search_templates(query: str, top_k: int = 2):
    """
    Takes a natural language query, embeds it, and searches ChromaDB 
    for the most relevant C++ code chunks.
    """
    print(f"\nSearching for: '{query}'...")
    
    # 2. Convert the user's question into a math vector
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )
    query_vector = response.embeddings[0].values
    
    # 3. Perform the mathematical similarity search
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    
    # 4. Print the formatted results
    print("\n--- Top Matches Found ---")
    
    # ChromaDB returns lists of lists, so we access the first item [0]
    for i in range(len(results["documents"][0])):
        text = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i] # Lower distance = better match
        
        print(f"\nMatch {i+1} | Source: {metadata['filename']} | Distance: {distance:.4f}")
        print("-" * 40)
        # Print a preview of the actual code chunk (first 200 characters)
        print(text[:200] + "...\n")
        
    return results

if __name__ == "__main__":
    # Test queries
    # Change these questions to match the code you actually put in your templates folder
    test_query_1 = "How do I implement a bfs and dfs?"
    search_templates(test_query_1, top_k=3)
    
    # test_query_2 = "Show me the lazy propagation update function for a segment tree."
    # search_templates(test_query_2, top_k=2)