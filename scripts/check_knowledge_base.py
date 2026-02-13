"""
Check and restore knowledge base files
"""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

print("🔍 Checking knowledge base status...\n")

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=os.environ.get("AZURE_AI_PROJECT_ENDPOINT") or os.environ["AZURE_AI_ENDPOINT"], 
        credential=credential
    ) as project_client,
):
    print("✅ Connected to Azure AI Foundry project")
    
    # Check for existing vector stores
    print("\n📚 Checking Vector Stores...")
    try:
        # Try to access inference client which has vector store operations
        with project_client.inference() as inference_client:
            # List vector stores
            stores = list(inference_client.vector_stores.list())
            
            if stores:
                print(f"✅ Found {len(stores)} vector store(s):")
                for store in stores:
                    print(f"\n   Store: {store.name} (ID: {store.id})")
                    print(f"   Status: {store.status}")
                    print(f"   Files: {store.file_counts.get('total', 0) if hasattr(store, 'file_counts') else 'unknown'}")
                    
                    # List files in this store
                    try:
                        files = list(inference_client.vector_stores.files.list(vector_store_id=store.id))
                        if files:
                            print(f"   📄 Files in store:")
                            for file in files[:10]:  # Show first 10
                                print(f"      - {file.id}")
                        else:
                            print(f"   ⚠️  No files in this store!")
                    except Exception as e:
                        print(f"   ⚠️  Could not list files: {e}")
            else:
                print("❌ No vector stores found!")
                print("   Knowledge base needs to be uploaded")
                
    except AttributeError:
        print("⚠️  Vector store access not available through inference client")
        print("   Trying alternative method...")
        
        # Try direct file upload operation
        try:
            # Check if files endpoint exists
            print("\n📂 Checking Files...")
            files = list(project_client.agents.list_files())
            if files:
                print(f"✅ Found {len(files)} file(s) in project:")
                for f in files[:10]:
                    print(f"   - {f.filename if hasattr(f, 'filename') else f.id}")
            else:
                print("❌ No files found in project")
        except Exception as e:
            print(f"⚠️  Could not access files: {e}")
    
    except Exception as e:
        print(f"❌ Error checking vector stores: {e}")

print("\n" + "="*50)
print("\n💡 Next Step:")
print("   If no files found, run: python scripts/upload_knowledge_base.py")
print("   This will re-upload the 7 knowledge base markdown files")
