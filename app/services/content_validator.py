import re
from ..config import settings

class ContentValidationError(Exception):
    pass

class ContentQualityEngine:
    FORBIDDEN_HALLUCINATIONS = [
        r"in my personal experience of 10 years",
        r"when i tested this in my own lab",
        r"we guarantee 100% cure",
        r"click here to get rich",
        r"best product in the universe"
    ]

    REQUIRED_STRUCTURAL_BLOCKS = [
        "specification",
        "who should buy",
        "who should avoid",
        "pros",
        "cons"
    ]

    @classmethod
    def validate(cls, html_content: str, title: str, word_count: int) -> bool:
        if word_count < settings.MIN_WORD_COUNT:
            raise ContentValidationError(
                f"Content word count ({word_count}) is lower than minimum ({settings.MIN_WORD_COUNT})"
            )

        lower_content = html_content.lower()

        for pattern in cls.FORBIDDEN_HALLUCINATIONS:
            if re.search(pattern, lower_content):
                raise ContentValidationError(f"Forbidden or misleading claim detected matching pattern: '{pattern}'")

        missing_blocks = []
        for block in cls.REQUIRED_STRUCTURAL_BLOCKS:
            if block not in lower_content:
                missing_blocks.append(block)

        if missing_blocks:
            raise ContentValidationError(f"Content is missing essential objective evaluation blocks: {missing_blocks}")

        return True
