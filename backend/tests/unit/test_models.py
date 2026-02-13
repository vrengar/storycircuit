"""
Unit tests for StoryCircuit models.
"""

import pytest
from datetime import datetime
from app.models.requests import ContentGenerationRequest, Platform
from app.models.responses import ContentPlan, Tweet, TwitterOutput
from pydantic import ValidationError


def test_content_generation_request_valid():
    """Test valid content generation request."""
    request = ContentGenerationRequest(
        topic="AI agent orchestration",
        platforms=[Platform.LINKEDIN, Platform.TWITTER],
        audience="software engineers"
    )
    
    assert request.topic == "AI agent orchestration"
    assert len(request.platforms) == 2
    assert Platform.LINKEDIN in request.platforms
    assert request.audience == "software engineers"


def test_content_generation_request_missing_topic():
    """Test request fails without topic."""
    with pytest.raises(ValidationError):
        ContentGenerationRequest(
            platforms=[Platform.LINKEDIN]
        )


def test_content_generation_request_short_topic():
    """Test request fails with too short topic."""
    with pytest.raises(ValidationError):
        ContentGenerationRequest(
            topic="AI",
            platforms=[Platform.LINKEDIN]
        )


def test_content_generation_request_no_platforms():
    """Test request fails without platforms."""
    with pytest.raises(ValidationError):
        ContentGenerationRequest(
            topic="AI agent orchestration",
            platforms=[]
        )


def test_content_generation_request_duplicate_platforms():
    """Test request fails with duplicate platforms."""
    with pytest.raises(ValidationError):
        ContentGenerationRequest(
            topic="AI agent orchestration",
            platforms=[Platform.LINKEDIN, Platform.LINKEDIN]
        )


def test_twitter_output_model():
    """Test Twitter output model."""
    tweet1 = Tweet(order=1, content="Test tweet", character_count=10)
    tweet2 = Tweet(order=2, content="Another tweet", character_count=13)
    
    twitter_output = TwitterOutput(
        thread_structure="2 tweets",
        tweets=[tweet1, tweet2]
    )
    
    assert twitter_output.thread_structure == "2 tweets"
    assert len(twitter_output.tweets) == 2
    assert twitter_output.tweets[0].order == 1


def test_content_plan_model():
    """Test content plan model."""
    plan = ContentPlan(
        hook="Test hook",
        narrative_frame="Problem → Solution",
        key_points=["Point 1", "Point 2"],
        example="Test example",
        cta="Test CTA"
    )
    
    assert plan.hook == "Test hook"
    assert len(plan.key_points) == 2
    assert plan.cta == "Test CTA"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
