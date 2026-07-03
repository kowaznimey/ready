import requests
import socket
import time
import os
import base64
from urllib.parse import urlparse, parse_qs

# ANSI Color UI Elements
G, Y, R, C, M, B, W = '\033[92m', '\033[93m', '\033[91m', '\033[96m', '\033[95m', '\033[1m', '\033[0m'
F_TXT = "voucher_history.txt"

# 🌟 Encoded Portal URL (လင့်ခ်ကို မမြင်ရအောင် အုပ်ထားပါသည်)
B64_DATA = (
    "aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3dpZmlkb2c/"
    "c3RhZ2U9cG9ydGFsJmd3X2lkPWM0NzBhYjdlYTFkNSZnd19zbj1HMVQwNDRSMDAyMDBCJmd3"
    "X2FkZHJlc3M9MTkyLjE2OC4xMTAuMSZnd19wb3J0PTIwNjAmaXA9MTkyLjE2OC4xMTAuMyZt"
    "YWM9ZDg6Y2U6M2E6ZGQ6Y2Q6MWYmc2xvdF9udW09MDZuYXNpcD0xOTIuMTY4LjEuMTQzJnNz"
    "aWQ9VkxBTjIzMyZ1c3RhdGU9MDZtYWNfcmVxPTA2dXJsPWh0dHBzJTNBJTJGJTJGaXB2NCUy"
    "RWljYW5oYXppclFjb20lMkYmY2hhcF9pZD0lNUMwMDEmY2hhcF9jaGFsbGVuZ2U9JTVDMjY2"
    "JTVDMzc0JTVDMjQ0JTVDMTI1JTVDMzAxJTVDMjQyJTVDMzY0JTVDMzU0JTVDMDc1JTVDMzc1"
    "JTVDMjE3JTVDMTc1JTVDMzE0JTVDMTUxJTVDMTUxJTVDMzAx"
)

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{C}{B}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{W}")
    print(f"{C}{B}┃      🌟 RUIJIE CAPTIVE PORTAL AUTO-BYPASS TOOL 🌟     ┃{W}")
    print(f"{C}{B}┃             ⚡ WiFiDog Protocol Powered ⚡             ┃{W}")
    print(f"{C}{B}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{W}")

def get_gw():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0].split('.')
        ip[-1] = '1'
        return '.'.join(ip)
    except: 
        return "192.168.60.1"

print_banner()
gw = get_gw()
print(f"{G}[+] စနစ်မှ ဖမ်းယူရရှိသည့် Wi-Fi Gateway IP: {B}{gw}{W}")

# နောက်ကွယ်တွင် URL အား ပုံမှန်ပြန်ဖြည်ခြင်း
try:
    init_url = base64.b64decode(B64_DATA).decode('utf-8')
except Exception as e:
    print(f"{R}[!] URL decode ပြုလုပ်၍ မရပါ- {e}{W}")
    init_url = ""

try:
    mac_address = parse_qs(urlparse(init_url).query).get('mac', ['d8:ce:3a:dd:cd:1f'])[0]
except:
    mac_address = 'd8:ce:3a:dd:cd:1f'

ss = requests.Session()
ss.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36', 'Connection': 'keep-alive'})

# ---------------------------------------------------------------------
# အဆင့် (၁) - Session ID ဖမ်းခြင်း
# ---------------------------------------------------------------------
print(f"\n{Y}[*] အဆင့် (၁): Redirect URL ထဲမှ Session Data များ စစ်ဆေးနေသည်...{W}")
try:
    resp = ss.get(init_url, allow_redirects=False, timeout=5)
    redirect_url = resp.headers.get('Location', resp.url)
    sid = parse_qs(urlparse(redirect_url).query).get('sessionId', [None])[0]
    
    if not sid:
        with ss.get(init_url, allow_redirects=True, stream=True, timeout=5) as r:
            sid = parse_qs(urlparse(r.url).query).get('sessionId', [None])[0]

    if not sid:
        raise ValueError("Session ID ကို Link ထဲမှ ရှာမတွေ့ပါ။")
        
    print(f"{G} ├── {B}Session ID:{W} {C}{sid}{W}")
    print(f"{G} └── {B}MAC Address:{W} {C}{mac_address}{W}")
except Exception as e:
    print(f"{R}[!] Connection Error (Default Token Used): {e}{W}")
    sid = '13ed4bb1e881482bab3de3a80514016a'

# ---------------------------------------------------------------------
# အဆင့် (၂) - Voucher Loop System
# ---------------------------------------------------------------------
cookies_step2 = {'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22267794%22%7D'}
headers_step2 = {'content-type': 'application/json', 'referer': f'https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?sessionId={sid}'}

