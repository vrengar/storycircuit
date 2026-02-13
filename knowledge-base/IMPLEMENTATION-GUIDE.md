# Implementation Guide: Grounding with Microsoft Docs & Web Search

## Overview

This guide explains how to enable grounding with Microsoft documentation and web search in your Azure AI Foundry agent.

## Architecture

```
User Request
    ↓
Agent (Chain-of-Thought)
    ↓
    ├─→ File Search → Knowledge Base (brand guidelines, examples)
    │
    ├─→ Bing Search → Microsoft Docs, blogs, research
    │
    └─→ Generate → Grounded, cited content
```

## Step 1: Upload Knowledge Documents to Azure AI Foundry

### Via Azure AI Foundry Studio

1. Navigate to https://ai.azure.com/
2. Select your project: `aiworkshop-ai-service-project`
3. Go to **"Files"** or **"Storage"** section
4. Click **"Upload files"**
5. Upload all knowledge base documents:
   - `brand-guidelines.md`
   - `platform-best-practices.md`
   - `technical-writing-guide.md`
   - `content-examples.md`
   - `microsoft-documentation-sources.md`
   - `agent-instructions.md`

### Verify Upload
```bash
# List uploaded files
az cognitiveservices account file-share files list \
  --account-name aiworkshop-ai-service \
  --resource-group aiworkshop-rg
```

---

## Step 2: Update Agent Configuration

### Enable File Search Tool

**In Azure AI Foundry Studio:**

1. Open your agent: `Social-Media-Communication-Agent`
2. Navigate to **"Agent Configuration"** or **"Settings"**
3. Under **"Tools"**, enable:
   - ✅ **file_search** (for knowledge base)
4. Click **"Save"**

**Via API (if needed):**

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = AIProjectClient(
    endpoint="https://aiworkshop-ai-service.services.ai.azure.com",
    credential=credential
)

# Update agent to include file_search
agent = client.agents.update_agent(
    assistant_id="your-agent-id",
    tools=[
        {"type": "file_search"}  # Enable file_search tool
    ]
)
```

---

## Step 3: Update Agent Instructions

Replace the current agent instructions with the enhanced Chain-of-Thought instructions from `agent-instructions.md`.

**In Azure AI Foundry Studio:**

1. Open your agent configuration
2. Find **"Instructions"** or **"System Prompt"** field
3. Copy the entire content from [agent-instructions.md](./agent-instructions.md)
4. Paste into the instructions field
5. Save changes

**Key sections in the new instructions:**
- 5-step reasoning process (Analyze → Research → Structure → Generate → Validate)
- File search query patterns
- Citation requirements
- Quality validation checklist

---

## Step 4: Enable Web Search (Optional but Recommended)

### Option A: Bing Search Tool (Recommended)

**In Azure AI Foundry Studio:**

1. Go to agent tools configuration
2. Add **"bing_search"** or **"web_search"** tool
3. Configure:
   ```json
   {
     "type": "bing_search",
     "config": {
       "search_domain": "microsoft.com,learn.microsoft.com",
       "max_results": 5
     }
   }
   ```

### Option B: Grounding with URLs

If Bing Search isn't available, you can ground with specific URLs:

```python
# In your request to the agent
grounding_sources = [
    "https://learn.microsoft.com/en-us/azure/",
    "https://techcommunity.microsoft.com/",
    "https://azure.microsoft.com/en-us/blog/"
]
```

---

## Step 5: Test Grounding

### Test File Search

**Request:**
```
"Create LinkedIn content about Kubernetes best practices"
```

**Expected Behavior:**
1. Agent searches knowledge base for:
   - Platform best practices (LinkedIn)
   - Technical writing guide (Kubernetes)
   - Content examples (LinkedIn posts)
2. Finds relevant guidelines
3. Generates content following those guidelines
4. Cites knowledge base in output

**Verify:**
- Does output follow LinkedIn format from guidelines?
- Are there 3-5 key points as recommended?
- Is brand voice applied (empowering, inclusive)?

### Test Web Search / Microsoft Docs Grounding

**Request:**
```
"Create content about Azure Container Apps with latest features"
```

**Expected Behavior:**
1. Agent searches web for latest Azure Container Apps documentation
2. Finds official Microsoft Learn pages
3. Extracts current features and best practices
4. Generates content with citations
5. Links to official documentation

**Verify:**
- Are there links to https://learn.microsoft.com/ ?
- Are features current (2026)?
- Are version numbers included?
- Is source properly cited?

---

## Step 6: Add Citation Tracking (Optional)

To track which sources were used, update your content service:

```python
# In content_service.py
class ContentService:
    async def generate_content(...):
        result = await self.agent_service.generate_content(...)
        
        # Extract citations from agent response
        citations = self._extract_citations(result)
        
        # Store in metadata
        metadata = {
            "citations": citations,
            "sources_used": [c["url"] for c in citations],
            "knowledge_base_refs": self._extract_file_refs(result)
        }
        
        return result, metadata
    
    def _extract_citations(self, content):
        # Parse markdown links and references
        import re
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        citations = []
        for match in re.finditer(pattern, content):
            citations.append({
                "text": match.group(1),
                "url": match.group(2)
            })
        return citations
