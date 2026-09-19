import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

BASE_DIR = r"C:\Users\TOPTECH\Desktop\AI-Affiliate-Engine"
BRANDED_DIR = os.path.join(BASE_DIR, "branded_pin_images")
PUBLISHED_LOG = os.path.join(BASE_DIR, "published_pins.json")

# بيانات المقالات والروابط والهاشتاغات التابعة للموقع (شاملة المقال الجديد)
CAMPAIGNS = [
    {
        "title": "Best Ergonomic Office Chairs for Back Pain Relief (2026)",
        "description": "Say goodbye to lower back pain. We tested the best ergonomic office chairs engineered for spinal alignment, lumbar support, and all-day comfort.",
        "hashtags": "#ErgonomicChair #OfficeSetup #BackPainRelief #WFHEssentials #ErgoEngine",
        "link": "https://ergoengine-site.onrender.com/posts/best-ergonomic-office-chairs"
    },
    {
        "title": "Top Adjustable Standing Desks for Healthy Workspaces",
        "description": "Boost daily energy and conquer sedentary fatigue with electric sit-to-stand desks. Complete review on dual-motor stability and cable management.",
        "hashtags": "#StandingDesk #ActiveWorkstation #ProductivityHacks #DeskSetup #Ergonomics",
        "link": "https://ergoengine-site.onrender.com/posts/top-adjustable-standing-desks"
    },
    {
        "title": "How to Build a Silent, Sensory-Friendly Ergonomic Setup",
        "description": "Eliminate sensory strain, desk vibrations, and visual glare with tested acoustic felt mats and low-fatigue workspace gear.",
        "hashtags": "#SensoryErgonomics #MinimalistDesk #WorkspaceGoals #Productivity #DeskInspo",
        "link": "https://ergoengine-site.onrender.com/posts/silent-sensory-ergonomic-desk-setup"
    },
    {
        "title": "Top Ergonomic Vertical Mice for Wrist Pain Relief (2026)",
        "description": "Say goodbye to wrist fatigue and carpal tunnel pain. Discover the best vertical ergonomic mice compared for precision, grip angle, and all-day comfort.",
        "hashtags": "#VerticalMouse #ErgonomicSetup #DeskPosture #WFHDesk #ErgoEngine",
        "link": "https://ergoengine-site.onrender.com/posts/best-vertical-ergonomic-mouse-guide"
    }
]

