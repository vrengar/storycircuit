"""
Configuration management for StoryCircuit application.
Loads settings from environment variables with validation.
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Mock Mode (for development without Azure)
    use_mock_services: bool = False
    use_mock_database: bool = False
    
    # Azure AI Configuration (optional if using mock services)
    azure_ai_endpoint: Optional[str] = None
    azure_ai_project_name: Optional[str] = None
    azure_tenant_id: Optional[str] = None
    agent_name: str = "Social-Media-Communication-Agent"
    agent_timeout: int = 30
    agent_max_retries: int = 3
    
    # Database Configuration (optional if using mock services)
    cosmos_endpoint: Optional[str] = None
    cosmos_key: Optional[str] = None
    cosmos_database: str = "storycircuit"
    cosmos_container: str = "content"
    
    # Authentication
    auth_enabled: bool = False
    
    # Application Configuration
    log_level: str = "INFO"
    environment: str = "development"
    
    # CORS Configuration
    cors_origins: str = "*"
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    
    # Optional: Application Insights
    applicationinsights_connection_string: Optional[str] = None
    
    # Optional: Azure Key Vault
    azure_key_vault_url: Optional[str] = None
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() == "production"
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins into a list."""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid re-reading environment variables.
    """
    return Settings()
