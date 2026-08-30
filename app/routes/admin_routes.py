import csv
import io
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..agents.analytics_agent import AnalyticsIntelligenceAgent
from ..models import AgentLog, Article, AffiliateClick, Product
from ..config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    analytics = AnalyticsIntelligenceAgent().compile_executive_report(db)
    logs = db.query(AgentLog).order_by(AgentLog.created_at.desc()).limit(15).all()
    articles = db.query(Article).all()
    
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "analytics": analytics,
            "logs": logs,
            "articles": articles,
            "settings": settings
        }
    )

@router.get("/admin/export/clicks-csv")
async def export_clicks_csv(db: Session = Depends(get_db)):
    clicks = db.query(AffiliateClick).join(Product).order_by(AffiliateClick.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Click ID", "Product Name", "Brand", "Source Placement", "Destination URL", "Timestamp"])
    
    for c in clicks:
        writer.writerow([
            c.id,
            c.product.name if c.product else "N/A",
            c.product.brand if c.product else "N/A",
            c.source_placement,
            c.destination_url,
            c.created_at.strftime("%Y-%m-%d %H:%M:%S")
        ])
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=affiliate_clicks_report.csv"}
    )
