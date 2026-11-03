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
    "https://github.com/MustafaBaqer/VestraNet-Nodes/raw/refs/heads/main/subscriptions/mix-normal.txt",
    "https://github.com/VOID-Anonymity/V.O.I.D-VPN_Bypass/raw/refs/heads/main/url_work.txt",
    "https://raw.githubusercontent.com/ashah404/V2rayCollector/refs/heads/main/subscribe/layers/ipv4",
    "https://github.com/YawStar/Proxy-Hunter/raw/refs/heads/main/configs/proxy_configs_tested.txt",
    "https://github.com/Mohamedhnini-a/testeur-2/raw/refs/heads/main/working_configs.txt",
    "https://github.com/kort0881/vpn-vless-configs-russia/raw/refs/heads/main/data/githubmirror/ru-sni/trojan.txt",
    "https://github.com/kort0881/vpn-vless-configs-russia/raw/refs/heads/main/data/githubmirror/ru-sni/vless.txt",
    "https://github.com/asgharkapk/Sub-Config-Extractor/raw/refs/heads/main/output_configs/mixed/10ium/HiN-VPN/subscription/hiddify/trojan.yaml",
    "https://github.com/asgharkapk/Sub-Config-Extractor/raw/refs/heads/main/output_configs/mixed/10ium/HiN-VPN/subscription/hiddify/vmess.yaml",
    "https://github.com/asgharkapk/Sub-Config-Extractor/raw/refs/heads/main/output_configs/mixed/AzadNet/-t.me.yaml",
    "https://github.com/roosterkid/openproxylist/raw/refs/heads/main/V2RAY_RAW.txt",
    "https://github.com/SoliSpirit/SolVPN/raw/refs/heads/main/Protocols/trojan.txt",
    "https://github.com/SoliSpirit/SolVPN/raw/refs/heads/main/Protocols/vmess.txt",
    "https://github.com/chaishpish/free_server_v2ray/raw/refs/heads/main/@TFMTProto",
    "https://github.com/lm705/vair/raw/refs/heads/main/vless_alive.txt",
    "https://github.com/SoliSpirit/SolVPN/raw/refs/heads/main/Protocols/vless.txt",
    "https://github.com/rtwo2/FastNodes/raw/refs/heads/main/sub/ipv4_only.txt",
    "https://github.com/crackbest/V2ray-Config/raw/refs/heads/main/config.txt",
    "https://github.com/10Dream/sub-mod/raw/refs/heads/main/sub/normal/10ium-V2Hub3-vless",
    "https://github.com/10Dream/sub-mod/raw/refs/heads/main/sub/normal/10ium-V2Hub3-trojan",
    "https://github.com/10Dream/sub-mod/raw/refs/heads/main/sub/normal/10Dream-VpnClashFaCollector-mixed.txt",
    "https://github.com/Firmfox/Proxify/raw/refs/heads/main/v2ray_configs/separated_by_protocol/trojan.txt",
    "https://github.com/Firmfox/Proxify/raw/refs/heads/main/v2ray_configs/separated_by_protocol/vless.txt",
    "https://github.com/Firmfox/Proxify/raw/refs/heads/main/v2ray_configs/separated_by_protocol/vmess.txt",
    "https://github.com/miladtahanian/V2RayCFGDumper/raw/refs/heads/main/sub.txt",
    "https://github.com/ShatakVPN/ConfigForge-V2Ray/raw/refs/heads/main/configs/all.txt",
    "https://github.com/miladtahanian/V2RayScrapeByCountry/raw/refs/heads/main/output_configs/Trojan.txt",
    "https://github.com/miladtahanian/V2RayScrapeByCountry/raw/refs/heads/main/output_configs/Vless.txt",
    "https://github.com/miladtahanian/V2RayScrapeByCountry/raw/refs/heads/main/output_configs/Vmess.txt",
    "https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix",
    "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/Splitted-By-Protocol/trojan.txt",
    "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/Splitted-By-Protocol/vless.txt",
    "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/Splitted-By-Protocol/vmess.txt",
    "https://github.com/iboxz/free-v2ray-collector/raw/refs/heads/main/main/mix.txt",
    "https://github.com/iboxz/free-v2ray-collector/raw/refs/heads/main/main/mix"
]

