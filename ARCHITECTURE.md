# StoryCircuit - Architecture Specification

**Version:** 1.0.0  
**Date:** February 11, 2026  
**Status:** Draft

## 1. Architecture Overview

### 1.1 Visual Architecture Diagram

For a comprehensive visual representation of the system architecture, see:

<img src="https://github.com/vrengar/storycircuit/blob/copilot/add-architecture-diagram/docs/architecture-diagram.svg" alt="StoryCircuit Architecture Diagram" width="100%">

*Complete system architecture showing all components, data flows, and Azure services*

### 1.2 System Context

```
┌──────────────────────────────────────────────────────────────┐
│                    StoryCircuit System                       │
│                                                              │
│  ┌──────────┐      ┌──────────┐      ┌─────────────────┐  │
│  │          │      │          │      │                 │  │
│  │  Web UI  │─────▶│  FastAPI │─────▶│  Azure AI       │  │
│  │ (Browser)│      │  Backend │      │  Foundry Agent  │  │
│  │          │◀─────│          │◀─────│  (StoryCircuit) │  │
│  └──────────┘      └────┬─────┘      └─────────────────┘  │
│                          │                                  │
│                          │                                  │
│                    ┌─────▼──────┐                          │
│                    │            │                          │
│                    │  Database  │                          │
│                    │ (Cosmos DB)│                          │
│                    │            │                          │
│                    └────────────┘                          │
└──────────────────────────────────────────────────────────────┘
```

### 1.3 Design Principles

1. **Separation of Concerns:** Clear boundaries between UI, API, business logic, and data
2. **Stateless Backend:** No session state in API layer for horizontal scaling
3. **Agent Abstraction:** Agent client isolated for easy swapping/testing
4. **Configuration-Driven:** Environment-based configuration (no hardcoded values)
5. **API-First:** Backend designed as REST API, consumable by any client

## 2. Component Architecture

### 2.1 Frontend Layer

**Technology:** HTML/CSS/JavaScript (with optional React/Vue if needed)

**Responsibilities:**
- User interface rendering
- Form validation
- API communication
- State management (local)
- Export/download handling

**Key Components:**
```
frontend/
├── index.html          # Main page
├── styles/
│   └── main.css       # Styling
├── scripts/
│   ├── app.js         # Main application logic
│   ├── api.js         # API client
│   └── utils.js       # Helper functions
└── assets/
    └── images/        # Icons, logos
```

### 2.2 Backend Layer (FastAPI)

**Technology:** Python 3.11+, FastAPI, Pydantic

**Responsibilities:**
- REST API endpoints
- Request validation
- Business logic orchestration
- Agent communication
- Database operations
- Error handling

**Key Modules:**
```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── requests.py         # Request models (Pydantic)
│   │   ├── responses.py        # Response models
│   │   └── database.py         # Database models
│   ├── services/
│   │   ├── agent_service.py    # Azure AI agent client
│   │   ├── content_service.py  # Content generation logic
│   │   └── export_service.py   # Export functionality
│   ├── repositories/
│   │   └── content_repo.py     # Database operations
│   ├── routers/
│   │   ├── content.py          # Content endpoints
│   │   ├── history.py          # History endpoints
│   │   └── health.py           # Health check
│   └── utils/
│       ├── logging.py          # Logging setup
│       └── exceptions.py       # Custom exceptions
└── tests/
    ├── unit/
    └── integration/
```

### 2.3 Agent Integration Layer

**Technology:** Azure AI Projects SDK

**Responsibilities:**
- Connection to Azure AI Foundry
- Request formatting for agent
- Response parsing
- Retry logic
- Error handling

**Implementation Pattern:**
```python
class AgentService:
    def __init__(self, endpoint: str, credential):
        self.client = AIProjectClient(endpoint, credential)
        
    async def generate_content(self, prompt: str) -> AgentResponse:
        # Agent communication logic
        pass
```

### 2.4 Data Layer

**Technology:** Azure Cosmos DB (NoSQL) or PostgreSQL

**Responsibilities:**
- Content persistence
- Query optimization
- Data integrity

**Schema Design (Cosmos DB):**

**Container: ContentGenerations**
```json
{
  "id": "uuid",
  "partitionKey": "userId",
  "topic": "string",
  "platforms": ["linkedin", "twitter"],
  "generatedContent": {
    "plan": {...},
    "outputs": {...},
    "notes": "..."
  },
  "metadata": {
    "userId": "string",
    "timestamp": "ISO8601",
    "agentVersion": "string",
    "duration": 2.5
  }
}
```

