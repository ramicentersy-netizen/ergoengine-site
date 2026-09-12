import json
import os
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="ErgoEngine Platform")

# خريطة روابط الأفلييت
AFFILIATE_MAP = {
    "chair-premium": "https://amzn.to/4xWtXos",
    "chair-budget": "https://amzn.to/4xQU5B3",
    "standing-desk": "https://amzn.to/4y2YYXG",
    "monitor-arm": "https://amzn.to/4xNeOpl"
}

STATS_FILE = "click_stats.json"

def log_click(slug: str, referer: str):
    data = {"total_clicks": 0, "by_product": {}, "recent_logs": []}
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass

    data["total_clicks"] = data.get("total_clicks", 0) + 1
    data["by_product"][slug] = data["by_product"].get(slug, 0) + 1
    
    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "product": slug,
        "source": referer or "Direct"
    }
    data["recent_logs"].insert(0, log_entry)
    data["recent_logs"] = data["recent_logs"][:50]  # حفظ آخر 50 نقرة فقط

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

BASE_CSS = """
<style>
    :root { --primary: #0284c7; --text: #1e293b; --bg: #f8fafc; --card: #ffffff; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.7; color: var(--text); background: var(--bg); margin: 0; padding: 20px; }
    .container { max-width: 850px; margin: 0 auto; background: var(--card); padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    h1 { color: #0f172a; font-size: 2.1rem; line-height: 1.3; }
    h2 { color: #334155; margin-top: 30px; }
    p { font-size: 1.05rem; color: #475569; }
    .cta-btn { display: inline-block; background: #ea580c; color: white; padding: 13px 26px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.05rem; margin: 15px 0; transition: background 0.2s; }
    .cta-btn:hover { background: #c2410c; }
    .btn-budget { background: #0284c7; }
    .btn-budget:hover { background: #0369a1; }
    table { width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 0.95rem; }
    th, td { border: 1px solid #e2e8f0; padding: 12px 16px; text-align: left; }
    th { background: #f1f5f9; color: #0f172a; }
    .badge { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 9999px; font-size: 0.85rem; font-weight: bold; }
    .metric-card { display: inline-block; background: #f1f5f9; padding: 15px 25px; border-radius: 8px; margin-right: 15px; margin-bottom: 15px; }
    .metric-val { font-size: 1.8rem; font-weight: bold; color: #0284c7; }
    .footer { margin-top: 40px; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 20px; }
</style>
"""

@app.get("/")
def home():
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="utf-8"><title>ErgoEngine | Workspace Architecture</title>{BASE_CSS}</head>
    <body>
        <div class="container">
            <h1>Engineered for Work Comfort & Longevity</h1>
            <p>High-end workspace reviews, ergonomic technical breakdowns, and posture-friendly office gear tested for serious productivity.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;">
            <h2>Featured Product Guides</h2>
            <ul>
                <li><a href="/posts/best-ergonomic-office-chairs" style="color: var(--primary); font-size: 1.15rem; font-weight: 600;">Say Goodbye to Lower Back Pain: Best Ergonomic Office Chairs Reviewed</a></li>
                <li style="margin-top: 15px;"><a href="/posts/top-adjustable-standing-desks" style="color: var(--primary); font-size: 1.15rem; font-weight: 600;">The Ultimate Motorized Standing Desk Setup for Peak Performance</a></li>
            </ul>
        </div>
    </body>
    </html>
    """)

@app.get("/go/{slug}")
def affiliate_redirect(slug: str, request: Request):
    referer = request.headers.get("referer", "")
    log_click(slug, referer)
    target = AFFILIATE_MAP.get(slug, "https://amzn.to/4xWtXos")
    return RedirectResponse(url=target, status_code=307)

@app.get("/analytics")
def show_analytics():
    data = {"total_clicks": 0, "by_product": {}, "recent_logs": []}
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass

    prod_rows = "".join([f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>" for k, v in data.get("by_product", {}).items()])
    log_rows = "".join([f"<tr><td>{entry.get('time')}</td><td>{entry.get('product')}</td><td>{entry.get('source')}</td></tr>" for entry in data.get("recent_logs", [])])

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="utf-8"><title>ErgoEngine | Live Metrics</title>{BASE_CSS}</head>
    <body>
        <div class="container">
            <h1>ErgoEngine Referral Traffic & Click Tracker</h1>
            <div style="margin: 20px 0;">
                <div class="metric-card">
                    <div>Total Outbound Clicks</div>
                    <div class="metric-val">{data.get("total_clicks", 0)}</div>
                </div>
            </div>

            <h2>Clicks Breakdown by Product</h2>
            <table>
                <tr><th>Product Endpoint</th><th>Total Direct Clicks</th></tr>
                {prod_rows or '<tr><td colspan="2">No outbound clicks recorded yet.</td></tr>'}
            </table>

            <h2>Recent Activity Feed (Last 50 Events)</h2>
            <table>
                <tr><th>Timestamp</th><th>Target Endpoint</th><th>Referer Source</th></tr>
                {log_rows or '<tr><td colspan="3">No activity logged yet. Tracking is active.</td></tr>'}
            </table>
        </div>
    </body>
    </html>
    """)

