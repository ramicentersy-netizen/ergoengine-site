from sqlalchemy.orm import Session
from sqlalchemy import func
from .base_agent import BaseAgent
from ..models import AffiliateClick, Article, Product

class AnalyticsIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Analytics Intelligence Agent")

    def compile_executive_report(self, db: Session) -> dict:
        total_articles = db.query(Article).count()
        total_clicks = db.query(AffiliateClick).count()
        total_products = db.query(Product).count()
        
        top_clicked_products = db.query(
            Product.name,
            func.count(AffiliateClick.id).label("clicks")
        ).join(AffiliateClick).group_by(Product.id).order_by(func.count(AffiliateClick.id).desc()).limit(5).all()

        actions = []
        if total_clicks == 0:
            actions.append("Acquire initial indexation & organic rankings to achieve Stage 2 (First Traffic).")
        elif total_clicks > 0 and total_clicks < 50:
            actions.append("Scale internal linking and test 'Sticky Verdict Bar' on mobile viewports to raise CTR.")
        else:
            actions.append("Expand coverage to Sub-cluster: 'Monitor Arms for Dual 32-inch Displays'.")

        report = {
            "total_articles": total_articles,
            "total_products": total_products,
            "total_clicks": total_clicks,
            "top_products": [{"name": p[0], "clicks": p[1]} for p in top_clicked_products],
            "actionable_next_step": actions[0] if actions else "Maintain monitoring loop."
        }

        self.log(db, "ANALYTICS_REPORT", "SUCCESS", f"Generated snapshot: {report}")
        return report
