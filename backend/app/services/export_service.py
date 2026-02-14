"""
Export Service.
Handles content export in various formats.
"""

import json
from typing import Literal
import structlog

from ..utils.exceptions import ExportError

logger = structlog.get_logger(__name__)


class ExportService:
    """Service for exporting content in various formats."""

    def export_as_markdown(
        self,
        content: dict,
        topic: str,
        platforms: list[str],
        platform_filter: str = "all",
    ) -> str:
        """
        Export content as Markdown.

        Args:
            content: Generated content dictionary
            topic: Content topic
            platforms: List of platforms
            platform_filter: Specific platform or 'all'

        Returns:
            Markdown formatted string
        """
        logger.info("Exporting content as markdown", platform_filter=platform_filter)

        try:
            lines = [f"# {topic}\n"]

            # Add plan section
            if "plan" in content:
                plan = content["plan"]
                lines.append("## Content Plan\n")
                lines.append(f"**Hook:** {plan.get('hook', 'N/A')}\n")
                lines.append(
                    f"**Narrative Frame:** {plan.get('narrativeFrame', 'N/A')}\n"
                )

                if "keyPoints" in plan:
                    lines.append("**Key Points:**")
                    for point in plan["keyPoints"]:
                        lines.append(f"- {point}")
                    lines.append("")

                lines.append(f"**Example:** {plan.get('example', 'N/A')}\n")
                lines.append(f"**CTA:** {plan.get('cta', 'N/A')}\n")

            # Add platform outputs
            if "outputs" in content:
                outputs = content["outputs"]

                # Filter by platform if specified
                platforms_to_export = (
                    [platform_filter] if platform_filter != "all" else platforms
                )

                for platform in platforms_to_export:
                    if platform in outputs:
                        lines.append(f"## {platform.capitalize()} Output\n")
                        lines.append(
                            self._format_platform_output(platform, outputs[platform])
                        )
                        lines.append("")

            # Add notes
            if "notes" in content:
                lines.append("## Notes\n")
                lines.append(content["notes"])
                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            logger.error("Failed to export as markdown", error=str(e))
            raise ExportError(f"Failed to export as Markdown: {str(e)}")

    def export_as_json(
        self,
        content_id: str,
        topic: str,
        platforms: list[str],
        content: dict,
        metadata: dict,
        platform_filter: str = "all",
    ) -> str:
        """
        Export content as JSON.

        Args:
            content_id: Content identifier
            topic: Content topic
            platforms: List of platforms
            content: Generated content
            metadata: Content metadata
            platform_filter: Specific platform or 'all'

        Returns:
            JSON formatted string
        """
        logger.info("Exporting content as JSON", platform_filter=platform_filter)

        try:
            # Filter outputs by platform if needed
            outputs = content.get("outputs", {})
            if platform_filter != "all" and platform_filter in outputs:
                outputs = {platform_filter: outputs[platform_filter]}

            export_data = {
                "id": content_id,
                "topic": topic,
                "platforms": (
                    platforms if platform_filter == "all" else [platform_filter]
                ),
                "content": {
                    "plan": content.get("plan", {}),
                    "outputs": outputs,
                    "notes": content.get("notes", ""),
                },
                "metadata": metadata,
            }

            return json.dumps(export_data, indent=2, default=str)

        except Exception as e:
            logger.error("Failed to export as JSON", error=str(e))
            raise ExportError(f"Failed to export as JSON: {str(e)}")

    def _format_platform_output(self, platform: str, output: dict) -> str:
        """Format platform-specific output for markdown."""
        lines = []

        try:
            if platform == "twitter" and "tweets" in output:
                lines.append(
                    f"**Thread Structure:** {output.get('threadStructure', 'N/A')}\n"
                )
                lines.append("**Tweets:**\n")
                for tweet in output["tweets"]:
                    lines.append(
                        f"{tweet['order']}. {tweet['content']} ({tweet['characterCount']} chars)"
                    )

            elif platform == "linkedin":
                if "shortVersion" in output:
                    lines.append("### Short Version\n")
                    lines.append(output["shortVersion"]["content"])
                    lines.append(
                        f"\n*({output['shortVersion']['characterCount']} chars, {output['shortVersion']['estimatedReadTime']})*\n"
                    )

                if "longVersion" in output:
                    lines.append("### Long Version\n")
                    lines.append(output["longVersion"]["content"])
                    lines.append(
                        f"\n*({output['longVersion']['characterCount']} chars, {output['longVersion']['estimatedReadTime']})*\n"
                    )

                if "carousel" in output and output["carousel"]:
                    lines.append("### Carousel\n")
                    for slide in output["carousel"]["slides"]:
                        lines.append(
                            f"**Slide {slide['slideNumber']}: {slide['title']}**"
                        )
                        for bullet in slide["bullets"]:
                            lines.append(f"- {bullet}")
                        lines.append("")

            elif platform == "github":
                lines.append("### README Snippet\n")
                lines.append("```markdown")
                lines.append(output.get("readmeSnippet", ""))
                lines.append("```\n")
                lines.append("### Release Notes\n")
                lines.append("```markdown")
                lines.append(output.get("releaseNotes", ""))
                lines.append("```")

            elif platform == "blog":
                lines.append(output.get("content", ""))
                lines.append(
                    f"\n*({output.get('characterCount', 0)} chars, {output.get('estimatedReadTime', 'N/A')})*"
                )

            elif platform == "video":
                lines.append(f"**Hook:** {output.get('hook', 'N/A')}")
                lines.append(f"**Payoff:** {output.get('payoff', 'N/A')}")

            else:
                # Fallback for unknown platforms or raw response
                lines.append(json.dumps(output, indent=2))

        except Exception as e:
            logger.warning(
                "Error formatting platform output", platform=platform, error=str(e)
            )
            lines.append(json.dumps(output, indent=2))

        return "\n".join(lines)

    def get_filename(
        self,
        content_id: str,
        format_type: Literal["markdown", "json"],
        platform: str = "all",
    ) -> str:
        """
        Generate export filename.

        Args:
            content_id: Content identifier
            format_type: Export format
            platform: Platform name

        Returns:
            Filename string
        """
        ext = "md" if format_type == "markdown" else "json"
        suffix = f"-{platform}" if platform != "all" else ""
        return f"storycircuit-{content_id[:8]}{suffix}.{ext}"
