"""
Mock services for local development without Azure dependencies.
"""

from typing import Any, Optional
import asyncio


class MockAgentService:
    """Mock agent service for local development."""

    def __init__(self, settings):
        self.settings = settings

    async def generate_content(
        self,
        topic: str,
        platforms: list[str],
        audience: Optional[str] = None,
        additional_context: Optional[str] = None,
    ) -> dict[str, Any]:
        """Mock content generation with realistic, topic-aware output."""
        await asyncio.sleep(1.5)  # Simulate API call

        # Generate more realistic content based on topic
        audience_text = f" for {audience}" if audience else ""
        context_text = (
            f"\n\nContext: {additional_context}" if additional_context else ""
        )

        return {
            "content": {
                "plan": {
                    "hook": f"Hot take: {topic} isn't just another buzzword—it's changing how we build software{audience_text}.",
                    "narrative_frame": "Challenge → Insight → Action",
                    "key_points": [
                        f"Why {topic} matters in modern development",
                        f"Real-world patterns and anti-patterns",
                        f"Actionable steps to implement {topic}",
                        "Common mistakes and how to avoid them",
                    ],
                    "example": f"Think about the last time you struggled with scaling your application. {topic} solves this by...",
                    "cta": f"Ready to level up your {topic} game? Drop a comment with your biggest challenge!",
                },
                "outputs": {
                    "twitter": (
                        {
                            "thread_structure": "7 tweet thread with hook → problem → solution → implementation → results",
                            "tweets": [
                                {
                                    "order": 1,
                                    "content": f"[Thread] Just spent 6 months deep-diving into {topic}{audience_text}.\n\nHere's what most people get wrong (and how to fix it):",
                                    "character_count": 150,
                                },
                                {
                                    "order": 2,
                                    "content": f"The Problem:\n\nMost teams approach {topic} wrong. They focus on tools before understanding principles.\n\nResult? Technical debt, frustrated developers, and failed implementations.",
                                    "character_count": 185,
                                },
                                {
                                    "order": 3,
                                    "content": f"Here's the reality:\n\n{topic} isn't about the latest framework—it's about solving real problems{audience_text}.\n\nStart with WHY, not HOW.",
                                    "character_count": 150,
                                },
                                {
                                    "order": 4,
                                    "content": f"3 key principles I learned:\n\n1. Start simple, scale intentionally\n2. Optimize for iteration speed\n3. Measure everything{context_text}",
                                    "character_count": 140,
                                },
                                {
                                    "order": 5,
                                    "content": f"Real example:\n\nWe implemented {topic} and reduced deployment time by 60%.\n\nNot through fancy tools—through better processes.",
                                    "character_count": 135,
                                },
                                {
                                    "order": 6,
                                    "content": "The results speak for themselves:\n- Faster releases\n- Fewer bugs in production\n- Happier developers\n- Better system reliability",
                                    "character_count": 140,
                                },
                                {
                                    "order": 7,
                                    "content": f"Bottom line:\n\n{topic} done right = competitive advantage.\n\nWhat's your experience? Reply with your biggest challenge!",
                                    "character_count": 130,
                                },
                            ],
                        }
                        if "twitter" in platforms
                        else None
                    ),
                    "linkedin": (
                        {
                            "short_version": {
                                "content": f"""Hot take: {topic} is a game-changer{audience_text}

After 6 months implementing this, here's what I learned:

What doesn't work:
• Following tutorials blindly
• Over-engineering from day one
• Ignoring team collaboration

What actually works:
• Start with clear objectives
• Iterate based on real feedback
• Build team buy-in early

The result? 60% faster delivery, higher quality, and happier teams.

{topic} isn't just a technical choice—it's a strategic advantage.

What's been your experience?{context_text}""",
                                "character_count": 500,
                                "estimated_read_time": "1 min",
                            },
                            "long_version": {
                                "content": f"""# Why {topic} Changed How We Build Software{audience_text}

## The Challenge

Six months ago, our team was struggling. Deployments took hours, bugs crept into production, and developer morale was low.

We knew something had to change.

## Enter {topic}

After researching modern approaches, we decided to embrace {topic}. Not because it was trendy, but because it solved our real problems.

## The Transformation

Here's what we implemented:

**Phase 1: Foundation**
• Simplified our architecture
• Established clear patterns
• Created reusable components

**Phase 2: Optimization**
• Automated repetitive tasks
• Implemented monitoring
• Built feedback loops

**Phase 3: Scale**
• Handled 10x traffic growth
• Maintained sub-second response times
• Zero downtime deployments

## Real Results

Metrics that matter:
• 60% faster deployment time
• 40% reduction in production bugs
• 95% developer satisfaction
• 99.9% uptime

## Key Lessons Learned

1. **Start Simple**: Don't over-engineer. Build what you need, when you need it.

2. **Measure Everything**: You can't improve what you don't measure.

3. **Team > Tools**: Technology is just an enabler. Success comes from people.

4. **Iterate Continuously**: Small improvements compound over time.

## Common Pitfalls to Avoid

- Following best practices blindly
- Premature optimization
- Ignoring team expertise
- Skipping documentation{context_text}

## The Bottom Line

{topic} isn't just about technology—it's about building better systems and better teams.

The question isn't whether to adopt it, but how to do it right.

---

What's your experience with {topic}? What challenges are you facing?

Found this helpful? Repost to help others in your network!

#SoftwareEngineering #TechLeadership #Development""",
                                "character_count": 1800,
                                "estimated_read_time": "4 min",
                            },
                        }
                        if "linkedin" in platforms
                        else None
                    ),
                    "github": (
                        {
                            "readme_snippet": f"""## {topic}

### Overview
This implementation demonstrates production-ready patterns for {topic}{audience_text}.

### Features
- Scalable architecture
- Comprehensive error handling
- Full test coverage
- Detailed documentation

### Quick Start
```bash
# Install dependencies
npm install

# Run tests
npm test

# Start development
npm run dev
```

### Architecture
```
{topic.replace(' ', '-')}/
├── src/           # Source code
├── tests/         # Test suite
├── docs/          # Documentation
└── examples/      # Usage examples
```

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.{context_text}""",
                            "release_notes": f"""## v1.0.0 - {topic} Implementation

### Features
- Implemented core {topic} functionality
- Added comprehensive test suite
- Included production-ready examples

### Documentation
- Complete API documentation
- Architecture decision records
- Migration guides

### Bug Fixes
- Fixed edge cases in error handling
- Improved performance under load

### Breaking Changes
None - this is the initial release!""",
                        }
                        if "github" in platforms
                        else None
                    ),
                    "blog": (
                        {
                            "content": f"""# Deep Dive: {topic}{audience_text}

## Introduction

{topic} has become crucial in modern software development. In this comprehensive guide, we'll explore why it matters and how to implement it effectively.

## The Problem

Many teams struggle with:
- Complex deployments
- Poor system reliability  
- Slow feedback loops
- Developer productivity bottlenecks

## Why {topic} Matters

{topic} addresses these challenges by providing:

1. **Better Architecture**: Clear patterns and practices
2. **Faster Iteration**: Rapid development and deployment
3. **Higher Quality**: Fewer bugs, better testing
4. **Team Alignment**: Shared understanding and practices

## Implementation Guide

### Step 1: Foundation
Start with the basics. Understand the core principles before diving into tools.

### Step 2: Tooling
Choose tools that fit your needs, not the other way around.

### Step 3: Process
Establish workflows that support your team's success.

### Step 4: Measure
Track metrics that matter and continuously improve.

## Real-World Example

Let me share how we implemented {topic} in production:

**Challenge**: Deployments took 4 hours and frequently failed
**Solution**: Applied {topic} principles
**Result**: 15-minute deployments with 99% success rate

## Best Practices

- Start simple and iterate
- Automate repetitive tasks
- Build in observability from day one
- Document decisions and learnings
- Foster team collaboration

## Common Mistakes

- Over-engineering too early
- Copying patterns without understanding
- Ignoring team feedback
- Skipping testing
- Poor documentation

## Conclusion

{topic} is a journey, not a destination. Focus on continuous improvement and team success.{context_text}

---

**What's Next?**
Start small, measure results, and iterate based on learning.

[Read more technical deep-dives →]""",
                            "character_count": 2000,
                            "estimated_read_time": "5 min",
                        }
                        if "blog" in platforms
                        else None
                    ),
                },
                "notes": f"⚠️ MOCK CONTENT: This is generated by mock services for local development. Real Azure AI Foundry would provide deeper technical analysis tailored to {topic}{audience_text}.",
            },
            "duration": 1.5,
        }

    async def health_check(self) -> bool:
        """Mock health check."""
        return True


class MockContentRepository:
    """Mock repository for local development."""

    def __init__(self, settings):
        self.settings = settings
        self._storage = {}

    async def create(self, document) -> Any:
        """Mock create."""
        self._storage[document.id] = document
        return document

    async def get_by_id(self, content_id: str, user_id: str) -> Any:
        """Mock get."""
        from ..utils.exceptions import ContentNotFoundError

        if content_id not in self._storage:
            raise ContentNotFoundError(f"Content {content_id} not found")
        return self._storage[content_id]

    async def query_by_user(self, user_id: str, **kwargs) -> Any:
        """Mock query."""
        from ..models.database import ContentQueryResult

        docs = [doc for doc in self._storage.values() if doc.partition_key == user_id]
        return ContentQueryResult(documents=docs, count=len(docs))

    async def delete(self, content_id: str, user_id: str) -> None:
        """Mock delete."""
        if content_id in self._storage:
            self._storage[content_id].deleted = True

    async def health_check(self) -> bool:
        """Mock health check."""
        return True
