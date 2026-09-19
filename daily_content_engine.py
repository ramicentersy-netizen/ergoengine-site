import os
import time
import json
import requests
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\TOPTECH\Desktop\AI-Affiliate-Engine"
RAW_DIR = os.path.join(BASE_DIR, "pin_images")
BRANDED_DIR = os.path.join(BASE_DIR, "branded_pin_images")
DOWNLOAD_HISTORY = os.path.join(BASE_DIR, "downloaded_history.json")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(BRANDED_DIR, exist_ok=True)

# كلمات بحث مستهدفة لأثاث المكاتب المريحة
SEARCH_QUERIES = [
    "ergonomic office chair",
    "electric standing desk",
    "minimalist desk setup",
    "workspace ergonomics",
    "monitor arm desk",
    "home office lumbar support"
]

def load_history():
    if os.path.exists(DOWNLOAD_HISTORY):
        try:
            with open(DOWNLOAD_HISTORY, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    with open(DOWNLOAD_HISTORY, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def fetch_fresh_images(target_count=18):
    history = set(load_history())
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    downloaded_files = []
    
    print(f"⏳ جاري البحث وتنزيل {target_count} صورة جديدة غير مكررة...")
    
    for query in SEARCH_QUERIES:
        if len(downloaded_files) >= target_count:
            break
            
        url = f"https://unsplash.com/napi/search/photos?query={requests.utils.quote(query)}&per_page=20&orientation=portrait"
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json()
                results = data.get("results", [])
                
                for item in results:
                    photo_id = item.get("id")
                    if photo_id in history:
                        continue  # تخطي أي صورة تم تنزيلها سابقاً نهائياً
                    
                    img_url = item.get("urls", {}).get("regular")
                    if not img_url:
                        continue
                        
                    img_res = requests.get(img_url, headers=headers, timeout=20)
                    if img_res.status_code == 200:
                        file_name = f"fresh_{photo_id}.jpg"
                        file_path = os.path.join(RAW_DIR, file_name)
                        with open(file_path, "wb") as f:
                            f.write(img_res.content)
                            
                        history.add(photo_id)
                        downloaded_files.append((file_name, file_path))
                        print(f"  ✅ تم تنزيل صورة جديدة: {file_name}")
                        
                    if len(downloaded_files) >= target_count:
                        break
                    time.sleep(0.3)
        except Exception as e:
            print(f"  ⚠️ خطأ في الاستعلام عن '{query}': {e}")
            
    save_history(list(history))
    print(f"🎉 تم تنزيل وتوثيق {len(downloaded_files)} صورة بنجاح في مجلد pin_images!\n")
    return downloaded_files

def get_font(size, bold=True):
    fonts = ["arialbd.ttf" if bold else "arial.ttf", "calibrib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
    for fn in fonts:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        bbox = draw.textbbox((0, 0), " ".join(curr), font=font)
        if (bbox[2] - bbox[0]) > max_width:
            curr.pop()
            lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines

def brand_and_design_images():
    raw_files = [f for f in os.listdir(RAW_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not raw_files:
        print("❌ لا توجد صور خام لتصميمها.")
        return

    # عناوين وزوايا تسويقية متنوعة لزيادة التفاعل
    titles = [
        "Say Goodbye to Lower Back Pain While Working",
        "The Ultimate Motorized Standing Desk Setup",
        "Top Tested Ergonomic Chairs for Long Workdays",
        "Minimalist Desk Setup for Deep Focus & Health",
        "How to Calibrate Your Monitor Height & Posture",
        "Active Workstations: Beat Sedentary Fatigue"
    ]

    print("🎨 جاري تصميم الصور وتطبيق قوالب ErgoEngine...")
    for idx, fname in enumerate(raw_files):
        src_path = os.path.join(RAW_DIR, fname)
        out_name = f"pin_ready_{fname}"
        out_path = os.path.join(BRANDED_DIR, out_name)
        
        if os.path.exists(out_path):
            continue
            
        try:
            img = Image.open(src_path).convert("RGBA")
            target_w, target_h = 1000, 1500
            
            # ضبط القياس العمودي للبنترست (1000x1500)
            ratio = img.width / img.height
            if ratio > (target_w / target_h):
                h = target_h
                w = int(h * ratio)
            else:
                w = target_w
                h = int(w / ratio)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            left = (w - target_w) // 2
            top = (h - target_h) // 2
            img = img.crop((left, top, left + target_w, top + target_h))

            # بطاقة النص الداكنة
            overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            draw_ov = ImageDraw.Draw(overlay)
            draw_ov.rounded_rectangle([70, 160, 930, 680], radius=26, fill=(9, 13, 22, 220), outline=(56, 189, 248, 180), width=3)
            
            img = Image.alpha_composite(img, overlay).convert("RGB")
            draw = ImageDraw.Draw(img)

            # بادج الهوية
            draw.rounded_rectangle([120, 205, 430, 255], radius=10, fill="#2563eb")
            draw.text((135, 213), "ERGONOMIC GUIDE", fill="#ffffff", font=get_font(24, True))

            # العنوان المختار
            selected_title = titles[idx % len(titles)]
            title_font = get_font(52, True)
            lines = wrap_text(selected_title, title_font, 760, draw)
            y = 290
            for line in lines[:3]:
                draw.text((120, y), line, fill="#ffffff", font=title_font)
                y += 68

            # دعوة لاتخاذ إجراء ورابط الموقع
            draw.text((120, 600), "👉 View Full Setup & Buying Guide", fill="#38bdf8", font=get_font(28, True))
            
            # شريط الموقع السفلي
            draw.rounded_rectangle([320, 1420, 680, 1470], radius=18, fill=(0, 0, 0, 190))
            draw.text((350, 1432), "ergoengine-site.onrender.com", fill="#ffffff", font=get_font(22, True))

            img.save(out_path, quality=92)
            print(f"  ✨ تم تصميم: {out_name}")
        except Exception as e:
            print(f"  ❌ خطأ في تصميم {fname}: {e}")

    print("🏁 انتهى توليد التصاميم المخصصة بنجاح!")

if __name__ == "__main__":
    fetch_fresh_images(target_count=18)
    brand_and_design_images()