@app.get("/posts/best-ergonomic-office-chairs")
def chair_review():
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Say Goodbye to Lower Back Pain: Best Ergonomic Office Chairs</title>{BASE_CSS}
    </head>
    <body>
        <div class="container">
            <span class="badge">Ergonomics Guide 2026</span>
            <h1>Say Goodbye to Lower Back Pain: Best Ergonomic Chairs</h1>
            <p>Prolonged sitting without adaptive spinal alignment causes cumulative lumbar tension and postural fatigue. Whether you want high-end adjustability or budget-conscious comfort, here are the top-rated ergonomic chairs.</p>
            
            <h2>1. Top Pick: Pro Mesh Lumbar Support Chair</h2>
            <p>Designed with dynamic 3D posture adaptive cushioning, highly breathable mesh, and multi-directional adjustable armrests to eliminate shoulder fatigue.</p>
            <a href="/go/chair-premium" class="cta-btn" target="_blank" rel="nofollow noopener">Check Premium Chair on Amazon &rarr;</a>

            <h2>2. Best Value: Budget-Friendly Ergonomic Desk Chair</h2>
            <p>Reliable lumbar support and durable breathable mesh that won't break the bank. Ideal for home office workers needing spine alignment on a budget.</p>
            <a href="/go/chair-budget" class="cta-btn btn-budget" target="_blank" rel="nofollow noopener">Check Budget Chair Deals on Amazon &rarr;</a>

            <h2>Head-to-Head Comparison Matrix</h2>
            <table>
                <tr><th>Feature</th><th>Premium Tier Pick</th><th>Budget-Friendly Pick</th></tr>
                <tr><td><strong>Lumbar Support</strong></td><td>Dynamic 3D Adaptive</td><td>Integrated Contoured Curve</td></tr>
                <tr><td><strong>Weight Capacity</strong></td><td>Up to 330 lbs (150 kg)</td><td>Up to 250 lbs (113 kg)</td></tr>
                <tr><td><strong>Recline Range</strong></td><td>90° to 135° Multi-Lock</td><td>Tilt Rocking Mechanism</td></tr>
                <tr><td><strong>Material</strong></td><td>High-Tension Double Mesh</td><td>Breathable Fabric Mesh</td></tr>
            </table>

            <div class="footer">
                <p>Affiliate Disclosure: ErgoEngine earns performance-based commissions from qualifying purchases through Amazon links at no extra cost to you.</p>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/posts/top-adjustable-standing-desks")
def desk_review():
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>The Ultimate Motorized Standing Desk Setup</title>{BASE_CSS}
    </head>
    <body>
        <div class="container">
            <span class="badge">Workspace Setup Guide</span>
            <h1>The Ultimate Motorized Standing Desk Setup</h1>
            <p>Balancing sitting and standing intervals throughout your workday elevates mental sharpness, optimizes blood circulation, and prevents sedentary strain.</p>

            <h2>1. Heavy-Duty Dual Motor Standing Desk</h2>
            <p>Whisper-quiet elevation motor, reinforced anti-wobble steel frame, and programmable digital height memory presets.</p>
            <a href="/go/standing-desk" class="cta-btn" target="_blank" rel="nofollow noopener">View Standing Desk on Amazon &rarr;</a>

            <h2>2. Essential Minimalist Add-on: Heavy-Duty Dual Monitor Arm</h2>
            <p>Elevate dual displays to exact eye level to instantly eradicate forward head posture, freeing up valuable desktop workspace for a clean, minimalist setup.</p>
            <a href="/go/monitor-arm" class="cta-btn btn-budget" target="_blank" rel="nofollow noopener">View Dual Monitor Arm on Amazon &rarr;</a>

            <h2>Workspace Hardware Metrics</h2>
            <table>
                <tr><th>Core Metric</th><th>Specification</th></tr>
                <tr><td><strong>Desk Motor Configuration</strong></td><td>Dual Synchronous High-Torque Motors</td></tr>
                <tr><td><strong>Max Load Capacity</strong></td><td>265 lbs (Heavy-duty multi-display setups)</td></tr>
                <tr><td><strong>Monitor Mount Compatibility</strong></td><td>VESA 75x75 & 100x100 (Up to 32-inch screens)</td></tr>
            </table>

            <div class="footer">
                <p>Affiliate Disclosure: ErgoEngine earns performance-based commissions from qualifying purchases through Amazon links at no extra cost to you.</p>
            </div>
        </div>
    </body>
    </html>
    """)
