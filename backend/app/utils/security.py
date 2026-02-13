"""
Security and content sanitization utilities
Ensures compliance with:
- No API keys, passwords, or credentials in content
- No customer data or PII
- No Microsoft Confidential information
- Only public, General-level content
"""
import re
from typing import Dict, List, Tuple

# Patterns to detect sensitive information
SENSITIVE_PATTERNS = {
    "api_key": re.compile(r'(api[_-]?key|apikey)[\'"\s:=]+[a-zA-Z0-9_-]{20,}', re.IGNORECASE),
    "password": re.compile(r'(password|passwd|pwd)[\'"\s:=]+\S+', re.IGNORECASE),
    "secret": re.compile(r'(secret|token|auth)[\'"\s:=]+[a-zA-Z0-9_-]{20,}', re.IGNORECASE),
    "connection_string": re.compile(r'(DefaultEndpointsProtocol|AccountKey|SharedAccessSignature)=', re.IGNORECASE),
    "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
    "phone": re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
    "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
    "credit_card": re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
    "ip_address": re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
    "azure_subscription_id": re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.IGNORECASE),
    "confidential_marker": re.compile(r'\b(confidential|internal|proprietary|msft\s+confidential)\b', re.IGNORECASE),
}

# Warning indicators for potentially sensitive content
WARNING_KEYWORDS = [
    "confidential", "internal only", "do not share", "proprietary",
    "customer name", "personal data", "private", "restricted",
    "msft confidential", "microsoft confidential"
]


class ContentSecurityValidator:
    """Validates content for security and compliance"""
    
    @staticmethod
    def scan_for_sensitive_data(text: str) -> Tuple[bool, List[str]]:
        """
        Scan text for sensitive information
        Returns: (is_safe, list of detected issues)
        """
        issues = []
        
        for pattern_name, pattern in SENSITIVE_PATTERNS.items():
            matches = pattern.findall(text)
            if matches:
                issues.append(f"Detected potential {pattern_name.replace('_', ' ')}")
        
        # Check for warning keywords
        text_lower = text.lower()
        for keyword in WARNING_KEYWORDS:
            if keyword in text_lower:
                issues.append(f"Contains restricted keyword: '{keyword}'")
        
        is_safe = len(issues) == 0
        return is_safe, issues
    
    @staticmethod
    def sanitize_user_input(text: str) -> str:
        """
        Remove potential sensitive patterns from user input
        """
        sanitized = text
        
        # Remove email addresses
        sanitized = re.sub(SENSITIVE_PATTERNS["email"], "[EMAIL-REMOVED]", sanitized)
        
        # Remove phone numbers
        sanitized = re.sub(SENSITIVE_PATTERNS["phone"], "[PHONE-REMOVED]", sanitized)
        
        # Remove SSN
        sanitized = re.sub(SENSITIVE_PATTERNS["ssn"], "[SSN-REMOVED]", sanitized)
        
        # Remove credit cards
        sanitized = re.sub(SENSITIVE_PATTERNS["credit_card"], "[CARD-REMOVED]", sanitized)
        
        # Remove IP addresses
        sanitized = re.sub(SENSITIVE_PATTERNS["ip_address"], "[IP-REMOVED]", sanitized)
        
        return sanitized
    
    @staticmethod
    def validate_content_request(topic: str, platforms: List[str]) -> Tuple[bool, str]:
        """
        Validate content request before processing
        Returns: (is_valid, error_message)
        """
        if not topic or len(topic.strip()) == 0:
            return False, "Topic cannot be empty"
        
        if len(topic) > 500:
            return False, "Topic is too long (max 500 characters)"
        
        # Scan topic for sensitive data
        is_safe, issues = ContentSecurityValidator.scan_for_sensitive_data(topic)
        if not is_safe:
            return False, f"Topic contains restricted content: {', '.join(issues)}"
        
        # Validate platforms
        allowed_platforms = ["linkedin", "twitter", "github", "blog"]
        for platform in platforms:
            if platform.lower() not in allowed_platforms:
                return False, f"Invalid platform: {platform}"
        
        return True, ""
    
    @staticmethod
    def get_security_disclaimer() -> str:
        """Get security disclaimer for UI"""
        return """
⚠️ SECURITY NOTICE:
• Do not enter API keys, passwords, or credentials
• Do not include customer names, emails, or PII
• Do not include Microsoft Confidential information
• Only use public, General-level content
✅ Content is automatically scanned for compliance
"""


class SecurityHeaders:
    """Security headers for HTTP responses"""
    
    @staticmethod
    def get_headers() -> Dict[str, str]:
        """Get recommended security headers"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
        }
