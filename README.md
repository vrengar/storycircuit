# StoryCircuit - Social Media Communication Agent

A Microsoft-aligned Technical Narrative Architect Agent that transforms complex technical topics into clear, platform-optimized social media content.

## 🎯 Overview

StoryCircuit helps technical practitioners generate high-quality social content across multiple platforms (LinkedIn, X/Twitter, GitHub, Blog) using Azure AI Foundry.

## 📸 Demo & Screenshots

### Application Interface
<img src="https://github.com/vrengar/storycircuit/blob/main/docs/screenshot-ui.png" alt="StoryCircuit UI" width="800">

*Clean, intuitive interface for generating platform-optimized content with casual shorthand input support*

### Generated Content Example
<img src="https://github.com/vrengar/storycircuit/blob/main/docs/screenshot-output.png" alt="Content Output" width="800">

*Professional content display with copy-to-clipboard buttons, styled hashtags, and formatted markdown*

**Sample Output:** See [example-output.md](docs/example-output.md) for a full content generation example.

## 🏆 Project Highlights

**Description:** StoryCircuit is an AI-powered technical narrative architect that transforms complex technical topics into platform-optimized social media content. Users input casual shorthand requests (e.g., "AKS security in prod") and the agent generates distinct, professional content tailored for LinkedIn, Twitter, GitHub, or Blog platforms. Built with Azure AI Foundry's agent framework, it employs Chain-of-Thought reasoning patterns with web search and file search capabilities to ground responses in current, verified information. The system stores generated content in Azure Cosmos DB for retrieval and features a modern web interface with one-click copy-to-clipboard functionality.

**Primary Language:** Python

**Key Technologies:**
- Azure AI Foundry - AI agent orchestration with web search and file search tools
- Azure Cosmos DB - NoSQL database for content storage
- FastAPI - Python web framework for REST API
- Azure AI Projects SDK - Agent communication with built-in tool capabilities
- Uvicorn - ASGI server for async request handling
- Knowledge Base - 987-line agent instructions with Chain-of-Thought reasoning patterns

**Technical Highlights:**
- Azure AI Foundry agent configured with web search tool for real-time access to current Microsoft documentation and official sources
- Implements sophisticated Chain-of-Thought reasoning with multiple patterns (ReAct, Self-Reflection) encoded in 987-line knowledge base
- Intelligently interprets casual shorthand requests (e.g., "AKS security in prod") and generates truly distinct platform-optimized outputs—not just reformatted duplicates
- File search capability against comprehensive knowledge base with Azure abbreviations, brand guidelines, and platform-specific best practices

## ✨ Features

- **Multi-platform content generation** - LinkedIn posts, Twitter threads, GitHub documentation, blog posts
- **Content history & versioning** - Track all generated content with full metadata
- **Export capabilities** - Download as Markdown, JSON, or platform-specific formats
- **Web UI + REST API** - User-friendly interface backed by FastAPI
- **Azure native** - Deploys to Azure Container Apps with Cosmos DB

## 📋 Specifications

- **[Requirements Specification](REQUIREMENTS.md)** - Full functional and non-functional requirements
- **[Architecture Specification](ARCHITECTURE.md)** - System design and component architecture
- **[API Specification](API_SPEC.md)** - Complete REST API documentation
- **[Security & Compliance Guidelines](SECURITY.md)** - Security requirements and best practices

## 🔒 Security & Compliance

**IMPORTANT:** This application is designed for **public, general-level content only**.

### Quick Compliance Checklist
- ❌ No API keys, passwords, or credentials
- ❌ No customer data or PII (names, emails, phone numbers)
- ❌ No Microsoft Confidential information
- ✅ Only public, General-level technical content

All content is **automatically scanned** for sensitive information. See [SECURITY.md](SECURITY.md) for complete guidelines.

### Security Features
- Azure AD authentication (no hardcoded keys)
- Automated content validation
- Security headers on all responses
- Input sanitization
- Compliance monitoring

## 🏗️ Project Structure

