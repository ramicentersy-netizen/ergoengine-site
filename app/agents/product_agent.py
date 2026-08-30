import json
from sqlalchemy.orm import Session
from .base_agent import BaseAgent
from ..models import Product

class ProductResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Product Research Agent")

    def run_catalog_sync(self, db: Session) -> list[Product]:
        seed_products = [
            {
                "name": "Herman Miller Aeron Ergonomic Chair",
                "slug": "herman-miller-aeron",
                "brand": "Herman Miller",
                "category": "Ergonomic Chairs",
                "price": 1295.00,
                "affiliate_url": "https://www.amazon.com/s?k=Herman+Miller+Aeron+Chair",
                "affiliate_source": "Amazon Associates",
                "rating": 4.8,
                "pros_json": json.dumps([
                    "Industry-standard Pellicle 8Z breathable mesh",
                    "Forward-tilt posture mechanism for typing focus",
                    "12-year 24/7 multi-shift warranty"
                ]),
                "cons_json": json.dumps([
                    "Firm outer plastic frame limits cross-legged sitting",
                    "High initial investment",
                    "Headrest sold separately"
                ]),
                "specs_json": json.dumps({
                    "Seat Height": "16 to 20.5 inches",
                    "Max Capacity": "350 lbs (Size B/C)",
                    "Lumbar Support": "PostureFit SL Dual Support",
                    "Material": "Composite Recycled Mesh"
                }),
                "ideal_for": "Knowledge workers sitting 8+ hours needing dedicated spine posture alignment.",
                "avoid_if": "Users who prefer thick memory foam cushions or like sitting cross-legged."
            },
            {
                "name": "ErgoChair Pro Ergonomic Task Chair",
                "slug": "ergochair-pro-autonomous",
                "brand": "Autonomous",
                "category": "Ergonomic Chairs",
                "price": 499.00,
                "affiliate_url": "https://www.amazon.com/s?k=Autonomous+ErgoChair+Pro",
                "affiliate_source": "Amazon Associates",
                "rating": 4.4,
                "pros_json": json.dumps([
                    "Fully adjustable 22-degree recline with 5 lockable angles",
                    "Integrated lumbar support cushion",
                    "Exceptional price-to-performance ratio"
                ]),
                "cons_json": json.dumps([
                    "Armrest padding wears over long-term intensive use",
                    "Cushion requires a 2-week break-in period"
                ]),
                "specs_json": json.dumps({
                    "Seat Height": "18 to 21 inches",
                    "Weight Limit": "300 lbs",
                    "Recline Angle": "Up to 122 degrees",
                    "Warranty": "2 Years"
                }),
                "ideal_for": "Remote workers wanting comprehensive posture adjustability under $500.",
                "avoid_if": "Heavyweight users requiring all-mesh seat bases or 10+ year warranties."
            },
            {
                "name": "Uplift V2 Commercial Standing Desk",
                "slug": "uplift-v2-commercial-standing-desk",
                "brand": "Uplift Desk",
                "category": "Standing Desks",
                "price": 699.00,
                "affiliate_url": "https://www.amazon.com/s?k=Uplift+V2+Standing+Desk",
                "affiliate_source": "Direct Partner",
                "rating": 4.7,
                "pros_json": json.dumps([
                    "Dual-motor lift system with anti-collision safety sensors",
                    "Lower crossbar provides superior lateral stability at 45+ inches",
                    "355 lbs lifting capacity handles heavy multi-monitor arrays"
                ]),
                "cons_json": json.dumps([
                    "Heavy package requiring two people for assembly",
                    "Wire management tray sold as an upgrade"
                ]),
                "specs_json": json.dumps({
                    "Height Range": "22.6 to 48.7 inches",
                    "Lifting Capacity": "355 lbs",
                    "Motor Type": "Quiet German Dual Motors (<48 dB)",
                    "Warranty": "15 Years Frame and Electronics"
                }),
                "ideal_for": "Tall professionals (>6'1\") and setups with triple-monitor mounts.",
                "avoid_if": "Compact workstations with less than 48 inches of room space."
            },
            {
                "name": "Ergotron LX Single Monitor Arm",
                "slug": "ergotron-lx-monitor-arm",
                "brand": "Ergotron",
                "category": "Monitor Arms",
                "price": 189.00,
                "affiliate_url": "https://www.amazon.com/s?k=Ergotron+LX+Single+Monitor+Arm",
                "affiliate_source": "Amazon Associates",
                "rating": 4.9,
                "pros_json": json.dumps([
                    "Constant Force lift technology enables effortless fingertip adjustment",
                    "10,000-cycle tested mechanical spring mechanism",
                    "Clears substantial desk surface space"
                ]),
                "cons_json": json.dumps([
                    "Premium price compared to basic gas-spring alternatives",
                    "Desk clamp requires minimum 0.8 inch desk thickness"
                ]),
                "specs_json": json.dumps({
                    "Max Screen Size": "34 inches",
                    "Weight Capacity": "7 to 25 lbs",
                    "Tilt Range": "75 degrees",
                    "Warranty": "10 Years"
                }),
                "ideal_for": "Users needing eye-level screen alignment to eliminate neck and cervical strain.",
                "avoid_if": "Ultra-heavy 49-inch curved ultrawide displays."
            },
            {
                "name": "BenQ ScreenBar Halo Monitor Light",
                "slug": "benq-screenbar-halo",
                "brand": "BenQ",
                "category": "Ergonomic Lighting",
                "price": 179.00,
                "affiliate_url": "https://www.amazon.com/s?k=BenQ+ScreenBar+Halo",
                "affiliate_source": "Amazon Associates",
                "rating": 4.7,
                "pros_json": json.dumps([
                    "Asymmetric optical design prevents on-screen glare and eye fatigue",
                    "Wireless smart controller for auto-dimming & color temperature",
                    "Integrated back-light for ambient eye relaxation"
                ]),
                "cons_json": json.dumps([
                    "High cost for a desk lamp category",
                    "Requires 3 AAA batteries for wireless puck"
                ]),
                "specs_json": json.dumps({
                    "Illuminance": "Center 800 Lux",
                    "Color Temp": "2700K to 6500K",
                    "Power Input": "USB 5V/1.5A",
                    "Compatibility": "Flat and 1000R-1800R Curved Monitors"
                }),
                "ideal_for": "Late-night developers and creatives working in low-light environments prone to digital eye strain.",
                "avoid_if": "Monitors with top-mounted thick webcams that lack clip clearance."
            }
        ]

        synced = []
        for item in seed_products:
            prod = db.query(Product).filter(Product.slug == item["slug"]).first()
            if not prod:
                prod = Product(**item)
                db.add(prod)
            else:
                for k, v in item.items():
                    setattr(prod, k, v)
            synced.append(prod)
        db.commit()
        self.log(db, "CATALOG_SYNC", "SUCCESS", f"Updated {len(synced)} active product affiliate destinations.")
        return synced