# ============================================================
# 2. القائمة العملاقة لنطاقات X / Cloudflare (أكثر من 120 نطاق)
# ============================================================
ALLOWED_DOMAINS = [
    # --- النطاقات الأساسية والجذور ---
    "x.com", "twitter.com", "twimg.com", "t.co", "pscp.tv", "periscope.tv",
    "ads-twitter.com", "grok.com", "x.ai",

    # --- نطاقات CDN الصريحة عبر Cloudflare ---
    "x.com.cdn.cloudflare.net",
    "api.twitter.com.cdn.cloudflare.net",
    "dynamic.x.com.cdn.cloudflare.net",
    "help.twitter.com.cdn.cloudflare.net",
    "pbs.twimg.com.cdn.cloudflare.net",
    "video.twimg.com.cdn.cloudflare.net",
    "abs.twimg.com.cdn.cloudflare.net",
    "cdn.syndication.twimg.com.cdn.cloudflare.net",
    "platform.twitter.com.cdn.cloudflare.net",
    "t.co.cdn.cloudflare.net",

    # --- نطاقات API والخدمات الأساسية (x.com) ---
    "api.x.com", "api-stream.x.com", "api-staging.x.com", "api-t4.x.com",
    "api-ak-dev.x.com", "graphql.x.com", "syapi.x.com", "niche-api.x.com",
    "mobile.x.com", "m.x.com", "app.x.com", "apps.x.com", "lite.x.com",
    "business.x.com", "developer.x.com", "developers.x.com", "docs.x.com",
    "blog.x.com", "about.x.com", "help.x.com", "support.x.com",
    "accounts.x.com", "auth.x.com", "login.x.com", "signin.x.com",
    "auth-grokgs.x.com", "account-grokgs.x.com", "grok.x.com", "grok-api.x.com",
    "chat-ws.x.com", "messages.x.com", "dms.x.com", "dm.x.com",
    "video.x.com", "video-s.x.com", "media.x.com", "img.x.com", "fonts.x.com",
    "analytics.x.com", "ads.x.com", "advertising.x.com", "ads-staging.x.com",
    "pay.x.com", "payments.x.com", "money.x.com", "p.payments-prod.x.com",
    "p.payments-staging.x.com", "money-support.x.com", "money-support-dev.x.com",
    "money-support-staging.x.com", "realm-a.x.com", "realm-b.x.com",
    "realm-cloud1.x.com", "realm-east1.x.com", "realm-west1.x.com",
    "safety.x.com", "security.x.com", "trust.x.com", "caps.x.com",
    "aa.x.com", "jf.x.com", "jf-t.x.com", "ton.x.com", "upload.x.com",
    "upload-a.x.com", "upload-b.x.com", "vault.x.com", "console.x.com",
    "brand.x.com", "brand-dev.x.com", "brand-staging.x.com", "cards.x.com",
    "cards-beta.x.com", "cards-dev.x.com", "cards-staging.x.com",
    "canary.x.com", "amplify.x.com", "birdwatch.x.com", "communitynotes.x.com",
    "communitynotes-staging.x.com", "create.x.com", "create-dev.x.com",
    "create-staging.x.com", "directresponse.x.com", "discover.x.com",
    "elections.x.com", "elp.x.com", "email.x.com", "eng.x.com",
    "ethicshelpline.x.com", "event.x.com", "gdpr-staging.x.com",
    "grow.x.com", "growth.x.com", "handles.x.com", "hsm-staging.x.com",
    "innovators.x.com", "legal-dev.x.com", "mail.x.com", "marketing.x.com",
    "marketing-dev.x.com", "marketing-staging.x.com", "momentmaker.x.com",
    "mx3.x.com", "mx4.x.com", "opensource.x.com", "partners.x.com",
    "paymentaging.x.com", "paymenxrod.x.com", "people.x.com", "platform.x.com",
    "port.x.com", "postmaster.x.com", "pr.x.com", "premium.x.com", "press.x.com",
    "privacy-dev.x.com", "probe.x.com", "proofpoint.x.com", "publish.x.com",
    "publisher.x.com", "redirect.x.com", "research.x.com", "salessupport.x.com",
    "search.x.com", "shop.x.com", "status.x.com", "studio-dev.x.com",
    "syndication.x.com", "td.x.com", "terafab.x.com", "transparency-dev.x.com",
    "transparency-staging.x.com", "tweetdeck.x.com", "twemoji.x.com",
    "verified.x.com", "verified-staging.x.com", "webhook.x.com", "wr.x.com",
    "ww.x.com", "cdn.syndication.x.com", "click.send.x.com", "dev.x.com",
    "developer-staging.x.com", "developers-mp-dev.x.com", "developers-mp.x.com",
    "spring-chicken.x.com", "spring-chicken-aa.x.com", "spring-chicken-an.x.com",
    "spring-chicken-at.x.com", "spring-chicken-au.x.com", "spruce-goose-ab.x.com",
    "spruce-goose-ac.x.com", "spruce-goose-af.x.com", "spruce-goose-ah.x.com",

    # --- نطاقات Twitter (twitter.com) ---
    "api.twitter.com", "api2.twitter.com", "graphql.twitter.com",
    "help.twitter.com", "support.twitter.com", "business.twitter.com",
    "developer.twitter.com", "dev.twitter.com", "ads.twitter.com",
    "analytics.twitter.com", "mobile.twitter.com", "platform.twitter.com",
    "pay.twitter.com", "payments.twitter.com", "upload.twitter.com",
    "ton.twitter.com", "jf.twitter.com", "jf-t.twitter.com", "caps.twitter.com",
    "safety.twitter.com", "security.twitter.com", "aa.twitter.com",
    "m.twitter.com", "apps.twitter.com", "careers.twitter.com",
    "marketing.twitter.com", "search.twitter.com", "t.twitter.com",
    "about.twitter.com", "blog.twitter.com", "events.twitter.com",
    "jobs.twitter.com", "media.twitter.com", "static.twitter.com",
    "www.twitter.com", "www2.twitter.com", "calendar.twitter.com",
    "data.twitter.com", "design.twitter.com", "download.twitter.com",
    "event.twitter.com", "live.twitter.com", "stream.twitter.com",
    "video.twitter.com", "mail.twitter.com", "mx.twitter.com", "mx1.twitter.com",
    "mx2.twitter.com", "mx3.twitter.com", "dashboard.twitter.com",

    # --- نطاقات Twimg (CDN الصور والوسائط) ---
    "pbs.twimg.com", "video.twimg.com", "abs.twimg.com", "ton.twimg.com",
    "p.twimg.com", "r.twimg.com", "g.twimg.com", "a0.twimg.com",
    "a1.twimg.com", "a2.twimg.com", "a3.twimg.com", "abs-0.twimg.com",
    "abs-ak.twimg.com", "abs-ft.twimg.com", "abs-o-ak.twimg.com",
    "pbs-t-1.twimg.com", "pbs-h2.twimg.com", "video-t-2.twimg.com",
    "video-s.twimg.com", "cdn.syndication.twimg.com", "si0.twimg.com",
    "amp.twimg.com", "widgets.twimg.com", "abs-t-1.twimg.com",
    "abs-zero.twimg.com", "dnt-o.twimg.com", "fastly-private-purge.twimg.com",
    "ftl.twimg.com", "video-zero.twimg.com",

    # --- نطاقات CloudFront (مرتبطة بـ X كما اتفقنا سابقاً) ---
    "d1muhwhmpsz4u8.cloudfront.net", "d2bchqfeno8n2m.cloudfront.net",
    "d2shtph9y6bxk.cloudfront.net", "dwo3ckksxlb0v.cloudfront.net",
    "d2rdfnizen5apl.cloudfront.net", "d2jxbhlohyq6u5.cloudfront.net",
    "d2ag3jdu89hmr4.cloudfront.net", "d2fawy817reudt.cloudfront.net",
]

