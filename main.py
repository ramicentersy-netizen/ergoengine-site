import os
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.models import Article, ContentStatus

# إنشاء الجداول إن لم تكن موجودة
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ErgoEngine",
    description="Ergonomic Workspaces & Desk Setups Platform",
    version="1.0.0"
)

# إعداد القوالب والملفات الثابتة
templates = Jinja2Templates(directory="templates")
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# قاموس روابط الإحالة المقنعة لمنتجات أمازون والشركاء
AFFILIATE_REDIRECTS = {
    # الكراسي والمكاتب
    "ergonomic-chair-pro": "https://www.amazon.com/dp/B08GP5186N?tag=ergoengine-20",
    "standing-desk-pro": "https://www.amazon.com/dp/B08GLQ5G37?tag=ergoengine-20",
    
    # الفارات المريحة العمودية الجديدة
    "mx-master-3s": "https://www.amazon.com/dp/B09HM94VDS?tag=ergoengine-20",
    "logitech-lift": "https://www.amazon.com/dp/B09J516ZBR?tag=ergoengine-20",
    "anker-vertical-mouse": "https://www.amazon.com/dp/B00BIFNTMC?tag=ergoengine-20",
}

@app.get("/go/{slug}")
async def affiliate_redirect(slug: str, request: Request):
    """
    توجيه نظيف (307 Temporary Redirect) لروابط الأفلييت لتتبع النقرات وحماية الروابط
    """
    target_url = AFFILIATE_REDIRECTS.get(slug)
    if not target_url:
        raise HTTPException(status_code=404, detail="Offer link not found")
    
    return RedirectResponse(url=target_url, status_code=307)

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    status_val = getattr(ContentStatus, "PUBLISHED", "published")
    articles = db.query(Article).filter(Article.status == status_val).all()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@app.get("/posts/{slug}", response_class=HTMLResponse)
async def read_article(slug: str, request: Request, db: Session = Depends(get_db)):
    status_val = getattr(ContentStatus, "PUBLISHED", "published")
    article = db.query(Article).filter(Article.slug == slug, Article.status == status_val).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # زيادة عداد المشاهدات
    if hasattr(article, "page_views"):
        article.page_views += 1
        db.commit()

    return templates.TemplateResponse("article.html", {"request": request, "article": article})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ErgoEngine"}