## 3. API Design

### 3.1 REST API Endpoints

**Base URL:** `/api/v1`

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/content/generate` | Generate content | Required |
| GET | `/content/history` | Get content history | Required |
| GET | `/content/{id}` | Get specific content | Required |
| GET | `/content/{id}/export` | Export content | Required |
| GET | `/health` | Health check | None |
| GET | `/health/ready` | Readiness check | None |

### 3.2 Request/Response Models

**POST /content/generate**

Request:
```json
{
  "topic": "AI agent orchestration patterns",
  "platforms": ["linkedin", "twitter", "github"],
  "audience": "software engineers",
  "additionalContext": "Focus on Microsoft tooling"
}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "content": {
    "plan": {
      "hook": "...",
      "narrativeFrame": "...",
      "keyPoints": [...],
      "example": "...",
      "cta": "..."
    },
    "outputs": {
      "twitter": {...},
      "linkedin": {...},
      "github": {...}
    },
    "notes": "..."
  },
  "metadata": {
    "generatedAt": "2026-02-11T10:30:00Z",
    "duration": 2.3
  }
}
```

## 4. Deployment Architecture

### 4.1 Azure Container Apps

**Configuration:**
- **Compute:** 0.5 vCPU, 1GB RAM per replica
- **Scaling:** Min 1, Max 10 replicas
- **Trigger:** HTTP requests per replica > 50
- **Ingress:** External, HTTPS only

**Components:**
```
┌─────────────────────────────────────────────┐
│        Azure Container Apps Environment     │
│                                             │
│  ┌────────────────────────────────────┐   │
│  │  StoryCircuit Container            │   │
│  │  - FastAPI backend + Static files  │   │
│  │  - Port 8000                       │   │
│  │  - Health: /health/ready           │   │
│  └────────────────────────────────────┘   │
│                                             │
│  Auto-scaling based on HTTP requests       │
└─────────────────────────────────────────────┘
         │                    │
         │                    │
    ┌────▼────┐        ┌──────▼──────┐
    │ Cosmos  │        │   Azure     │
    │   DB    │        │ AI Foundry  │
    └─────────┘        └─────────────┘
```

### 4.2 Infrastructure as Code

**Technology:** Bicep (Azure native)

**Resources:**
- Container Apps Environment
- Container App (StoryCircuit)
- Cosmos DB Account + Database + Container
- Container Registry
- Managed Identity
- Log Analytics Workspace
- Application Insights

## 5. Security Architecture

### 5.1 Authentication & Authorization

**Development:**
- No auth (local development)
- Environment flag: `AUTH_ENABLED=false`

**Production:**
- Azure AD authentication
- JWT bearer tokens
- Role-based access control (RBAC)

### 5.2 Secrets Management

**Azure Key Vault Integration:**
- `AZURE_AI_ENDPOINT` - Agent endpoint URL
- `COSMOS_CONNECTION_STRING` - Database connection
- `APPLICATION_INSIGHTS_KEY` - Monitoring key

**Access via:**
- Managed Identity (production)
- DefaultAzureCredential (development)

### 5.3 Network Security

- HTTPS only (TLS 1.2+)
- CORS configuration for frontend
- API rate limiting (100 req/min per user)
- DDoS protection via Azure

## 6. Data Flow

### 6.1 Content Generation Flow

```
1. User submits form → Frontend
2. Frontend validates → POST /api/v1/content/generate
3. Backend validates request (Pydantic)
4. ContentService orchestrates:
   a. Format prompt for agent
   b. Call AgentService.generate_content()
   c. AgentService → Azure AI Foundry
   d. Parse agent response
   e. ContentRepository.save()
   f. Return formatted response
