from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product, AffiliateClick
from ..services.affiliate_service import AffiliateComplianceService
from ..services.telegram_notifier import TelegramNotificationService

router = APIRouter()

@router.get("/go/{slug}")
async def outbound_affiliate_router(
    slug: str,
    background_tasks: BackgroundTasks,
    src: str = Query(default="direct", description="Placement context identifier"),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.slug == slug).first()
    if not product:
        raise HTTPException(status_code=404, detail="Target catalog product not found")

    # 1. تسجيل النقرة بأمان في قاعدة البيانات
    try:
        click = AffiliateClick(
            product_id=product.id,
            source_placement=src,
            destination_url=product.affiliate_url or ""
        )
        db.add(click)
        db.commit()
    except Exception as e:
        db.rollback()

    # 2. تشغيل إشعار تيليجرام كـ Background Task (بدون التأثير على التوجيه في حال فشل الاتصال)
    try:
        background_tasks.add_task(
            TelegramNotificationService.notify_click,
            product_name=product.name,
            brand=product.brand,
            source_tag=src,
            target_url=product.affiliate_url or ""
        )
    except Exception:
        pass

    # 3. توليد الرابط الآمن وإعادة التوجيه
    safe_target_url = AffiliateComplianceService.generate_safe_affiliate_link(product)
    return RedirectResponse(url=safe_target_url, status_code=307)
