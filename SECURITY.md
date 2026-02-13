# Security & Compliance Guidelines

## Overview
StoryCircuit is designed to generate **public, general-level technical content only**. This document outlines the security measures and compliance requirements for using the application.

## Security Requirements

### ❌ Prohibited Content
The following types of information **MUST NOT** be entered into the application:

1. **Credentials & Secrets**
   - API keys
   - Passwords
   - Access tokens
   - Connection strings
   - Private keys
   - Certificates

2. **Personal Identifiable Information (PII)**
   - Customer names
   - Email addresses
   - Phone numbers
   - Social Security Numbers
   - Credit card information
   - Home addresses
   - IP addresses

3. **Microsoft Confidential Information**
   - Internal roadmaps
   - Unreleased product details
   - Customer-specific implementations
   - Internal metrics or data
   - Proprietary algorithms
   - Any content marked "Microsoft Confidential"

4. **Restricted Data**
   - Customer data
   - Internal-only documentation
   - Private repository code
   - Non-public Azure subscription IDs
   - Resource-specific identifiers

### ✅ Acceptable Content
- Public technical concepts
- General best practices
- Publicly available Azure services
- Open-source technologies
- Industry-standard patterns
- Educational technical content

## Automated Security Controls

### Content Validation
All user input is automatically validated for:
- API keys and credentials patterns
- Email addresses
- Phone numbers
- Social Security Numbers
- Credit card numbers
- IP addresses
- Azure subscription GUIDs
- Confidential markers ("Microsoft Confidential", "Internal Only", etc.)

### Security Headers
All HTTP responses include security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security`
- `Content-Security-Policy`
- `Referrer-Policy`

### Authentication
- Azure AD authentication for all Azure services (Cosmos DB, AI Foundry)
- No hardcoded credentials or API keys
- Environment variables for configuration (never committed to git)

## Configuration Security

### Environment Variables
Create a `.env` file (never commit to git) with:

```env
# Azure AI Foundry - uses Azure AD, no keys required
AZURE_AI_ENDPOINT=https://your-ai-service.services.ai.azure.com/...

# Cosmos DB - uses Azure AD, no keys required
COSMOS_ENDPOINT=https://your-cosmos-account.documents.azure.com:443/
COSMOS_DATABASE=storycircuit
COSMOS_CONTAINER=content
```

**NEVER** include:
- `COSMOS_KEY` - Use Azure AD authentication instead
- `AZURE_AI_KEY` - Use Azure AD authentication instead
- Any other secrets or credentials

### Git Security
The `.gitignore` file excludes:
- `.env` files
- `*.key` files
- `.azure/` directory
- `*.azureauth` files

**Before committing code:**
1. Run `git status` to verify no sensitive files are staged
2. Review changed files for any hardcoded secrets
3. Use `git diff` to check file contents

## Data Handling

### User Data
- User ID: Non-PII identifier (e.g., `dev-user@example.com` in dev)
- No personal information stored
- All content is treated as public, general-level

### Storage
- **Cosmos DB**: Stores generated content only
- **No sensitive data**: Never store credentials, PII, or confidential information
- **Azure AD RBAC**: All database access uses role-based authentication

### Data Retention
- Content is stored indefinitely until manually deleted
- Soft delete supported (not implemented by default)

## Deployment Security

### Production Checklist
Before deploying to production:

- [ ] Remove all test/development credentials
- [ ] Verify `.env` files are not deployed
- [ ] Enable Azure AD authentication for all services
- [ ] Configure managed identity for App Service
- [ ] Set up Azure Key Vault for any required secrets
- [ ] Enable Application Insights for monitoring
- [ ] Configure CORS for production domains only
- [ ] Review and test all security headers
- [ ] Enable HTTPS only
- [ ] Set up DDoS protection

### Azure Resources
- **Cosmos DB**: Configure with local key auth disabled (Azure AD only)
- **AI Foundry**: Use system-assigned managed identity
- **App Service**: Enable managed identity and Key Vault references

## Incident Response

### If Sensitive Data is Detected
1. **Immediately stop** content generation
2. **Delete** any generated content containing sensitive data
3. **Report** to security team
4. **Review** logs to identify source

### If Credentials are Exposed
1. **Immediately rotate** the compromised credential
2. **Remove** from git history if committed
3. **Audit** access logs for unauthorized use
4. **Report** incident per company policy

## Reporting Security Issues

If you discover a security vulnerability:
1. **Do not** create a public GitHub issue
2. **Report** to: [security contact email]
3. **Include**: Description, steps to reproduce, potential impact

## Compliance

This application complies with:
- Microsoft Security Development Lifecycle (SDL)
- Azure Security Best Practices
- GDPR (no PII processing)
- SOC 2 (when using Azure services)

## Monitoring

### Security Logging
The application logs:
- Content validation failures
- Security header additions
- Authentication attempts
- API request patterns

### Alerts
Configure alerts for:
- Unusual content validation failures
- Multiple failed authentication attempts
- Unexpected error rates

## Developer Guidelines

### Code Review Checklist
- [ ] No hardcoded credentials
- [ ] No PII in logs or error messages
- [ ] Input validation for all user data
- [ ] Security headers on all responses
- [ ] Azure AD authentication only
- [ ] No sensitive data in exceptions

### Testing
- Test with intentionally sensitive input to verify blocking
- Verify security headers in responses
- Test Azure AD authentication flows
- Validate error messages don't leak info

## References

- [Microsoft Security Development Lifecycle](https://www.microsoft.com/en-us/securityengineering/sdl/)
- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/fundamentals/best-practices-and-patterns)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Azure AD Authentication](https://docs.microsoft.com/en-us/azure/active-directory/develop/)

---

**Last Updated**: February 2026  
**Document Owner**: Development Team
