import os
import chromadb
from groq import Groq
from dotenv import load_dotenv

# Automatically look for the .env file and load its variables into system memory
load_dotenv()

def test_cloud_rag(user_query):
    # 1. Connect to your local indexed database
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="lauki_docs")
    
    # 2. Extract matching documentation context chunks
    print(f"\n🔍 Searching local vector store for: '{user_query}'...")
    results = collection.query(query_texts=[user_query], n_results=2)
    
    retrieved_docs = results.get('documents', [[]])
    context = "\n---\n".join([doc for sublist in retrieved_docs for doc in sublist])
    
    if not context.strip():
        print("⚠️ Warning: No matching document context found inside ChromaDB.")
        return

    print("📄 Found matching documentation context layout!")
    
    # 3. Instantiate the Groq API Client 
    groq_client = Groq()
    
    system_prompt = (
        "You are a helpful, spoken voice agent answering questions based ONLY on the provided context. "
        "Keep your response strictly to 1 or 2 sentences max so it sounds natural when read aloud. "
        f"Context from documents:\n{context}"
    )
    
    # 4. Route payload to Groq's cloud endpoint
    print("🚀 Sending payload to Groq Cloud API...")
    try:
        completion = groq_client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )
        print("\n🤖 [Groq API Response]:")
        # FIX: Added [0] index to read the list object correctly
        print(completion.choices[0].message.content)
        
    except Exception as e:
        print(f"\n❌ Groq API Error: {e}")
        print("Please verify that your GROQ_API_KEY is spelled correctly inside your .env file.")

if __name__ == "__main__":
    test_cloud_rag("What are the available billing plans?")
