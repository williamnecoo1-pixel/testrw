import re
import urllib.request
import base64
import json
import concurrent.futures
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

# الـ IP الثابت اللي بغينا نحطو
TARGET_IP = "104.18.37.127"

# ============================================================
# 2. دالة جلب رابط واحد (مع Timeout)
# ============================================================
def fetch_single_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"❌ خطأ فـ الجلب من {url[:40]}...: {e}")
        return ""

# ============================================================
# 3. التحقق من نوع النقل (Transport)
# ============================================================
def is_valid_network(net_type):
    # كنقبلو xhttp, grpc, tcp, raw، وإلا ما كانش مكتوب شي حاجة (الافتراضي tcp)
    if not net_type: return True 
    net_type = net_type.lower()
    return net_type in ['xhttp', 'grpc', 'tcp', 'raw']

# ============================================================
# 4. الفلترة والتعديل
# ============================================================
def process_configs(text: str):
    # استخراج جميع الروابط
    all_configs = re.findall(r'(?:vless|trojan|vmess)://[^\s]+', text)
    original_links = []
    modified_links = []
    
    count = 0
    for link in all_configs:
        link_lower = link.lower()
        count += 1
        
        if count % 2000 == 0:
            print(f"⏳ تم فحص {count} رابط...")

        # === معالجة VLESS و Trojan ===
        if link_lower.startswith('vless://') or link_lower.startswith('trojan://'):
            try:
                parsed = urlparse(link)
                query_params = parse_qs(parsed.query)
                
                # 1. التحقق من TLS
                security = query_params.get('security', [''])[0].lower()
                if security != 'tls': 
                    continue
                
                # 2. التحقق من البورت 443
                if parsed.port != 443: 
                    continue
                
                # 3. التحقق من نوع النقل (Type/Net)
                net_type = query_params.get('type', query_params.get('net', ['']))[0]
                if not is_valid_network(net_type):
                    continue
                
                # --- وصلنا لهنا، يعني الكونفيغ مطابق ---
                original_links.append(link)
                
                # تعديل الـ IP والـ Host
                sni = query_params.get('sni', [None])[0]
                if sni:
                    query_params['host'] = [sni] # باش ما يطيحش مع كلاودفلير
                    new_query = urlencode(query_params, doseq=True)
                else:
                    new_query = parsed.query
                
                new_netloc = f"{TARGET_IP}:443"
                
                modified_link = urlunparse((
                    parsed.scheme,
                    new_netloc,
                    parsed.path,
                    parsed.params,
                    new_query,
                    parsed.fragment
                ))
                modified_links.append(modified_link)
                
            except Exception:
                pass
            
        # === معالجة VMess ===
        elif link_lower.startswith('vmess://'):
            try:
                b64_data = link[8:]
                b64_data += '=' * (-len(b64_data) % 4)
                decoded_json = base64.b64decode(b64_data).decode('utf-8')
                config = json.loads(decoded_json)
                
                # 1. التحقق من TLS
                tls = config.get('tls', '').lower()
                if tls != 'tls':
                    continue
                
                # 2. التحقق من البورت 443
                port = str(config.get('port', ''))
                if port != '443':
                    continue
                
                # 3. التحقق من نوع النقل
                net_type = config.get('net', '')
                if not is_valid_network(net_type):
                    continue
                
                # --- وصلنا لهنا، يعني الكونفيغ مطابق ---
                original_links.append(link)
                
                # تعديل الـ IP والـ Host
                config['add'] = TARGET_IP
                sni = config.get('sni', '')
                if sni:
                    config['host'] = sni # باش ما يطيحش مع كلاودفلير
                
                new_json_str = json.dumps(config, ensure_ascii=False)
                new_b64 = base64.b64encode(new_json_str.encode('utf-8')).decode('utf-8')
                modified_links.append(f"vmess://{new_b64}")
                
            except Exception:
                pass

    return list(dict.fromkeys(original_links)), list(dict.fromkeys(modified_links))

# ============================================================
# 5. التشغيل الرئيسي
# ============================================================
if __name__ == "__main__":
    print("🔄 جاري جمع الروابط من المصادر (بشكل متوازي)...")
    
    raw_data_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch_single_url, SOURCES))
        for res in results:
            if res:
                raw_data_list.append(res)
    
    raw_content = "\n".join(raw_data_list)
    print(f"✅ تم جلب {len(raw_data_list)} مصدر بنجاح.")

    print(f"\n🔍 جاري الفلترة (XHTTP/gRPC/TCP + TLS + 443) وتغيير الـ IP لـ {TARGET_IP}...")
    originals, modifieds = process_configs(raw_content)

    # حفظ النتائج
    with open("reality_configs.txt", "w", encoding="utf-8") as f:
        f.write("# ==========================================\n")
        f.write("# 1. الروابط الأصلية (بدون تعديل)\n")
        f.write("# ==========================================\n\n")
        for link in originals:
            f.write(link + "\n")
            
        f.write("\n\n")
        
        f.write("# ==========================================\n")
        f.write(f"# 2. الروابط المعدلة (IP: {TARGET_IP} + Host مطابق لـ SNI)\n")
        f.write("# ==========================================\n\n")
        for link in modifieds:
            f.write(link + "\n")

    print(f"\n✅ تم العثور على {len(originals)} كونفيغ أصلي.")
    print(f"✅ تم إنشاء {len(modifieds)} كونفيغ معدل.")
    print(f"📁 تم الحفظ فـ الملف: reality_configs.txt")
