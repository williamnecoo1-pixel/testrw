import urllib.request
import base64
import json
import re
import urllib.parse

# ================== الإعدادات ==================
SOURCES = [
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
