import urllib.request
import base64
import json
import re
import urllib.parse

# ================== الإعدادات ==================
SOURCES = [
    "https://raw.githubusercontent.com/6b3478/telegram-configs-collector2/main/countries/ro/mixed",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_013.txt",
"https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/main/data/githubmirror/clean/trojan.txt",
"https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/tls.txt",
"https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/main/output/vless.txt",
"https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/lite.txt",
"https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/best.txt",
"https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/all.txt",
"https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/trojan.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/protocols/trojan.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_014.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/009.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_015.txt",
"https://raw.githubusercontent.com/Abobirec/bezdelnicha-vpn0chek/HEAD/BLACK_VLESS_RUS_mobile.txt",
"https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/countries/MH.txt",
"https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/main/configs/trojan.txt",
"https://raw.githubusercontent.com/pie-with-jam/5ubscrpt10n-Reborn/main/mini/m1n1-5ub-14.txt",
"https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/main/data/githubmirror/clean/vless.txt",
"https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/main/configs/trojan_sub.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_004.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_004.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_011.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_011.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_007.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_008.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_006.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_008.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_006.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_003.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_005.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_005.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_012.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/010.txt",
"https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/HEAD/configs/trojan.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_002.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_001.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/013.txt",
"https://raw.githubusercontent.com/6b3478/telegram-configs-collector2/main/countries/lu/mixed",
"https://raw.githubusercontent.com/TheCrowCreature/v2rayExtractor/refs/heads/main/trojan.html",
"https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/mini.txt",
"https://alireza786786.github.io/Free-V2ray-Configs/servers/trojan_servers.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_009.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_013.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/reality.txt",
"https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/countries/IM.txt",
"https://raw.githubusercontent.com/hamedcode/port-based-v2ray-configs/main/sub/trojan.txt",
"https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/medium.txt",
"https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/main/data/githubmirror/ru-sni/vless.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_016.txt",
"https://raw.githubusercontent.com/6b3478/telegram-configs-collector2/main/countries/kz/mixed",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/non-tls.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/datacenters/cloudflare.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/xhttp.txt",
"https://raw.githubusercontent.com/thealiiakbarii-ai/VCC/main/configs/all.txt",
"https://raw.githubusercontent.com/thealiiakbarii-ai/VCC/main/configs/vless.txt",
"https://raw.githubusercontent.com/hamedcode/port-based-v2ray-configs/main/detailed/trojan/443.txt",
"https://raw.githubusercontent.com/penhandev/AutoAiVPN/HEAD/allConfigs.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/non-tls.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/countries/US.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_010.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/xhttp.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/030.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/tls.txt",
"https://gh-proxy.com/https://raw.githubusercontent.com/zueston/proxy-hub/main/out/base64.txt",
"https://ghproxy.net/https://raw.githubusercontent.com/zueston/proxy-hub/main/out/base64.txt",
"https://gcore.jsdelivr.net/gh/zueston/proxy-hub@main/out/base64.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/normal/10ium-telegram-configs-collector-tls",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/tls.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/10ium-telegram-configs-collector-tls",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/020.txt",
"https://raw.githubusercontent.com/aydinverse/my-sub/HEAD/sub.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/datacenters/cloudflare.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/ipv4.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/normal/10ium-telegram-configs-collector-ws",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/ipv4.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/ws.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/ws.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/countries/US.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/10ium-telegram-configs-collector-ws",
"https://raw.githubusercontent.com/Leon406/SubCrawler/master/sub/share/vless",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/normal/10ium-telegram-configs-collector-trojan",
"https://raw.githubusercontent.com/MohammadBahemmat/V2ray-Collector/main/servers/trojan_servers.txt",
"https://raw.githubusercontent.com/Danialsamadi/v2go/main/Splitted-By-Protocol/trojan.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/normal/10ium-telegram-configs-collector-vless",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/10ium-telegram-configs-collector-vless",
"https://raw.githubusercontent.com/LeilaoMi/AutoMergePublicNodes-Optimized/main/output/global.txt",
"https://raw.githubusercontent.com/R3ZARAHIMI/tg-v2ray-configs-every2h/main/conf-week.txt",
"https://raw.githubusercontent.com/EEvanescence/4Diana/main/By-protocol/cloudflare.txt",
"https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/main/data/githubmirror/clean/ss.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/protocols/vless.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/037.txt",
"https://raw.githubusercontent.com/chenzhihan1751-cyber/node-sub-zixf/HEAD/sub/base64.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/protocols/vless.txt",
"https://raw.githubusercontent.com/Freedom-Guard-Builder/Freedom-Finder/main/out/channels/PSG.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_012.txt",
"https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/iran.txt",
"https://raw.githubusercontent.com/pie-with-jam/5ubscrpt10n-Reborn/main/mini/m1n1-5ub-13.txt",
"https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/HEAD/configs/trojan_sub.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/025.txt",
"https://raw.githubusercontent.com/6b3478/telegram-configs-collector2/main/countries/na/mixed",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/countries/NL.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/10ium-V2Hub3-trojan",
"https://raw.githubusercontent.com/SoliSpirit/SolVPN/main/all_configs.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/023.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/countries/us.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/countries/us.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/countries/NL.txt",
"https://raw.githubusercontent.com/Mokafela/Config-Finder/master/split/sub-ALL.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/10ium-telegram-configs-collector-trojan",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/normal/SoliSpirit-v2ray-configs-trojan.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/002.txt",
"https://raw.githubusercontent.com/myominn062-svg/mk-studio-vpn-service/main/trojan_configs.txt",
"https://raw.githubusercontent.com/pie-with-jam/PulseProxy/main/githubmirror/30.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/countries/DE.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_003.txt",
"https://raw.githubusercontent.com/YawStar/Proxy-Hunter/refs/heads/main/configs/proxy_configs_deduplicated.txt",
"https://raw.githubusercontent.com/MrTelepathic/v2ray-sub/refs/heads/main/configs.txt",
"https://raw.githubusercontent.com/pog7x/vpn-configs/refs/heads/master/githubmirror/10.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/024.txt",
"https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/shadowsocks.txt",
"https://raw.githubusercontent.com/sakha1370/OpenRay/main/output/kind/trojan.txt",
"https://raw.githubusercontent.com/chenzhihan1751-cyber/node-sub-zixf/main/sub/v2ray.txt",
"https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/CentralAfricanRepublic.txt",
"https://raw.githubusercontent.com/cyrusalbert/ArashOnline-Public/main/arashonline.txt#ArashOnline-Public",
"https://raw.githubusercontent.com/miraali1372/mirsub/main/subscription.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/019.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/normal/10ium-VpnClashFaCollector-trojan.txt",
"https://raw.githubusercontent.com/drmikecrypto/PulseConfigs/main/verified/configs_base64.txt",
"https://raw.githubusercontent.com/Surfboardv2ray/v2ray-worker-sub/refs/heads/master/providers/providers",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_007.txt",
"https://raw.githubusercontent.com/thealiiakbarii-ai/VCC/main/configs/lite.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_009.txt",
"https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/main/data/githubmirror/clean/hysteria2.txt",
"https://raw.githubusercontent.com/6b3478/telegram-configs-collector2/main/subscribe/protocols/trojan",
"https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/main/configs/vless_sub.txt",
"https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/HEAD/configs/vless.txt",
"https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/all.txt",
"https://raw.githubusercontent.com/drmikecrypto/PulseConfigs/HEAD/verified/configs_base64.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/017.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/datacenters/fastly.txt",
"https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/countries/MT.txt",
"https://raw.githubusercontent.com/Danialsamadi/v2go/main/Sub1.txt",
"https://raw.githubusercontent.com/aqayerez/MatnOfficial-VPN/refs/heads/main/MatnOfficial",
"https://raw.githubusercontent.com/aqayerez/MatnOfficial-VPN/refs/heads/main/MatnOfficial#MatnOfficial",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_002.txt",
"https://raw.githubusercontent.com/lorenzazy7kenyon/free-vpn-subscriptions/main/output/v2ray-base64.txt",
"https://raw.githubusercontent.com/6b3478/telegram-configs-collector2/main/countries/lt/mixed",
"https://raw.githubusercontent.com/drmikecrypto/PulseConfigs/HEAD/verified/configs.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/tcp-pass/batch_001.txt",
"https://raw.githubusercontent.com/6b3478/telegram-configs-collector2/main/countries/ph/mixed",
"https://raw.githubusercontent.com/3inker/v2ray-subscription/main/subs/all_not_ru.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/normal/10ium-V2Hub3-vless",
"https://raw.githubusercontent.com/hamedcode/port-based-v2ray-configs/main/detailed/vless/80.txt",
"https://raw.githubusercontent.com/kort0881/vpn-checker-backend/main/checked/RU_Best/ru_white_part3.txt",
"https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/countries/EE.txt",
"https://vless.svinakraft.workers.dev/vless.txt",
"https://raw.githubusercontent.com/mrdevmohamed/v2ray-configs/main/All_Configs_base64_Sub.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/0xRadikal-Free-v2ray-secure.txt",
"https://gh-proxy.com/https://raw.githubusercontent.com/chenzhihan1751-cyber/node-sub-zixf/main/sub/base64.txt",
"https://raw.githubusercontent.com/6b3478/telegram-configs-collector2/main/countries/si/mixed",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/roosterkid-openproxylist-V2RAY_RAW.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/003.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/normal/0xRadikal-Free-v2ray-secure.txt",
"https://raw.githubusercontent.com/ZendanTeam/SS44-sub/main/SS44.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/countries/SC.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/countries/SC.txt",
"https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/vless.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/split/datacenters/fastly.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/022.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/007.txt",
"https://raw.githubusercontent.com/chenzhihan1751-cyber/node-sub-zixf/main/sub/base64.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/base64/split/tcp.txt",
"https://raw.githubusercontent.com/arg9244/V2R-Subs/HEAD/subs/1000/027.txt",
"https://raw.githubusercontent.com/pie-with-jam/5ubscrpt10n-Reborn/main/mini/m1n1-5ub-11.txt",
"https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/tcp-pass/batch_014.txt",
"https://vless.svinakraft.workers.dev/fastest.txt",
"https://raw.githubusercontent.com/pie-with-jam/PulseProxy/main/githubmirror/13.txt",
"https://raw.githubusercontent.com/svinakraft-maker/FlareFeed/main/public/fastest.txt",
"https://raw.githubusercontent.com/gbcwror/v2ray-tester/HEAD/configs/vless/vless-1.txt",
"https://raw.githubusercontent.com/10Dream/sub-mod/main/sub/normal/flaafix-AetrisVPN-black-list-configs.txt",
    "https://github.com/miladtahanian/Config-Collector/raw/refs/heads/main/mixed_iran.txt",
    "https://github.com/10Dream/sub-mod/raw/refs/heads/main/sub/normal/0xRadikal-Free-v2ray-fast.txt",
    
    "https://github.com/0xRadikal/Free-v2ray-Configs/raw/refs/heads/main/all/configs.txt",
    "https://github.com/MatinGhanbari/v2ray-configs/raw/refs/heads/main/subscriptions/v2ray/all_sub.txt",
    "https://github.com/Alirewa/V2ray-Configs/raw/refs/heads/main/config.txt",
    
    "https://raw.githubusercontent.com/ashah404/V2rayCollector/refs/heads/main/subscribe/layers/ipv4",
    "https://github.com/0xRadikal/Free-v2ray-Configs/raw/refs/heads/main/all/configs.txt",
    "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/All_Configs_Sub.txt",
    "https://github.com/MatinGhanbari/v2ray-configs/raw/refs/heads/main/subscriptions/v2ray/all_sub.txt",
    "https://github.com/morpheusadam/v2ray-config/raw/refs/heads/main/subs/bundles/all.txt",
]

