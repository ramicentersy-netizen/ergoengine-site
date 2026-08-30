import json
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..models import Article

class SEOEngineAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SEO Optimization & Schema Agent")

    def generate_and_inject_schema(self, db: Session, article_id: int):
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            return

        schema_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article.title,
            "description": article.meta_description,
            "author": {
                "@type": "Organization",
                "name": "ErgoEngine Research Group"
            },
            "datePublished": article.created_at.isoformat(),
            "dateModified": article.updated_at.isoformat(),
            "mainEntityOfPage": f"http://localhost:8000/reviews/{article.slug}"
        }

        article.schema_json = json.dumps(schema_data, indent=2)
        db.commit()
        self.log(db, "SCHEMA_INJECTION", "SUCCESS", f"Structured JSON-LD schema injected for article ID {article.id}")