def get_published():
    if os.path.exists(PUBLISHED_LOG):
        try:
            with open(PUBLISHED_LOG, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def log_published(filename):
    data = get_published()
    if filename not in data:
        data.append(filename)
        with open(PUBLISHED_LOG, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def setup_browser():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    return webdriver.Chrome(options=options)

def run_daily_scheduler(pins_limit=3):
    published = set(get_published())
    available = [f for f in os.listdir(BRANDED_DIR) if f.lower().endswith(('.jpg', '.png')) and f not in published]

    if not available:
        print("⚠️ لا توجد صور مصممة جديدة غير منشورة! شغّل أولاً: python daily_content_engine.py")
        return

    selected_today = available[:pins_limit]
    print(f"🚀 سيتم الآن رفع وجدولة {len(selected_today)} دبابيس لليوم...")

    driver = setup_browser()
    wait = WebDriverWait(driver, 15)

    for idx, img_name in enumerate(selected_today):
        camp = CAMPAIGNS[idx % len(CAMPAIGNS)]
        img_path = os.path.abspath(os.path.join(BRANDED_DIR, img_name))
        full_desc = f"{camp['description']}\n\n{camp['hashtags']}"

        print(f"\n📌 [{idx+1}/{len(selected_today)}] جاري إدراج: {camp['title'][:35]}...")
        driver.get("https://www.pinterest.com/pin-builder/")
        time.sleep(5)

        try:
            # 1. إدراج الصورة
            file_input = None
            try:
                file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            except Exception:
                inputs = driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    if inp.get_attribute("type") == "file":
                        file_input = inp
                        break

            if file_input:
                file_input.send_keys(img_path)
                print(f"   ✔️ رُفعت الصورة: {img_name}")
                time.sleep(4)
            else:
                raise Exception("تعذر العثور على عنصر رفع الملفات (input type=file)")

            # 2. إدخال العنوان
            title_selectors = [
                "//input[contains(@id, 'storyboard-selector-title')]",
                "//div[@role='textbox' and (contains(@aria-label, 'عنوان') or contains(@aria-label, 'Title'))]",
                "//textarea[contains(@placeholder, 'عنوان') or contains(@placeholder, 'Title')]",
                "//input[@type='text' and contains(@placeholder, 'عنوان')]"
            ]
            for sel in title_selectors:
                try:
                    title_elem = driver.find_element(By.XPATH, sel)
                    title_elem.click()
                    title_elem.send_keys(Keys.CONTROL + "a")
                    title_elem.send_keys(Keys.BACKSPACE)
                    title_elem.send_keys(camp["title"])
                    print("   ✔️ كُتب العنوان.")
                    break
                except Exception:
                    continue

            # 3. إدخال الوصف مع الهاشتاغات
            try:
                desc_selectors = [
                    "//div[@role='textbox' and (contains(@aria-label, 'وصف') or contains(@aria-label, 'Description'))]",
                    "//textarea[contains(@placeholder, 'وصف') or contains(@placeholder, 'قصة')]",
                    "//div[contains(@class, 'notranslate') and @role='textbox']"
                ]
                for d_sel in desc_selectors:
                    try:
                        desc_elem = driver.find_element(By.XPATH, d_sel)
                        desc_elem.click()
                        desc_elem.send_keys(full_desc)
                        print("   ✔️ كُتب الوصف والهاشتاغات.")
                        break
                    except Exception:
                        continue
            except Exception:
                pass

            # 4. الرابط الرسمي للمقال
            try:
                link_selectors = [
                    "//input[contains(@id, 'storyboard-selector-link')]",
                    "//input[contains(@placeholder, 'رابط') or contains(@placeholder, 'link')]",
                    "//input[@type='text' and contains(@id, 'link')]"
                ]
                for l_sel in link_selectors:
                    try:
                        link_elem = driver.find_element(By.XPATH, l_sel)
                        link_elem.click()
                        link_elem.send_keys(Keys.CONTROL + "a")
                        link_elem.send_keys(camp["link"])
                        print("   ✔️ أُضيف الرابط الرسمي.")
                        break
                    except Exception:
                        continue
            except Exception:
                pass

            time.sleep(2)

            # 5. اختيار 'النشر في تاريخ لاحق'
            try:
                schedule_options = driver.find_elements(
                    By.XPATH, 
                    "//label[contains(., 'النشر في تاريخ لاحق')] | //input[@value='SCHEDULE']/.. | //span[contains(text(), 'النشر في تاريخ لاحق')]/ancestor::label"
                )
                if schedule_options:
                    driver.execute_script("arguments[0].click();", schedule_options[0])
                    print("   ✔️ حُدد خيار الجدولة.")
                    time.sleep(2)
            except Exception:
                pass

            # 6. الضغط على زر الحفظ / النشر المجدول
            publish_selectors = [
                "//button[@data-test-id='board-dropdown-save-button']",
                "//button[contains(@class, 'red') or contains(@style, 'background-color')][contains(., 'نشر') or contains(., 'Publish') or contains(., 'جدولة') or contains(., 'Schedule')]",
                "//div[contains(@class, 'PinCreation')]//button[contains(., 'نشر') or contains(., 'Publish')]",
                "//button[contains(., 'نشر') or contains(., 'Publish')]"
            ]

            btn_clicked = False
            for p_sel in publish_selectors:
                try:
                    candidates = driver.find_elements(By.XPATH, p_sel)
                    for btn in candidates:
                        if btn.is_displayed():
                            driver.execute_script("arguments[0].click();", btn)
                            btn_clicked = True
                            print("   🎉 تم النقر على زر النشر / الحفظ بنجاح!")
                            break
                    if btn_clicked:
                        break
                except Exception:
                    continue

            if not btn_clicked:
                driver.execute_script("let b = document.querySelector('button[type=\"submit\"], button.red, [data-test-id*=\"save\"]'); if(b) b.click();")
                print("   🎉 تم تنفيذ أمر النقر بالـ JS بنجاح!")

            log_published(img_name)
            time.sleep(8)

        except Exception as e:
            print(f"   ❌ تعذر إتمام الدبوس: {e}")

    print("\n🏁 اكتملت الجدولة بنجاح!")

if __name__ == "__main__":
    run_daily_scheduler(pins_limit=3)