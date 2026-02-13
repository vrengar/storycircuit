# Microsoft & Azure MCP Tools - Quick Start Guide

## 🎯 Objective
Integrate Microsoft Docs and Azure MCP servers to enable your agent to:
1. Search and fetch official Microsoft documentation
2. Get verified code samples
3. Generate Azure CLI commands
4. Access Azure architecture best practices
5. Query Azure resources (when needed)

---

## 📦 Available MCP Tools

### Microsoft Docs MCP Server
✅ **Already available in your VS Code environment**

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `microsoft_docs_search` | Search learn.microsoft.com | Find AKS security docs |
| `microsoft_docs_fetch` | Get full article content | Retrieve complete guide |
| `microsoft_code_sample_search` | Find code examples | Get Python SDK samples |

### Azure MCP Server  
✅ **Already available in your VS Code environment**

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `azure_cli_generate` | Generate Azure CLI commands | Create AKS cluster command |
| `azure_architecture` | Get architecture recommendations | Event-driven patterns |
| `azure_resources` | Query Azure subscriptions/resources | List container registries |
| `azure_bicep` | Get Bicep code & modules | Infrastructure as Code |

---

## 🚀 Quick Start (15 minutes)

### Step 1: Update Agent Instructions (5 min)

You've already done this! Your [agent-instructions.md](knowledge-base/agent-instructions.md) now includes:
- ✅ Microsoft Docs MCP tool descriptions
- ✅ Azure MCP tool descriptions  
- ✅ Usage patterns with ReAct reasoning
- ✅ 3 comprehensive examples
- ✅ Decision matrix for when to use each tool

**Next:** Upload updated instructions to Azure AI Foundry

### Step 2: Upload to Azure AI Foundry (5 min)

#### Option A: Manual Upload (Recommended for now)
1. Go to https://ai.azure.com/
2. Open project: `aiworkshop-ai-service-project`
3. Navigate to: **BUILD → Agents → Social-Media-Communication-Agent**
4. Click **Edit** on Instructions section
5. **Copy entire contents** of `knowledge-base/agent-instructions.md`
6. **Paste** into Instructions field
7. Click **Save**

#### Option B: Via Knowledge Base
1. Go to **BUILD → Knowledge** section
2. Find your existing `agent-instructions.md` file
3. Click **Replace** or **Update**
4. Upload the new version
5. The agent will automatically use the updated version

### Step 3: Test MCP Integration (5 min)

#### Test 1: Microsoft Docs MCP
**Test Query:** "Create LinkedIn post about Azure Kubernetes Service security best practices"

**Expected Behavior:**
- Agent uses `microsoft_docs_search` to find official AKS security docs
- Agent uses `microsoft_docs_fetch` to get full article
- Generated content cites URLs like: `https://learn.microsoft.com/en-us/azure/aks/best-practices-cluster-security`
- Citations are REAL URLs (not placeholders `#`)

#### Test 2: Azure MCP + Microsoft Docs
**Test Query:** "Create content showing how to create a secure AKS cluster with Azure CLI"

**Expected Behavior:**
- Agent uses `azure_cli_generate` to create AKS creation command
- Agent uses `microsoft_docs_search` to explain security settings
- Generated content includes:
  - Working Azure CLI command
  - Official Microsoft docs citations
  - Explanation of security flags
  
#### Test 3: Code Samples
**Test Query:** "Create GitHub README showing Azure Functions Event Grid trigger example in Python"

**Expected Behavior:**
- Agent uses `microsoft_code_sample_search` with `language="python"`
- Generated content includes verified code sample from Microsoft docs
- Links to source documentation

---

## 📊 Success Criteria

### ✅ Microsoft Docs MCP Working
- [ ] Agent generates content with real `learn.microsoft.com` URLs
- [ ] Citations link to actual documentation (not placeholder `#`)
- [ ] Information is from 2026 documentation (current)
- [ ] Code examples are pulled from official Microsoft samples

### ✅ Azure MCP Working  
- [ ] Agent generates valid Azure CLI commands
- [ ] Commands are properly formatted and tested
- [ ] Architecture recommendations align with Azure best practices
- [ ] Integration with Microsoft Docs for explanations

### ✅ Reasoning Patterns Active
- [ ] Agent shows Thought → Action → Observation flow in responses
- [ ] Multiple MCP tools used together (docs + Azure)
- [ ] Self-reflection validates technical accuracy

---

## 🔧 Troubleshooting

### Issue: Agent not using MCP tools

**Symptoms:**
- Still seeing placeholder citations `[text](#)`
- No `microsoft_docs_search` in agent's reasoning
- Content doesn't cite learn.microsoft.com

**Solutions:**
1. **Verify instructions uploaded:**
   - Go to Azure AI Foundry agent settings
   - Check Instructions field contains MCP tool descriptions
   - Look for "## MCP Tools Available" section

2. **Check tool availability:**
   - MCP tools must be enabled in Azure AI Foundry project
   - May need to enable in project settings

3. **Test with explicit request:**
   - Try: "Search Microsoft docs for Azure Container Apps AND create LinkedIn post"
   - Explicit search request may trigger MCP tool usage

### Issue: Citations still show placeholder `#`

**Cause:** Bing Search may not be enabled, OR topic has no Microsoft docs