```

---

## Configuration Summary

### Agent Configuration JSON

```json
{
  "name": "Social-Media-Communication-Agent",
  "model": "gpt-4",
  "instructions": "[Content from agent-instructions.md]",
  "tools": [
    {
      "type": "file_search",
      "file_ids": [
        "file-123...",  // brand-guidelines.md
        "file-456...",  // platform-best-practices.md
        "file-789...",  // technical-writing-guide.md
        "file-abc...",  // content-examples.md
        "file-def...",  // microsoft-documentation-sources.md
        "file-ghi..."   // agent-instructions.md
      ]
    },
    {
      "type": "bing_search",
      "config": {
        "max_results": 5,
        "search_domain": "microsoft.com,learn.microsoft.com,techcommunity.microsoft.com,azure.microsoft.com"
      }
    }
  ],
  "metadata": {
    "version": "2.0",
    "grounding_enabled": true,
    "last_updated": "2026-02-12"
  }
}
```

---

## Monitoring Grounding Quality

### Check Each Generated Content For:

**Knowledge Base Grounding:**
- [ ] Follows brand voice guidelines
- [ ] Uses platform-specific format
- [ ] Applies technical writing best practices
- [ ] Matches successful examples pattern

**Microsoft Docs Grounding:**
- [ ] Links to official Microsoft documentation
- [ ] Cites current (2026) information
- [ ] Includes version numbers where relevant
- [ ] References specific features accurately

**Quality Indicators:**
- [ ] At least 1-3 citations per content piece
- [ ] Links are to microsoft.com, learn.microsoft.com, or techcommunity.microsoft.com
- [ ] Facts are verifiable against official docs
- [ ] No outdated or inaccurate information

---

## Troubleshooting

### Issue: Agent not searching knowledge base

**Solution:**
1. Verify files are uploaded in Azure AI Foundry
2. Check file_search tool is enabled
3. Verify file IDs are in agent configuration
4. Try explicit instruction: "Search knowledge base for brand guidelines"

### Issue: No Microsoft docs citations

**Solution:**
1. Check if Bing Search tool is enabled
2. Verify search domain includes microsoft.com
3. Try more specific request: "Include official Azure documentation link"
4. Manually provide URLs in request if web search unavailable

### Issue: Citations not showing in output

**Solution:**
1. Update agent instructions to explicitly request citations
2. Add to instructions: "Always include source links in format [Text](URL)"
3. Check output format requirements in agent-instructions.md

---

## Next Steps

1. ✅ Upload all knowledge documents
2. ✅ Enable file_search tool
3. ✅ Update agent instructions
4. ✅ Enable Bing Search (if available)
5. ✅ Test with sample requests
6. ✅ Verify citations and grounding
7. ✅ Monitor quality metrics
8. 🔄 Iterate and refine based on results

---

**Document Version**: 1.0  
**Last Updated**: February 2026  
**Purpose**: Step-by-step guide for implementing grounding with Microsoft documentation
