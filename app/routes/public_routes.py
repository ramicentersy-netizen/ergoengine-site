from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Article, Product
from ..config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.status == "published").all()
    products = db.query(Product).all()
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "articles": articles,
            "products": products,
            "settings": settings
        }
    )

@router.get("/reviews/{slug}", response_class=HTMLResponse)
async def review_detail(request: Request, slug: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return templates.TemplateResponse(
        request=request,
        name="article.html",
        context={
            "article": article,
            "settings": settings
        }
    )

@router.get("/disclosure", response_class=HTMLResponse)
async def disclosure(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="disclosure.html",
        context={"settings": settings}
    )

@router.get("/templates/project-management", response_class=HTMLResponse)
async def project_management_template(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="notion_template.html",
        context={"settings": settings}
    )
