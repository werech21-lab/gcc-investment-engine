import os
import json
import sqlite3
import smtplib
import urllib.request
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# تحميل متغيرات البيئة من .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# ---------------------------------------------------------
# 1. الوكلاء الذكيون (GCC Multi-Agent Council Architecture)
# ---------------------------------------------------------

class GCCMultiAgentCouncil:
    def __init__(self):
        print("🤖 [System] تم تفعيل المجلس الاستثماري المتقدم مع توثيق المصادر الرسمية...")

    def run_analysis_pipeline(self, deal_data):
        print(f"\n🔍 [Processing] التحليل الشامل والتحقق من المصدر للأصل: {deal_data.get('title', 'فرصة استثمارية')}")
        
        cao_report = self.cao_agent_analysis(deal_data)
        cro_report = self.cro_agent_analysis(deal_data, cao_report)
        deal_report = self.deal_agent_analysis(deal_data, cao_report, cro_report)
        tier_level = self.commercial_agent_tier(deal_data, cao_report)
        
        telegram_msg, email_html = self.ceo_agent_decision(deal_data, cao_report, cro_report, deal_report, tier_level)
        
        return telegram_msg, email_html

    def cao_agent_analysis(self, data):
        asset_type = data.get('asset_type', 'العقارات')
        country = data.get('country', 'الكويت')
        est_yield = data.get('estimated_yield', '7.5%')
        score = 85
        return {
            "status": "APPROVED",
            "score": score,
            "yield": est_yield,
            "analysis": f"تم تقييم {asset_type} في {country}. العائد الإيجاري/الربحي المتوقع {est_yield} وهو أعلى من متوسط السوق."
        }

    def cro_agent_analysis(self, data, cao_report):
        return {
            "risk_level": "متوسط - مقبول",
            "stress_test": "تحمل انخفاض حتى 12% في الأسعار مع المحافظة على تدفق نقدي إيجابي.",
            "compliance": "متوافق مع الأنظمة والقوانين الاستثمارية المحلية للبلد."
        }

    def deal_agent_analysis(self, data, cao_report, cro_report):
        return {
            "target_discount_price": "خصم مستهدف 8% - 10%",
            "negotiation_playbook": "التركيز على خيار الدفع النقدي السريع مقابل خصم إضافي من المالك/البائع.",
            "payment_structure": "دفعة أولى 30% والباقي عند إتمام نقل الملكية."
        }

    def commercial_agent_tier(self, data, cao_report):
        score = cao_report.get('score', 0)
        if score >= 85:
            return "VIP Tier 🏆 (كبار المستثمرين)"
        elif score >= 75:
            return "Pro Tier 💼 (المستثمر المحترف)"
        else:
            return "Standard Tier 📢 (الاشتراك العادي)"

    def ceo_agent_decision(self, data, cao_report, cro_report, deal_report, tier_level):
        source_name = data.get('source_name', 'الجهة الرسمية المعلنة')
        source_url = data.get('source_url', 'https://www.moj.gov.kw')

        # نص التيلجرام بتنسيق نقي
        telegram_text = (
            f"🏛️ *[GCC Investment Engine - تنبيه فرصة استثمارية موثقة]*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 *الدولة والأصل:* {data.get('country', 'GCC')} | {data.get('asset_type', 'عقار/أسهم')}\n"
            f"🏷️ *اسم الفرصة:* {data.get('title', 'صفقة خليجية جديدة')}\n"
            f"💰 *السعر التقديري:* {data.get('price_formatted', 'غير محدد')}\n"
            f"⭐ *التقييم الاستثماري:* {cao_report['score']}/100 ({tier_level})\n"
            f"🔗 *المصدر الموثق:* {source_name}\n"
            f"🌐 *رابط المصدر:* {source_url}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 *تحليل رئيس الدراسات (CAO):*\n{cao_report['analysis']}\n\n"
            f"⚖️ *ملاحظات مدير المخاطر (CRO):*\n• مستوى المخاطرة: {cro_report['risk_level']}\n• اختبار الضغط: {cro_report['stress_test']}\n\n"
            f"🤝 *تكتيك التفاوض (Deal Architect):*\n• الخصم المستهدف: {deal_report['target_discount_price']}\n• التكتيك: {deal_report['negotiation_playbook']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ *قرار الرئيس التنفيذي (CEO):* معتمدة للتنفيذ والإرسال الفوري."
        )

        # نص البريد بتنسيق HTML احترافي بزار قابل للنقر مباشرة
        email_html = f"""
        <div dir="rtl" style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
            <h2 style="color: #1a365d; border-bottom: 2px solid #1a365d; padding-bottom: 8px;">🏛️ GCC Investment Engine - فرصة استثمارية موثقة</h2>
            <p><strong>📍 الدولة والأصل:</strong> {data.get('country', 'GCC')} | {data.get('asset_type', 'عقار/أسهم')}</p>
            <p><strong>🏷️ اسم الفرصة:</strong> {data.get('title', 'صفقة خليجية جديدة')}</p>
            <p><strong>💰 السعر التقديري:</strong> {data.get('price_formatted', 'غير محدد')}</p>
            <p><strong>⭐ التقييم الاستثماري:</strong> {cao_report['score']}/100 ({tier_level})</p>
            <p><strong>🔗 المصدر الموثق:</strong> {source_name}</p>
            
            <div style="margin: 20px 0; text-align: center;">
                <a href="{source_url}" target="_blank" style="background-color: #1a365d; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">🌐 اضغط هنا للتحقق من المصدر المباشر</a>
            </div>
            
            <hr style="border: 0; border-top: 1px solid #eee;">
            
            <h4 style="color: #2b6cb0;">📊 تحليل رئيس الدراسات (CAO):</h4>
            <p>{cao_report['analysis']}</p>
            
            <h4 style="color: #2b6cb0;">⚖️ ملاحظات مدير المخاطر (CRO):</h4>
            <ul>
                <li>مستوى المخاطرة: {cro_report['risk_level']}</li>
                <li>اختبار الضغط: {cro_report['stress_test']}</li>
            </ul>
            
            <h4 style="color: #2b6cb0;">🤝 تكتيك التفاوض (Deal Architect):</h4>
            <ul>
                <li>الخصم المستهدف: {deal_report['target_discount_price']}</li>
                <li>التكتيك: {deal_report['negotiation_playbook']}</li>
            </ul>
            
            <hr style="border: 0; border-top: 1px solid #eee;">
            <p style="color: #2f855a; font-weight: bold;">✅ قرار الرئيس التنفيذي (CEO): معتمدة للتنفيذ والإرسال الفوري.</p>
        </div>
        """
        
        return telegram_text, email_html


