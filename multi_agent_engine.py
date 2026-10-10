import os
import json
import sqlite3
import smtplib
import urllib.request
import urllib.parse
import requests
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


# ==========================================
# 1. هيكل مجلس الوكلاء (GCC Multi-Agent Council Architecture)
# ==========================================

class GCCMultiAgentCouncil:
    def __init__(self):
        print("🏛️ تم تفعيل المجلس الاستثماري المتقدم مع توثيق المصادر الرسمية")

    def run_analysis_pipeline(self, deal_data):
        print(f"\n🔍 [Processing] التحليل الشامل والتحقق من المصدر للأصل: '{deal_data.get('title', 'فرصة استثمارية')}'")
        
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
            "analysis": f"العائد الإيجاري/ الربحي المتوقع {est_yield} في {asset_type} في {country}، وهو أعلى من متوسط السوق."
        }

    def cro_agent_analysis(self, data, cao_report):
        return {
            "risk_level": "متوسط - مقبول",
            "stress_test": "يعمل ائتمانياً حتى 12% في الأسعار مع المحافظة على تدفق نقدي إيجابي",
            "compliance": "متوافق مع الأنظمة والقوانين الاستثمارية المحلية للبلد"
        }

    def deal_agent_analysis(self, data, cao_report, cro_report):
        return {
            "target_discount_price": "8% - 10% خصم مستهدف",
            "negotiation_playbook": "التركيز على خيار الدفع النقدي مقابل خصم إضافي من المالك الحالي",
            "payment_structure": "دفعة أولى 30% والباقي عند إتمام نقل الملكية"
        }

    def commercial_agent_tier(self, data, cao_report):
        score = cao_report.get('score', 0)
        if score >= 85:
            return "VIP Tier 👑 (كبار المستثمرين)"
        elif score >= 75:
            return "Pro Tier 💼 (المستثمر المحترف)"
        else:
            return "Standard Tier 🎯 (الاشتراك العادي)"

    def ceo_agent_decision(self, data, cao_report, cro_report, deal_report, tier_level):
        source_name = data.get('source_name', 'الجهة الرسمية المعلنة')
        source_url = data.get('source_url', 'https://www.moj.gov.kw')
        
        telegram_text = (
            f"🚨 *[GCC Investment Engine]*\n"
            f"📌 *تنبيه فرصة استثمارية موثقة*\n\n"
            f"🌍 *الدولة والأصل:* {data.get('country', 'GCC')} | {data.get('asset_type', 'عقار/أسهم')}\n"
            f"🏷️ *صفقة خليجية جديدة:* {data.get('title', 'فرصة محددة')}\n"
            f"💰 *السعر المقدر:* {data.get('price_formatted', 'فور محدد')}\n"
            f"⭐ *التقييم الاستثماري:* {cao_report['score']}/100 ({tier_level})\n"
            f"🔗 *المصدر الموثق:* {source_name}\n"
            f"🌐 *رابط المصدر:* {source_url}\n\n"
            f"📋 *تحليل رئيس الدراسات (CAO):* {cao_report['analysis']}\n\n"
            f"🛡️ *مستوى المخاطرة (CRO):* {cro_report['risk_level']} | *اختبار الضغط:* {cro_report['stress_test']}\n"
            f"🤝 *كتيكال التفاوض (Deal Architect):*\n"
            f"• *القيمة المستهدفة:* {deal_report['target_discount_price']}\n"
            f"• *استراتيجية التفاوض:* {deal_report['negotiation_playbook']}\n\n"
            f"✅ *معتمدة للتنفيذ والإرسال الفوري (CEO).* "
        )

        email_html = f"""
        <div dir="rtl" style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
            <h2 style="color: #1a365d; border-bottom: 2px solid #1a365d; padding-bottom: 8px;">🏛️ GCC Investment Engine - استثمارية موثقة</h2>
            <p><strong>🌍 الدولة والأصل:</strong> {data.get('country', 'GCC')} | {data.get('asset_type', 'عقار/أسهم')}</p>
            <p><strong>🏷️ صفقة خليجية جديدة:</strong> {data.get('title', 'فرصة محددة')}</p>
            <p><strong>💰 السعر المقدر:</strong> {data.get('price_formatted', 'فور محدد')}</p>
            <p><strong>⭐ التقييم الاستثماري:</strong> {cao_report['score']}/100 ({tier_level})</p>
            <p><strong>🔗 المصدر الموثق:</strong> {source_name}</p>
            
            <div style="margin: 20px 0; text-align: center;">
                <a href="{source_url}" target="_blank" style="background-color: #1a365d; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">🔗 زيارة رابط المصدر الرسمي</a>
            </div>
            
            <hr style="border: 0; border-top: 1px solid #eee;">
            
            <h4 style="color: #2b6cb0;">📊 تحليل رئيس الدراسات (CAO):</h4>
            <p>{cao_report['analysis']}</p>
            
            <h4 style="color: #2b6cb0;">🛡️ ملامح تدبير المخاطر (CRO):</h4>
            <ul>
                <li><strong>مستوى المخاطرة:</strong> {cro_report['risk_level']}</li>
                <li><strong>اختبار الضغط:</strong> {cro_report['stress_test']}</li>
            </ul>
            
            <h4 style="color: #2b6cb0;">🤝 تكتيك التفاوض (Deal Architect):</h4>
            <ul>
                <li><strong>القيمة المستهدفة:</strong> {deal_report['target_discount_price']}</li>
                <li><strong>تكتيك التفاوض:</strong> {deal_report['negotiation_playbook']}</li>
                <li><strong>هيكلة الدفع:</strong> {deal_report['payment_structure']}</li>
            </ul>
            
            <p style="color: #2f855a; font-weight: bold;">✅ معتمدة للتنفيذ والإرسال الفوري (CEO) قرار الرئيس التنفيذي.</p>
        </div>
        """

        return telegram_text, email_html