TARGET_IP = "104.18.37.127"
ALLOWED_PROTOCOLS = ["vless", "vmess", "trojan"]
ALLOWED_PORT = 443
ALLOWED_TRANSPORT = "xhttp"

# ================== دوال مساعدة للتشفير ==================
def b64_decode(s):
    """فك تشفير Base64 مع دعم Base64URL والـ Padding"""
    s = s.strip().replace('-', '+').replace('_', '/')
    s += '=' * ((4 - len(s) % 4) % 4)
    try:
        return base64.b64decode(s).decode('utf-8', errors='ignore')
    except Exception:
        return ""

def b64_encode(s):
    """تشفير Base64 عادي"""
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

# ================== دوال المعالجة ==================
def process_vless_trojan(link):
    try:
        parsed = urllib.parse.urlparse(link)
        
        # 1. التحقق من البورت
        port = parsed.port or 443
        if port != ALLOWED_PORT:
            return None
            
        # 2. التحقق من الإعدادات (TLS و XHTTP)
        query_dict = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        
        security = query_dict.get('security', [''])[0].lower()
        if security != 'tls':
            return None
            
        net_type = query_dict.get('type', query_dict.get('network', ['']))[0].lower()
        if net_type != ALLOWED_TRANSPORT:
            return None

        original_host = parsed.hostname
        if not original_host:
            return None

        # 3. الحفاظ على الـ SNI و Host الأصليين قبل تغيير الدومين
        if 'sni' not in query_dict:
            query_dict['sni'] = [original_host]
        if 'host' not in query_dict:
            query_dict['host'] = [original_host]

        # 4. إعادة بناء الرابط بأمان (تجنب مشكل UserInfo)
        # نقسمو الـ netloc باش نعزلوا الـ UserInfo
        userinfo = ""
        if '@' in parsed.netloc:
            userinfo = parsed.netloc.split('@')[0] + "@"
            
        new_netloc = f"{userinfo}{TARGET_IP}:{port}"
        
        # إعادة بناء الـ Query String مع الحفاظ على كاع البارامترات
        new_query = urllib.parse.urlencode(query_dict, doseq=True)
        
        # تجميع الرابط النهائي
        new_link = urllib.parse.urlunparse((
            parsed.scheme,
            new_netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        return new_link
    except Exception as e:
        print(f"Error processing VLESS/Trojan {link[:30]}: {e}")
        return None

def process_vmess(link):
    try:
        # فصل الـ Fragment (الاسم) باش ما يخربش الـ Base64
        parts = link.split('#', 1)
        b64_part = parts[0].replace("vmess://", "").strip()
        fragment = f"#{parts[1]}" if len(parts) > 1 else ""
        
        decoded = b64_decode(b64_part)
        if not decoded:
            return None
            
        obj = json.loads(decoded)
        
        # 1. التحقق من البورت
        if int(obj.get("port", 0)) != ALLOWED_PORT:
            return None
            
        # 2. التحقق من TLS
        tls_value = obj.get("tls") or obj.get("security") or ""
        if tls_value.lower() != "tls":
            return None
            
        # 3. التحقق من XHTTP
        net_value = obj.get("net") or obj.get("network") or ""
        if net_value.lower() != ALLOWED_TRANSPORT:
            return None

        original_add = obj.get("add")
        if not original_add:
            return None

        # 4. حفظ SNI و Host الأصليين إذا لم يكونا موجودين
        if not obj.get("host"):
            obj["host"] = original_add
        if not obj.get("sni"):
            obj["sni"] = original_add

        # 5. تغيير العنوان إلى IP الجديد
        obj["add"] = TARGET_IP

        # إعادة التشفير بدون مسافات زائدة
        new_json = json.dumps(obj, separators=(',', ':'))
        new_b64 = b64_encode(new_json)
        
        return f"vmess://{new_b64}{fragment}"
    except Exception as e:
        print(f"Error processing VMess: {e}")
        return None

# ================== السكريبت الرئيسي ==================
def main():
    all_links = []
    for url in SOURCES:
        content = fetch_url(url)
        if content:
            all_links.extend(content.splitlines())

    valid_configs = set()  # هنا كيتم منع التكرار

    for link in all_links:
        link = link.strip()
        if not link:
            continue

        protocol_match = re.match(r'^(vless|vmess|trojan)://', link, re.IGNORECASE)
        if not protocol_match:
            continue
        protocol = protocol_match.group(1).lower()

        if protocol == "vmess":
            processed = process_vmess(link)
            if processed:
                valid_configs.add(processed)
        elif protocol in ["vless", "trojan"]:
            processed = process_vless_trojan(link)
            if processed:
                valid_configs.add(processed)

    # حفظ النتيجة
    output_file = "reality_configs.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(valid_configs))

    print(f"✅ تم استخراج {len(valid_configs)} كونفيغ XHTTP+TLS بدون تكرار وحفظهم فـ {output_file}")

if __name__ == "__main__":
    main()
