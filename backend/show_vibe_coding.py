"""Show full Vibe Coding content from Cosmos DB"""
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = CosmosClient(os.getenv('COSMOS_ENDPOINT'), credential=DefaultAzureCredential())
container = client.get_database_client(os.getenv('COSMOS_DATABASE')).get_container_client(os.getenv('COSMOS_CONTAINER'))

# Query for Vibe Coding document
query = "SELECT * FROM c WHERE c.topic = 'Vibe Coding evolution'"
items = list(container.query_items(query=query, enable_cross_partition_query=True))

if not items:
    print("Document not found")
else:
    item = items[0]
    
    print('\n' + '='*80)
    print('📄 VIBE CODING EVOLUTION - Complete Content')
    print('='*80)
    
    print(f"\n📌 Document Info:")
    print(f"   ID: {item.get('id')}")
    print(f"   Topic: {item.get('topic')}")
    print(f"   Platforms: {', '.join(item.get('platforms', []))}")
    print(f"   Created: {item.get('createdAt', 'N/A')}")
    print(f"   Generation Time: {item.get('metadata', {}).get('duration', 'N/A')}s")
    
    gen_content = item.get('generatedContent', {})
    
    # Show Plan
    plan = gen_content.get('plan', {})
    if plan:
        print(f"\n{'='*80}")
        print("📋 PLAN")
        print('='*80)
        
        print(f"\n🎣 Hook:")
        print(f"{plan.get('hook', 'N/A')}")
        
        print(f"\n📖 Narrative Frame:")
        print(f"{plan.get('narrative_frame', 'N/A')}")
        
        key_points = plan.get('key_points', [])
        if key_points:
            print(f"\n🔑 Key Points:")
            for i, point in enumerate(key_points, 1):
                print(f"   {i}. {point}")
        
        print(f"\n💡 Example:")
        example = plan.get('example', 'N/A')
        print(f"{example}")
        
        print(f"\n📣 Call to Action:")
        print(f"{plan.get('cta', 'N/A')}")
    
    # Show LinkedIn Output
    outputs = gen_content.get('outputs', {})
    linkedin = outputs.get('linkedin', {})
    if linkedin:
        print(f"\n\n{'='*80}")
        print("📱 LINKEDIN POST CONTENT")
        print('='*80)
        
        content = linkedin.get('content', '')
        print(f"\n{content}")
        
        hashtags = linkedin.get('hashtags', [])
        if hashtags:
            print(f"\n\n🏷️ Hashtags: {', '.join(hashtags)}")
    
    # Show Notes
    notes = gen_content.get('notes', '')
    if notes:
        print(f"\n\n{'='*80}")
        print("📝 NOTES")
        print('='*80)
        print(f"\n{notes}")
    
    print(f"\n\n{'='*80}")
    print("✅ Complete Vibe Coding content retrieved from Cosmos DB")
    print('='*80)
