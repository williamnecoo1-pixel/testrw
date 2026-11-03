import re
import urllib.request
import base64
import json
import socket
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

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

# الكلمات المفتاحية ديال X (اختياري، إلا بغيتي تحيدو، غير مسحو من الشروط تحت)
X_KEYWORDS = [
    "x.com", "twitter.com", "twimg.com", "t.co", "x.ai", 
    "grok.com", "pscp.tv", "ads-twitter.com"
]

# IP احتياطي يلا ما قدرش يحل الدومين (Cloudflare)
FALLBACK_IP = "104.18.37.127"

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
# 3. دالة لحل الدومين وجلب الـ IP
# ============================================================
def resolve_domain(domain):
    try:
        # كنجيبو غير الـ IPv4 باش نتفاداو مشاكل IPv6 فبعض التطبيقات
        ip = socket.gethostbyname(domain)
        return ip
    except Exception:
        return FALLBACK_IP

# ============================================================
# 4. الفلترة والتعديل
# ============================================================
def process_configs(text: str):
    # استخراج الروابط
    all_configs = re.findall(r'(?:vless|trojan|vmess)://[^\s]+', text)
    
    original_links = []
    modified_links = []
    
    for link in all_configs:
        link_lower = link.lower()
        
        # شرط الكلمات المفتاحية (إلا بغيتي تحيد هاد الشرط، غير مسح هاد السطرين)
        # if not any(keyword in link_lower for keyword in X_KEYWORDS):
        #     continue
            
        # === معالجة VLESS و Trojan ===
        if link_lower.startswith('vless://') or link_lower.startswith('trojan://'):
            is_xhttp = 'type=xhttp' in link_lower
            is_tls = 'security=tls' in link_lower
            is_443 = ':443?' in link_lower or ':443#' in link_lower or ':443/' in link_lower or link_lower.endswith(':443')
            
            if is_xhttp and is_tls and is_443:
                original_links.append(link)
                
                try:
                    # تفكيك الرابط
                    parsed = urlparse(link)
                    query_params = parse_qs(parsed.query)
                    
                    # جلب الـ SNI
                    sni = query_params.get('sni', [None])[0]
                    
                    if sni:
                        # 1. جلب الـ IP ديال الـ SNI
                        new_ip = resolve_domain(sni)
                        
                        # 2. تعديل الـ Host باش يولي هو نفسه الـ SNI
                        query_params['host'] = [sni]
                        
                        # 3. إعادة بناء الـ Query
                        new_query = urlencode(query_params, doseq=True)
                        
                        # 4. تعديل الـ netloc (الـ IP والـ Port)
                        # الـ netloc كيكون بحال: [2401:c080...]:443 أو 1.2.3.4:443
                        port = parsed.port if parsed.port else 443
                        new_netloc = f"{new_ip}:{port}"
                        
                        # 5. بناء الرابط الجديد
                        modified_link = urlunparse((
                            parsed.scheme,
                            new_netloc,
                            parsed.path,
                            parsed.params,
                            new_query,
                            parsed.fragment
                        ))
                        
                        modified_links.append(modified_link)
                except Exception as e:
                    print(f"⚠️ فشل تعديل الرابط: {link[:40]}... ({e})")
                
        # === معالجة VMess ===
        elif link_lower.startswith('vmess://'):
            try:
                b64_data = link[8:]
                b64_data += '=' * (-len(b64_data) % 4)
                decoded_json = base64.b64decode(b64_data).decode('utf-8')
                config = json.loads(decoded_json)
                
                net = config.get('net', '').lower()
                tls = config.get('tls', '').lower()
                port = str(config.get('port', ''))
                
                if net == 'xhttp' and tls == 'tls' and port == '443':
                    original_links.append(link)
                    
                    sni = config.get('sni', '') or config.get('host', '')
                    if sni:
                        new_ip = resolve_domain(sni)
                        
                        # تعديل البيانات
                        config['add'] = new_ip
                        config['host'] = sni
                        
                        new_json_str = json.dumps(config, ensure_ascii=False)
                        new_b64 = base64.b64encode(new_json_str.encode('utf-8')).decode('utf-8')
                        modified_links.append(f"vmess://{new_b64}")
                        
            except Exception:
                pass

    # إزالة التكرار
    return list(dict.fromkeys(original_links)), list(dict.fromkeys(modified_links))

# ============================================================
# 5. التشغيل الرئيسي
# ============================================================
if __name__ == "__main__":
    print("🔄 جاري جمع الروابط من المصادر...")
    raw_content = fetch_raw_links()

    print(f"\n🔍 جاري الفلترة والتعديل الذكي (تطابق SNI مع Host وحل الـ IP)...")
    originals, modifieds = process_configs(raw_content)

    # حفظ النتائج فـ الملف
    with open("reality_configs.txt", "w", encoding="utf-8") as f:
        # القسم الأول: الروابط الأصلية
        f.write("# ==========================================\n")
        f.write("# 1. الروابط الأصلية (بدون تعديل)\n")
        f.write("# ==========================================\n\n")
        for link in originals:
            f.write(link + "\n")
            
        f.write("\n\n")
        
        # القسم الثاني: الروابط المعدلة
        f.write("# ==========================================\n")
        f.write("# 2. الروابط المعدلة (IP جديد + Host مطابق لـ SNI)\n")
        f.write("# ==========================================\n\n")
        for link in modifieds:
            f.write(link + "\n")

    print(f"\n✅ تم العثور على {len(originals)} كونفيغ أصلي.")
    print(f"✅ تم إنشاء {len(modifieds)} كونفيغ معدل.")
    print(f"📁 تم الحفظ فـ الملف: reality_configs.txt")
    
    # طباعة عينة
    if modifieds:
        print("\n🔎 عينة من الروابط المعدلة:")
        for link in modifieds[:3]:
            print(f"   - {link[:120]}...")
