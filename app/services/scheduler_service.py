from apscheduler.schedulers.background import BackgroundScheduler
from ..database import SessionLocal
from ..agents.keyword_agent import KeywordResearchAgent
from ..agents.product_agent import ProductResearchAgent
from ..agents.conversion_agent import ConversionOptimizationAgent
from ..agents.analytics_agent import AnalyticsIntelligenceAgent

scheduler = BackgroundScheduler()

def run_daily_agent_jobs():
    db = SessionLocal()
    try:
        kw_agent = KeywordResearchAgent()
        kw_agent.discover_and_cluster_keywords(db)

        prod_agent = ProductResearchAgent()
        prod_agent.run_catalog_sync(db)

        conv_agent = ConversionOptimizationAgent()
        conv_agent.analyze_cta_performance(db)

        analytics_agent = AnalyticsIntelligenceAgent()
        analytics_agent.compile_executive_report(db)
    finally:
        db.close()

def start_system_scheduler():
    if not scheduler.running:
        scheduler.add_job(run_daily_agent_jobs, "interval", hours=24, id="daily_agent_sync")
        scheduler.start()