5. Frontend displays results
6. User can export → GET /api/v1/content/{id}/export
```

### 6.2 History Retrieval Flow

```
1. User navigates to History → GET /api/v1/content/history
2. Backend queries Cosmos DB with filters
3. Repository returns list of content summaries
4. Frontend renders history list
5. User clicks item → GET /api/v1/content/{id}
6. Backend retrieves full content
7. Frontend displays details
```

## 7. Error Handling

### 7.1 Error Categories

| Category | HTTP Code | Handling |
|----------|-----------|----------|
| Validation | 400 | Return field-level errors |
| Authentication | 401 | Return auth challenge |
| Authorization | 403 | Return forbidden message |
| Not Found | 404 | Return resource not found |
| Agent Error | 502 | Retry + user message |
| Database Error | 503 | Retry + fallback |
| Server Error | 500 | Log + generic message |

### 7.2 Retry Strategy

**Agent Calls:**
- Max retries: 3
- Backoff: Exponential (1s, 2s, 4s)
- Retry on: 429, 500, 502, 503, 504

**Database Calls:**
- Max retries: 2
- Backoff: Fixed (1s)
- Retry on: Transient errors

## 8. Observability

### 8.1 Logging

**Log Levels:**
- DEBUG: Development only
- INFO: Request/response, business events
- WARNING: Degraded performance
- ERROR: Failures requiring attention
- CRITICAL: System-wide issues

**Structured Logging:**
```python
logger.info("content_generated", extra={
    "content_id": content_id,
    "topic": topic,
    "platforms": platforms,
    "duration": duration,
    "user_id": user_id
})
```

### 8.2 Metrics

**Application Insights:**
- Request duration
- Agent call duration
- Database query duration
- Error rates
- Active users
- Content generation count

### 8.3 Tracing

**Distributed Tracing:**
- Correlation ID per request
- Track request through: Frontend → API → Agent → Database

## 9. Performance Considerations

### 9.1 Optimization Strategies

1. **Caching:** Redis for frequent queries (future)
2. **Database Indexing:** On userId, timestamp
3. **Async Operations:** All I/O operations use async/await
4. **Connection Pooling:** Reuse agent client connections
5. **Static File CDN:** Serve frontend from Azure CDN (future)

### 9.2 Performance Targets

- API response time: < 5s (P95)
- Database query: < 100ms (P95)
- Frontend load: < 2s (P95)
- Agent response: < 4s (P95)

## 10. Disaster Recovery

### 10.1 Backup Strategy

**Cosmos DB:**
- Continuous backup (7 days)
- Point-in-time restore
- Geo-redundancy (optional)

### 10.2 Recovery Procedures

1. **Agent Unavailable:** Return cached/fallback message, queue requests
2. **Database Unavailable:** Graceful degradation, read-only mode
3. **Total Outage:** Azure Container Apps auto-restart

## 11. Testing Strategy

### 11.1 Test Levels

1. **Unit Tests:** Individual functions/methods (70% coverage)
2. **Integration Tests:** API endpoints + database
3. **E2E Tests:** Full user workflows (future)
4. **Load Tests:** 100+ concurrent users (future)

### 11.2 Test Mocking

- Mock Azure AI agent responses for unit tests
- Use test database for integration tests
- Mock external dependencies

## 12. Deployment Strategy

### 12.1 CI/CD Pipeline

**GitHub Actions:**
1. Trigger on: Push to main, PR
2. Steps:
   - Lint code (flake8, black)
   - Run unit tests
   - Build Docker image
   - Push to Azure Container Registry
   - Deploy to Container Apps (staging)
   - Smoke tests
   - Deploy to production (manual approval)

### 12.2 Environments

- **Local:** Developer machine
- **Staging:** Azure Container Apps (pre-prod)
- **Production:** Azure Container Apps (prod)

## 13. Migration Strategy

### 13.1 Database Migrations

**Tool:** Alembic (if using SQL) or versioned scripts (Cosmos DB)

**Process:**
1. Create migration script
2. Test in staging
3. Apply to production (backward compatible)
4. Deploy new app version

## 14. Scalability Considerations

### 14.1 Horizontal Scaling

- Stateless API design enables unlimited replicas
- Database handles concurrent connections
- Agent rate limits considered

### 14.2 Vertical Scaling

- Increase container vCPU/memory if needed
- Database throughput adjustment (RU/s for Cosmos DB)

## 15. Technology Alternatives

| Component | Current Choice | Alternatives |
|-----------|----------------|--------------|
| Backend | FastAPI | Flask, Django, Node.js |
| Database | Cosmos DB | PostgreSQL, MongoDB |
| Frontend | Vanilla JS | React, Vue, Svelte |
| Deployment | Container Apps | App Service, AKS, Functions |
| Auth | Azure AD | Auth0, Cognito |

---

**Document Control:**
- Created: February 11, 2026
- Last Modified: February 11, 2026
- Next Review: March 11, 2026