```
social-media-agent/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── config.py          # Configuration management
│   │   ├── models/            # Pydantic models
│   │   ├── services/          # Business logic
│   │   ├── repositories/      # Data access layer
│   │   ├── routers/           # API endpoints
│   │   └── utils/             # Helper utilities
│   ├── tests/                 # Test suite
│   └── requirements.txt       # Python dependencies
├── frontend/                   # Web UI
│   ├── index.html
│   ├── styles/
│   └── scripts/
├── infra/                      # Infrastructure as Code
│   ├── main.bicep             # Azure resources
│   └── main.parameters.json
├── .github/
│   └── workflows/             # CI/CD pipelines
├── Dockerfile                  # Container definition
├── azure.yaml                  # Azure Developer CLI config
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Azure subscription
- Azure AI Foundry agent deployed
- Azure CLI installed

### Local Development

**Prerequisites:** Python 3.11+, Azure subscription, Azure AI Foundry project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vrengar/storycircuit.git
   cd social-media-agent
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure AI Foundry endpoint and credentials
   ```

3. **Install dependencies:**
   ```bash
5. **Start the server:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

6. **Access the application:**
   - Web UI: http://localhost:8001
   - API Docs: http://localhost:8001/docs
   - ReDoc: http://localhost:8001/redoc

7. **Generate content:** Enter a technical topic (e.g., "Container Apps scaling") and select target platforms
4. **Run the application:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application:**
   - Web UI: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Azure Deployment

**Using Azure Developer CLI (azd):**

```bash
# Initialize (first time only)
azd init

# Provision infrastructure and deploy
azd up

# Or separately:
azd provision  # Create Azure resources
azd deploy     # Deploy application
```

**Manual deployment:**

See [deployment documentation](docs/DEPLOYMENT.md) for detailed instructions.

## 🧪 Testing

```bash
# Run all tests
pytest backend/tests/

# Run with coverage
pytest backend/tests/ --cov=app --cov-report=html

# Run specific test categories
pytest backend/tests/unit/
pytest backend/tests/integration/
```

## 📊 API Usage

### Generate Content

```bash
curl -X POST http://localhost:8000/api/v1/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI agent orchestration patterns",
    "platforms": ["linkedin", "twitter"],
    "audience": "software engineers"
  }'
```

### View History

```bash
curl http://localhost:8000/api/v1/content/history?limit=10
```

### Export Content

```bash
curl http://localhost:8000/api/v1/content/{id}/export?format=markdown \
  -o export.md
```

See [API_SPEC.md](API_SPEC.md) for complete API documentation.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AZURE_AI_ENDPOINT` | Azure AI Foundry endpoint URL | Yes | - |
| `AZURE_TENANT_ID` | Azure tenant ID | Yes | - |
| `COSMOS_ENDPOINT` | Cosmos DB endpoint | Yes | - |
| `COSMOS_DATABASE` | Database name | No | `storycircuit` |
| `COSMOS_CONTAINER` | Container name | No | `content` |
| `AUTH_ENABLED` | Enable Azure AD auth | No | `false` |
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `CORS_ORIGINS` | Allowed CORS origins | No | `*` |

### Azure Resources

- **Container Apps** - Host the application
- **Cosmos DB** - Store content history
- **Container Registry** - Store Docker images
- **Application Insights** - Monitoring and logging
- **Key Vault** - Secrets management

## 📚 Documentation

- [Requirements Specification](REQUIREMENTS.md)
- [Architecture Specification](ARCHITECTURE.md)
- [API Specification](API_SPEC.md)
- [Deployment Guide](docs/DEPLOYMENT.md) *(coming soon)*
- [Development Guide](docs/DEVELOPMENT.md) *(coming soon)*

## 🤝 Contributing

This project follows spec-driven development:

1. Read specifications in `REQUIREMENTS.md`, `ARCHITECTURE.md`, `API_SPEC.md`
2. Create feature branch from main
3. Implement according to specs
4. Add tests (maintain 70%+ coverage)
5. Submit pull request with spec references

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋 Support

For issues or questions:
- Create an issue: [GitHub Issues](https://github.com/vrengar/storycircuit/issues)
- View documentation in this repository
- Check existing issues for solutions

## 🗺️ Roadmap

- **v1.0** (Current)
  - Multi-platform content generation
  - Content history & versioning
  - Export capabilities
  - Web UI + API

- **v1.1** (Planned)
  - Content templates
  - Batch processing
  - Enhanced analytics

- **v2.0** (Future)
  - Direct social posting
  - Collaborative editing
  - Mobile app

---

**Built with ❤️ using Azure AI Foundry**
