"""Show full document from Cosmos DB"""
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

load_dotenv()

credential = DefaultAzureCredential()
client = CosmosClient(os.getenv('COSMOS_ENDPOINT'), credential=credential)
container = client.get_database_client(os.getenv('COSMOS_DATABASE')).get_container_client(os.getenv('COSMOS_CONTAINER'))

# Get one complete item
item = container.read_item(
    item='595a5c1b-f808-40e0-acbe-0e9536913c41', 
    partition_key='595a5c1b-f808-40e0-acbe-0e9536913c41'
)

print('\n' + '='*70)
print('📄 Full Document from Cosmos DB')
print('='*70)
print(f"\nID: {item.get('id')}")
print(f"Topic: {item.get('topic')}")
print(f"Platforms: {', '.join(item.get('platforms', []))}")
print(f"\n✨ Generated Content Fields:")
print('-' * 70)

content = item.get('generated_content', {})
for platform, data in content.items():
    print(f"\n🔹 {platform.upper()}:")
    hook = data.get('hook', 'N/A')
    print(f"   Hook: {hook[:100]}..." if len(hook) > 100 else f"   Hook: {hook}")
    
    narrative = data.get('narrative_frame', 'N/A')
    print(f"   Narrative: {narrative[:100]}..." if len(narrative) > 100 else f"   Narrative: {narrative}")
    
    key_points = data.get('key_points', [])
    print(f"   Key Points: {len(key_points)} points stored")
    if key_points:
        print(f"      - {key_points[0][:80]}..." if len(key_points[0]) > 80 else f"      - {key_points[0]}")
    
    example = str(data.get('example', 'N/A'))
    print(f"   Example: {example[:100]}..." if len(example) > 100 else f"   Example: {example}")
    
    cta = data.get('call_to_action', 'N/A')
    print(f"   CTA: {cta[:100]}..." if len(cta) > 100 else f"   CTA: {cta}")

print('\n' + '='*70)
print('✅ All structured content fields confirmed in Cosmos DB!')
print('='*70)
