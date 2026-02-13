"""
Upload Knowledge Base Files to Azure AI Foundry
Note: Files should be uploaded manually via Azure AI Foundry UI for now
"""

import os
from pathlib import Path

# Configuration
KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "knowledge-base"

def list_knowledge_files():
    """List all knowledge base markdown files"""
    
    print("📚 Knowledge Base Files")
    print("="*60)
    print(f"\nDirectory: {KNOWLEDGE_BASE_DIR}\n")
    
    # Find all markdown files
    md_files = sorted(KNOWLEDGE_BASE_DIR.glob("*.md"))
    
    if not md_files:
        print(f"❌ No markdown files found in {KNOWLEDGE_BASE_DIR}")
        return
    
    print(f"Found {len(md_files)} files:\n")
    for i, file_path in enumerate(md_files, 1):
        file_size = file_path.stat().st_size
        print(f"{i}. {file_path.name}")
        print(f"   Size: {file_size:,} bytes")
        print(f"   Path: {file_path}\n")
    
    print("="*60)
    print("\n📋 MANUAL UPLOAD STEPS:")
    print("="*60)
    print("\n1. Go to Azure AI Foundry: https://ai.azure.com")
    print("2. Navigate to: Your Project → Build → Vector Stores")
    print("3. Create or select vector store: 'knowledge-base'")
    print("4. Click 'Upload files'")
    print("5. Upload all 7 files listed above")
    print("\nOR manually upload via UI:")
    print("   Project → Build → Tools → File Search → Configure")
    print("\n✨ The files are ready at:")
    print(f"   {KNOWLEDGE_BASE_DIR}")

if __name__ == "__main__":
    list_knowledge_files()
