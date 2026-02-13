# Microsoft Official Documentation & Resources

## Primary Microsoft Documentation Sources

### Azure Documentation
- **Main Portal**: https://learn.microsoft.com/en-us/azure/
- **What's New**: https://azure.microsoft.com/en-us/updates/
- **Architecture Center**: https://learn.microsoft.com/en-us/azure/architecture/

### Azure AI Services
- **Azure AI Foundry**: https://learn.microsoft.com/en-us/azure/ai-studio/
- **Azure OpenAI Service**: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- **Cognitive Services**: https://learn.microsoft.com/en-us/azure/ai-services/

### Compute & Containers
- **Azure Container Apps**: https://learn.microsoft.com/en-us/azure/container-apps/
- **Azure Kubernetes Service**: https://learn.microsoft.com/en-us/azure/aks/
- **Azure App Service**: https://learn.microsoft.com/en-us/azure/app-service/
- **Azure Functions**: https://learn.microsoft.com/en-us/azure/azure-functions/

### Data & Storage
- **Azure Cosmos DB**: https://learn.microsoft.com/en-us/azure/cosmos-db/
- **Azure Storage**: https://learn.microsoft.com/en-us/azure/storage/
- **Azure SQL Database**: https://learn.microsoft.com/en-us/azure/azure-sql/

### DevOps & Development
- **Azure DevOps**: https://learn.microsoft.com/en-us/azure/devops/
- **GitHub Actions for Azure**: https://learn.microsoft.com/en-us/azure/developer/github/
- **Azure Developer CLI**: https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/

### Security & Identity
- **Microsoft Entra ID**: https://learn.microsoft.com/en-us/entra/identity/
- **Azure Key Vault**: https://learn.microsoft.com/en-us/azure/key-vault/
- **Microsoft Defender for Cloud**: https://learn.microsoft.com/en-us/azure/defender-for-cloud/

## Microsoft Research & Blogs

### Microsoft Research
- **Main Portal**: https://www.microsoft.com/en-us/research/
- **AI Research**: https://www.microsoft.com/en-us/research/research-area/artificial-intelligence/
- **Publications**: https://www.microsoft.com/en-us/research/publications/

### Official Blogs
- **Azure Blog**: https://azure.microsoft.com/en-us/blog/
- **Tech Community**: https://techcommunity.microsoft.com/
- **Developer Blogs**: https://devblogs.microsoft.com/
- **Cloud Advocate Content**: https://learn.microsoft.com/en-us/shows/

### Specific Technical Blogs
- **Azure Architecture**: https://techcommunity.microsoft.com/t5/azure-architecture-blog/bg-p/AzureArchitectureBlog
- **Azure Developer**: https://techcommunity.microsoft.com/t5/azure-developer-community-blog/bg-p/AzureDevCommunityBlog
- **Azure AI**: https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/bg-p/Azure-AI-Services-blog

## How to Reference Microsoft Docs

### When Creating Content

#### Always Link to Official Docs
```markdown
According to [Azure Container Apps documentation](https://learn.microsoft.com/en-us/azure/container-apps/overview), 
Container Apps provides serverless containers with built-in scaling.
```

#### Cite Specific Features
```markdown
Azure Cosmos DB supports [multiple consistency levels](https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels)
including Strong, Bounded Staleness, Session, Consistent Prefix, and Eventual.
```

#### Reference Best Practices
```markdown
Microsoft's [Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
recommends implementing health endpoints for all services.
```

### Citation Format

**For LinkedIn/Blog Posts**:
```
Based on Microsoft's Azure Architecture Center recommendations...
[Link to specific doc]
```

**For Technical Content**:
```
Source: Azure Container Apps Documentation
https://learn.microsoft.com/en-us/azure/container-apps/
Last verified: [Date]
```

## Key Microsoft Frameworks & Methodologies

### Azure Well-Architected Framework
- **Reliability**: https://learn.microsoft.com/en-us/azure/well-architected/reliability/
- **Security**: https://learn.microsoft.com/en-us/azure/well-architected/security/
- **Cost Optimization**: https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/
- **Operational Excellence**: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/
- **Performance Efficiency**: https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/

### Cloud Adoption Framework
- **Main Portal**: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/
- **Strategy**: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/strategy/
- **Migration**: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/

### Enterprise-Scale Landing Zones
- **Overview**: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/

## Current Trends & What's New (2026)

### Check These Regularly
- **Azure Updates**: https://azure.microsoft.com/en-us/updates/
- **Announcements**: Filter by service and date
- **Preview Features**: https://azure.microsoft.com/en-us/updates/?status=inpreview

