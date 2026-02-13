# StoryCircuit - API Specification

**Version:** 1.0.0  
**Date:** February 11, 2026  
**OpenAPI Version:** 3.0.3

## 1. Overview

### 1.1 Base Information

- **Base URL:** `https://storycircuit.azurecontainerapps.io/api/v1`
- **Protocol:** HTTPS only
- **Authentication:** Bearer token (Azure AD) - Optional in development
- **Content-Type:** `application/json`
- **API Version:** v1

### 1.2 Rate Limits

- **Authenticated Users:** 100 requests/minute
- **Unauthenticated (dev):** 20 requests/minute

## 2. Authentication

### 2.1 Development Mode (No Auth)

```http
GET /api/v1/content/history
```

### 2.2 Production Mode (Azure AD)

```http
GET /api/v1/content/history
Authorization: Bearer {JWT_TOKEN}
```

## 3. API Endpoints

---

### 3.1 POST /content/generate

Generate platform-optimized content from a technical topic.

**Request:**

```http
POST /api/v1/content/generate
Content-Type: application/json

{
  "topic": "Understanding AI agent orchestration patterns",
  "platforms": ["linkedin", "twitter", "github"],
  "audience": "software engineers",
  "additionalContext": "Focus on Microsoft Azure AI Foundry tools"
}
```

**Request Schema:**

```typescript
{
  topic: string;           // Required. Technical topic (3-500 chars)
  platforms: string[];     // Required. Valid: linkedin, twitter, github, blog
  audience?: string;       // Optional. Target audience description
  additionalContext?: string; // Optional. Extra context for agent
}
```

**Response (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "content": {
    "plan": {
      "hook": "Most teams struggle with AI agent orchestration—here's why...",
      "narrativeFrame": "Problem → Solution → Implementation",
      "keyPoints": [
        "Sequential vs parallel tool execution",
        "Error handling in multi-step workflows",
        "State management across agent calls"
      ],
      "example": "Picture a customer support agent that needs to...",
      "cta": "Try building your first orchestrated agent with Azure AI Foundry →"
    },
    "outputs": {
      "twitter": {
        "threadStructure": "7 tweets",
        "tweets": [
          {
            "order": 1,
            "content": "Most teams struggle with AI agent orchestration. Here's what I learned building production agents at scale 🧵",
            "characterCount": 138
          },
          {
            "order": 2,
            "content": "The core challenge: coordinating multiple tools while maintaining context and handling failures gracefully.",
            "characterCount": 128
          }
          // ...more tweets
        ]
      },
      "linkedin": {
        "shortVersion": {
          "content": "# Understanding AI Agent Orchestration\n\nMost teams...",
          "characterCount": 850,
          "estimatedReadTime": "2 min"
        },
        "longVersion": {
          "content": "# Understanding AI Agent Orchestration Patterns\n\nAfter building...",
          "characterCount": 2100,
          "estimatedReadTime": "5 min"
        },
        "carousel": {
          "slides": [
            {
              "slideNumber": 1,
              "title": "AI Agent Orchestration 101",
              "bullets": [
                "Why orchestration matters",
                "Common patterns",
                "Microsoft approach"
              ]
            }
            // ...more slides
          ]
        }
      },
      "github": {
        "readmeSnippet": "## Agent Orchestration Pattern\n\nThis implementation...",
        "releaseNotes": "### New: Agent Orchestration Support\n\n- Sequential execution\n- Parallel tool calling..."
      }
    },
    "notes": "Agent assumed audience has basic understanding of AI agents. Cross-verified orchestration patterns against Azure AI Foundry documentation."
  },
  "metadata": {
    "generatedAt": "2026-02-11T14:30:45.123Z",
    "duration": 3.2,
    "userId": "user@example.com",
    "agentVersion": "storycircuit-v1.0"
  }
}
```

**Error Responses:**

```json
// 400 Bad Request - Validation Error
{
  "detail": [
    {
      "loc": ["body", "topic"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}

// 502 Bad Gateway - Agent Error
{
  "detail": "Agent service temporarily unavailable. Please try again.",
  "errorCode": "AGENT_UNAVAILABLE",
  "retryAfter": 30
}

// 500 Internal Server Error
{
  "detail": "An unexpected error occurred. Please contact support.",
  "errorCode": "INTERNAL_ERROR",
  "traceId": "a1b2c3d4-e5f6-7890"
}
```

---

### 3.2 GET /content/history

Retrieve user's content generation history with optional filtering.

**Request:**

```http
GET /api/v1/content/history?limit=20&offset=0&platform=linkedin&sortBy=date&order=desc
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| limit | integer | No | 20 | Number of items (1-100) |
| offset | integer | No | 0 | Pagination offset |
| platform | string | No | all | Filter by platform |
| sortBy | string | No | date | Sort field (date, topic) |
| order | string | No | desc | Sort order (asc, desc) |
| startDate | string | No | - | ISO 8601 date filter |
| endDate | string | No | - | ISO 8601 date filter |

**Response (200 OK):**

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "topic": "AI agent orchestration patterns",
      "platforms": ["linkedin", "twitter", "github"],
      "generatedAt": "2026-02-11T14:30:45.123Z",
      "userId": "user@example.com",
      "summary": "Most teams struggle with AI agent orchestration—here's why..."
    },
    {
      "id": "660f9511-f30c-52e5-b827-557766551111",
      "topic": "Azure Container Apps best practices",
      "platforms": ["twitter"],
      "generatedAt": "2026-02-10T09:15:22.456Z",
      "userId": "user@example.com",
      "summary": "5 things I wish I knew before deploying to Azure Container Apps..."
    }
  ],
  "pagination": {
    "total": 47,
    "limit": 20,
    "offset": 0,
    "hasMore": true
  }
}
```

---

### 3.3 GET /content/{id}

Retrieve full details of a specific content generation.

**Request:**

```http
GET /api/v1/content/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "topic": "AI agent orchestration patterns",
  "platforms": ["linkedin", "twitter", "github"],
  "content": {
    "plan": { /* same as generate response */ },
    "outputs": { /* same as generate response */ },
    "notes": "..."
  },
  "metadata": {
    "generatedAt": "2026-02-11T14:30:45.123Z",
    "duration": 3.2,
    "userId": "user@example.com",
    "agentVersion": "storycircuit-v1.0"
  }
}
```

**Error Response (404 Not Found):**

```json
{
  "detail": "Content not found",
  "errorCode": "NOT_FOUND"
}
```

---

### 3.4 GET /content/{id}/export

Export content in specified format.

**Request:**

```http
GET /api/v1/content/550e8400-e29b-41d4-a716-446655440000/export?format=markdown&platform=all
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| format | string | No | markdown | Export format (markdown, json) |
| platform | string | No | all | Specific platform or all |

