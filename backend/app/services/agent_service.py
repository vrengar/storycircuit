"""
Azure AI Agent Service.
Handles communication with Azure AI Foundry agent using azure-ai-projects SDK.
"""

import asyncio
from typing import Any, Optional
import structlog
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from ..config import Settings
from ..utils.exceptions import AgentServiceError, AgentTimeoutError

logger = structlog.get_logger(__name__)


class AgentService:
    """Service for interacting with Azure AI Foundry agent using SDK."""

    def __init__(self, settings: Settings):
        """
        Initialize agent service.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self._project_client: Optional[AIProjectClient] = None
        self._agent = None

    def _get_project_client(self) -> AIProjectClient:
        """Get or create AI Project Client."""
        if self._project_client is None:
            logger.info(
                "Initializing Azure AI Project Client",
                endpoint=self.settings.azure_ai_endpoint,
            )
            self._project_client = AIProjectClient(
                endpoint=self.settings.azure_ai_endpoint,
                credential=DefaultAzureCredential(),
            )
        return self._project_client

    def _get_agent(self):
        """Get agent by name from Azure AI Foundry."""
        if self._agent is None:
            client = self._get_project_client()
            logger.info(
                "Getting agent from Foundry by name",
                agent_name=self.settings.agent_name,
            )
            try:
                # Get agent by name - works for new Foundry agents
                self._agent = client.agents.get(agent_name=self.settings.agent_name)
                logger.info(
                    "Agent retrieved successfully",
                    agent_name=self._agent.name,
                    agent_id=self._agent.id,
                )

            except Exception as e:
                logger.error(
                    "Failed to get agent",
                    agent_name=self.settings.agent_name,
                    error=str(e),
                )
                raise AgentServiceError(
                    f"Failed to get agent '{self.settings.agent_name}': {str(e)}"
                )
        return self._agent

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True,
    )
    async def generate_content(
        self,
        topic: str,
        platforms: list[str],
        audience: Optional[str] = None,
        additional_context: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Generate content using Azure AI Foundry agent with SDK.

        Args:
            topic: Technical topic for content generation
            platforms: List of target platforms
            audience: Optional target audience
            additional_context: Optional additional context

        Returns:
            Generated content from agent

        Raises:
            AgentServiceError: If agent communication fails
            AgentTimeoutError: If request times out
        """
        try:
            # Build prompt for agent
            prompt = self._build_prompt(topic, platforms, audience, additional_context)

            logger.info(
                "Generating content with new Foundry agent",
                topic=topic,
                platforms=platforms,
                agent_name=self.settings.agent_name,
                prompt_length=len(prompt),
            )

            start_time = asyncio.get_event_loop().time()

            # Get project client and agent
            client = self._get_project_client()
            agent = self._get_agent()

            # Get OpenAI client from project
            openai_client = client.get_openai_client()

            # Call agent using responses API
            logger.info("Calling agent via responses API")
            response = openai_client.responses.create(
                input=[{"role": "user", "content": prompt}],
                extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
            )

            duration = asyncio.get_event_loop().time() - start_time

            # Extract content from response
            content = response.output_text

            logger.info(
                "Content generated successfully with new Foundry agent",
                duration=duration,
                content_length=len(content),
            )

            # Parse the content into structured format
            parsed_content = self._parse_agent_response(content)

            return {
                "content": parsed_content,
                "duration": duration,
            }

        except AgentServiceError:
            raise
        except Exception as e:
            logger.error(
                "Unexpected error during content generation",
                error=str(e),
                error_type=type(e).__name__,
            )
            raise AgentServiceError(f"Failed to generate content: {str(e)}")

    def _build_prompt(
        self,
        topic: str,
        platforms: list[str],
        audience: Optional[str],
        additional_context: Optional[str],
    ) -> str:
        """
        Build prompt for agent.

        Args:
            topic: Technical topic
            platforms: Target platforms
            audience: Optional audience
            additional_context: Optional context

        Returns:
            Formatted prompt string
        """
        platform_str = ", ".join(platforms)

        prompt_parts = [
            f"Generate technical content about: {topic}",
            f"Target platforms: {platform_str}",
        ]

        if audience:
            prompt_parts.append(f"Target audience: {audience}")

        if additional_context:
            prompt_parts.append(f"Additional context: {additional_context}")

        prompt_parts.append(
            f"\nIMPORTANT: You MUST generate SEPARATE, DISTINCT content for EACH platform: {platform_str}."
        )
        prompt_parts.append(
            "Each platform requires different formatting and length (see agent-instructions.md)."
        )
        prompt_parts.append(
            "\nPlease provide a complete Content Pack with plan, platform outputs for ALL requested platforms, and notes."
        )

        return "\n".join(prompt_parts)

    def _parse_agent_response(self, content_text: str) -> dict[str, Any]:
        """
        Parse agent response into structured format.

        Args:
            content_text: Raw text response from agent

        Returns:
            Parsed content dictionary
        """
        try:
            logger.debug("Parsing agent response", content_length=len(content_text))

            # Try to parse as JSON if the agent returns structured JSON
            try:
                import json

                parsed_content = json.loads(content_text)
                logger.info("Successfully parsed JSON response from agent")
                return parsed_content
            except json.JSONDecodeError:
                # If not JSON, extract structured content from markdown text
                logger.info("Agent response is plain text, extracting structure")

                import re

                # Extract the Plan section first
                plan_section_match = re.search(
                    r"##\s*A\)\s*Plan\s*\n(.*?)(?:##\s*B\)|$)",
                    content_text,
                    re.IGNORECASE | re.DOTALL,
                )
                plan_section = (
                    plan_section_match.group(1) if plan_section_match else content_text
                )

                # Extract hook - format: **Hook:**  \nContent text
                hook = (
                    content_text[:250].split("\n")[0]
                    if content_text
                    else "Generated content available below"
                )
                hook_match = re.search(
                    r"\*\*Hook:\*\*\s*\n(.+?)(?:\n\s*\n|\*\*)",
                    plan_section,
                    re.IGNORECASE | re.DOTALL,
                )
                if hook_match:
                    hook = hook_match.group(1).strip()

                # Extract narrative frame - format: **Narrative Frame:**  \nContent
                narrative = "Structured content framework provided"
                narrative_match = re.search(
                    r"\*\*Narrative\s*Frame:\*\*\s*\n(.+?)(?:\n\s*\n|\*\*)",
                    plan_section,
                    re.IGNORECASE | re.DOTALL,
                )
                if narrative_match:
                    narrative = narrative_match.group(1).strip()

                # Extract key points - split approach
                key_points = [
                    "Full detailed content available in the Notes section below"
                ]
                # Split on "Key Points:" and get the section after it
                if (
                    "**Key Points:**" in plan_section
                    or "**Key Points**" in plan_section
                ):
                    # Find the section after Key Points
                    kp_split = re.split(
                        r"\*\*Key\s*Points?:?\*\*", plan_section, flags=re.IGNORECASE
                    )
                    if len(kp_split) > 1:
                        kp_section = kp_split[1]
                        # Extract until the next heading or end
                        kp_text_match = re.search(
                            r"^(.+?)(?:\n\s*-\s*\*\*|\n\s*##|$)", kp_section, re.DOTALL
                        )
                        if kp_text_match:
                            kp_text = kp_text_match.group(1)
                            # Now extract all bullet points (with or without indentation)
                            extracted_points = re.findall(
                                r"^\s*[-•]\s+(.+?)$", kp_text, re.MULTILINE
                            )
                            if extracted_points:
                                key_points = [
                                    p.strip() for p in extracted_points if p.strip()
                                ]

                # Extract example - format: **Example:**  \nContent
                example = "Detailed examples provided in the full content below"
                example_match = re.search(
                    r"\*\*Example:\*\*\s*\n(.+?)(?:\n\s*\n|\*\*|$)",
                    plan_section,
                    re.IGNORECASE | re.DOTALL,
                )
                if example_match:
                    example = example_match.group(1).strip()

                # Extract CTA - format: **CTA:**  \nContent
                cta = "Review and utilize the generated content"
                cta_match = re.search(
                    r"\*\*(?:CTA|Call[- ]to[- ]Action):\*\*\s*\n(.+?)(?:\n\s*\n|\*\*|---+|$)",
                    plan_section,
                    re.IGNORECASE | re.DOTALL,
                )
                if cta_match:
                    cta = cta_match.group(1).strip()

                logger.info(
                    "Extracted structured fields",
                    hook_found=bool(hook_match),
                    narrative_found=bool(narrative_match),
                    key_points_count=len(key_points),
                    example_found=bool(example_match),
                    cta_found=bool(cta_match),
                )

                # Extract platform-specific outputs from "B) PLATFORM OUTPUTS" section
                outputs = {}
                platform_section_match = re.search(
                    r"##\s*B\)\s*(?:PLATFORM\s*)?OUTPUTS\s*\n(.*?)(?:##\s*C\)|$)",
                    content_text,
                    re.IGNORECASE | re.DOTALL,
                )

                if platform_section_match:
                    platform_section = platform_section_match.group(1)
                    logger.info(
                        "Found PLATFORM OUTPUTS section",
                        section_length=len(platform_section),
                    )

                    # Extract content for each platform
                    for platform in ["linkedin", "twitter", "github", "blog"]:
                        # Pattern: ### LinkedIn or #### **LinkedIn Post** or ### Twitter
                        # More flexible regex to handle various heading formats
                        platform_pattern = rf"####?\s*\*?\*?{platform}[\s\w]*\*?\*?[:\s]*\n(.*?)(?:###|\*\*Hashtags:|\*\*Call to Action:|$)"
                        platform_match = re.search(
                            platform_pattern,
                            platform_section,
                            re.IGNORECASE | re.DOTALL,
                        )

                        if platform_match:
                            platform_content = platform_match.group(1).strip()

                            # Extract hashtags for this platform (flexible pattern)
                            hashtags_pattern = rf"####?\s*\*?\*?{platform}[\s\w]*\*?\*?.*?\*\*Hashtags:\*\*\s*(.+?)(?:\n\s*\n|\*\*|###|$)"
                            hashtags_match = re.search(
                                hashtags_pattern,
                                platform_section,
                                re.IGNORECASE | re.DOTALL,
                            )
                            hashtags = []
                            if hashtags_match:
                                hashtag_text = hashtags_match.group(1).strip()
                                hashtags = re.findall(r"#\w+", hashtag_text)

                            # Extract platform-specific CTA (flexible pattern)
                            cta_pattern = rf"####?\s*\*?\*?{platform}[\s\w]*\*?\*?.*?\*\*(?:Call to Action|CTA):\*\*\s*(.+?)(?:\n\s*\n|###|$)"
                            cta_match = re.search(
                                cta_pattern, platform_section, re.IGNORECASE | re.DOTALL
                            )
                            platform_cta = (
                                cta_match.group(1).strip() if cta_match else cta
                            )

                            outputs[platform] = {
                                "content": platform_content,
                                "hashtags": hashtags,
                                "call_to_action": platform_cta,
                            }
                            logger.info(
                                f"Extracted {platform} content",
                                content_length=len(platform_content),
                                hashtag_count=len(hashtags),
                            )
                        else:
                            logger.warning(f"No content found for platform: {platform}")
                else:
                    logger.warning("PLATFORM OUTPUTS section not found, using fallback")

                # Fallback: if no platform-specific content found, use the full text for all
                if not outputs:
                    logger.info("Using fallback: duplicating content to all platforms")
                    for platform in ["linkedin", "twitter", "github", "blog"]:
                        outputs[platform] = {
                            "content": content_text,
                            "hashtags": [],
                            "call_to_action": cta,
                        }

                return {
                    "plan": {
                        "hook": hook,
                        "narrative_frame": narrative,
                        "key_points": key_points,
                        "example": example,
                        "cta": cta,
                    },
                    "outputs": outputs,
                    "notes": content_text,
                }

        except Exception as e:
            logger.error("Error parsing agent response", error=str(e))
            # Return minimal valid structure with the full text
            return {
                "plan": {
                    "hook": "Content generated successfully",
                    "narrative_frame": "See full content below",
                    "key_points": ["Review the complete content in the notes section"],
                    "example": "Full details available below",
                    "cta": "Review and use the generated content",
                },
                "outputs": {},
                "notes": content_text if content_text else f"Error: {str(e)}",
            }

    async def health_check(self) -> bool:
        """
        Check if agent service is healthy.

        Returns:
            True if service is accessible, False otherwise
        """
        try:
            logger.info("Performing health check on Azure AI agent service")
            client = self._get_project_client()
            # Try to get agent to verify connection
            agent = self._get_agent()
            is_healthy = agent is not None
            logger.info(
                "Health check completed",
                healthy=is_healthy,
                agent_name=agent.name if agent else None,
            )
            return is_healthy
        except Exception as e:
            logger.error("Agent health check failed", error=str(e))
            return False
