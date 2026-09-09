import os
from PIL import Image, ImageDraw, ImageFont

def generate_profile_avatar():
    size = 800
    img = Image.new("RGB", (size, size), "#090d16")
    draw = ImageDraw.Draw(img)

    center = size // 2
    for r in range(260, 100, -10):
        draw.ellipse([center - r, center - r, center + r, center + r], fill="#111c35")

    draw.ellipse([60, 60, size - 60, size - 60], outline="#1e293b", width=8)
    draw.ellipse([68, 68, size - 68, size - 68], outline="#2563eb", width=4)

    draw.rounded_rectangle([250, 230, 310, 530], radius=15, fill="#38bdf8")
    draw.rounded_rectangle([310, 230, 550, 290], radius=15, fill="#38bdf8")
    draw.rounded_rectangle([310, 350, 480, 410], radius=15, fill="#60a5fa")
    draw.rounded_rectangle([310, 470, 550, 530], radius=15, fill="#2563eb")
    draw.ellipse([500, 240, 540, 280], fill="#ffffff")

    try:
        font_large = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 44)
        font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((250, 580), "ERGOENGINE", fill="#ffffff", font=font_large)
    draw.text((310, 640), "WORKSPACE LAB", fill="#38bdf8", font=font_small)

    os.makedirs("app/static", exist_ok=True)
    out = os.path.abspath("app/static/pinterest_profile.png")
    img.save(out, quality=95)
    print("SUCCESS_FILE_CREATED:" + out)

generate_profile_avatar()