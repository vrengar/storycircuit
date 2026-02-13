# StoryCircuit - Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Azure Deployment](#azure-deployment)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Azure CLI** - [Install Guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Azure Developer CLI (azd)** - [Install Guide](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd)
- **Docker** (optional, for containerization) - [Download](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download](https://git-scm.com/downloads)

### Azure Requirements
- Active  Azure subscription
- Azure AI Foundry project with StoryCircuit agent deployed
- Appropriate permissions to create resources

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd social-media-agent
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example backend/.env
```

Edit `backend/.env` with your Azure credentials:

```env
# Azure AI Foundry Configuration
AZURE_AI_ENDPOINT=https://your-ai-service.services.ai.azure.com/api/projects/your-project
AZURE_TENANT_ID=your-tenant-id

# Azure Cosmos DB Configuration
COSMOS_ENDPOINT=https://your-cosmos-account.documents.azure.com:443/
COSMOS_DATABASE=storycircuit
COSMOS_CONTAINER=content

# Authentication (set to false for local development)
AUTH_ENABLED=false

# Application Configuration
LOG_LEVEL=INFO
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Agent Configuration
AGENT_NAME=Social-Media-Communication-Agent
```

### 4. Run the Application Locally

```bash
# From project root
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the application:
- **Web UI:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **API (Interactive):** http://localhost:8000/redoc

### 5. Run Tests

```bash
# Run all tests
pytest backend/tests/

# Run with coverage
pytest backend/tests/ --cov=app --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

---

## Azure Deployment

### Method 1: Azure Developer CLI (Recommended)

#### 1. Initialize Azure Developer CLI

```bash
# Login to Azure
azd auth login

# Initialize project (first time only)
azd init
```

When prompted:
- **Environment name:** Choose a name (e.g., `dev`, `staging`, `prod`)
- **Location:** Choose an Azure region (e.g., `eastus`)

#### 2. Set Required Configuration

```bash
# Set Azure AI Foundry endpoint
azd env set AZURE_AI_ENDPOINT "https://your-ai-service.services.ai.azure.com/api/projects/your-project"

# Set tenant ID
azd env set AZURE_TENANT_ID "your-tenant-id"
```

#### 3. Provision Infrastructure

```bash
# Provision all Azure resources
azd provision
```

This creates:
- Resource Group
- Container Apps Environment
- Container Registry
- Cosmos DB account, database, and container
- Log Analytics Workspace
- Application Insights
- Container App (StoryCircuit)

#### 4. Deploy Application

```bash
# Build and deploy
azd deploy

# Or do both provision + deploy
azd up
```

#### 5. Access Deployed Application

```bash
# Get the application URL
azd env get-values | grep CONTAINER_APP_URL
```

Visit the URL in your browser.

### Method 2: Manual Deployment

#### 1. Create Azure Resources

```bash
# Set variables
RESOURCE_GROUP="rg-storycircuit"
LOCATION="eastus"
ENVIRONMENT_NAME="prod"

# Login
az login

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy infrastructure using Bicep
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file infra/main.bicep \
  --parameters environmentName=$ENVIRONMENT_NAME location=$LOCATION
```

#### 2. Build and Push Docker Image

```bash
# Get container registry name from deployment output
REGISTRY_NAME=$(az deployment group show \
  --resource-group $RESOURCE_GROUP \
  --name main \
  --query properties.outputs.AZURE_CONTAINER_REGISTRY_NAME.value \
  --output tsv)

# Login to registry
az acr login --name $REGISTRY_NAME

# Build image
docker build -t storycircuit:latest .

# Tag image
docker tag storycircuit:latest $REGISTRY_NAME.azurecr.io/storycircuit:latest

# Push image
docker push $REGISTRY_NAME.azurecr.io/storycircuit:latest
```

#### 3. Update Container App

```bash
# Get container app name
APP_NAME=$(az deployment group show \
  --resource-group $RESOURCE_GROUP \
  --name main \
  --query properties.outputs.AZURE_CONTAINER_APP_NAME.value \
  --output tsv)

# Update container app
az containerapp update \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --image $REGISTRY_NAME.azurecr.io/storycircuit:latest
```

---

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AZURE_AI_ENDPOINT` | Azure AI Foundry endpoint URL | ✅ | - |
| `AZURE_TENANT_ID` | Azure tenant ID | ✅ | - |
| `COSMOS_ENDPOINT` | Cosmos DB endpoint | ✅ | - |
| `COSMOS_DATABASE` | Database name | ❌ | `storycircuit` |
| `COSMOS_CONTAINER` | Container name | ❌ | `content` |
| `AUTH_ENABLED` | Enable Azure AD authentication | ❌ | `false` |
| `LOG_LEVEL` | Logging level | ❌ | `INFO` |
| `ENVIRONMENT` | Environment name | ❌ | `development` |
| `CORS_ORIGINS` | Allowed CORS origins | ❌ | `*` |
| `AGENT_NAME` | Agent name in Azure AI Foundry | ❌ | `Social-Media-Communication-Agent` |
| `AGENT_TIMEOUT` | Agent request timeout (seconds) | ❌ | `30` |
| `AGENT_MAX_RETRIES` | Max retry attempts | ❌ | `3` |
| `RATE_LIMIT_PER_MINUTE` | API rate limit | ❌ | `100` |

### Azure Resources Configuration

#### Container App Scaling

Edit in `infra/core/container-app.bicep`:

```bicep
minReplicas: 1     // Minimum instances
maxReplicas: 10    // Maximum instances
```

#### Cosmos DB Throughput

Edit in `infra/core/cosmos-db.bicep`:

```bicep
offer_throughput: 400  // Request Units per second
```

---

## Troubleshooting

### Common Issues

#### 1. Agent Connection Failed

**Error:** `Agent service temporarily unavailable`

**Solutions:**
- Verify `AZURE_AI_ENDPOINT` is correct
- Check Azure AI Foundry agent is deployed and running
- Ensure managed identity has permissions to access agent
- Check network connectivity

```bash
# Test endpoint
curl -H "Authorization: Bearer $(az account get-access-token --query accessToken -o tsv)" \
  $AZURE_AI_ENDPOINT
```

#### 2. Database Connection Failed

**Error:** `Database temporarily unavailable`

**Solutions:**
- Verify `COSMOS_ENDPOINT` is correct
- Check Cosmos DB is running
- Ensure managed identity has read/write permissions
- Verify database and container exist

```bash
# List databases
az cosmosdb sql database list \
  --account-name $COSMOS_ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP
```

#### 3. CORS Errors in Browser

**Error:** `Access to fetch blocked by CORS policy`

**Solutions:**
- Add frontend origin to `CORS_ORIGINS` environment variable
- For local development: `CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000`
- For production: Set to your actual domain

#### 4. Container App Not Starting

**Check logs:**

```bash
az containerapp logs show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --follow
```

**Common causes:**
- Missing environment variables
- Invalid configuration
- Image pull errors
- Insufficient memory/CPU

#### 5. High Latency

**Optimization steps:**
1. Increase Container App replicas
2. Increase Cosmos DB RU/s
3. Enable Application Insights for diagnostics
4. Check agent response times
5. Consider adding caching layer (Redis)

### Debugging

#### Enable Debug Logging

```bash
# Set log level to DEBUG
azd env set LOG_LEVEL DEBUG
azd deploy
```

#### View Application Logs

```bash
# Container App logs
az containerapp logs show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --tail 100

# Application Insights queries
az monitor app-insights query \
  --app $APP_INSIGHTS_NAME \
  --analytics-query "traces | where timestamp > ago(1h) | order by timestamp desc"
```

#### Health Checks

```bash
# Basic health
curl https://your-app-url/api/v1/health

# Readiness (includes dependencies)
curl https://your-app-url/api/v1/health/ready
```

---

## Monitoring

### Application Insights

1. Navigate to Azure Portal → Application Insights
2. Key metrics to monitor:
   - **Request duration:** API response times
   - **Failed requests:** Error rate
   - **Dependencies:** Agent/DB call durations
   - **Exceptions:** Application errors

### Container App Metrics

```bash
# CPU usage
az monitor metrics list \
  --resource $CONTAINER_APP_ID \
  --metric "CpuUsage"

# Memory usage
az monitor metrics list \
  --resource $CONTAINER_APP_ID \
  --metric "MemoryUsage"

# Request count
az monitor metrics list \
  --resource $CONTAINER_APP_ID \
  --metric "Requests"
```

### Cosmos DB Metrics

- **Request Units:** Monitor RU/s consumption
- **Latency:** Track read/write latency
- **Throttling:** Monitor 429 errors

---

## Scaling

### Manual Scaling

```bash
# Scale Container App
az containerapp update \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --min-replicas 2 \
  --max-replicas 20
```

### Auto-scaling Rules

Edit in `infra/core/container-app.bicep`:

```bicep
scale: {
  minReplicas: 1
  maxReplicas: 10
  rules: [
    {
      name: 'http-rule'
      http: {
        metadata: {
          concurrentRequests: '50'
        }
      }
    }
  ]
}
```

---

## Security Best Practices

1. **Enable Azure AD Authentication** in production
2. **Use Managed Identity** for Azure service access
3. **Store secrets** in Azure Key Vault
4. **Enable HTTPS only**
5. **Restrict CORS origins** to specific domains
6. **Monitor and alert** on security events
7. **Regular updates** of dependencies
8. **Use network restrictions** (VNet integration)

---

## Support

For issues or questions:
- Create an issue in the repository
- Check [API Documentation](API_SPEC.md)
- Review [Architecture Documentation](ARCHITECTURE.md)

---

**Last Updated:** February 11, 2026
