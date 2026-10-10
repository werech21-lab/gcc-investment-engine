import os
import json
import urllib.request
import urllib.parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from supabase import create_client, Client

# ==========================================
# 1. إعداد المتغيرات والأسرار من البيئة (Environment Secrets)
# ==========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ==========================================
# 2. نظام التنبيهات وإدارة البيانات
# ==========================================

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=payload)
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            if res.get("ok"):
                print("✅ [Telegram] تم إرسال التقرير المحدث بنجاح!")
                return True
    except Exception as e:
        print(f"❌ [Telegram Error]: {e}")
    return False


def send_email_alert(subject, html_body):
    if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
        return False
        
    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ [Email] تم إرسال التقرير بنجاح عبر البريد الإلكتروني!")
        return True
    except Exception as e:
        print(f"❌ [Email Error]: {e}")
        return False


def save_deal_to_supabase(title, price, rating, analysis, source_url, category):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠️ لم يتم العثور على أسرار Supabase. يرجى التحقق من الإعدادات.")
        return False
        
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        deal_data = {
            "title": title,
            "price": price,
            "rating": rating,
            "analysis": analysis,
            "source_url": source_url,
            "category": category
        }
        response = supabase.table("deals").insert(deal_data).execute()
        print("✅ تم حفظ الفرصة بنجاح في Supabase!")
        return True
    except Exception as e:
        print(f"❌ خطأ أثناء الحفظ في Supabase: {e}")
        return False

# ==========================================
# 3. تشغيل المحرك والتحليل الاستثماري
# ==========================================
if __name__ == "__main__":
    print("🚀 بدء تشغيل GCC Investment Engine...")
    
    # مثال لعينة من الفرص الاستثمارية المستخرجة
    sample_deal = {
        "title": "فرصة الاستثمار في الطاقة التجديدية - مشروع الخليج",
        "price": "$500,000",
        "rating": "9/10",
        "analysis": "مشروع ذو عائد استثماري مجزٍ ونسبة مخاطرة منخفضة وفقاً لبيانات السوق الأخيرة.",
        "source_url": "https://example.com/deal",
        "category": "Clean Energy"
    }
    
    # 1. حفظ الفرصة في قاعدة البيانات
    save_deal_to_supabase(
        title=sample_deal["title"],
        price=sample_deal["price"],
        rating=sample_deal["rating"],
        analysis=sample_deal["analysis"],
        source_url=sample_deal["source_url"],
        category=sample_deal["category"]
    )
    
    # 2. إرسال التنبيهات
    telegram_text = f"🏛 **{sample_deal['title']}**\nالسعر: {sample_deal['price']}\nالتقييم: {sample_deal['rating']}\nالتحليل: {sample_deal['analysis']}"
    send_telegram_alert(telegram_text)
    
    email_html = f"<h2>{sample_deal['title']}</h2><p><b>السعر:</b> {sample_deal['price']}</p><p><b>التقييم:</b> {sample_deal['rating']}</p><p>{sample_deal['analysis']}</p>"
    send_email_alert("🏛 تقرير GCC Multi-Agent: فرصة استثمارية موثقة", email_html)
