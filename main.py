import re
import urllib.request

# ============================================================
# 1. قائمة المصادر (RAW URLs)
# ============================================================
SOURCES = [
     "https://github.com/morpheusadam/v2ray-config/raw/refs/heads/main/subs/bundles/vmess.txt",
    "https://github.com/morpheusadam/v2ray-config/raw/refs/heads/main/subs/bundles/vless.txt",
    "https://github.com/morpheusadam/v2ray-config/raw/refs/heads/main/subs/bundles/trojan.txt",
    "https://github.com/liMilCo/v2r/raw/refs/heads/main/new_configs.txt",
    "https://github.com/Delta-Kronecker/V2ray-Config/raw/refs/heads/main/config/all_configs.txt",
    "https://github.com/0xRadikal/Free-v2ray-Configs/raw/refs/heads/main/all/configs.txt",
    "https://github.com/MaxFreudDrethe/VCC/raw/refs/heads/main/configs/tls.txt",
    "https://github.com/MaxFreudDrethe/VCC/raw/refs/heads/main/configs/all.txt",
    "https://github.com/MohammadBahemmat/V2ray-Collector/raw/refs/heads/main/servers/trojan_servers.txt",
    "https://github.com/MohammadBahemmat/V2ray-Collector/raw/refs/heads/main/servers/vless_servers.txt",
    "https://github.com/MohammadBahemmat/V2ray-Collector/raw/refs/heads/main/servers/vmess_servers.txt",
    "https://raw.githubusercontent.com/0xRadikal/Free-v2ray-Configs/refs/heads/main/all/configs.txt",
    "https://raw.githubusercontent.com/Firmfox/Proxify/refs/heads/main/v2ray_configs/separated_by_protocol/mixed.txt",
    "https://raw.githubusercontent.com/MustafaBaqer/VestraNet-Nodes/refs/heads/main/subscriptions/mix-normal.txt",
    "https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/refs/heads/main/sub.txt",
    "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/All_Configs_Sub.txt",
     "https://github.com/Mohamedhnini-a/testeur/raw/refs/heads/main/working_configs.txt",
    "https://github.com/Mohamedhnini-a/testeur/raw/refs/heads/main/working_configs.txt",
    "https://github.com/MustafaBaqer/VestraNet-Nodes/raw/refs/heads/main/subscriptions/mix-normal.txt",
     "https://github.com/VOID-Anonymity/V.O.I.D-VPN_Bypass/raw/refs/heads/main/url_work.txt",
     "https://raw.githubusercontent.com/ashah404/V2rayCollector/refs/heads/main/subscribe/layers/ipv4",
     "https://github.com/YawStar/Proxy-Hunter/raw/refs/heads/main/configs/proxy_configs_tested.txt",
     "https://github.com/Mohamedhnini-a/testeur-2/raw/refs/heads/main/working_configs.txt",
     "https://github.com/0xRadikal/Free-v2ray-Configs/raw/refs/heads/main/all/configs.txt",
     "https://github.com/kort0881/vpn-vless-configs-russia/raw/refs/heads/main/data/githubmirror/ru-sni/trojan.txt",
     "https://github.com/kort0881/vpn-vless-configs-russia/raw/refs/heads/main/data/githubmirror/ru-sni/vless.txt",
     "https://github.com/asgharkapk/Sub-Config-Extractor/raw/refs/heads/main/output_configs/mixed/10ium/HiN-VPN/subscription/hiddify/trojan.yaml",
     "https://github.com/asgharkapk/Sub-Config-Extractor/raw/refs/heads/main/output_configs/mixed/10ium/HiN-VPN/subscription/hiddify/vmess.yaml",
     "https://github.com/asgharkapk/Sub-Config-Extractor/raw/refs/heads/main/output_configs/mixed/AzadNet/-t.me.yaml",
     "https://github.com/roosterkid/openproxylist/raw/refs/heads/main/V2RAY_RAW.txt",
     "https://github.com/SoliSpirit/SolVPN/raw/refs/heads/main/Protocols/trojan.txt",
     "https://github.com/SoliSpirit/SolVPN/raw/refs/heads/main/Protocols/vmess.txt",
     "https://github.com/YawStar/Proxy-Hunter/raw/refs/heads/main/configs/proxy_configs_tested.txt",
     "https://github.com/chaishpish/free_server_v2ray/raw/refs/heads/main/@TFMTProto",
     "https://github.com/lm705/vair/raw/refs/heads/main/vless_alive.txt",
     "https://github.com/SoliSpirit/SolVPN/raw/refs/heads/main/Protocols/vless.txt",
    "https://github.com/rtwo2/FastNodes/raw/refs/heads/main/sub/ipv4_only.txt",
  "https://github.com/crackbest/V2ray-Config/raw/refs/heads/main/config.txt",
  "https://github.com/Delta-Kronecker/V2ray-Config/raw/refs/heads/main/config/all_configs.txt",
  "https://github.com/10Dream/sub-mod/raw/refs/heads/main/sub/normal/10ium-V2Hub3-vless",
  "https://github.com/10Dream/sub-mod/raw/refs/heads/main/sub/normal/10ium-V2Hub3-trojan",
  "https://github.com/10Dream/sub-mod/raw/refs/heads/main/sub/normal/10Dream-VpnClashFaCollector-mixed.txt",
  "https://github.com/MustafaBaqer/VestraNet-Nodes/raw/refs/heads/main/subscriptions/mix-normal.txt",
  "https://github.com/Firmfox/Proxify/raw/refs/heads/main/v2ray_configs/separated_by_protocol/trojan.txt",
  "https://github.com/Firmfox/Proxify/raw/refs/heads/main/v2ray_configs/separated_by_protocol/vless.txt",
  "https://github.com/Firmfox/Proxify/raw/refs/heads/main/v2ray_configs/separated_by_protocol/vmess.txt",
  "https://github.com/miladtahanian/V2RayCFGDumper/raw/refs/heads/main/sub.txt",
  "https://github.com/Delta-Kronecker/V2ray-Config/raw/refs/heads/main/config/all_configs.txt",
  "https://github.com/ShatakVPN/ConfigForge-V2Ray/raw/refs/heads/main/configs/all.txt",
  "https://github.com/0xRadikal/Free-v2ray-Configs/raw/refs/heads/main/all/configs.txt",
  "https://github.com/roosterkid/openproxylist/raw/refs/heads/main/V2RAY_RAW.txt",
  "https://github.com/miladtahanian/V2RayScrapeByCountry/raw/refs/heads/main/output_configs/Trojan.txt",
  "https://github.com/miladtahanian/V2RayScrapeByCountry/raw/refs/heads/main/output_configs/Vless.txt",
  "https://github.com/miladtahanian/V2RayScrapeByCountry/raw/refs/heads/main/output_configs/Vmess.txt",
  "https://github.com/miladtahanian/V2RayScrapeByCountry/raw/refs/heads/main/Countries/.txt",
  "https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix",
  "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/Splitted-By-Protocol/trojan.txt",
  "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/Splitted-By-Protocol/vless.txt",
  "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/Splitted-By-Protocol/vmess.txt",
     "https://github.com/iboxz/free-v2ray-collector/raw/refs/heads/main/main/mix.txt",
  "https://github.com/iboxz/free-v2ray-collector/raw/refs/heads/main/main/mix",
  "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/Splitted-By-Protocol/trojan.txt",
  "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/Splitted-By-Protocol/vless.txt",
  "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/Splitted-By-Protocol/vmess.txt",
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
