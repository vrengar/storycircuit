"""Show full document from Cosmos DB with proper partition key handling"""
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

load_dotenv()

credential = DefaultAzureCredential()
client = CosmosClient(os.getenv('COSMOS_ENDPOINT'), credential=credential)
container = client.get_database_client(os.getenv('COSMOS_DATABASE')).get_container_client(os.getenv('COSMOS_CONTAINER'))

# Query for one item to get all details
query = "SELECT * FROM c WHERE c.topic = 'Kubernetes best practices'"
items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

if not items:
    print("No items found")
else:
    item = items[0]
    
    print('\n' + '='*70)
    print('📄 Full Document from Cosmos DB (Direct Query)')
    print('='*70)
    print(f"\nID: {item.get('id')}")
    print(f"Partition Key: {item.get('partition_key')}")
    print(f"Topic: {item.get('topic')}")
    print(f"Platforms: {', '.join(item.get('platforms', []))}")
    print(f"User ID: {item.get('user_id')}")
    print(f"Generated At: {item.get('generated_at', 'N/A')}")
    
    print(f"\n✨ Generated Content:")
    print('-' * 70)
    
    content = item.get('generated_content', {})
    for platform, data in content.items():
        print(f"\n🔹 {platform.upper()} Platform:")
        
        hook = data.get('hook', 'N/A')
        print(f"\n   Hook:")
        print(f"   {hook[:200]}..." if len(hook) > 200 else f"   {hook}")
        
        narrative = data.get('narrative_frame', 'N/A')
        print(f"\n   Narrative Frame:")
        print(f"   {narrative[:200]}..." if len(narrative) > 200 else f"   {narrative}")
        
        key_points = data.get('key_points', [])
        print(f"\n   Key Points ({len(key_points)} stored):")
        for i, point in enumerate(key_points[:3], 1):
            print(f"   {i}. {point}")
        
        example = data.get('example', 'N/A')
        if isinstance(example, dict):
            print(f"\n   Example:")
            for key, value in example.items():
                print(f"      {key}: {value}")
        else:
            print(f"\n   Example: {str(example)[:200]}...")
        
        cta = data.get('call_to_action', 'N/A')
        print(f"\n   Call to Action:")
        print(f"   {cta[:200]}..." if len(cta) > 200 else f"   {cta}")
    
    # Show metadata
    metadata = item.get('metadata', {})
    print(f"\n📊 Metadata:")
    print(f"   Generation Time: {metadata.get('generation_time_seconds', 'N/A')}s")
    print(f"   Content Length: {metadata.get('content_length_chars', 'N/A')} characters")
    print(f"   Agent ID: {metadata.get('agent_id', 'N/A')}")
    
    print('\n' + '='*70)
    print('✅ Complete document with all fields retrieved from Cosmos DB!')
    print('='*70)