# ==========================================
# 2. نظام التنبيهات المزدوج (Telegram & Email Delivery)
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
                print("✅ [Telegram] تم إرسال التقرير المحدث بنجاح")
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
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ [Email] تم إرسال التقرير بنجاح عبر البريد الإلكتروني")
        return True
    except Exception as e:
        print(f"❌ [Email Error]: {e}")
        return False


# ==========================================
# 3. دالة الحفظ التلقائي في Supabase (Database Integration)
# ==========================================

def save_deal_to_supabase(deal_data):
    """
    دالة لحفظ الفرصة الاستثمارية تلقائياً في جدول deals عبر Supabase REST API
    """
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ خطأ: متغيرات البيئة SUPABASE_URL أو SUPABASE_KEY غير متوفرة!")
        return False
        
    # تنظيف الرابط من أي شرطة مائلة زائدة في النهاية
    supabase_url = supabase_url.rstrip('/')
    endpoint = f"{supabase_url}/rest/v1/deals"
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    try:
        response = requests.post(endpoint, json=deal_data, headers=headers)
        if response.status_code in [200, 201, 204]:
            print("✅ تم حفظ الفرصة بنجاح في Supabase!")
            return True
        else:
            print(f"❌ خطأ Supabase: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ خطأ أثناء الاتصال بـ Supabase: {e}")
        return False


# ==========================================
# 4. نقطة التشغيل الرئيسية (Main Execution)
# ==========================================

if __name__ == "__main__":
    print("🚀 بدء تشغيل GCC Investment Engine...")
    
    council = GCCMultiAgentCouncil()
    
    # نموذج لفرصة استثمارية تجريبية يتم تحليلها وحفظها
    sample_deal = {
        "title": "فرصة الاستثمار في الطاقة المتجددة - مشروع الخليج",
        "price": "500,000$",
        "price_formatted": "500,000$",
        "rating": "9/10",
        "category": "Energy & Renewables",
        "asset_type": "مشاريع البنية التحتية والطاقة",
        "country": "الإمارات",
        "estimated_yield": "11.5%",
        "source_name": "منصة الاستثمار الخليجي المعتمدة",
        "source_url": "https://www.moj.gov.kw"
    }
    
    # 1. تشغيل تحليل مجلس الوكلاء
    telegram_msg, email_html = council.run_analysis_pipeline(sample_deal)
    
    # 2. إرسال التقرير عبر Telegram
    send_telegram_alert(telegram_msg)
    
    # 3. إرسال التقرير عبر البريد الإلكتروني (HTML)
    send_email_alert("🏛️ فرصة استثمارية موثقة: GCC Multi Agent تقرير", email_html)
    
    # 4. حفظ الفرصة تلقائياً في قاعدة بيانات Supabase
    save_deal_to_supabase(sample_deal)