### Popular Topics (February 2026)
- AI and machine learning integration
- Sustainable/green computing
- Zero-trust security
- Cloud-native development
- Serverless architectures
- Multi-cloud strategies

## Research Papers & Whitepapers

### How to Find Relevant Research
1. Search Microsoft Research: https://www.microsoft.com/en-us/research/
2. Filter by topic (e.g., "distributed systems", "AI", "cloud computing")
3. Look for recent publications (last 2 years)
4. Check citation count for impact

### Reference Format for Research
```
Based on Microsoft Research paper "Title" (Year):
[Key finding or methodology]

Citation: Author et al. (Year). Title. Microsoft Research.
https://[paper-url]
```

## Technical Case Studies

### Azure Case Studies
- **Main Portal**: https://azure.microsoft.com/en-us/case-studies/
- **Filter by Industry**: Healthcare, Finance, Retail, etc.
- **Filter by Service**: AI, Kubernetes, Cosmos DB, etc.

### How to Use Case Studies
- Extract real-world metrics and results
- Reference specific customer successes (when public)
- Highlight lessons learned
- Note: Respect customer confidentiality, use only published info

## Code Samples & Repos

### Official Microsoft Repos
- **Azure Samples**: https://github.com/Azure-Samples
- **Azure Quickstarts**: https://github.com/Azure/azure-quickstart-templates
- **Microsoft Docs Samples**: https://github.com/Azure-Samples/
- **Best Practices**: https://github.com/mspnp

### How to Reference Code
```python
# Based on Azure-Samples official example
# Source: https://github.com/Azure-Samples/[repo-name]

# [Your code with proper attribution]
```

## Verification Checklist

Before publishing content with Microsoft documentation references:

- [ ] Link to current (not archived) documentation
- [ ] Verify facts against official docs (not third-party blogs)
- [ ] Check publication date (preferably within last year)
- [ ] Confirm feature is Generally Available (not just preview)
- [ ] Test code samples if included
- [ ] Cite sources properly
- [ ] Note versions (e.g., "Azure Kubernetes Service 1.28+")

## Common Microsoft Terminology

### Use Official Names
- ✅ "Azure Container Apps" (not "Container Apps")
- ✅ "Microsoft Entra ID" (not "Azure AD" - name changed 2023)
- ✅ "Azure OpenAI Service" (not just "OpenAI on Azure")
- ✅ "Azure Cosmos DB" (not "CosmosDB")

### Service Abbreviations
Only use after first mention:
- Azure Kubernetes Service (AKS)
- Azure Container Apps (ACA)
- Azure Storage (no abbreviation)
- Azure Functions (no abbreviation)

## Example: Well-Cited Technical Content

```markdown
## How to Deploy Containers to Azure Container Apps

Azure Container Apps is a fully managed serverless platform for running 
containerized applications at scale [1].

### Key Benefits

According to Microsoft's official documentation [2], Container Apps provides:

- **Automatic scaling**: Scale to zero, or scale to thousands of instances
- **Built-in traffic splitting**: Enable blue-green deployments
- **Integrated monitoring**: Application Insights included
- **Managed identity**: No credential management required

### Architecture

Following Azure's Well-Architected Framework reliability pillar [3], 
we'll implement:

1. Health checks for automatic recovery
2. Multiple replicas for high availability
3. Distributed tracing for observability

### Implementation

```bash
# Create Container App (based on official quickstart [4])
az containerapp create \
  --name my-app \
  --resource-group my-rg \
  --environment my-env \
  --image myregistry.azurecr.io/my-app:latest
```

### References

[1] Azure Container Apps Overview:
https://learn.microsoft.com/en-us/azure/container-apps/overview

[2] Container Apps Features:
https://learn.microsoft.com/en-us/azure/container-apps/compare-options

[3] Well-Architected Framework - Reliability:
https://learn.microsoft.com/en-us/azure/well-architected/reliability/

[4] Quickstart - Deploy your first container app:
https://learn.microsoft.com/en-us/azure/container-apps/quickstart-portal
```

---

## Staying Current

### Monthly Tasks
- Review Azure Updates page
- Check new blog posts on Tech Community
- Scan research publications
- Update content with new features

### When Microsoft Docs Change
- Documentation is versioned and timestamped
- Some features may be deprecated
- Always verify against current docs before publishing
- Note in content: "Last verified: February 2026"

---

**Document Version**: 1.0  
**Last Updated**: February 2026  
**Purpose**: Guide for referencing official Microsoft documentation and research  
**Maintained By**: Content team - update quarterly
