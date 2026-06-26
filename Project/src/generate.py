import os
from google import genai
from retrieve import search_templates

# Initialize the Gemini Client
client = genai.Client()

def answer_query(query: str):
    """
    1. Searches the local vector database for relevant code chunks.
    2. Injects the chunks into a prompt.
    3. Uses Gemini 2.5 Flash to generate a final answer based ONLY on the chunks.
    """
    print(f"Processing query: '{query}'...\n")
    
    # 1. Retrieve the top 2 most relevant chunks from Phase 4
    results = search_templates(query, top_k=2)
    
    # If no results are found (e.g., empty database), handle gracefully
    if not results["documents"][0]:
        print("No relevant templates found in the database.")
        return
        
    # 2. Extract the text chunks and format them into a single string
    retrieved_texts = results["documents"][0]
    retrieved_metadata = results["metadatas"][0]
    
    context_blocks = []
    for idx, text in enumerate(retrieved_texts):
        filename = retrieved_metadata[idx]['filename']
        context_blocks.append(f"--- From file: {filename} ---\n{text}\n")
        
    context_string = "\n".join(context_blocks)
    
    # 3. Construct the strict System Prompt
    prompt = f"""
You are an expert competitive programming assistant. 
Use ONLY the following C++ reference templates to answer the user's request. 
If the templates do not contain the answer, politely state that you do not have the reference material for it.
When writing out code, provide brief explanations of how it works based on the template.

--- Reference Templates ---
{context_string}

--- User Request ---
{query}
"""

    print("\nSynthesizing answer with Gemini 2.5 Flash...\n")
    print("=" * 60)
    
    # 4. Generate the final answer
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    # 5. Save the result to a text file
    output_path = "output.txt"
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(response.text)

    print(f"Answer written to {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    # Test the full pipeline!
    user_question = "i have weighted graph i want to find shortest path and do bfs both in same graph in single code bfs in different function and dijkstra in different function for bfs part we will ingnore the weights?"
    answer_query(user_question)