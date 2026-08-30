import pytest
from app.services.content_validator import ContentQualityEngine, ContentValidationError

def test_validator_rejects_hallucinated_first_person_claims():
    bad_content = """
    This is an ergonomic review. In my personal experience of 10 years, I felt great.
    Here are the specifications: High height.
    Who should buy: developers. Who should avoid: gamers.
    Pros: good. Cons: expensive.
    """
    with pytest.raises(ContentValidationError) as exc:
        ContentQualityEngine.validate(bad_content, "Test Title", word_count=800)
    assert "Forbidden or misleading claim detected" in str(exc.value)

def test_validator_rejects_short_content():
    short_content = "<p>Too short</p>"
    with pytest.raises(ContentValidationError) as exc:
        ContentQualityEngine.validate(short_content, "Short Title", word_count=50)
    assert "lower than minimum" in str(exc.value)
