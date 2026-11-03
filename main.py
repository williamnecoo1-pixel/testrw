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

# الكلمات المفتاحية ديال X
X_KEYWORDS = [
    "x.com", "twitter.com", "twimg.com", "t.co", "x.ai", 
    "grok.com", "pscp.tv", "ads-twitter.com"
]

# الـ IP الجديد اللي بغينا نحطو (Cloudflare)
NEW_IP = "104.18.37.127"

# ============================================================
# 2. جلب الروابط
# ============================================================
def fetch_raw_links() -> str:
    raw_data = ""
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as response:
                raw_data += response.read().decode("utf-8", errors="ignore") + "\n"
                print(f"✅ تم الجلب من: {url[:50]}...")
        except Exception as e:
            print(f"❌ خطأ فـ الجلب من {url[:50]}: {e}")
    return raw_data

# ============================================================
# 3. الفلترة والتعديل
# ============================================================
def filter_and_modify_xhttp(text: str):
    # 1. استخراج جميع الروابط
    all_configs = re.findall(r'(?:vless|trojan)://[^\s]+', text)
    
    filtered_links = []
    
    for link in all_configs:
        link_lower = link.lower()
        
        # 2. شروط الفلترة: XHTTP + TLS + Port 443
        is_xhttp = 'type=xhttp' in link_lower
        is_tls = 'security=tls' in link_lower
        # التاكد من أن البورت هو 443 (سواء كان مكتوب :443 أو port=443)
        is_443 = ':443?' in link_lower or ':443#' in link_lower or ':443/' in link_lower or link_lower.endswith(':443')
        
        # 3. شرط الكلمات المفتاحية ديال X (يلا بغيتي تحيد هاد الشرط، غير امسح هاد السطر)
        is_x_related = any(keyword in link_lower for keyword in X_KEYWORDS)
        
        if is_xhttp and is_tls and is_443 and is_x_related:
            
            # 4. تبديل الـ IP
            # هاد الـ Regex كيقلب على أي حاجة جات مورا @ وقبل : (البورت) وكيبدلها بالـ IP الجديد
            # مثال: @1.2.3.4:443 كتولي @104.18.37.127:443
            new_link = re.sub(r'(?<=@)[^:/]+(?=:\d+)', NEW_IP, link)
            
            filtered_links.append(new_link)

    # إزالة التكرار
    return list(dict.fromkeys(filtered_links))

# ============================================================
# 4. التشغيل الرئيسي
# ============================================================
if __name__ == "__main__":
    print("🔄 جاري جمع الروابط من المصادر...")
    raw_content = fetch_raw_links()

    print(f"\n🔍 جاري الفلترة: (XHTTP + TLS + 443) وتبديل الـ IP بـ {NEW_IP}...")
    x_links = filter_and_modify_xhttp(raw_content)

    # حفظ النتائج
    with open("xhttp_tls_443_x_configs.txt", "w", encoding="utf-8") as f:
        for link in x_links:
            f.write(link + "\n")

    print(f"\n✅ تم حفظ {len(x_links)} كونفيغ مطابق فـ الملف: xhttp_tls_443_x_configs.txt")
    
    # طباعة أول 10 ديال الروابط باش تشوف بعينك النتيجة
    if x_links:
        print("\n🔎 تأكيد: عينة من الروابط اللي تحفظو بعد التعديل:")
        for link in x_links[:10]:
            print(f"   - {link[:100]}...")
