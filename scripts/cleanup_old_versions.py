"""
Clean up old agent versions with MCP tool
Keep only the latest version (11) with Web Search
"""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

print("🧹 Cleaning up old agent versions...")

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=os.environ.get("AZURE_AI_PROJECT_ENDPOINT") or os.environ["AZURE_AI_ENDPOINT"], 
        credential=credential
    ) as project_client,
):
    print("✅ Connected to Azure AI Foundry project")
    
    agent_name = "Social-Media-Communication-Agent"
    
    print(f"\n🔍 Listing all versions of: {agent_name}")
    agents = list(project_client.agents.list_versions(agent_name=agent_name))
    
    print(f"   Found {len(agents)} version(s)")
    
    if len(agents) > 1:
        # Sort by version (latest first)
        agents.sort(key=lambda a: a.version, reverse=True)
        
        latest = agents[0]
        print(f"\n📌 Latest version: {latest.version}")
        print(f"   Keeping this version (has Web Search tool)")
        
        # Delete older versions
        versions_to_delete = agents[1:]
        print(f"\n🗑️  Deleting {len(versions_to_delete)} old version(s):")
        
        for agent in versions_to_delete:
            try:
                print(f"   - Version {agent.version}...", end=" ")
                project_client.agents.delete_version(
                    agent_name=agent_name,
                    agent_version=agent.version
                )
                print("✅ Deleted")
            except Exception as e:
                print(f"❌ Error: {e}")
    else:
        print(f"\n✅ Only 1 version exists (version {agents[0].version})")
        print(f"   Nothing to clean up")

print("\n✨ Done! Old MCP versions removed.")
print(f"\n💡 Refresh your Azure AI Foundry UI to see the updated agent.")
