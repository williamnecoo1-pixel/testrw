import re
import urllib.request

# ============================================================
# 1. قائمة المصادر (RAW URLs)
# ============================================================
SOURCES = [
    "https://raw.githubusercontent.com/your-repo/links/main/links.txt",
    # زيد هنا المصادر ديالك
]

# ============================================================
# 2. النطاقات الأساسية ديال X / Twitter
#    المطابقة كتتم إما بالضبط (exact) أو كـ subdomain
#    مثال: "x.com" كيقبل "x.com" و "api.x.com" و "mobile.x.com"
#    ولكن ما كيقبلش "fakex.com" ولا "notx.com"
# ============================================================
X_BASE_DOMAINS = [
    # --- X و Twitter ---
    "x.com",
    "twitter.com",
    "twimg.com",       # CDN ديال الصور والوسائط
    "t.co",            # الرابط القصير الرسمي
    "pscp.tv",         # البث المباشر
    "periscope.tv",
    "grok.com",        # خدمة Grok
    "x.ai",            # شركة xAI
    "ads-twitter.com", # إعلانات

    # --- نطاقات فرعية رئيسية ديال X (كـ exact للاحتياط) ---
    "api.x.com",
    "api-stream.x.com",
    "mobile.x.com",
    "business.x.com",
    "developer.x.com",
    "docs.x.com",
    "blog.x.com",
    "about.x.com",
    "help.x.com",
    "support.x.com",
    "accounts.x.com",
    "auth.x.com",
    "login.x.com",
    "signin.x.com",
    "video.x.com",
    "video-s.x.com",
    "messages.x.com",
    "dm.x.com",
    "chat-ws.x.com",
    "analytics.x.com",
    "ads.x.com",
    "pay.x.com",
    "payments.x.com",
    "money.x.com",
    "grok.x.com",
    "grok-api.x.com",
    "api.grok.x.com",
    "xchat.x.com",
    "safety.x.com",
    "security.x.com",
    "caps.x.com",
    "aa.x.com",
    "jf.x.com",
    "jf-t.x.com",
    "ton.x.com",
    "upload.x.com",
    "vault.x.com",
    "console.x.com",
    "brand.x.com",
    "cards.x.com",
    "cards-beta.x.com",
    "cards-dev.x.com",
    "canary.x.com",
    "amplify.x.com",
    "birdwatch.x.com",
    "m.x.com",

    # --- نطاقات فرعية ديال twitter.com ---
    "api.twitter.com",
    "help.twitter.com",
    "support.twitter.com",
    "business.twitter.com",
    "developer.twitter.com",
    "dev.twitter.com",
    "ads.twitter.com",
    "analytics.twitter.com",
    "mobile.twitter.com",
    "platform.twitter.com",
    "pay.twitter.com",
    "payments.twitter.com",
    "upload.twitter.com",
    "ton.twitter.com",
    "jf.twitter.com",
    "jf-t.twitter.com",
    "caps.twitter.com",
    "safety.twitter.com",
    "security.twitter.com",
    "aa.twitter.com",
    "m.twitter.com",
    "apps.twitter.com",
    "careers.twitter.com",
    "marketing.twitter.com",
    "search.twitter.com",
    "t.twitter.com",
    "about.twitter.com",

    # --- نطاقات فرعية ديال twimg.com (CDN) ---
    "pbs.twimg.com",
    "video.twimg.com",
    "abs.twimg.com",
    "ton.twimg.com",
    "p.twimg.com",
    "r.twimg.com",
    "g.twimg.com",
    "a0.twimg.com",
    "a1.twimg.com",
    "a2.twimg.com",
    "a3.twimg.com",
    "abs-0.twimg.com",
    "abs-ak.twimg.com",
    "abs-ft.twimg.com",
    "abs-o-ak.twimg.com",
    "pbs-t-1.twimg.com",
    "pbs-h2.twimg.com",
    "video-t-2.twimg.com",
    "video-s.twimg.com",
    "cdn.syndication.twimg.com",
    "si0.twimg.com",
    "amp.twimg.com",
    "widgets.twimg.com",
]