**Response (200 OK) - Markdown:**

```http
Content-Type: text/markdown
Content-Disposition: attachment; filename="storycircuit-export-550e8400.md"

# AI Agent Orchestration Patterns

## Plan
**Hook:** Most teams struggle with AI agent orchestration—here's why...
...
```

**Response (200 OK) - JSON:**

```http
Content-Type: application/json
Content-Disposition: attachment; filename="storycircuit-export-550e8400.json"

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "topic": "AI agent orchestration patterns",
  ...
}
```

---

### 3.5 DELETE /content/{id}

Delete a specific content generation (soft delete).

**Request:**

```http
DELETE /api/v1/content/550e8400-e29b-41d4-a716-446655440000
```

**Response (204 No Content):**

```
(No body)
```

**Error Response (404 Not Found):**

```json
{
  "detail": "Content not found",
  "errorCode": "NOT_FOUND"
}
```

---

### 3.6 GET /health

Basic health check endpoint.

**Request:**

```http
GET /api/v1/health
```

**Response (200 OK):**

```json
{
  "status": "healthy",
  "timestamp": "2026-02-11T15:00:00.000Z",
  "version": "1.0.0"
}
```

---

### 3.7 GET /health/ready

Readiness probe with dependency checks.

**Request:**

```http
GET /api/v1/health/ready
```

**Response (200 OK) - All Services Healthy:**

```json
{
  "status": "ready",
  "checks": {
    "database": "healthy",
    "agent": "healthy"
  },
  "timestamp": "2026-02-11T15:00:00.000Z"
}
```

**Response (503 Service Unavailable) - Degraded:**

```json
{
  "status": "not_ready",
  "checks": {
    "database": "healthy",
    "agent": "unhealthy"
  },
  "timestamp": "2026-02-11T15:00:00.000Z"
}
```

---

## 4. Data Models

### 4.1 ContentGenerationRequest

```typescript
interface ContentGenerationRequest {
  topic: string;              // 3-500 characters
  platforms: Platform[];      // At least 1, max 5
  audience?: string;          // Optional, max 200 chars
  additionalContext?: string; // Optional, max 1000 chars
}

type Platform = "linkedin" | "twitter" | "github" | "blog";
```

### 4.2 ContentGenerationResponse

