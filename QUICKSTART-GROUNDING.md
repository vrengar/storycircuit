# Quick Start: Enable Grounded Content Generation

## 🎯 Goal
Add knowledge base grounding and Microsoft documentation citations to your social media agent in **15 minutes**.

## Prerequisites
- ✅ Azure CLI installed and logged in (`az login`)
- ✅ Backend running successfully
- ✅ Agent created in Azure AI Foundry

---

## Step 1: Upload Knowledge Base (5 min)

### Option A: Automated Upload (Recommended)

```powershell
cd c:\Users\vrengarajan\OneDrive - Microsoft\Documents\Work-Documents\dev-space\project-Repos\social-media-agent

# Run upload script
python scripts/upload_knowledge_base.py
```

**What it does:**
- Uploads all 7 knowledge base files
- Returns file IDs needed for next step
- Shows upload status and file sizes

**Expected output:**
```
✅ Successfully uploaded 7 files:
   brand-guidelines.md
   └─ ID: file-abc123...
   
📋 File IDs for Agent Configuration:
file_ids = [
    "file-abc123...",
    "file-def456...",
    ...
]
```

📋 **SAVE THE FILE IDS** - you'll need them in Step 2!

### Option B: Manual Upload via Azure Portal

1. Go to https://ai.azure.com/
2. Select project: `aiworkshop-ai-service-project`
3. Navigate to **"Files"** section
4. Click **"Upload"**
5. Select all files from `knowledge-base/` folder
6. Note the file IDs from the upload confirmation

---

## Step 2: Configure Agent (5 min)

### Option A: Automated Configuration (Recommended)

```powershell
# Run configuration script
python scripts/configure_agent.py
```

**When prompted:**
- Paste the file IDs from Step 1 (comma-separated)
- Or press Enter to just enable file_search tool

**What it does:**
- Finds your "Social-Media-Communication-Agent"
- Enables `file_search` tool
- Attaches knowledge base files
- Updates agent instructions with Chain-of-Thought reasoning

**Expected output:**
```
✅ Agent updated successfully!

🔧 Tools Enabled:
   ✅ file_search

📝 Instructions: Updated (18,524 chars)
   - 5-step Chain-of-Thought reasoning
   - File search integration
   - Citation requirements

📁 Knowledge Base: 7 files attached
```

### Option B: Manual Configuration via Azure Portal

1. Open agent in Azure AI Foundry Studio
2. Go to **Settings** → **Tools**
3. Enable: ✅ `file_search`
4. Under **"Files"**, attach all 7 uploaded files
5. Open **"Instructions"** field
6. Copy entire content from `knowledge-base/agent-instructions.md`
7. Paste and save

---

## Step 3: Test Grounding (5 min)

### Start Backend

```powershell
cd c:\Users\vrengarajan\OneDrive - Microsoft\Documents\Work-Documents\dev-space\project-Repos\social-media-agent\backend

python -m uvicorn app.main:app --reload
```

### Option A: Automated Test

```powershell
# In a new terminal
python scripts/test_grounding.py
```

**What it tests:**
- Content generation with knowledge base
- Citation extraction
- Platform-specific formatting
- Microsoft docs links
- Quality validation

### Option B: Manual Test via UI

1. Open http://localhost:8000
2. Enter topic: "Kubernetes best practices"
3. Select platform: LinkedIn
4. Generate content

**What to verify:**
- ✅ Content follows LinkedIn format (1300-2000 chars)
- ✅ Has numbered or bulleted key points
- ✅ Contains citations like `[text](url)`
- ✅ Links to microsoft.com or learn.microsoft.com
- ✅ Professional, inclusive language
- ✅ Has hashtags
- ✅ No credentials or PII

### Option C: Manual Test via Postman/curl

```powershell
curl http://localhost:8000/api/generate `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"topic":"Azure Container Apps deployment","platform":"LinkedIn","tone":"professional"}'
```

---

## ✅ Success Criteria

Your grounded agent is working if you see:

**In generated content:**
```markdown
## Kubernetes Best Practices for Production

Based on Microsoft's official AKS documentation[1], here are 5 critical practices...

1. **Resource Limits**: Always define CPU/memory limits
2. **Health Checks**: Implement liveness and readiness probes
...

[1] Azure Kubernetes Service best practices
https://learn.microsoft.com/en-us/azure/aks/best-practices
```

**Validation checklist:**
- ✅ Citations present: `[text](url)` format
- ✅ Microsoft docs linked: learn.microsoft.com
- ✅ Platform format: Correct length and structure
- ✅ Brand voice: Empowering, inclusive, clear
- ✅ Technical accuracy: Specific features, versions
- ✅ No sensitive data: No credentials, PII, confidential info

---

## 🐛 Troubleshooting

### "No citations in output"

**Causes:**
- file_search tool not enabled
- Files not attached to agent
- Agent instructions missing file_search guidance

**Fix:**
```powershell
# Re-run configuration
python scripts/configure_agent.py

# Verify in Azure AI Foundry:
# - Tools section shows file_search enabled
# - Files section shows 7 files attached
```

### "Agent not found"

**Causes:**
- Agent name mismatch
- Wrong project/endpoint

**Fix:**
```powershell
# List available agents
az cognitiveservices account list-keys --name aiworkshop-ai-service --resource-group aiworkshop-rg

# Verify endpoint in scripts/upload_knowledge_base.py and scripts/configure_agent.py
```

### "Authentication failed"

**Causes:**
- Not logged in to Azure CLI
- Insufficient permissions

**Fix:**
```powershell
# Login to Azure
az login

# Verify account
az account show

# Check permissions
az role assignment list --scope /subscriptions/YOUR_SUBSCRIPTION_ID
```

### "Content not following guidelines"

**Causes:**
- Agent not using knowledge base
- Instructions not updated

**Fix:**
1. Verify agent instructions match `agent-instructions.md`
2. Check file_search tool is enabled
3. Test with explicit prompt: "Use knowledge base guidelines for LinkedIn post about Kubernetes"

---

## 📊 Monitoring Quality

After each generation, check:

```python
# Extract quality metrics
import re

def validate_content(content):
    checks = {
        "has_citations": len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)) > 0,
        "microsoft_docs": 'microsoft.com' in content.lower(),
        "appropriate_length": 1000 < len(content) < 3000,
        "has_structure": any(m in content for m in ['1.', '2.', '•', '#']),
        "no_credentials": not re.search(r'api[_-]?key|password|secret', content, re.I)
    }
    
    return all(checks.values()), checks
```

---

## 🎉 Next Steps

Once grounding is working:

1. **Monitor citation quality**
   - Are links current and valid?
   - Do they support the content claims?

2. **Expand knowledge base**
   - Add more examples
   - Update with latest Azure features
   - Add industry-specific guidelines

3. **Enable analytics**
   - Track which sources are cited most
   - Measure content quality scores
   - Monitor user engagement

4. **Production deployment**
   - Add Managed Identity
   - Enable Application Insights
   - Set up CI/CD for knowledge base updates

---

**Estimated Total Time**: 15 minutes  
**Difficulty**: Easy (fully automated)  
**Prerequisites**: Azure CLI + Existing agent  
**Outcome**: Grounded content with Microsoft docs citations