# ============================================================
# 3. نطاقات CloudFront المرتبطة بـ X (exact match فقط)
# ============================================================
X_CLOUDFRONT_DOMAINS = [
    "d1muhwhmpsz4u8.cloudfront.net",  # chat-ws.x.com
    "d2bchqfeno8n2m.cloudfront.net",  # analytics.x.com
    "d2shtph9y6bxk.cloudfront.net",   # analytics.x.com
    "dwo3ckksxlb0v.cloudfront.net",   # تحميل الوسائط (media)
    "d2rdfnizen5apl.cloudfront.net",  # s.twimg.com (تاريخياً)
    "d2jxbhlohyq6u5.cloudfront.net",  # مرتبط بـ AS13414 (Twitter)
    "d2ag3jdu89hmr4.cloudfront.net",  # ملفات twitter.webp
    "d2fawy817reudt.cloudfront.net",  # t.co analytics
]

# دمج الكل فـ ليستة واحدة
ALLOWED_DOMAINS = X_BASE_DOMAINS + X_CLOUDFRONT_DOMAINS


# ============================================================
# 4. دالة التحقق من النطاق (exact أو subdomain)
# ============================================================
def is_allowed_sni(sni_value: str) -> bool:
    """
    كترجع True إلا كان الـ SNI مطابق بالضبط أو هو subdomain
    ديال واحد من النطاقات المسموحة.
    
    مثال:
      - "api.x.com"       ✅ (subdomain ديال x.com)
      - "x.com"           ✅ (exact)
      - "fakex.com"       ❌ (ماشي subdomain، حيت ما كيبداش بـ ".")
      - "notx.com"        ❌
      - "x.com.evil.com"  ❌
    """
    sni = sni_value.strip().lower().rstrip(".")
    if not sni:
        return False

    for domain in ALLOWED_DOMAINS:
        domain = domain.lower()
        if sni == domain or sni.endswith("." + domain):
            return True
    return False


# ============================================================
# 5. جلب الروابط من المصادر
# ============================================================
def fetch_raw_links() -> str:
    raw_data = ""
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as response:
                raw_data += response.read().decode("utf-8", errors="ignore") + "\n"
                print(f"✅ تم الجلب من: {url}")
        except Exception as e:
            print(f"❌ خطأ فـ الجلب من {url}: {e}")
    return raw_data


# ============================================================
# 6. فلترة روابط VLESS Reality حسب SNI
# ============================================================
def filter_vless_reality(text: str) -> list:
    vless_links = re.findall(r"(vless://[^\s]+)", text)
    filtered_links = []
    rejected_sni = set()

    for link in vless_links:
        # خاص يكون Reality
        if "security=reality" not in link:
            continue

        # استخراج SNI
        sni_match = re.search(r"[?&]sni=([^&]+)", link)
        if not sni_match:
            continue

        sni_value = sni_match.group(1).lower()

        if is_allowed_sni(sni_value):
            filtered_links.append(link)
        else:
            rejected_sni.add(sni_value)

    # إزالة التكرار
    filtered_links = list(dict.fromkeys(filtered_links))

    return filtered_links, rejected_sni


# ============================================================
# 7. التشغيل الرئيسي
# ============================================================
if __name__ == "__main__":
    print("🔄 جاري جمع الروابط...")
    raw_content = fetch_raw_links()

    print("🔍 جاري الفلترة: VLESS Reality + نطاقات X الموثوقة...")
    reality_links, rejected_sni = filter_vless_reality(raw_content)

    # حفظ النتائج
    with open("reality_configs.txt", "w", encoding="utf-8") as f:
        for link in reality_links:
            f.write(link + "\n")

    # طباعة ملخص
    print(f"\n✅ تم حفظ {len(reality_links)} كونفيغ Reality متوافق.")
    if rejected_sni:
        print(f"⚠️  تم رفض {len(rejected_sni)} SNI غير مطابق (أمثلة):")
        for sni in list(rejected_sni)[:10]:
            print(f"   - {sni}")
