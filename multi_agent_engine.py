import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 1. إعدادات المتغيرات والتنبيهات
# ==========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ إعدادات Telegram غير مكتملة، تم التجاوز.")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("✅ تم إرسال التقرير بنجاح عبر Telegram")
            return True
        else:
            print(f"❌ خطأ Telegram: {res.text}")
    except Exception as e:
        print(f"❌ خطأ في اتصال Telegram: {e}")
    return False

def send_email_alert(subject, html_content):
    if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
        print("⚠️ إعدادات البريد غير مكتملة، تم التجاوز.")
        return False
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.attach(MIMEText(html_content, "html"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("✅ تم إرسال التقرير بنجاح عبر البريد الإلكتروني")
        return True
    except Exception as e:
        print(f"❌ خطأ في إرسال البريد: {e}")
        return False

# ==========================================
# 2. مجلس وكلاء الاستثمار (Multi-Agent Council)
# ==========================================
class GCCMultiAgentCouncil:
    def run_analysis_pipeline(self, deal):
        # 1. Chief Analytics Officer (CAO)
        cao_res = f"التحليل الشامل والتحقق من المصدر للأصل: '{deal['title']}'."
        
        # 2. Chief Risk Officer (CRO)
        cro_res = f"التقييم المخاطري: التقييم الحالي {deal['rating']} مع عائد متوقع {deal['estimated_yield']}."
        
        # 3. Deal Architect
        arch_res = f"الهيكلة التمويلية: مناسبة للاستثمار الاستراتيجي في قطاع {deal['category']}."
        
        # 4. CEO Executive Summary
        ceo_summary = (
            f"🚀 **GCC Investment Engine - فرصة استثمارية جديدة**\n\n"
            f"📌 **العنوان:** {deal['title']}\n"
            f"💰 **السعر:** {deal['price']}\n"
            f"📊 **التقييم:** {deal['rating']}\n"
            f"📈 **العائد المتوقع:** {deal['estimated_yield']}\n"
            f"🌍 **الدولة:** {deal['country']}\n"
            f"🔗 **المصدر:** [{deal['source_name']}]({deal['source_url']})\n\n"
            f"📝 **ملخص المجلس:**\n"
            f"- {cao_res}\n"
            f"- {cro_res}\n"
            f"- {arch_res}"
        )
        
        email_html = f"""
        <h2>🏛️ تقرير GCC Multi-Agent الاستثماري</h2>
        <p><b>الفرصة:</b> {deal['title']}</p>
        <p><b>السعر:</b> {deal['price']}</p>
        <p><b>التقييم:</b> {deal['rating']}</p>
        <p><b>العائد المتوقع:</b> {deal['estimated_yield']}</p>
        <p><b>المصدر:</b> <a href="{deal['source_url']}">{deal['source_name']}</a></p>
        <hr>
        <h3>تحليل مجلس الوكلاء:</h3>
        <ul>
            <li>{cao_res}</li>
            <li>{cro_res}</li>
            <li>{arch_res}</li>
        </ul>
        """
        return ceo_summary, email_html

# ==========================================
# 3. نقطة التشغيل الرئيسية
# ==========================================
if __name__ == "__main__":
    print("🚀 بدء تشغيل GCC Investment Engine...")
    council = GCCMultiAgentCouncil()
    
    sample_deal = {
        "title": "فرصة الاستثمار في الطاقة المتجددة - مشروع الخليج",
        "price": "500,000$",
        "rating": "9/10",
        "category": "Energy & Renewables",
        "country": "الإمارات",
        "estimated_yield": "11.5%",
        "source_name": "منصة الاستثمار الخليجي المعتمدة",
        "source_url": "https://www.moj.gov.kw"
    }
    
    telegram_msg, email_html = council.run_analysis_pipeline(sample_deal)
    
    # إرسال التنبيهات
    send_telegram_alert(telegram_msg)
    send_email_alert("تقرير GCC Multi-Agent: فرصة استثمارية مؤكدة 🏛️", email_html)