# ============================================================
# 3. دالة التحقق (Exact match أو Subdomain)
# ============================================================
def is_allowed_sni(sni_value: str) -> bool:
    sni = sni_value.strip().lower().rstrip(".")
    if not sni:
        return False

    for domain in ALLOWED_DOMAINS:
        domain = domain.lower()
        if sni == domain or sni.endswith("." + domain):
            return True
    return False

# ============================================================
# 4. جلب الروابط
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
# 5. الفلترة
# ============================================================
def filter_vless_reality(text: str):
    vless_links = re.findall(r"(vless://[^\s]+)", text)
    filtered_links = []
    
    for link in vless_links:
        if "security=reality" not in link:
            continue

        sni_match = re.search(r"[?&]sni=([^&]+)", link)
        if not sni_match:
            continue

        sni_value = sni_match.group(1).lower()

        if is_allowed_sni(sni_value):
            filtered_links.append(link)

    return list(dict.fromkeys(filtered_links))

# ============================================================
# 6. التشغيل الرئيسي
# ============================================================
if __name__ == "__main__":
    print("🔄 جاري جمع الروابط من المصادر...")
    raw_content = fetch_raw_links()

    print("🔍 جاري الفلترة: VLESS Reality + نطاقات X و Cloudflare فقط...")
    reality_links = filter_vless_reality(raw_content)

    # حفظ النتائج فـ الملف
    with open("reality_configs.txt", "w", encoding="utf-8") as f:
        for link in reality_links:
            f.write(link + "\n")

    print(f"\n✅ تم حفظ {len(reality_links)} كونفيغ Reality متوافق مع X و Cloudflare.")
    
    # طباعة أول 5 ديال SNI باش نتأكدو
    if reality_links:
        print("\n🔎 تأكيد: عينة من الـ SNI اللي تحفظو:")
        for link in reality_links[:5]:
            sni = re.search(r"[?&]sni=([^&]+)", link).group(1)
            print(f"   - {sni}")
