import urllib.request
import base64
import json
import re
import urllib.parse

# ================== الإعدادات ==================
SOURCES = [
    "https://raw.githubusercontent.com/ashah404/V2rayCollector/refs/heads/main/subscribe/layers/ipv4",
    "https://github.com/0xRadikal/Free-v2ray-Configs/raw/refs/heads/main/all/configs.txt",
    "https://github.com/barry-far/V2ray-Config/raw/refs/heads/main/All_Configs_Sub.txt",
    "https://github.com/MatinGhanbari/v2ray-configs/raw/refs/heads/main/subscriptions/v2ray/all_sub.txt"
]

TARGET_IP = "104.18.37.127"
ALLOWED_PROTOCOLS = ["vless", "vmess", "trojan"]
ALLOWED_PORT = "443"
ALLOWED_TRANSPORT = "xhttp"

# ================== دوال مساعدة ==================
def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def is_xhttp(link):
    return bool(re.search(r'[?&](type|network)=xhttp', link, re.IGNORECASE)) or 'xhttp' in link.lower()

def is_tls(link):
    return bool(re.search(r'[?&](security=tls|tls=1|tls=true)', link, re.IGNORECASE))

def replace_vless_trojan_ip(link):
    # كيبدل الـ IP أو الدومين اللي مورا @ ويخلي البورت
    # مثال: vless://uuid@1.1.1.1:443?... كيولي vless://uuid@104.18.37.127:443?...
    return re.sub(r'@[^:/?#]+(:[0-9]+)?', f'@{TARGET_IP}\\1', link)

def process_vmess(link):
    try:
        b64 = link.replace("vmess://", "").strip()
        # تصحيح base64 إلا كان ناقص
        b64 += "=" * ((4 - len(b64) % 4) % 4)
        decoded = base64.b64decode(b64).decode('utf-8')
        obj = json.loads(decoded)
        
        # الفلترة
        if str(obj.get("port")) != ALLOWED_PORT: return None
        if obj.get("tls") != "tls" and obj.get("security") != "tls": return None
        if obj.get("net") != ALLOWED_TRANSPORT and obj.get("network") != ALLOWED_TRANSPORT: return None
        
        # تبديل الـ IP
        obj["add"] = TARGET_IP
        
        # إعادة التشفير
        new_json = json.dumps(obj, separators=(',', ':'))
        new_b64 = base64.b64encode(new_json.encode('utf-8')).decode('utf-8')
        return f"vmess://{new_b64}"
    except Exception:
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
        if not link: continue

        # 1. التحقق من البروتوكول
        protocol_match = re.match(r'^(vless|vmess|trojan)://', link, re.IGNORECASE)
        if not protocol_match: continue
        protocol = protocol_match.group(1).lower()

        if protocol == "vmess":
            processed = process_vmess(link)
            if processed:
                valid_configs.add(processed)
                
        elif protocol in ["vless", "trojan"]:
            # 2. التحقق من البورت، TLS، و XHTTP
            if f":{ALLOWED_PORT}" not in link: continue
            if not is_tls(link): continue
            if not is_xhttp(link): continue

            # 3. تبديل الـ IP
            processed = replace_vless_trojan_ip(link)
            valid_configs.add(processed)

    # حفظ النتيجة فـ الملف
    output_file = "reality_configs.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(valid_configs))
        
    print(f"✅ تم استخراج {len(valid_configs)} كونفيغ بدون تكرار وحفظهم فـ {output_file}")

if __name__ == "__main__":
    main()
