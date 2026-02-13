"""Show raw document JSON"""
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = CosmosClient(os.getenv('COSMOS_ENDPOINT'), credential=DefaultAzureCredential())
container = client.get_database_client(os.getenv('COSMOS_DATABASE')).get_container_client(os.getenv('COSMOS_CONTAINER'))

query = "SELECT * FROM c WHERE c.topic = 'Kubernetes best practices'"
items = list(container.query_items(query=query, enable_cross_partition_query=True))

if items:
    print('\n' + '='*70)
    print('📄 RAW DOCUMENT FROM COSMOS DB')
    print('='*70)
    print(json.dumps(items[0], indent=2, default=str))
    print('='*70)
else:
    print("No items found")
