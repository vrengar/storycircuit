"""
Direct Cosmos DB verification script
Queries the database directly using Azure SDK to prove data storage
"""
import os
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Cosmos DB configuration
ENDPOINT = os.getenv("COSMOS_ENDPOINT")
DATABASE_NAME = os.getenv("COSMOS_DATABASE")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER")

print("\n" + "="*70)
print("🔍 Direct Cosmos DB Verification (Independent of Application)")
print("="*70)
print(f"\n📍 Endpoint: {ENDPOINT}")
print(f"📍 Database: {DATABASE_NAME}")
print(f"📍 Container: {CONTAINER_NAME}")

# Initialize Cosmos client with Azure AD (same as app)
print("\n🔐 Authenticating with Azure AD...")
credential = DefaultAzureCredential()
client = CosmosClient(ENDPOINT, credential=credential)

# Get database and container
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

print("✅ Successfully connected to Cosmos DB\n")

# Query all items
print("📊 Querying all items from Cosmos DB...\n")
query = "SELECT c.id, c.topic, c.platforms, c.user_id, c.generated_at FROM c ORDER BY c._ts DESC"
items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

print("="*70)
print(f"✅ Found {len(items)} items in Cosmos DB")
print("="*70)

if items:
    print("\n📝 Content Items (from Cosmos DB directly):\n")
    for idx, item in enumerate(items, 1):
        created = item.get('generated_at', 'N/A').split('T')[0] if item.get('generated_at') else 'N/A'
        print(f"{idx}. 🔹 ID: {item.get('id')}")
        print(f"   Topic: {item.get('topic')}")
        print(f"   Platforms: {', '.join(item.get('platforms', []))}")
        print(f"   User: {item.get('user_id')}")
        print(f"   Created: {created}\n")
else:
    print("\n⚠️  No items found in database")

print("="*70)
print("✅ Verification complete - Data is stored in Cosmos DB!")
print("="*70)
