"""Show all content stored in Cosmos DB"""
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = CosmosClient(os.getenv('COSMOS_ENDPOINT'), credential=DefaultAzureCredential())
container = client.get_database_client(os.getenv('COSMOS_DATABASE')).get_container_client(os.getenv('COSMOS_CONTAINER'))

# Query all items
query = "SELECT * FROM c ORDER BY c._ts DESC"
items = list(container.query_items(query=query, enable_cross_partition_query=True))

print('\n' + '='*80)
print(f'📊 COMPLETE COSMOS DB CONTENT - Total Items: {len(items)}')
print('='*80)

for idx, item in enumerate(items, 1):
    print(f'\n\n{"="*80}')
    print(f'DOCUMENT #{idx}')
    print('='*80)
    
    print(f"\n📌 Basic Info:")
    print(f"   ID: {item.get('id')}")
    print(f"   Topic: {item.get('topic')}")
    print(f"   Platforms: {', '.join(item.get('platforms', []))}")
    print(f"   User ID: {item.get('userId', 'N/A')}")
    print(f"   Created: {item.get('createdAt', 'N/A')}")
    
    # Show metadata
    metadata = item.get('metadata', {})
    if metadata:
        print(f"\n📊 Metadata:")
        print(f"   Generation Time: {metadata.get('duration', 'N/A')}s")
        print(f"   Agent Version: {metadata.get('agentVersion', 'N/A')}")
        print(f"   Timestamp: {metadata.get('timestamp', 'N/A')}")
    
    # Show generated content summary
    gen_content = item.get('generatedContent', {})
    if gen_content:
        print(f"\n✨ Generated Content:")
        
        # Plan section
        plan = gen_content.get('plan', {})
        if plan:
            print(f"\n   📋 PLAN:")
            hook = plan.get('hook', 'N/A')
            print(f"      Hook: {hook[:150]}..." if len(hook) > 150 else f"      Hook: {hook}")
            
            narrative = plan.get('narrative_frame', 'N/A')
            print(f"      Narrative: {narrative[:150]}..." if len(narrative) > 150 else f"      Narrative: {narrative}")
            
            key_points = plan.get('key_points', [])
            print(f"      Key Points: {len(key_points)} items")
            if key_points and isinstance(key_points, list):
                for i, point in enumerate(key_points[:3], 1):
                    point_str = str(point)
                    print(f"         {i}. {point_str[:100]}..." if len(point_str) > 100 else f"         {i}. {point_str}")
        
        # Outputs section
        outputs = gen_content.get('outputs', {})
        if outputs:
            print(f"\n   📱 PLATFORM OUTPUTS:")
            for platform, content_data in outputs.items():
                if isinstance(content_data, dict):
                    content_text = content_data.get('content', '')
                    print(f"      • {platform.upper()}: {len(content_text)} characters")
                    if content_text:
                        preview = content_text[:200].replace('\n', ' ')
                        print(f"        Preview: {preview}...")
    
    # Show raw storage info
    print(f"\n🗄️ Cosmos DB Internal:")
    print(f"   _ts: {item.get('_ts', 'N/A')}")
    print(f"   _etag: {item.get('_etag', 'N/A')[:50]}...")
    print(f"   Deleted: {item.get('deleted', False)}")
    
    print(f"\n{'='*80}")

print(f"\n\n{'='*80}")
print(f"✅ Showed all {len(items)} documents from Cosmos DB")
print('='*80)
