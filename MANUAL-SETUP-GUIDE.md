# 🚀 Manual Setup: Enable Grounded Content (10 minutes)

## Step 1: Upload Knowledge Base Files (3 minutes)

1. Open Azure AI Foundry Studio: https://ai.azure.com/

2. Select your project: **aiworkshop-ai-service-project**

3. In left sidebar, click **"Files"** or **"Storage"**

4. Click **"+ Upload files"** button

5. Navigate to:
   ```
   c:\Users\vrengarajan\OneDrive - Microsoft\Documents\Work-Documents\dev-space\project-Repos\social-media-agent\knowledge-base\
   ```

6. **Select all 7 files:**
   - ✅ agent-instructions.md
   - ✅ brand-guidelines.md
   - ✅ content-examples.md
   - ✅ IMPLEMENTATION-GUIDE.md
   - ✅ microsoft-documentation-sources.md
   - ✅ platform-best-practices.md
   - ✅ technical-writing-guide.md

7. Click **"Upload"**

8. ✅ Wait for "Upload successful" confirmation

---

## Step 2: Configure Agent with File Search (5 minutes)

1. In Azure AI Foundry Studio, go to **"Agents"**

2. Find and click: **"Social-Media-Communication-Agent"**

3. Click **"Edit"** or **"Settings"**

### Enable File Search Tool

4. Scroll to **"Tools"** section

5. Click **"+ Add tool"**

6. Select: **"file_search"**  or **"File Search"**

7. Enable the toggle ✅

### Attach Knowledge Base Files

8. In **"Files"** or **"Vector Stores"** section:

9. Click **"+ Add files"** or **"Create vector store"**

10. Select all 7 uploaded files:
    - agent-instructions.md
    - brand-guidelines.md
    - content-examples.md
    - IMPLEMENTATION-GUIDE.md
    - microsoft-documentation-sources.md
    - platform-best-practices.md
    - technical-writing-guide.md

11. Click **"Add"** or **"Attach"**

### Update Agent Instructions

12. Find **"Instructions"** or **"System message"** field

13. Open this file: `knowledge-base\agent-instructions.md`

14. **Copy ALL content** (Ctrl+A, Ctrl+C)

15. **Paste** into Instructions field (replacing existing)

16. Click **"Save"** at top right

17. ✅ Confirmation: "Agent updated successfully"

---

## Step 3: Test Grounded Generation (2 minutes)

### Start Backend

```powershell
cd c:\Users\vrengarajan\OneDrive - Microsoft\Documents\Work-Documents\dev-space\project-Repos\social-media-agent\backend

python -m uvicorn app.main:app --reload
```

### Test via Web UI

1. Open: http://localhost:8000

2. **Topic**: "Kubernetes best practices for production"

3. **Platform**: LinkedIn

4. **Click**: "Generate"

5. **Wait**: 15-20 seconds

### Verify Success ✅

Check generated content for:

✅ **Citations present**:
```
According to Microsoft's AKS documentation[1]...

[1] https://learn.microsoft.com/en-us/azure/aks/best-practices
```

✅ **LinkedIn format**: 1,300-2,000 characters

✅ **Professional structure**: 
- Hook/opening
- 3-5 numbered points
- Concrete example
- Call to action
- 3-5 hashtags

✅ **Grounded facts**: 
- Links to microsoft.com or learn.microsoft.com
- Specific version numbers or feature names
- Real data/metrics

✅ **Responsible AI compliance**:
- Inclusive language
- No credentials/PII
- Transparent about limitations

---

## ✅ Success Example

**Good output:**
```markdown
## Kubernetes Production Best Practices

Based on Microsoft's official AKS documentation[1], here are 5 critical 
practices that reduce incidents by 60%:

1. **Resource Limits**: Define CPU/memory limits for every container
2. **Health Checks**: Implement liveness and readiness probes
3. **Pod Disruption Budgets**: Ensure high availability during updates
4. **Network Policies**: Segment traffic with Kubernetes NetworkPolicy
5. **Monitoring**: Enable Container Insights for real-time metrics

Real Example:
A retail company reduced their MTTR from 4 hours to 20 minutes by 
implementing automated health checks and PDBs[2].

What's your biggest K8s production challenge? 

[1] AKS Best Practices: https://learn.microsoft.com/en-us/azure/aks/best-practices
[2] Azure Case Studies: https://azure.microsoft.com/case-studies/

#Kubernetes #Azure #DevOps #CloudNative #SRE
```

---

## 🐛 Troubleshooting

### "No citations in generated content"

**Fix:**
1. Verify file_search tool shows ✅ enabled in agent settings
2. Check all 7 files are attached under Files/Vector Stores
3. Try regenerating - first attempt might warm up the vector store
4. Check agent instructions include "Search knowledge base" guidance

### "Content doesn't follow LinkedIn format"

**Fix:**
1. Verify agent instructions were pasted correctly
2. Check agent-instructions.md was uploaded to Files
3. In request, be explicit: "Create LinkedIn post following brand guidelines"

### "Generic content, not grounded in Microsoft docs"

**Fix:**
1. Check microsoft-documentation-sources.md is uploaded
2. Enable Bing Search tool (if available in your Azure AI Foundry)
3. In prompt, add: "Include link to official Microsoft documentation"

### "Backend connection error"

**Fix:**
```powershell
# Verify agent name in .env matches Azure AI Foundry
cd c:\Users\vrengarajan\OneDrive - Microsoft\Documents\Work-Documents\dev-space\project-Repos\social-media-agent\backend

cat .env | Select-String "AGENT_NAME"

# Should show: AGENT_NAME="Social-Media-Communication-Agent"
```

---

## 📊 Quality Checklist

After each generation, verify:

- [ ] Content has citations in `[text](url)` format
- [ ] Links point to microsoft.com/learn.microsoft.com
- [ ] Platform format is correct (length, structure)
- [ ] Professional, inclusive language
- [ ] No credentials, PII, or confidential data
- [ ] Specific technical details (not generic)
- [ ] Actionable insights

---

## 🎉 You're Done!

Your agent is now grounded with:
- ✅ 7 knowledge base documents
- ✅ Microsoft Responsible AI principles
- ✅ Platform-specific best practices
- ✅ Chain-of-Thought reasoning
- ✅ Citation requirements

**Next**: Generate diverse content and watch quality improve! 🚀

---

**Total Time**: ~10 minutes  
**Difficulty**: Easy (point-and-click)  
**Result**: Grounded content with Microsoft docs citations
