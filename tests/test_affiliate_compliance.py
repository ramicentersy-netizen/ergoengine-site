import pytest
from app.models import Product
from app.services.affiliate_service import AffiliateComplianceService
from app.config import settings

def test_amazon_affiliate_tag_injection():
    product = Product(
        name="Test Chair",
        slug="test-chair",
        brand="TestBrand",
        category="Chairs",
        price=299.0,
        affiliate_url="https://www.amazon.com/dp/B01TEST123?ref=test",
        pros_json="[]",
        cons_json="[]",
        specs_json="{}",
        ideal_for="All",
        avoid_if="None"
    )

    clean_link = AffiliateComplianceService.generate_safe_affiliate_link(product)
    assert f"tag={settings.AMAZON_TRACKING_TAG}" in clean_link
    assert "linkCode=as2" in clean_link
