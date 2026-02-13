# Deploy Azure MCP Server to Azure Functions

## 🚀 Quick Deploy (3 Commands, 10 Minutes)

### Prerequisites Check

**1. Install Azure Developer CLI (azd)**
```powershell
winget install microsoft.azd
```

**2. Verify installation**
```powershell
azd version
```

Expected: `azd version 1.x.x` or higher

---

## 📦 Deploy to Azure Functions

### Step 1: Login to Azure
```powershell
azd auth login
```

This opens your browser for Azure authentication.

---

### Step 2: Initialize from Template
```powershell
cd c:\Users\vrengarajan\OneDrive - Microsoft\Documents\Work-Documents\dev-space\project-Repos\social-media-agent

# Create directory for MCP server
mkdir azure-mcp-server
cd azure-mcp-server

# Initialize from Microsoft's official template
azd init --template https://github.com/microsoft/mcp --location servers/Azure.Mcp.Server
```

When prompted:
- **Environment name**: `social-media-mcp` (or your choice)
- **Location**: Choose closest region (e.g., `eastus`, `westus2`)

---

### Step 3: Deploy
```powershell
azd up
```

This command will:
1. Create Azure resource group
2. Create Azure Storage account
3. Create Azure Function App
4. Deploy the MCP server code
5. Configure authentication

**Wait time**: ~5-8 minutes

---

## 📋 Get Connection Details

After deployment completes, you'll see output like:

```
Deployment completed successfully!

Function App: func-social-media-mcp-abc123
Endpoint: https://func-social-media-mcp-abc123.azurewebsites.net/runtime/webhooks/mcp
```

### Get the Function Key

```powershell
# Get the function key from environment
azd env get-values | Select-String "MCP_SYSTEM_KEY"
```

**Save this key!** You'll need it to connect to Foundry.

---

## 🔗 Connect to Azure AI Foundry

### In Foundry Portal:

1. **Navigate to your agent**
   - Go to https://ai.azure.com/
   - Project: `aiworkshop-ai-service-project`
   - Select: `Social-Media-Communication-Agent`

2. **Add MCP Tool**
   - Tools section → **Add** button
   - Select **Custom** tab
   - Choose **Model Context Protocol (MCP)**
   - Click **Create**

3. **Configure Connection**
   ```
   Name: Azure MCP Server
   
   Remote MCP Server endpoint: 
   https://func-social-media-mcp-abc123.azurewebsites.net/runtime/webhooks/mcp
   
   Authentication: Key-based
   
   Credential:
   {"x-functions-key": "your-function-key-here"}
   ```

4. **Click Connect**

5. **Save agent configuration**

---

## ✅ Test the Connection

### In Azure AI Foundry Playground:

**Test 1: Verify tools are available**
```
User: What Azure tools do you have access to?
```

Expected: Agent lists Azure MCP Server tools (best practices, Azure services, etc.)

**Test 2: Use a tool**
```
User: AKS security in prod
```

Expected: Agent uses Azure MCP Server to get best practices and generates content

---

## 🛠️ Troubleshooting

### Issue: `azd` command not found
```powershell
# Restart PowerShell after installation
# Or run:
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

### Issue: Deployment fails
```powershell
# Check Azure subscription
az account show

# Try with specific subscription
azd up --subscription "your-subscription-id"
```

### Issue: Can't get function key
```powershell
# Alternative method using Azure CLI
$FUNCTION_APP_NAME = "func-social-media-mcp-abc123"  # Your function app name
az functionapp keys list --name $FUNCTION_APP_NAME --resource-group rg-social-media-mcp --query systemKeys
```

### Issue: Connection fails in Foundry
1. Verify endpoint URL is correct (no trailing slash)
2. Test endpoint directly:
   ```powershell
   $endpoint = "https://func-social-media-mcp-abc123.azurewebsites.net/runtime/webhooks/mcp"
   $key = "your-function-key"
   curl $endpoint -H "x-functions-key: $key"
   ```
3. Check function app is running:
   ```powershell
   az functionapp show --name $FUNCTION_APP_NAME --resource-group rg-social-media-mcp --query state
   ```

---

## 📊 What This Provides

### Azure Best Practices Tool
**Namespace**: `get_bestpractices`

Get guidance on:
- Azure Functions development
- Azure SDK usage
- Deployment best practices

**Example agent prompt**: "What are Azure Functions best practices for production?"

### Azure AI Foundry Tools
**Namespace**: `foundry`

- List available models
- Query deployments
- Get endpoint information

**Example agent prompt**: "Show me available AI models in Azure Foundry"

### 80+ Azure Service Tools

Including:
- **AKS** (Azure Kubernetes Service)
- **App Service** 
- **Functions**
- **Storage**
- **Key Vault**
- **Cosmos DB**
- **Networking**
- And 70+ more...

**Example agent prompt**: "List all Azure Kubernetes clusters"

---

## 💰 Cost Estimate

**Azure Functions Consumption Plan:**
- First 1 million executions: **FREE**
- Storage: ~$0.10/month
- **Estimated total for your use case: $0-2/month**

---

## 🔄 Update/Redeploy

If you need to update the MCP server:

```powershell
cd c:\Users\vrengarajan\OneDrive - Microsoft\Documents\Work-Documents\dev-space\project-Repos\social-media-agent\azure-mcp-server

# Redeploy
azd up
```

---

## 🗑️ Clean Up (If Needed Later)

```powershell
# Remove all Azure resources
azd down
```

This deletes:
- Function App
- Storage Account
- Resource Group
- All associated resources

---

## 📝 Next Steps After Deployment

1. ✅ Upload agent-instructions.md to Foundry agent Instructions field
2. ✅ Test with casual request: "AKS security in prod"
3. ✅ Verify agent uses Azure MCP Server for Azure-related content
4. ✅ Check that responses include Azure best practices

---

## 🎯 Success Criteria

After deployment and connection, your agent should:

- ✅ Accept casual requests ("AKS security in prod")
- ✅ Use Azure MCP Server for Azure service information
- ✅ Use File Search for brand guidelines
- ✅ Generate content grounded in both internal knowledge and Azure documentation
- ✅ Respond in 15-20 seconds (some cold start delay on first request)

---

## 📞 Support

**If you get stuck:**
1. Check Azure Function logs: `azd monitor`
2. Test endpoint directly with curl
3. Verify function key is correct
4. Ensure Foundry project can reach the endpoint (no firewall blocks)

**Microsoft Docs:**
- [Azure MCP Server](https://learn.microsoft.com/azure/developer/azure-mcp-server/)
- [Azure Functions](https://learn.microsoft.com/azure/azure-functions/)
- [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
