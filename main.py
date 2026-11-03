
     
import re
import urllib.request
import base64
from collections import Counter

# المصادر ديالك (نفس القائمة اللي عندك)
SOURCES = [
    "https://github.com/morpheusadam/v2ray-config/raw/refs/heads/main/subs/bundles/vless.txt",
    "https://github.com/liMilCo/v2r/raw/refs/heads/main/new_configs.txt",
    "https://github.com/Delta-Kronecker/V2ray-Config/raw/refs/heads/main/config/all_configs.txt",
    "https://github.com/0xRadikal/Free-v2ray-Configs/raw/refs/heads/main/all/configs.txt",
    "https://github.com/MaxFreudDrethe/VCC/raw/refs/heads/main/configs/tls.txt",
    "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/All_Configs_Sub.txt",
    "https://github.com/Mohamedhnini-a/testeur/raw/refs/heads/main/working_configs.txt",
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

ALLOWED_SNI_KEYWORDS = [
    'x.com', 'twitter.com', 'twimg.com', 't.co', 'pscp.tv'
]

def fetch_raw_links():
    raw_data = ""
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode('utf-8', errors='ignore')
                # نتأكدو واش ماشي صفحة HTML ديال 404
                if "<!DOCTYPE html>" in content or "<html>" in content:
                    print(f"⚠️ تحذير: {url} رجع صفحة HTML (يمكن رابط خايب)")
                    continue
                raw_data += content + "\n"
                print(f"✅ تم الجلب من: {url}")
        except Exception as e:
            print(f"❌ خطأ فـ الجلب من {url}: {e}")
    return raw_data

def try_base64_decode(text):
    try:
        # فك تشفير Base64 يلا كان
        decoded = base64.b64decode(text + '===').decode('utf-8', errors='ignore')
        if 'vless://' in decoded or 'vmess://' in decoded:
            return decoded
    except:
        pass
    return text

if __name__ == "__main__":
    print("🔄 جاري جمع الروابط...")
    raw_content = fetch_raw_links()
    
    print(f"📦 طول النص الإجمالي: {len(raw_content)} حرف")
    if len(raw_content) == 0:
        print("❌ النص خاوي! المصادر ماقراوش مزيان.")
        exit()

    # نحاولو نفكو التشفير
    decoded_content = try_base64_decode(raw_content)
    
    # 1. نستخرجو كل الروابط
    all_links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s]+', decoded_content)
    print(f"🔗 إجمالي الروابط (كل البروتوكولات): {len(all_links)}")
    
    # 2. نستخرجو غير VLESS
    vless_links = [link for link in all_links if link.startswith('vless://')]
    print(f"🟢 إجمالي روابط VLESS: {len(vless_links)}")
    
    # 3. نشوفو شحال فيهم Reality
    reality_links = [link for link in vless_links if 'security=reality' in link.lower()]
    print(f"🛡️ إجمالي روابط VLESS Reality: {len(reality_links)}")
    
    # 4. نحللو الـ SNIs ديال Reality
    found_snis = []
    accepted_links = []
    
    for link in reality_links:
        # استخراج SNI بأكثر من طريقة
        sni_match = re.search(r'[?&](?:sni|serverName|host)=([^&]+)', link, re.IGNORECASE)
        if sni_match:
            sni = sni_match.group(1).lower()
            found_snis.append(sni)
            
            if any(keyword in sni for keyword in ALLOWED_SNI_KEYWORDS):
                accepted_links.append(link)
    
    # 5. نطبعو أكثر 15 SNI مستعمل
    print("\n📊 أكثر 15 SNI مستعمل في الروابط Reality:")
    sni_counts = Counter(found_snis).most_common(15)
    for sni, count in sni_counts:
        print(f"   - {sni} (تكرر {count} مرة)")
        
    print(f"\n✅ عدد الروابط اللي فازو بالفلترة (فيها X/Twitter): {len(accepted_links)}")
    
    # حفظ النتيجة
    with open("reality_configs.txt", "w", encoding="utf-8") as f:
        for link in accepted_links:
            f.write(link + "\n")