**Solution:**
1. Test with known Azure topic: "Azure Kubernetes Service"
2. Agent should find real learn.microsoft.com URLs via `microsoft_docs_search`
3. If still placeholders, Bing Search tool may need to be enabled separately

### Issue: Azure CLI commands look wrong

**Solution:**
1. Agent should be using `azure_cli_generate` MCP tool
2. Verify Azure MCP server is active in VS Code
3. Test standalone: Ask agent "Generate Azure CLI command to create AKS cluster"

---

## 🎓 Usage Patterns

### Pattern 1: Documentation-First (Most Common)

```
User: "Create content about Azure Container Apps"

Agent Reasoning:
1. [microsoft_docs_search: "Azure Container Apps"] → Get official docs
2. [microsoft_docs_fetch: URL] → Get full article
3. [file_search: "platform best practices LinkedIn"] → Get formatting guidelines
4. Generate content with citations to official docs
```

### Pattern 2: Azure CLI + Documentation

```
User: "Show how to create secure AKS cluster"

Agent Reasoning:
1. [azure_cli_generate: "create AKS with security"] → Get CLI command
2. [microsoft_docs_search: "AKS security best practices"] → Explain why
3. [microsoft_code_sample_search: "AKS RBAC"] → Get code example
4. Generate content with command + explanation + example
```

### Pattern 3: Architecture + Documentation

```
User: "Design event-driven architecture on Azure"

Agent Reasoning:
1. [azure_architecture: "event-driven serverless"] → Get recommendations
2. [microsoft_docs_search: "Azure architecture patterns"] → Get guidance
3. [microsoft_code_sample_search: "Azure Functions Event Grid"] → Get implementation
4. Generate comprehensive architecture content
```

---

## 📈 Next Steps

### Immediate (Today)
1. ✅ Update agent instructions → **DONE** (you have the updated file)
2. ⏱️ Upload to Azure AI Foundry
3. ⏱️ Test with AKS security topic
4. ⏱️ Verify real Microsoft docs URLs appear

### This Week
1. Test all 3 MCP tool categories:
   - Microsoft Docs Search & Fetch
   - Azure CLI generation
   - Code sample search
2. Create 5 test topics covering:
   - Azure Kubernetes Service
   - Azure Functions
   - Azure Container Apps
   - Azure Cosmos DB
   - Azure Application Insights
3. Verify citations quality across all tests

### Next Week
1. Integrate MCP tool usage into regular workflow
2. Monitor citation quality (100% real URLs target)
3. Collect feedback on content technical accuracy
4. Consider adding more MCP servers if needed:
   - GitHub MCP (for code examples)
   - Slack MCP (for team collaboration)
   - Analytics MCP (for tracking content performance)

---

## 💡 Tips for Best Results

### 1. Be Specific in Requests
❌ Bad: "Create content about Azure"
✅ Good: "Create LinkedIn post about Azure Kubernetes Service production best practices"

### 2. Mention Documentation When Needed
❌ "Tell me about AKS"
✅ "Search Microsoft docs for AKS security best practices and create content"

### 3. Request Code Examples Explicitly
❌ "Explain Azure Functions"
✅ "Show Azure Functions Event Grid trigger example with code from Microsoft docs"

### 4. Combine Tools for Richer Content
✅ "Generate Azure CLI command for AKS cluster creation AND explain security settings from official docs"

### 5. Verify Technical Accuracy
- Always check that generated Azure CLI commands are valid
- Verify code samples execute properly
- Confirm citations link to current (2026) documentation

---

## 🎯 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Real Microsoft docs citations | 100% | Check all URLs are learn.microsoft.com |
| Azure CLI commands validity | 100% | Test commands in Azure CLI |
| Code samples executable | 100% | Run code samples without errors |
| Response time with MCP tools | < 20s | Time from request to content |
| Technical accuracy | 100% | Verify against official docs |
| Content quality score | 8/10+ | User feedback rating |

---

## 📚 Resources

- **Microsoft Learn**: https://learn.microsoft.com/
- **Azure Documentation**: https://learn.microsoft.com/azure/
- **Azure Architecture Center**: https://learn.microsoft.com/azure/architecture/
- **Azure CLI Reference**: https://learn.microsoft.com/cli/azure/
- **Azure Code Samples**: https://learn.microsoft.com/samples/browse/

---

## ✅ Checklist

Before you start testing:
- [ ] `agent-instructions.md` updated with MCP tools
- [ ] Instructions uploaded to Azure AI Foundry agent
- [ ] Agent saved in Azure AI Foundry
- [ ] Test topic selected (recommend: AKS security)
- [ ] Ready to verify real Microsoft docs URLs in output

After first test:
- [ ] Agent used `microsoft_docs_search` tool
- [ ] Content cites real `learn.microsoft.com` URLs
- [ ] Technical information is accurate
- [ ] Code examples (if any) are from official docs
- [ ] LinkedIn/Twitter formatting follows guidelines

**Ready to test? Go to your application and try: "Create LinkedIn post about Azure Kubernetes Service production security best practices"**

Expected output should include citations like:
- [Best practices for cluster security and upgrades in AKS](https://learn.microsoft.com/en-us/azure/aks/best-practices-cluster-security)
- [Use Microsoft Entra ID in AKS](https://learn.microsoft.com/en-us/azure/aks/azure-ad-integration-cli)

🚀 **Let's see those real Microsoft docs URLs!**