```typescript
interface ContentGenerationResponse {
  id: string;                      // UUID
  status: "success" | "error";
  content: GeneratedContent;
  metadata: Metadata;
}

interface GeneratedContent {
  plan: ContentPlan;
  outputs: PlatformOutputs;
  notes: string;
}

interface ContentPlan {
  hook: string;
  narrativeFrame: string;
  keyPoints: string[];
  example: string;
  cta: string;
}

interface PlatformOutputs {
  twitter?: TwitterOutput;
  linkedin?: LinkedInOutput;
  github?: GitHubOutput;
  blog?: BlogOutput;
}

interface TwitterOutput {
  threadStructure: string;
  tweets: Tweet[];
}

interface Tweet {
  order: number;
  content: string;
  characterCount: number;
}

interface LinkedInOutput {
  shortVersion: {
    content: string;
    characterCount: number;
    estimatedReadTime: string;
  };
  longVersion: {
    content: string;
    characterCount: number;
    estimatedReadTime: string;
  };
  carousel?: {
    slides: CarouselSlide[];
  };
}

interface CarouselSlide {
  slideNumber: number;
  title: string;
  bullets: string[];
}

interface GitHubOutput {
  readmeSnippet: string;
  releaseNotes: string;
}

interface BlogOutput {
  content: string;
  characterCount: number;
  estimatedReadTime: string;
}

interface Metadata {
  generatedAt: string;      // ISO 8601
  duration: number;         // seconds
  userId: string;
  agentVersion: string;
}
```

### 4.3 ContentHistoryItem

```typescript
interface ContentHistoryItem {
  id: string;
  topic: string;
  platforms: Platform[];
  generatedAt: string;
  userId: string;
  summary: string;
}

interface ContentHistoryResponse {
  items: ContentHistoryItem[];
  pagination: {
    total: number;
    limit: number;
    offset: number;
    hasMore: boolean;
  };
}
```

### 4.4 Error Response

```typescript
interface ErrorResponse {
  detail: string | ValidationError[];
  errorCode?: string;
  traceId?: string;
  retryAfter?: number;
}

interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}
```

---

## 5. Error Codes

| Code | HTTP Status | Description | Action |
|------|-------------|-------------|--------|
| VALIDATION_ERROR | 400 | Invalid request format | Fix request body |
| UNAUTHORIZED | 401 | Missing/invalid token | Authenticate |
| FORBIDDEN | 403 | Insufficient permissions | Contact admin |
| NOT_FOUND | 404 | Resource doesn't exist | Check ID |
| RATE_LIMITED | 429 | Too many requests | Wait and retry |
| AGENT_UNAVAILABLE | 502 | Agent service down | Retry after delay |
| DATABASE_ERROR | 503 | Database unavailable | Retry |
| INTERNAL_ERROR | 500 | Unexpected error | Contact support |

---

## 6. Versioning

**Strategy:** URL path versioning

- Current: `/api/v1`
- Future: `/api/v2`

**Backward Compatibility:**
- v1 supported for 12 months after v2 release
- Breaking changes require new version
- Deprecation warnings in headers

---

## 7. CORS Configuration

**Allowed Origins (Production):**
- `https://storycircuit.azurecontainerapps.io`

**Allowed Origins (Development):**
- `http://localhost:8000`
- `http://127.0.0.1:8000`

**Allowed Methods:**
- GET, POST, DELETE, OPTIONS

**Allowed Headers:**
- Content-Type, Authorization

---

## 8. OpenAPI Schema

The complete OpenAPI 3.0 schema is available at:

```
GET /api/v1/openapi.json
```

Interactive API documentation (Swagger UI):

```
GET /docs
```

Alternative documentation (ReDoc):

```
GET /redoc
```

---

## 9. Client Examples

### 9.1 Python

```python
import requests

BASE_URL = "https://storycircuit.azurecontainerapps.io/api/v1"

def generate_content(topic: str, platforms: list[str]):
    response = requests.post(
        f"{BASE_URL}/content/generate",
        json={
            "topic": topic,
            "platforms": platforms,
            "audience": "software engineers"
        },
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()

# Usage
result = generate_content(
    topic="AI agent orchestration",
    platforms=["linkedin", "twitter"]
)
print(result["content"]["plan"]["hook"])
```

### 9.2 JavaScript

```javascript
const BASE_URL = "https://storycircuit.azurecontainerapps.io/api/v1";

async function generateContent(topic, platforms) {
  const response = await fetch(`${BASE_URL}/content/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      topic,
      platforms,
      audience: "software engineers",
    }),
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}

// Usage
generateContent("AI agent orchestration", ["linkedin", "twitter"])
  .then(result => console.log(result.content.plan.hook))
  .catch(error => console.error("Error:", error));
```

### 9.3 cURL

```bash
curl -X POST https://storycircuit.azurecontainerapps.io/api/v1/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI agent orchestration",
    "platforms": ["linkedin", "twitter"],
    "audience": "software engineers"
  }'
```

---

**Document Control:**
- Created: February 11, 2026
- Last Modified: February 11, 2026
- Next Review: March 11, 2026
