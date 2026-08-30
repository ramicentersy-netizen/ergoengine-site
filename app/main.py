from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import engine, Base, SessionLocal
from .routes import public_routes, affiliate_routes, admin_routes
from .agents.product_agent import ProductResearchAgent
from .agents.keyword_agent import KeywordResearchAgent
from .agents.content_agent import ContentGenerationAgent
from .agents.seo_agent import SEOEngineAgent
from .services.scheduler_service import start_system_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(public_routes.router)
app.include_router(affiliate_routes.router)
app.include_router(admin_routes.router)

@app.on_event("startup")
def on_startup_initialization():
    db = SessionLocal()
    try:
        prod_agent = ProductResearchAgent()
        prod_agent.run_catalog_sync(db)

        kw_agent = KeywordResearchAgent()
        kw_agent.discover_and_cluster_keywords(db)

        content_agent = ContentGenerationAgent()
        
        # 1. إنشاء المقال التجميعي
        article1 = content_agent.build_best_list_article(
            db=db,
            target_keyword="best ergonomic office chairs for lower back pain"
        )
        if article1:
            SEOEngineAgent().generate_and_inject_schema(db, article1.id)

        # 2. إنشاء مقال المقارنة المباشرة
        article2 = content_agent.build_comparison_article(
            db=db,
            slug1="herman-miller-aeron",
            slug2="ergochair-pro-autonomous",
            target_keyword="herman miller aeron vs autonomous ergochair pro"
        )
        if article2:
            SEOEngineAgent().generate_and_inject_schema(db, article2.id)

        start_system_scheduler()
    finally:
        db.close()
