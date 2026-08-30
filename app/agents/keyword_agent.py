from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..models import Keyword, IntentLevel

class KeywordResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Keyword Research Agent")

    def discover_and_cluster_keywords(self, db: Session):
        seed_keywords = [
            {
                "term": "best ergonomic office chairs for lower back pain",
                "cluster": "Ergonomic Chairs",
                "intent": IntentLevel.COMMERCIAL_INVESTIGATION,
                "search_volume": 8100,
                "keyword_difficulty": 38.0
            },
            {
                "term": "herman miller aeron vs autonomous ergochair pro",
                "cluster": "Chair Comparisons",
                "intent": IntentLevel.COMMERCIAL_INVESTIGATION,
                "search_volume": 2400,
                "keyword_difficulty": 26.0
            },
            {
                "term": "best heavy duty standing desk for home office",
                "cluster": "Standing Desks",
                "intent": IntentLevel.TRANSACTIONAL,
                "search_volume": 4200,
                "keyword_difficulty": 31.0
            },
            {
                "term": "best heavy duty monitor arm for neck pain relief",
                "cluster": "Monitor Arms",
                "intent": IntentLevel.COMMERCIAL_INVESTIGATION,
                "search_volume": 3600,
                "keyword_difficulty": 22.0
            },
            {
                "term": "best monitor light bar for eye strain reduction",
                "cluster": "Ergonomic Lighting",
                "intent": IntentLevel.TRANSACTIONAL,
                "search_volume": 5100,
                "keyword_difficulty": 18.0
            }
        ]

        added = 0
        for kw_data in seed_keywords:
            exists = db.query(Keyword).filter(Keyword.term == kw_data["term"]).first()
            if not exists:
                kw = Keyword(**kw_data)
                db.add(kw)
                added += 1
        db.commit()
        self.log(db, "KEYWORD_CLUSTERING", "SUCCESS", f"Clustered {added} new targeted high-intent keywords across expanded categories.")
