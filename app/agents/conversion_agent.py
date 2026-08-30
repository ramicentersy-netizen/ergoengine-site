from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models import AffiliateClick

class ConversionOptimizationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Conversion Optimization Agent")

    def analyze_cta_performance(self, db: Session) -> dict:
        results = db.query(
            AffiliateClick.cta_placement,
            func.count(AffiliateClick.id).label("total_clicks")
        ).group_by(AffiliateClick.cta_placement).all()

        summary = {row[0]: row[1] for row in results}
        self.log(db, "CONVERSION_AUDIT", "SUCCESS", f"CTR Placement analysis: {summary}")
        return summary
