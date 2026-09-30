import os
import chromadb
from pypdf import PdfReader

def ingest_documents(docs_folder="./docs", db_path="./chroma_db"):
    # 1. Initialize ChromaDB in local persistent storage mode
    client = chromadb.PersistentClient(path=db_path)
    
    # ChromaDB automatically uses its built-in free open-source 
    # embedding model ('all-MiniLM-L6-v2') if none is specified.
    collection = client.get_or_create_collection(name="lauki_docs")
    
    id_counter = 0
    if not os.path.exists(docs_folder):
        print(f"❌ Error: Folder '{docs_folder}' not found. Please create it and add your PDFs.")
        return

    # 2. Scan the docs folder for your lauki PDF files
    pdf_files = [f for f in os.listdir(docs_folder) if f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"⚠️ Warning: No PDF files found in '{docs_folder}'. Make sure your files are placed there.")
        return

    print(f"📚 Found {len(pdf_files)} PDF files. Starting local ingestion process...")

    for filename in pdf_files:
        file_path = os.path.join(docs_folder, filename)
        print(f"⚙️ Processing: {filename}...")
        
        try:
            reader = PdfReader(file_path)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if not text or not text.strip():
                    continue
                
                # Split text by double newlines into logical chunks
                chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
                
                for chunk in chunks:
                    collection.add(
                        documents=[chunk],
                        metadatas=[{"source": filename, "page": page_num + 1}],
                        ids=[f"doc_{id_counter}"]
                    )
                    id_counter += 1
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
                    
    print(f"\n✅ Successfully indexed {id_counter} document chunks locally into '{db_path}'!")

if __name__ == "__main__":
    ingest_documents()
