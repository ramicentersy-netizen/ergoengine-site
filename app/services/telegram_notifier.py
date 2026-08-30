import httpx
import logging
from ..config import settings

logger = logging.getLogger("telegram_service")

class TelegramNotificationService:
    @staticmethod
    async def notify_click(product_name: str, brand: str, source_tag: str, target_url: str):
        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            return

        message = (
            f"🎯 <b>New Affiliate Click Recorded!</b>\n\n"
            f"📦 <b>Product:</b> {product_name}\n"
            f"🏷️ <b>Brand:</b> {brand}\n"
            f"📍 <b>Source Placement:</b> <code>{source_tag}</code>\n"
            f"🔗 <b>Destination:</b> Amazon / Direct Partner"
        )

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(url, json=payload)
        except Exception as e:
            logger.error(f"Failed to send Telegram click alert: {e}")
