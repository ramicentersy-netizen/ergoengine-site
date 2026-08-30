from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from ..config import settings
from ..models import Product

class AffiliateComplianceService:
    @staticmethod
    def generate_safe_affiliate_link(product: Product) -> str:
        base_url = product.affiliate_url
        if not base_url:
            return "#"

        tag = settings.AMAZON_TRACKING_TAG or "ergoengine-20"
        
        # معالجة روابط أمازون لحقن كود التتبع بأمان
        if "amazon.com" in base_url or "amzn.to" in base_url:
            parsed = urlparse(base_url)
            query_params = parse_qs(parsed.query)
            query_params["tag"] = [tag]
            
            new_query = urlencode(query_params, doseq=True)
            return urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment
            ))
            
        return base_url