old_v = open(F_TXT, "r").read().strip() if os.path.exists(F_TXT) else None

while True:
    print(f"\n{M}┏━━━━━━━ [ AUTHENTICATION CARD ] ━━━━━━━┓{W}")
    if old_v:
        v_in = input(f"{M}┃{Y} [❓] Voucher Code -> {W}(အဟောင်း [{G}{old_v}{W}] ကိုသုံးရန် Enter ခေါက်ပါ): ").strip() or old_v
    else:
        v_in = input(f"{M}┃{Y} [❓] Voucher Code ကို ထည့်သွင်းပါ -> {W}").strip()
        if not v_in: continue
    print(f"{M}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{W}")

    print(f"\n{Y}[*] အဆင့် (၂): Ruijie Cloud သို့ Voucher တင်သွင်းစစ်ဆေးနေသည်...{W}")
    data = {'accessCode': v_in, 'sessionId': sid, 'apiVersion': 1}
    
    try:
        res = ss.post('https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US', cookies=cookies_step2, headers=headers_step2, json=data, timeout=5).json()
        
        if res.get("success") is True:
            print(f"{G}[🎉] အောင်မြင်သည်: Voucher Code အမှန်ကန်ဖြစ်ပါသည်။{W}")
            open(F_TXT, "w").write(v_in)
            
            p_parsed = parse_qs(urlparse(res["result"]["logonUrl"]).query)
            token_val = p_parsed.get('token', [sid])[0]
            phone_val = p_parsed.get('phoneNumber', [v_in])[0]
            break
        else:
            print(f"{R}[❌] Voucher ကုဒ် မှားယွင်းနေသည် သို့မဟုတ် Session သက်တမ်းကုန်ဆုံးသွားပါပြီ။{W}")
            if old_v == v_in and os.path.exists(F_TXT): os.remove(F_TXT); old_v = None
    except Exception as e:
        print(f"{R}[!] Network Request Error: {e}{W}")

# ---------------------------------------------------------------------
# အဆင့် (၃ & ၄) - Local Router Auth နှင့် Live Heartbeat Dashboard
# ---------------------------------------------------------------------
print(f"\n{Y}[*] အဆင့် (၃): Local Router Gateway ဆီသို့ လိုင်းဖွင့်ရန် တောင်းဆိုနေသည်...{W}")
r_url = f"http://{gw}:2060/wifidog/auth"
params = {'token': token_val, 'phoneNumber': phone_val, 'mac': mac_address}

try:
    router_res = ss.get(r_url, params=params, headers={'Upgrade-Insecure-Requests': '1'}, timeout=5)
    
    if router_res.status_code == 200 and ("Auth: 1" in router_res.text or "<html" in router_res.text.lower()):
        print(f"\n{G}{B}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{W}")
        print(f"{G}{B}┃               🚀 BYPASS SUCCESSFUL !! 🚀               ┃{W}")
        print(f"{G}{B}┃         ဝိုင်ဖိုင် Firewall အား ကျော်ဖြတ်ပြီးပါပြီ        ┃{W}")
        print(f"{G}{B}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{W}")
        
        print(f"\n{C}{B}┌─────────────────── [ LIVE MONITOR ] ───────────────────┐{W}")
        print(f"{C}{B}│ {Y}Target Gateway:{W} {gw:<10} │ {Y}Voucher Code:{W} {phone_val:<11} │{W}")
        print(f"{C}{B}└────────────────────────────────────────────────────────┘{W}")
        
        ping_count = 1
        status_color = G
        status_text = "CONNECTED"
        
        while True:
            for remaining in range(30, 0, -1):
                current_time = time.strftime('%H:%M:%S')
                print(f"\r{C} [{current_time}] {status_color}● {status_text}{W} | {B}Count:{W} {ping_count:<3} | {Y}Next Ping in: {remaining:02d}s{W} ", end="", flush=True)
                time.sleep(1)
            
            print(f"\r{C} [{time.strftime('%H:%M:%S')}] {Y}🔄 PINGING ROUTER GATEWAY...                      {W}", end="", flush=True)
            
            try:
                if ss.get(r_url, params=params, timeout=4).status_code == 200:
                    status_color = G
                    status_text = "ACTIVE LINE"
                else:
                    status_color = R
                    status_text = "LINE DROPPED"
            except:
                status_color = R
                status_text = "TIMEOUT ERR "
            ping_count += 1
            
except KeyboardInterrupt:
    print(f"\n\n{R}[-] Heartbeat Loop အား အသုံးပြုသူမှ ရပ်တန့်လိုက်ပါပြီ။{W}\n")
except Exception as e:
    print(f"{R}[!] Router Error: {e}{W}")