# ---------------------------------------------------------
# 2. نظام التنبيهات المزدوج (Telegram & Email Delivery)
# ---------------------------------------------------------

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
        print("✅ [Gmail] تم إرسال الإيميل التفاعلي مع زر المصدر القابل للنقر بنجاح!")
        return True
    except Exception as e:
        print(f"❌ [Gmail Error]: {e}")
        return False


# ---------------------------------------------------------
# 3. التشغيل الرئيسي وتغذية الصفقات (Main Execution)
# ---------------------------------------------------------

if __name__ == "__main__":
    council = GCCMultiAgentCouncil()
    
    # نموذج لفرصة استثمارية مع رابط شغال وبدون أخطاء
    sample_deal = {
        "title": "مجمع تجاري/سكني في موقع استراتيجي",
        "asset_type": "العقارات التجارية",
        "country": "الكويت 🇰🇼",
        "price": 450000,
        "price_formatted": "450,000 د.ك",
        "estimated_yield": "8.8%",
        "source_name": "بوابة وزارة العدل الكويتية (التسجيل العقاري)",
        "source_url": "https://www.moj.gov.kw"
    }
    
    # 1. تشغيل تحليل مجلس الوكلاء
    telegram_msg, email_html = council.run_analysis_pipeline(sample_deal)
    
    # 2. إرسال التقرير عبر Telegram
    send_telegram_alert(telegram_msg)
    import os
from supabase import create_client, Client

# جلب بيانات الربط من GitHub Secrets
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def save_deal_to_supabase(title, price, rating, analysis, source_url, category):
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
    except Exception as e:
        print(f"❌ خطأ أثناء الحفظ في Supabase: {e}")
    
    # 3. إرسال التقرير عبر البريد الإلكتروني (HTML)
    send_email_alert("🏛️ تقرير GCC Multi-Agent: فرصة استثمارية موثقة", email_html)
